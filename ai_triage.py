"""
AI-powered issue triage using GitHub Models inference API.

This module replaces the regex/heuristic classifier with an actual LLM call
(GitHub Models — same models Copilot uses) that reads the full issue body
and reasons about what to do.

Required env vars:
    GITHUB_TOKEN   — already present in every Actions run.
                     For private repos / org models you may need a token with
                     the `models:read` scope. In public repos the default
                     GITHUB_TOKEN works.

Optional env vars:
    AI_MODEL       — model id to use. Default: "openai/gpt-4o-mini".
    AI_DEBUG       — if set to "1", prints the full prompt and raw response.

The module exposes two functions:
    ai_triage_issue(issue) -> dict
    ai_or_fallback(issue)  -> dict   (falls back to issue_analyzer if AI fails)

The returned dict always has the shape:

    {
        "classification": "auto_fix" | "needs_human" | "needs_context" | "spam",
        "confidence":     int (0-100),
        "reasoning":      str,           # why the AI chose this label
        "comment":        str,           # markdown body to post on the issue
        "fix_plan": {                    # populated only when classification == auto_fix
            "module_url":    str | null,
            "current_text":  str | null, # short literal phrase to find in the docs
            "desired_text":  str | null, # short literal phrase to replace it with
            "explanation":   str | null,
        } | null,
        "source":         "ai" | "fallback",
    }
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

# GitHub Models inference endpoint (OpenAI-compatible Chat Completions API)
_GITHUB_MODELS_URL = "https://models.github.ai/inference/chat/completions"
_DEFAULT_MODEL = os.environ.get("AI_MODEL", "openai/gpt-4o-mini")
_DEBUG = os.environ.get("AI_DEBUG") == "1"


SYSTEM_PROMPT = """You are an automated issue triage agent for the
MicrosoftDocs/learn-pr GitHub repository. You read user-submitted issues
about Microsoft Learn training modules and decide what action to take.

Your job has THREE parts:

1) IGNORE THE ISSUE TEMPLATE SCAFFOLDING.
   Issues are submitted through a GitHub issue form whose body contains a lot
   of fixed template text — section headers, checkbox option labels, and
   placeholder values. You must mentally strip ALL of this out and only
   reason about what the USER actually typed. Treat these as noise:
     • "Which of the MS Learn modules from the dropdown are you submitting..."
     • "Additional information"
     • "Information about the requested update"
     • "Fix a broken user experience (broken links, exercise error, etc.)"
     • "Update incorrect information"
     • "Add new content to the module"
     • "Some other request"
     • "[REPLACE_WITH_MODULE_TITLE]"
     • "No response", standalone "None"
     • Any line consisting solely of "- [ ]" or "- [x]" plus one of the option labels above.

2) DECIDE A CLASSIFICATION (exactly one):

   • spam          — After stripping template noise the user wrote nothing of
                     substance (empty, gibberish, single word, placeholder
                     left in, etc.).
   • auto_fix      — The user clearly identifies a SPECIFIC, LITERAL piece of
                     text in a SPECIFIC Microsoft Learn page that is wrong,
                     AND tells you the SHORT, LITERAL replacement text. The
                     change must be small enough to apply as a plain text
                     substitution (typo fix, wrong answer marked correct,
                     swapped term, broken URL, etc.). If the fix requires
                     rewriting a paragraph, restructuring content, or making
                     an editorial judgement call, this is NOT auto_fix.
   • needs_human   — The user reports a real, substantive problem with a
                     specific module but the fix requires human judgement
                     (rewrite, restructure, editorial decision, ambiguous
                     correction).
   • needs_context — The user's report is too vague to act on: no module link,
                     no specific section, or no clear statement of what is
                     wrong vs. what should be there. A selected module name by
                     itself, with no requested action, is needs_context rather
                     than spam or needs_human.

3) PRODUCE A USER-FRIENDLY COMMENT for the issue thread that:
   - Tells the user what you classified the issue as and WHY in 1–2 plain
     sentences.
     - For needs_human: ask precisely for what is missing.
     - For needs_context: explain that the issue will be closed for now and can
         be reopened when the user provides a URL and specific requested change.
   - For auto_fix: confirm you understood the requested change and say a PR
     attempt is being made.
   - For spam: politely explain the issue appears empty/template-only and ask
     them to refile with the form filled out.

OUTPUT FORMAT — STRICT.

Reply with a SINGLE JSON object, no markdown fences, no prose before/after.
Schema:

{
  "classification": "spam" | "auto_fix" | "needs_human" | "needs_context",
  "confidence":      <integer 0-100>,
  "reasoning":       "<one paragraph explaining your decision>",
  "comment":         "<markdown body to post on the issue>",
  "fix_plan": {
    "module_url":   "<the MS Learn URL the user cited, or null>",
    "current_text": "<short literal phrase in the docs to be replaced, or null>",
    "desired_text": "<short literal replacement phrase, or null>",
    "explanation":  "<one sentence describing the change, or null>"
  }
}

Rules:
- "fix_plan" MUST be present in every response.
- Set every field of "fix_plan" to null UNLESS classification == "auto_fix".
- When classification == "auto_fix", "current_text" and "desired_text" must
  both be non-null AND must be short literal phrases (typically 1–15 words)
  that could be found by exact-string search in the source markdown.
- Never invent a URL the user did not provide.
- Never include the issue template scaffolding text in any field.
"""


def _build_user_message(issue: dict) -> str:
    """Format the issue into the user turn of the chat."""
    number = issue.get("number", "?")
    title = issue.get("title") or ""
    body = issue.get("body") or ""
    return (
        f"Triage this GitHub issue.\n\n"
        f"Issue number: #{number}\n"
        f"Issue title:\n{title}\n\n"
        f"Issue body (raw, includes template scaffolding — strip it mentally):\n"
        f"---BODY START---\n{body}\n---BODY END---\n"
    )


def _call_github_models(messages: list[dict], model: str, token: str) -> dict:
    """POST to the GitHub Models chat completions endpoint."""
    payload = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        _GITHUB_MODELS_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _parse_ai_response(api_response: dict) -> dict:
    """Pull the JSON object out of the chat-completion response."""
    try:
        content = api_response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise ValueError(f"Unexpected API response shape: {api_response}") from exc

    if _DEBUG:
        print("─── AI raw content ───")
        print(content)
        print("──────────────────────")

    # Models occasionally wrap JSON in ```json fences despite response_format.
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    return json.loads(cleaned)


_VALID_CLASSIFICATIONS = {"spam", "auto_fix", "needs_human", "needs_context"}


def _normalize(result: dict) -> dict:
    """Make sure the AI's response matches the contract we promise callers."""
    classification = result.get("classification")
    if classification not in _VALID_CLASSIFICATIONS:
        raise ValueError(
            f"AI returned invalid classification: {classification!r}. "
            f"Expected one of {_VALID_CLASSIFICATIONS}."
        )

    confidence_raw = result.get("confidence", 50)
    try:
        confidence = max(0, min(100, int(confidence_raw)))
    except (TypeError, ValueError):
        confidence = 50

    fix_plan = result.get("fix_plan") or {
        "module_url": None,
        "current_text": None,
        "desired_text": None,
        "explanation": None,
    }
    # If the AI said auto_fix but didn't actually give us a swap, downgrade.
    if classification == "auto_fix":
        if not (fix_plan.get("current_text") and fix_plan.get("desired_text")):
            classification = "needs_human"
            fix_plan = {
                "module_url": fix_plan.get("module_url"),
                "current_text": None,
                "desired_text": None,
                "explanation": (
                    "AI proposed auto_fix but did not provide both current_text "
                    "and desired_text; downgraded to needs_human."
                ),
            }

    return {
        "classification": classification,
        "confidence": confidence,
        "reasoning": (result.get("reasoning") or "").strip(),
        "comment": (result.get("comment") or "").strip(),
        "fix_plan": fix_plan if classification == "auto_fix" else None,
        "source": "ai",
    }


def ai_triage_issue(issue: dict, token: str | None = None, model: str | None = None) -> dict:
    """Run a single issue through GitHub Models and return the structured decision.

    Raises on any error — callers that want a fallback should use
    ``ai_or_fallback`` instead.
    """
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN not set — cannot call GitHub Models.")

    model = model or _DEFAULT_MODEL
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_message(issue)},
    ]

    if _DEBUG:
        print("─── AI prompt (user turn) ───")
        print(messages[-1]["content"])
        print("─────────────────────────────")

    api_response = _call_github_models(messages, model=model, token=token)
    parsed = _parse_ai_response(api_response)
    return _normalize(parsed)


def ai_or_fallback(issue: dict) -> dict:
    """Try the AI; if anything goes wrong, fall back to the heuristic analyzer."""
    try:
        return ai_triage_issue(issue)
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError,
            json.JSONDecodeError, RuntimeError, KeyError) as exc:
        print(f"⚠️ AI triage failed ({type(exc).__name__}: {exc}); "
              f"falling back to heuristic analyzer.")
        # Local import keeps this file usable even if issue_analyzer is missing.
        from issue_analyzer import intelligent_classify, generate_context_aware_comment

        classification, confidence, analysis = intelligent_classify(issue)
        analysis = analysis or {}

        # The spam fast-path returns an empty analysis dict; build a minimal
        # comment ourselves rather than asking the templated comment generator
        # (which expects fully populated keys).
        if classification == "spam" or not analysis:
            comment = (
                "🗑️ This issue appears to be empty or to contain only the "
                "unfilled MS Learn issue template. If this was a mistake, "
                "please reopen with the form filled in."
            )
        else:
            try:
                comment = generate_context_aware_comment(analysis, classification)
            except (KeyError, TypeError) as comment_exc:
                print(f"⚠️ Heuristic comment generation failed ({comment_exc}); "
                      f"using a generic fallback comment.")
                comment = (
                    f"This issue has been classified as `{classification}` by the "
                    "heuristic fallback (the AI triage was unavailable). A human "
                    "reviewer will follow up shortly."
                )

        return {
            "classification": classification,
            "confidence": int(confidence) if isinstance(confidence, (int, float)) else 50,
            "reasoning": "Heuristic fallback (no AI response).",
            "comment": comment,
            "fix_plan": None,  # heuristic path doesn't propose a structured fix
            "source": "fallback",
        }


# ───────────────────────────────────────────────────────────────────
# Fix-plan refinement: ground current/desired in the actual file
# ───────────────────────────────────────────────────────────────────
REFINEMENT_SYSTEM_PROMPT = """You are an expert at producing patches for
Microsoft Learn module source files.

A `MicrosoftDocs/learn-pr` module directory looks like:

    learn-pr/learn-pr/<topic>/<module-slug>/
    ├── index.yml                       ← module metadata + unit list
    ├── <n>-knowledge-check.yml         ← knowledge-check questions/answers (YAML)
    ├── ...
    └── includes/
        ├── <n>-<unit-name>.md          ← unit prose content (Markdown)
        └── ...

You will be given:
  1. A user-reported issue about something incorrect in a module.
  2. The user's high-level "current"/"desired" description (which may be
     paraphrased and may NOT match the file verbatim).
  3. The file we have determined is the one to edit, including its path
     and full contents. Pay attention to the FILE TYPE:
       • `.yml` / `.yaml` → structured data; edit fields, not prose.
       • `.md`           → prose; edit the literal text.

Your job: produce a literal text substitution that, when applied with a
plain Python `str.replace`, fixes the bug described by the user.

Output a SINGLE JSON object — no markdown fences, no prose:

{
  "current_text": "<EXACT substring copied verbatim from the file>",
  "desired_text": "<the replacement string>",
  "explanation":  "<one sentence describing the change>"
}

CRITICAL RULES (read carefully):

  • "current_text" MUST appear EXACTLY in the file (whitespace,
    indentation, punctuation, casing — all matching). If you cannot
    find such a substring, return all three fields as null instead of
    guessing.
  • "current_text" should be the smallest UNIQUE snippet that captures
    the bug. Include enough surrounding context (1–3 lines) so the
    substring appears only ONCE in the file.
  • The substitution must leave the document syntactically valid
    (preserve YAML indentation, Markdown link syntax, etc.).

HOW TO HANDLE KNOWLEDGE-CHECK YAML FILES (.yml):
    These files contain entries like:

        - content: "Project name"
          isCorrect: true
          explanation: "..."
        - content: "Project description"
          isCorrect: false
          explanation: "..."

    To CHANGE WHICH ANSWER IS CORRECT, toggle the `isCorrect:` flags —
    do not edit the `content:` strings.

    SPECIAL CASE — "NONE OF THE ABOVE":
    If the user says something like "none of the options are correct",
    "the correct answer is 'none of the above'", "none of them", or similar:
    
    1. FIRST, check if there is ALREADY an answer choice with content
       containing "none of the above", "none of them", "none", or similar.
    2. If such an option EXISTS: Set that choice's `isCorrect: true` and
       ALL others to `isCorrect: false`.
    3. If NO "none" option exists: Set ALL existing `isCorrect:` values
       to `false`. In your "explanation" field, include exactly this
       marker: "[NEEDS_HUMAN: no 'none of the above' option exists]"

    IMPORTANT: Your substitution must leave the YAML valid. Normally at
    least one answer should be `isCorrect: true`. The ONLY exception is
    the "none of the above" case when no such option exists — then the
    marker in explanation signals human review is required.

    Your `current_text` and `desired_text` should be MULTI-LINE blocks
    that include enough YAML to be unambiguous (e.g. the `content:`
    line above the `isCorrect:` line, so we know WHICH answer's flag
    is being toggled).

HOW TO HANDLE UNIT MARKDOWN FILES (.md):
    Edit the literal prose. For typos, broken links, factually-wrong
    sentences, etc., make the smallest change that fixes the bug. Do
    NOT rewrite whole paragraphs unless the user explicitly says so.

GENERAL:
  • Never invent quotes or content that isn't in the file.
  • Keep desired_text minimal — change only what is necessary.
  • If the file genuinely doesn't contain anything matching the user's
    description, return all three fields as null. We'd rather skip a
    fix than ship a wrong one.
"""


def refine_fix_plan_with_file_content(
    issue: dict,
    fix_plan: dict,
    file_path: str,
    token: str | None = None,
    model: str | None = None,
    max_file_chars: int = 16000,
) -> dict | None:
    """Ask the LLM to convert a vague current/desired pair into an
    exact verbatim substitution rooted in the actual file contents.

    Returns the refined fix_plan dict (with the SAME shape as the input
    plus a guaranteed-grounded current_text/desired_text), or None when
    the model gives up / errors out.
    """
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            file_contents = fh.read()
    except OSError as exc:
        print(f"⚠️ Could not read {file_path} for refinement: {exc}")
        return None

    # Keep the prompt under control by truncating very large files. Most
    # Learn unit files are small (a few KB); 16 KB is plenty.
    truncated = file_contents[:max_file_chars]
    truncation_note = (
        f"\n\n[file truncated to {max_file_chars} chars of {len(file_contents)}]"
        if len(file_contents) > max_file_chars else ""
    )

    file_ext = os.path.splitext(file_path)[1].lower()
    file_kind = {
        ".yml":  "YAML (likely a knowledge-check; edit `isCorrect:` flags, not `content:` strings)",
        ".yaml": "YAML (likely a knowledge-check; edit `isCorrect:` flags, not `content:` strings)",
        ".md":   "Markdown unit prose (edit the literal text)",
    }.get(file_ext, "unknown file type")

    user_msg = (
        f"Issue title:\n{issue.get('title', '')}\n\n"
        f"Issue body:\n{issue.get('body', '')}\n\n"
        f"AI's first-pass interpretation of the change:\n"
        f"  current (paraphrased): {fix_plan.get('current_text')!r}\n"
        f"  desired (paraphrased): {fix_plan.get('desired_text')!r}\n"
        f"  explanation:          {fix_plan.get('explanation')!r}\n\n"
        f"File path: {file_path}\n"
        f"File type: {file_kind}\n\n"
        f"File contents below — your current_text MUST be a verbatim "
        f"substring of this:\n"
        f"---FILE START---\n{truncated}{truncation_note}\n---FILE END---"
    )

    messages = [
        {"role": "system", "content": REFINEMENT_SYSTEM_PROMPT},
        {"role": "user",   "content": user_msg},
    ]

    if _DEBUG:
        print("─── Refinement prompt (user turn) ───")
        print(user_msg[:1200] + ("...[trimmed]" if len(user_msg) > 1200 else ""))
        print("─────────────────────────────────────")

    try:
        api_response = _call_github_models(messages, model=model or _DEFAULT_MODEL, token=token)
        raw_content = api_response["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError,
            IndexError, ValueError) as exc:
        print(f"⚠️ Refinement call failed ({type(exc).__name__}: {exc})")
        return None

    if _DEBUG:
        print("─── Refinement raw content ───")
        print(raw_content)
        print("──────────────────────────────")

    # Strip stray markdown fences if any
    cleaned = raw_content
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        refined = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        print(f"⚠️ Refinement JSON parse failed: {exc}")
        return None

    current = refined.get("current_text")
    desired = refined.get("desired_text")
    explanation = refined.get("explanation") or fix_plan.get("explanation")

    if not current or not desired:
        print("⚠️ Refinement returned null current/desired — model declined to guess.")
        return None

    # Hard guard: the model is REQUIRED to ground current in the file.
    # If it didn't, the substitution would silently fail.
    if current not in file_contents:
        print(f"⚠️ Refined current_text not found verbatim in {file_path}; rejecting.")
        return None

    return {
        "module_url":   fix_plan.get("module_url"),
        "current_text": current,
        "desired_text": desired,
        "explanation":  explanation,
    }


# Convenience for ad-hoc debugging:  `python3 ai_triage.py <issue.json>`
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ai_triage.py <issue.json>")
        sys.exit(1)
    with open(sys.argv[1]) as fh:
        issue_data = json.load(fh)
    result = ai_or_fallback(issue_data)
    print(json.dumps(result, indent=2))
