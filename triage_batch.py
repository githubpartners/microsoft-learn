import os
import json
import subprocess
import re
import sys
from datetime import datetime
from issue_analyzer import (
    generate_context_aware_comment,
    generate_pr_description,
    intelligent_classify,
    is_skills_exercise_issue,
)
from ai_triage import ai_or_fallback

REPO = os.environ.get("GITHUB_REPOSITORY")

# ==============================
# UTILITIES
# ==============================
def run(cmd):
    """Execute shell command safely"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Command failed: {cmd}")
        print(f"STDERR: {result.stderr}")
    return result.stdout.strip()


def gh(cmd):
    """GitHub CLI wrapper"""
    return run(f'gh {cmd} --repo "{REPO}"')


# ==============================
# LABEL MANAGEMENT
# ==============================
def ensure_label(label):
    """Create label if it doesn't exist"""
    run(f'gh label create "{label}" --repo "{REPO}" 2>/dev/null || true')


def add_label(issue, label):
    """Add label to issue"""
    ensure_label(label)
    gh(f'issue edit {issue} --add-label "{label}"')


# Labels we apply during triage. Used to detect "already processed"
# issues so the scheduled batch run doesn't re-comment / re-PR them.
TRIAGE_LABELS = frozenset({
    "triaged",
    "auto-fix",
    "auto-fix-applied",
    "auto-fix-attempted",
    "needs-review",
    "needs-context",
    "skills-review-needed",
    "spam",
})


def _issue_labels(issue):
    """Return a normalized set of label names on the issue.

    `gh issue list` returns labels as `[{"name": "...", ...}, ...]`, but
    raw API payloads sometimes pass them as plain strings. Handle both.
    """
    labels = issue.get("labels") or []
    out = set()
    for lbl in labels:
        if isinstance(lbl, dict):
            name = lbl.get("name")
        else:
            name = lbl
        if name:
            out.add(name.strip().lower())
    return out


def already_triaged(issue):
    """True iff the issue already carries one of our triage labels.

    The single-issue (event-driven) workflow path always re-processes —
    when a human edits an issue, they want fresh triage — but the
    scheduled batch run uses this to skip issues it has already handled.
    """
    return bool(_issue_labels(issue) & {l.lower() for l in TRIAGE_LABELS})


# ==============================
# TEXT PARSING
# ==============================
def extract_urls(text):
    """Extract URLs from text"""
    return re.findall(r'https?://\S+', text)


def extract_module_slug(url):
    """Extract MS Learn module slug from URL"""
    if "training/modules/" not in url:
        return None
    match = re.search(r'/training/modules/([^/?]+)', url)
    return match.group(1) if match else None


def extract_unit_slug(url):
    """Extract the unit slug from a Microsoft Learn module URL.

    Handles both shapes you'll see in the wild:
      • .../modules/<mod>/units/<unit>          (the formal anchor)
      • .../modules/<mod>/<n>-<unit-name>       (the public training URL,
                                                  e.g. .../7-knowledge-check)
    """
    if not url:
        return None

    # Strip query/fragment so a trailing ? or # never trips the regex.
    url = url.split("?", 1)[0].split("#", 1)[0]

    # Shape 1: explicit /units/<slug>
    m = re.search(r"/units/([^/?#]+)", url)
    if m:
        return m.group(1)

    # Shape 2: trailing segment after /modules/<mod>/ — e.g.
    #   /training/modules/manage-work-github-projects/7-knowledge-check
    m = re.search(r"/training/modules/[^/]+/([^/?#]+)/?$", url)
    if m:
        slug = m.group(1)
        # Only accept it if it looks like a unit slug (starts with a digit
        # or contains a hyphen), to avoid grabbing query-only paths.
        if re.match(r"^\d+[-/]?|\w[-\w]*$", slug):
            return slug

    return None


# ==============================
# CLASSIFICATION (AI-powered, with heuristic fallback)
# ==============================
def classify(issue):
    """
    Ask an LLM (via GitHub Models) to triage the issue. The full structured
    decision — including the user-facing comment and an auto-fix plan — is
    cached on the issue dict for downstream steps. The function returns the
    classification string for backward compatibility with existing callers.
    """
    if is_skills_exercise_issue(issue):
        issue["_confidence"] = 100
        return "skills_review_needed"

    # If we've already classified this issue in this run, reuse it. This avoids
    # paying for the same LLM call twice (once during the auto_fix pre-scan,
    # once during process_issue) and avoids flaky non-determinism between calls.
    if "_ai_decision" in issue:
        return issue["_ai_decision"]["classification"]

    decision = ai_or_fallback(issue)
    issue["_ai_decision"] = decision
    # Preserve the legacy keys that other code still reads.
    issue["_confidence"] = decision["confidence"]
    issue["_analysis"] = {
        "specificity_score": decision["confidence"],   # informational only
        "confidence":        decision["confidence"],
        "actionability":     decision["confidence"],
        "issue_type":        [],
        "context_level":     {},
        "problem_statement": {
            "current": (decision.get("fix_plan") or {}).get("current_text"),
            "desired": (decision.get("fix_plan") or {}).get("desired_text"),
            "location": (decision.get("fix_plan") or {}).get("module_url"),
            "summary":  issue.get("title", ""),
        },
        "proposed_fix": {
            "explicit":   (decision.get("fix_plan") or {}).get("explanation"),
            "inferred":   None,
            "confidence": decision["confidence"] / 100.0,
        },
        "_source": decision["source"],
        "_reasoning": decision["reasoning"],
    }
    return decision["classification"]


# ==============================
# LEARN REPO FILE RESOLUTION
# ==============================
UPSTREAM_REPO = "MicrosoftDocs/learn-pr"
REPO_PATH = "/tmp/learn-pr"


def _gh_authenticated_user(token):
    """Return the login of the account behind LEARN_PR_TOKEN."""
    result = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"],
        capture_output=True, text=True,
        env={**os.environ, "GH_TOKEN": token, "GITHUB_TOKEN": token},
    )
    if result.returncode != 0:
        print(f"⚠️ Could not resolve token owner: {result.stderr.strip()}")
        return None
    return result.stdout.strip() or None


def _ensure_fork(token, upstream=UPSTREAM_REPO):
    """Ensure the token's owner has a fork of `upstream`.

    Returns the fork in `owner/repo` form, or None on failure.

    Strategy:
      1. Resolve the token owner via `gh api user`.
      2. Probe `gh api repos/<owner>/<repo-name>` — if it exists and is a
         fork, we're done (saves a CLI call and avoids the flag-compat
         issues with `gh repo fork`).
      3. Otherwise call `gh repo fork <upstream>` to create it. We don't
         pass `--clone=false` / `--remote=false` because newer `gh`
         versions reject those flags when a repository argument is given;
         the bare command is already "fork, don't clone" by default in
         non-interactive contexts.
    """
    owner = _gh_authenticated_user(token)
    if not owner:
        return None

    repo_name = upstream.split("/", 1)[1]
    fork = f"{owner}/{repo_name}"

    print(f"🔱 Ensuring fork {fork} exists ...")
    gh_env = {**os.environ, "GH_TOKEN": token, "GITHUB_TOKEN": token}

    # 1. Quick existence probe via the REST API.
    probe = subprocess.run(
        ["gh", "api", f"repos/{fork}", "--jq", ".fork"],
        capture_output=True, text=True, env=gh_env,
    )
    if probe.returncode == 0 and probe.stdout.strip().lower() == "true":
        print(f"✅ Fork already exists: {fork}")
        return fork

    # 2. Create the fork. `gh repo fork` is idempotent: if the fork was
    #    just created by a parallel run it prints a notice and exits 0.
    print(f"🔱 Creating fork {fork} from {upstream} ...")
    result = subprocess.run(
        ["gh", "repo", "fork", upstream],
        capture_output=True, text=True, env=gh_env,
    )
    combined = (result.stdout + result.stderr).lower()
    if result.returncode != 0 and "already exists" not in combined:
        print(f"❌ Could not fork {upstream}: "
              f"{(result.stderr or result.stdout).strip()}")
        return None

    print(f"✅ Fork ready: {fork}")
    return fork


def _sync_fork_main(token, fork, upstream=UPSTREAM_REPO):
    """Sync the fork's default branch with the upstream's default branch.

    Uses the GitHub REST endpoint POST /repos/{owner}/{repo}/merge-upstream
    which is the same thing the "Sync fork" button does in the web UI.
    Safe to call repeatedly; it's a no-op when the fork is already up to date.
    """
    print(f"🔄 Syncing {fork}:main ⇐ {upstream}:main ...")
    result = subprocess.run(
        ["gh", "api", "--method", "POST",
         f"repos/{fork}/merge-upstream",
         "-f", "branch=main"],
        capture_output=True, text=True,
        env={**os.environ, "GH_TOKEN": token, "GITHUB_TOKEN": token},
    )
    if result.returncode != 0:
        # Non-fatal: an out-of-date fork is still usable, but we want to log
        # it loudly so we know to investigate if PRs start diverging.
        msg = (result.stderr or result.stdout or "").strip()
        print(f"⚠️ Could not sync fork main (continuing anyway): {msg}")
        return False
    print(f"✅ Fork main synced: {result.stdout.strip()}")
    return True


def clone_learn_repo():
    """Sparse-clone the user's fork (as `origin`) after syncing it with upstream.

    The MS Learn monorepo is ~1–2 GB; a full clone exhausts the runner's
    disk (`No space left on device`). Instead we do a partial + sparse
    clone that downloads only the commit graph (no blobs, no working
    copy). Individual module subtrees are materialized on demand via
    :func:`ensure_sparse_paths` when an auto-fix issue actually needs them.

    Why we clone the fork rather than the upstream:
      • `MicrosoftDocs/learn-pr` is behind SAML SSO and rejects
        unauthenticated `git clone`.
      • The fork lives in the LEARN_PR_TOKEN owner's own namespace, so it
        is freely accessible with the token — no SAML authorization needed.
      • Before cloning we hit `POST repos/<fork>/merge-upstream`, which is
        the same thing the "Sync fork" button does in the UI. GitHub
        performs the merge server-side, so we don't need direct upstream
        access to keep the fork current.

    Returns the (repo_path, fork_slug) tuple, or (None, None) on failure.
    """
    token = os.environ.get("LEARN_PR_TOKEN")
    if not token:
        print("❌ LEARN_PR_TOKEN not set — skipping auto-PR step.")
        return None, None

    # 1. Ensure a fork exists in the token-owner's namespace.
    fork = _ensure_fork(token)
    if not fork:
        print("❌ Could not establish a fork — aborting auto-PR step.")
        return None, None

    # 2. Sync the fork's `main` with upstream's `main` FIRST. We do this
    #    before cloning so the fork we then pull down is already current.
    _sync_fork_main(token, fork)

    # 3. Sparse-clone the fork as `origin`. Flags explained:
    #      --filter=blob:none   — fetch the commit + tree graph but no
    #                             file blobs (blobs are pulled lazily
    #                             when paths are checked out).
    #      --no-checkout        — don't materialize a working copy yet.
    #      --sparse             — enable sparse-checkout mode (we'll add
    #                             specific paths later via
    #                             ensure_sparse_paths()).
    #    Combined with `git sparse-checkout`, this means we only ever
    #    pay for the module subtrees we actually edit.
    print(f"📥 Sparse-cloning fork {fork} as origin "
          f"(blob:none, no checkout) ...")
    run(f"rm -rf {REPO_PATH}")
    fork_url = f"https://x-access-token:{token}@github.com/{fork}.git"
    result = subprocess.run(
        f"git clone --filter=blob:none --no-checkout --sparse "
        f"{fork_url} {REPO_PATH}",
        shell=True, capture_output=True, text=True,
    )
    if result.returncode != 0 or not os.path.isdir(os.path.join(REPO_PATH, ".git")):
        print(f"❌ Failed to sparse-clone fork {fork}: "
              f"{result.stderr.strip()}")
        return None, None
    print(f"✅ Sparse-cloned fork to {REPO_PATH}")

    # 4. Initialize sparse-checkout in no-cone mode with an effectively
    #    empty pattern set. We use a literal path that will never match
    #    anything in the repo as a placeholder; subsequent
    #    ensure_sparse_paths() calls will replace this with real patterns.
    run(f"cd {REPO_PATH} && git sparse-checkout init --no-cone")
    run(f"cd {REPO_PATH} && git sparse-checkout set '/__no_match_placeholder__'")

    # 5. Add the upstream as a read-only remote called `upstream`. This
    #    might 401 in a SAML-enforced setup, which is fine — we never
    #    fetch from it; `origin/main` is already in sync thanks to the
    #    REST sync above.
    upstream_url = f"https://github.com/{UPSTREAM_REPO}.git"
    run(f"cd {REPO_PATH} && git remote remove upstream 2>/dev/null; "
        f"git remote add upstream {upstream_url}")

    # 6. Make sure origin/main is the freshest view of the fork's default
    #    branch (it should be after the clone, but a no-op fetch costs
    #    nothing and guards against odd default-branch races).
    run(f"cd {REPO_PATH} && git fetch origin main --quiet || true")

    # 7. Track which sparse paths we've already added in-process so
    #    repeated calls for the same module are no-ops.
    if not hasattr(clone_learn_repo, "_materialized_paths"):
        clone_learn_repo._materialized_paths = set()
    clone_learn_repo._materialized_paths.clear()

    return REPO_PATH, fork


def _candidate_module_paths(module_slug):
    """Return the sparse-checkout path patterns to try for a module slug.

    The MS Learn monorepo nests modules under several roots. The two most
    common in `MicrosoftDocs/learn-pr` are:
      • `learn-pr/learn-pr/<topic>/<module-slug>/`   ← e.g. .../github/manage-work-...
      • `learn-pr/<topic>/<module-slug>/`
      • `learn-pr-mooc/...`

    Materializing all plausible roots costs only an extra index entry per
    pattern, so we over-include rather than guess.
    """
    safe_slug = module_slug.strip("/").strip()
    if not safe_slug:
        return []
    return [
        # 4-deep nesting (the common case in the modern monorepo)
        f"learn-pr/learn-pr/**/{safe_slug}/**",
        # 3-deep nesting
        f"learn-pr/**/{safe_slug}/**",
        # Legacy / direct nesting
        f"learn-pr/{safe_slug}/**",
        f"learn-pr-mooc/**/{safe_slug}/**",
        f"{safe_slug}/**",
    ]


def ensure_sparse_paths(repo_path, module_slugs):
    """Materialize the working-copy slices needed for the given module(s).

    Call this before reading files from a module. It:
      1. Adds the candidate sparse-checkout paths for each slug.
      2. Runs `git checkout` to materialize matching files (blobs are
         pulled on-demand thanks to the partial clone).
    Subsequent calls for the same slug are no-ops.
    """
    if not module_slugs:
        return
    if not hasattr(clone_learn_repo, "_materialized_paths"):
        clone_learn_repo._materialized_paths = set()
    cache = clone_learn_repo._materialized_paths

    new_patterns = []
    for slug in module_slugs:
        if not slug or slug in cache:
            continue
        cache.add(slug)
        patterns = _candidate_module_paths(slug)
        if patterns:
            print(f"🧩 Materializing sparse paths for module {slug!r}...")
            for p in patterns:
                print(f"   + {p}")
            new_patterns.extend(patterns)

    if not new_patterns:
        return

    # `sparse-checkout add` is incremental — it ORs new patterns into the
    # existing set, so previously materialized modules stay materialized.
    quoted = " ".join(f"'{p}'" for p in new_patterns)
    run(f"cd {repo_path} && git sparse-checkout add {quoted}")
    # Materialize matching files on the current branch.
    run(f"cd {repo_path} && git checkout --quiet")
    print("✅ Sparse paths materialized")


def find_module_path(repo_path, module_slug):
    """Find the directory whose **basename** matches module_slug exactly.

    We compare on basename, not substring, so a slug like
    `code-reviews-pull-requests-github-copilot` doesn't accidentally
    match a parent directory that happens to contain the substring.
    """
    slug = module_slug.lower()
    for root, dirs, _files in os.walk(repo_path):
        # Skip the .git internals
        dirs[:] = [d for d in dirs if d != ".git"]
        for d in dirs:
            if d.lower() == slug:
                return os.path.join(root, d)
    return None


def _file_matches_unit(filename, unit_slug):
    """True when the file name corresponds to the given unit slug.

    Handles both shapes seen in practice:
      • `7-knowledge-check.yml`          (most modules)
      • `knowledge-check.yml`            (older modules)
      • `7-knowledge-check.md`           (rare; some units are full md)
    The match is on the stem (without extension) and tolerates a leading
    `<digits>-` ordering prefix on either side.
    """
    if not unit_slug:
        return False
    stem = os.path.splitext(filename)[0].lower()
    slug = unit_slug.lower()
    # Strip a leading "N-" ordering prefix from BOTH sides for comparison.
    stem_naked = re.sub(r"^\d+-", "", stem)
    slug_naked = re.sub(r"^\d+-", "", slug)
    return (
        stem == slug
        or stem_naked == slug_naked
        or stem.endswith("-" + slug_naked)
        or slug_naked == stem
    )


def find_target_file(repo_path, module_slug, unit_slug):
    """Locate the file that this issue is about.

    MS Learn modules in `MicrosoftDocs/learn-pr` are laid out like:

        learn-pr/learn-pr/<topic>/<module-slug>/
        ├── index.yml
        ├── <n>-knowledge-check.yml     ← knowledge-check answers
        ├── ...
        └── includes/
            ├── <n>-<unit-name>.md      ← unit prose content
            └── ...

    Strategy:
      1. Locate the module directory by exact basename.
      2. If we have a unit slug, look for a file whose stem matches it,
         checking BOTH the module root (for .yml) and `includes/`
         (for .md). Prefer .yml when the unit slug looks like a
         knowledge check, since fixes for "this answer is wrong" need
         to edit the YAML, not the markdown.
      3. If we don't have a unit slug, give up — we refuse to guess
         which file to edit.
    """
    module_path = find_module_path(repo_path, module_slug)
    if not module_path:
        return None

    # Search roots, in priority order.
    search_roots = [module_path]
    includes_path = os.path.join(module_path, "includes")
    if os.path.isdir(includes_path):
        search_roots.append(includes_path)

    if not unit_slug:
        print("⚠️ No unit slug — refusing to guess which file to edit.")
        return None

    is_kc = "knowledge" in unit_slug.lower() and "check" in unit_slug.lower()

    # Build a list of (filepath, ext) candidates whose name matches unit_slug.
    candidates = []
    for root in search_roots:
        try:
            entries = os.listdir(root)
        except OSError:
            continue
        for f in entries:
            full = os.path.join(root, f)
            if not os.path.isfile(full):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext not in (".yml", ".yaml", ".md"):
                continue
            if _file_matches_unit(f, unit_slug):
                candidates.append((full, ext))

    if not candidates:
        return None

    # Prefer YAML for knowledge checks, otherwise prefer markdown.
    def score(item):
        path, ext = item
        if is_kc:
            return 0 if ext in (".yml", ".yaml") else 1
        return 0 if ext == ".md" else 1

    candidates.sort(key=score)
    return candidates[0][0]


# ==============================
# GIT OPERATIONS
# ==============================
def _run_git(repo_path, args, check=False):
    """Run `git <args>` in `repo_path` without going through a shell.

    Returns the completed CompletedProcess so callers can inspect both
    stdout and stderr — `run()` swallows stderr, which has bitten us in
    the past (silent commit failures).
    """
    cmd = ["git", "-C", repo_path, *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"❌ git {' '.join(args)} failed (exit {result.returncode})")
        if result.stdout:
            print(f"   stdout: {result.stdout.strip()}")
        if result.stderr:
            print(f"   stderr: {result.stderr.strip()}")
    return result


def setup_git_config():
    """Configure a global git identity for the bot.

    Note: we ALSO set repo-local user.name/email inside commit_changes() —
    this global config is just a belt-and-suspenders default in case some
    git operation runs outside a known repo.
    """
    run("git config --global user.name 'issue-triage-bot'")
    run("git config --global user.email 'bot@github.com'")


def reset_repo(repo_path):
    """Reset repo to clean state"""
    run(f"cd {repo_path} && git fetch origin main && git reset --hard origin/main && git clean -fd")


def create_branch(repo_path, branch_name):
    """Create a fresh branch off the upstream's latest `main`.

    Defensive in two ways:
      1. Refuse to ever create a branch literally named "main" — we never
         want to push directly to the default branch.
      2. Delete any pre-existing local branch with the same name and recreate
         it from a fresh `origin/main`, so re-running the workflow always
         produces a PR based on the freshest upstream content.
    """
    if branch_name.strip().lower() in {"main", "master"}:
        raise ValueError(
            f"Refusing to create a working branch named {branch_name!r} — "
            "fixes must live on a feature branch, never on main."
        )

    # Make sure we have origin/main up-to-date locally
    run(f"cd {repo_path} && git fetch origin main --quiet")
    # Wipe any pre-existing local branch with the same name
    run(f"cd {repo_path} && git checkout --quiet origin/main")
    run(f"cd {repo_path} && git branch -D {branch_name} 2>/dev/null || true")
    # Create the branch off the latest upstream main
    run(f"cd {repo_path} && git checkout -b {branch_name} origin/main")


def commit_changes(repo_path, issue_num, commit_msg):
    """Stage all changes and commit them, returning True iff a commit was made.

    Differs from the old implementation in three important ways:
      1. Uses subprocess directly with a list of args — no shell quoting,
         so commit messages with apostrophes / colons / quotes are safe.
      2. Sets repo-local user.name/user.email before committing, so a
         missing or wrong global git identity doesn't silently break us.
      3. Pre-checks `git status --porcelain` so "nothing staged" is
         reported as exactly that, rather than inferred from a stderr
         substring after the fact.
    Every git invocation's stdout AND stderr are surfaced on failure so
    we never again see a "STDERR:" with empty content.
    """
    # Repo-local identity — the global config may be absent in some
    # runner environments (cached/restored repos, etc.).
    _run_git(repo_path, ["config", "user.name",  "issue-triage-bot"])
    _run_git(repo_path, ["config", "user.email", "bot@github.com"])

    # Stage everything (additions, modifications, deletions).
    add = _run_git(repo_path, ["add", "-A"], check=True)
    if add.returncode != 0:
        print(f"❌ Could not stage changes for issue #{issue_num} — aborting commit.")
        return False

    # Did anything actually change?
    status = _run_git(repo_path, ["status", "--porcelain"])
    if not status.stdout.strip():
        print(f"⚠️ No staged changes for issue #{issue_num} — nothing to commit.")
        return False

    # Commit. Passing the message as a separate argv entry avoids ALL
    # shell-escaping issues.
    commit = _run_git(repo_path, ["commit", "-m", commit_msg])
    if commit.returncode != 0:
        print(f"❌ git commit failed for issue #{issue_num} "
              f"(exit {commit.returncode})")
        if commit.stdout:
            print(f"   stdout: {commit.stdout.strip()}")
        if commit.stderr:
            print(f"   stderr: {commit.stderr.strip()}")
        return False

    # Optional but useful: surface the commit short-hash + subject.
    head = _run_git(repo_path, ["log", "-1", "--pretty=%h %s"])
    print(f"✅ Committed: {head.stdout.strip()}")
    return True


def push_branch(repo_path, branch_name, remote="origin"):
    """Push branch to the named remote.

    Default is `origin`, which is wired to the user's fork by
    `clone_learn_repo()` (see that function's docstring for why we clone
    the fork as origin rather than the upstream).

    Hard-refuses to push to `main` / `master` — those branches are managed
    purely by the upstream-sync step (`_sync_fork_main`).
    """
    if branch_name.strip().lower() in {"main", "master"}:
        raise ValueError(
            f"Refusing to push branch {branch_name!r} — "
            "the fork's default branch is kept in sync with upstream, "
            "never modified by the bot."
        )
    run(
        f"cd {repo_path} && "
        f"git push {remote} {branch_name} --force-with-lease "
        f"|| git push {remote} {branch_name} --force"
    )


def create_pr(repo, branch_name, issue_num, title, body, head_owner=None):
    """Open a PR against `repo` from the user's fork.

    `head_owner` is the GitHub login of the fork's owner; when provided we
    use the cross-repo `--head <owner>:<branch>` syntax so gh knows to look
    on the fork.
    """
    # Write the body to a file to avoid quoting hell in the shell.
    body_path = f"/tmp/pr-body-{issue_num}.md"
    with open(body_path, "w") as f:
        f.write(body)

    head = f"{head_owner}:{branch_name}" if head_owner else branch_name
    gh_cmd = (
        f"pr create "
        f"--repo {repo} "
        f"--title \"{title}\" "
        f"--body-file {body_path} "
        f"--head {head} "
        f"--base main"
    )
    # We need to call gh with the LEARN_PR_TOKEN, not GITHUB_TOKEN (which is
    # scoped to the triage repo and can't see the fork).
    token = os.environ.get("LEARN_PR_TOKEN")
    if token:
        return subprocess.run(
            f"gh {gh_cmd}",
            shell=True, capture_output=True, text=True,
            env={**os.environ, "GH_TOKEN": token, "GITHUB_TOKEN": token},
        ).stdout.strip()
    return run(f"gh {gh_cmd}")


# ==============================
# ISSUE PROCESSING
# ==============================
def apply_intelligent_fix(file_path, analysis):
    """Apply a literal text substitution and PERSIST it to disk.

    Returns True iff the file was changed AND saved. Previously this
    function mutated `content` in memory and returned True without ever
    writing the file back — which made every "successful" auto-fix end
    with `git status` reporting no staged changes. Don't do that again.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    problem = analysis.get("problem_statement", {})
    current = problem.get("current")
    desired = problem.get("desired")

    if not current or not desired:
        return False

    new_content = None
    fix_kind = None

    # Strategy 1: exact substring match (preferred — predictable).
    if current in original_content:
        new_content = original_content.replace(current, desired, 1)
        fix_kind = "exact"

    # Strategy 2: case-insensitive single replacement.
    if new_content is None:
        ci_pattern = re.compile(re.escape(current), re.IGNORECASE)
        if ci_pattern.search(original_content):
            new_content = ci_pattern.sub(desired, original_content, count=1)
            fix_kind = "case-insensitive"

    # Strategy 3: long-phrase contextual rewrite (rarely needed; keep as a
    # last-resort fallback).
    if new_content is None and len(current) > 20:
        key_words = current.split()[:3]
        kw_pattern = r"\b" + r"\s+".join(re.escape(w) for w in key_words) + r"\b"
        match = re.search(kw_pattern, original_content, re.IGNORECASE)
        if match:
            start, end = match.start(), match.end()
            sentence_start = original_content.rfind(".", 0, start) + 1
            sentence_end = original_content.find(".", end) + 1
            if sentence_end == 0:
                sentence_end = len(original_content)
            new_content = (
                original_content[:sentence_start]
                + desired
                + original_content[sentence_end:]
            )
            fix_kind = "contextual"

    if new_content is None:
        print(f"⚠️ Could not find pattern to replace in {file_path}")
        return False

    if new_content == original_content:
        # The substitution was a no-op (e.g. current == desired). Nothing
        # to write, and reporting success would mislead the caller.
        print(f"⚠️ Substitution was a no-op ({fix_kind}); not writing {file_path}")
        return False

    # PERSIST the change. This is the line whose absence caused issue #4
    # to "succeed" with `git status` clean.
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    delta = len(new_content) - len(original_content)
    print(f"✅ Applied {fix_kind} fix to {file_path} "
          f"({len(original_content)} → {len(new_content)} chars, {delta:+d})")
    return True


def validate_knowledge_check_yaml(file_path, explanation=None):
    """Validate a knowledge-check YAML after edits.

    Returns a tuple of (is_valid, needs_human_review, reason).

    Checks:
      1. The file parses as valid YAML.
      2. At least one answer has `isCorrect: true` — UNLESS the
         explanation contains "[NEEDS_HUMAN:" which signals the AI
         intentionally set all to false for a "none of the above"
         case where no such option exists.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in (".yml", ".yaml"):
        # Not a YAML file — skip validation, assume OK.
        return (True, False, None)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as exc:
        return (False, True, f"Could not read file: {exc}")

    # Check for the special marker indicating intended "all false" state.
    needs_human_marker = "[NEEDS_HUMAN:" in (explanation or "")

    # Count isCorrect occurrences.
    true_count = len(re.findall(r"isCorrect:\s*true", content, re.IGNORECASE))
    false_count = len(re.findall(r"isCorrect:\s*false", content, re.IGNORECASE))
    total_answers = true_count + false_count

    if total_answers == 0:
        # Not a knowledge-check file, or unexpected format.
        return (True, False, "No isCorrect fields found — not a knowledge-check YAML")

    if true_count == 0:
        if needs_human_marker:
            # The AI intentionally set all to false; flag for human review
            # but don't block the PR.
            return (True, True, 
                    "All answers marked incorrect (no 'none of the above' option exists) — "
                    "human review required to add the missing option or correct the question.")
        else:
            # No correct answer and no marker — this is an error.
            return (False, True, 
                    "No correct answer (`isCorrect: true`) found in knowledge-check YAML. "
                    "This would break the module. Human review required.")

    if true_count > 1:
        # Multiple correct answers — MS Learn knowledge checks typically
        # allow only one correct answer per question.
        return (True, True, 
                f"Multiple correct answers ({true_count}) found. "
                "Verify this is intentional for this question type.")

    # Exactly one correct answer — all good.
    return (True, False, None)


def process_auto_fix_issue(issue, repo_path, fork_slug=None):
    """
    Process auto-fix issues using the AI's structured fix plan.

    Workflow:
      1. Resolve the MS Learn URL → module / unit → target markdown file
      2. Apply the literal current_text → desired_text replacement that the
         AI produced (falling back to the heuristic analysis if absent).
      3. Commit, push to the user's fork, open a cross-repo PR against
         MicrosoftDocs/learn-pr.
    """
    issue_num = issue["number"]
    body = issue.get("body", "")
    title = issue.get("title", "")

    decision = issue.get("_ai_decision") or {}
    fix_plan = decision.get("fix_plan") or {}
    analysis = issue.get("_analysis", {})

    # Prefer the URL the AI extracted (it ignored template noise); fall back
    # to scanning the body ourselves.
    primary_url = fix_plan.get("module_url")
    if not primary_url:
        urls = extract_urls(body)
        if not urls:
            print(f"⚠️ Issue #{issue_num} has no URL — cannot auto-fix")
            return False
        primary_url = urls[0]

    module_slug = extract_module_slug(primary_url)
    unit_slug = extract_unit_slug(primary_url)

    if not module_slug:
        print(f"⚠️ Issue #{issue_num} URL doesn't match a learn module pattern: {primary_url}")
        return False

    print(f"🔍 Module: {module_slug}, Unit: {unit_slug}")

    # Materialize ONLY this module's files from the sparse-clone.
    # The clone itself is blobless + no-checkout (see clone_learn_repo);
    # this is the step that actually puts files on disk.
    ensure_sparse_paths(repo_path, [module_slug])

    # Find file to edit
    target_file = find_target_file(repo_path, module_slug, unit_slug)
    if not target_file:
        print(f"⚠️ Could not locate file in learn-pr for module={module_slug}")
        return False

    print(f"📝 Target file: {target_file}")

    # Create branch
    branch_name = f"fix/issue-{issue_num}"
    create_branch(repo_path, branch_name)

    # Snapshot content before mutation so we can revert if the commit fails.
    with open(target_file, "r") as f:
        original_content = f.read()

    # ─── Refine the AI's fix plan against the ACTUAL file ────────────
    # The first-pass classification (run on issue body alone) often
    # paraphrases — e.g. it produces "first answer is marked as correct"
    # which doesn't appear verbatim in the source markdown. Here we
    # re-ask the LLM with the file contents in hand to ground the
    # current/desired pair in real text.
    from ai_triage import refine_fix_plan_with_file_content
    refined = refine_fix_plan_with_file_content(issue, fix_plan, target_file)
    if refined:
        fix_plan = refined
        # Update the cached decision so PR body / explanation reflect the
        # grounded substitution.
        decision["fix_plan"] = refined

    # Prefer the (now-grounded) AI literal current/desired pair. Fall
    # back to the heuristic extraction stashed in `_analysis` only if
    # refinement failed AND the original plan also had something usable.
    current = fix_plan.get("current_text") or (analysis.get("problem_statement") or {}).get("current")
    desired = fix_plan.get("desired_text") or (analysis.get("problem_statement") or {}).get("desired")

    if not (current and desired):
        print(f"⚠️ No grounded current/desired pair for issue #{issue_num} — skipping PR")
        return False

    # Final sanity check: even after refinement, refuse to attempt a
    # substitution where current isn't actually in the file. This stops
    # us from creating empty PRs.
    if current not in original_content:
        print(f"⚠️ current_text {current!r} not found verbatim in target file — "
              "refusing to attempt fix")
        return False

    fix_applied = apply_intelligent_fix(
        target_file,
        {"problem_statement": {"current": current, "desired": desired}},
    )

    if fix_applied:
        # ─── Validate knowledge-check YAMLs ────────────────────────────
        # For YAML files, check that we haven't left the file in a broken
        # state (e.g. no correct answer). The AI may have intentionally
        # set all answers to false for a "none of the above" case — the
        # validation function detects this via the [NEEDS_HUMAN:] marker.
        ai_explanation = fix_plan.get("explanation")
        is_valid, needs_human, validation_reason = validate_knowledge_check_yaml(
            target_file, explanation=ai_explanation
        )

        if not is_valid:
            # The fix broke the file — revert and abort.
            print(f"❌ Post-fix validation failed: {validation_reason}")
            with open(target_file, "w") as f:
                f.write(original_content)
            return False

        # Commit and push to the fork (origin)
        commit_msg = f"Fix #{issue_num}: {title[:50]}"
        if commit_changes(repo_path, issue_num, commit_msg):
            push_branch(repo_path, branch_name, remote="origin")

            # PR description — prefer the AI's explanation, fall back to template
            pr_body = generate_pr_description(issue, {
                "problem_statement": {"current": current, "desired": desired,
                                       "location": primary_url,
                                       "summary": title},
                "proposed_fix": {"explicit": ai_explanation, "inferred": None},
                "issue_type": [],
                "specificity_score": decision.get("confidence", 0),
            })

            # Add validation warning to PR body if human review is needed.
            if needs_human and validation_reason:
                pr_body += (
                    "\n\n---\n\n"
                    "⚠️ **Reviewer attention required:**\n\n"
                    f"{validation_reason}\n"
                )

            pr_title = f"Fix #{issue_num}: {title[:60]}"

            # Open a cross-repo PR: head = <fork-owner>:<branch>, base = upstream main
            head_owner = fork_slug.split("/", 1)[0] if fork_slug else None
            pr_url = create_pr(
                repo=UPSTREAM_REPO,
                branch_name=branch_name,
                issue_num=issue_num,
                title=pr_title,
                body=pr_body,
                head_owner=head_owner,
            )

            print(f"✅ PR created: {pr_url or branch_name}")

            fork_link = (
                f"https://github.com/{fork_slug}/tree/{branch_name}"
                if fork_slug else "(see fork)"
            )

            # Build comment with optional human review warning.
            comment_body = (
                "✅ **Auto-fix PR opened**\n\n"
                f"Branch: `{branch_name}` on {fork_link}\n\n"
                f"{pr_url if pr_url else 'PR submitted (URL pending)'}"
            )
            if needs_human and validation_reason:
                comment_body += (
                    "\n\n⚠️ **Note:** This fix may require human review. "
                    f"{validation_reason}"
                )

            _post_comment(issue_num, comment_body)
            return True
        else:
            # Revert file if commit failed
            with open(target_file, "w") as f:
                f.write(original_content)
            return False
    else:
        # Could not apply fix, revert
        with open(target_file, "w") as f:
            f.write(original_content)
        print(f"⚠️ Could not apply fix to {target_file}")
        return False


def _post_comment(issue_num, body):
    """Post a comment via a temp file so multi-line / special-char bodies survive."""
    path = f"/tmp/triage-comment-{issue_num}.txt"
    with open(path, "w") as f:
        f.write(f"{body.rstrip()}\n\n<!-- issue-triage-agent -->\n")
    gh(f"issue comment {issue_num} -F {path}")


_TRIAGE_COMMENT_MARKERS = (
    "<!-- issue-triage-agent -->",
    "🧠 **Auto-triage Analysis:**",
    "🚩 **Review Needed**",
    "❓ **More Context Needed**",
    "❓ **Closed: More Specific Details Needed**",
    "🗑️ **Closed:**",
    "⚠️ I classified this as auto-fixable",
    "This issue has been classified as",
)


def _delete_previous_triage_comments(issue_num):
    """Delete earlier comments created by this triage workflow."""
    result = subprocess.run(
        [
            "gh", "api", "--paginate", "--slurp",
            f"repos/{REPO}/issues/{issue_num}/comments",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"⚠️ Could not list previous triage comments for issue #{issue_num}: "
              f"{result.stderr.strip()}")
        return

    try:
        pages = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"⚠️ Could not parse comments for issue #{issue_num}: {exc}")
        return

    comments = [comment for page in pages for comment in page]
    for comment in comments:
        author = (comment.get("user") or {}).get("login")
        body = comment.get("body") or ""
        if author != "github-actions[bot]" or not any(
            marker in body for marker in _TRIAGE_COMMENT_MARKERS
        ):
            continue
        delete = subprocess.run(
            [
                "gh", "api", "--method", "DELETE",
                f"repos/{REPO}/issues/comments/{comment['id']}",
            ],
            capture_output=True,
            text=True,
        )
        if delete.returncode == 0:
            print(f"🧹 Deleted previous triage comment {comment['id']} "
                  f"from issue #{issue_num}")
        else:
            print(f"⚠️ Could not delete triage comment {comment['id']} "
                  f"from issue #{issue_num}: {delete.stderr.strip()}")


def _comment_for(issue, classification, override=None):
    """Pick the best comment text: AI-authored if present, else templated fallback."""
    if override:
        return override
    decision = issue.get("_ai_decision") or {}
    if decision.get("comment"):
        return decision["comment"]
    return generate_context_aware_comment(issue.get("_analysis", {}), classification)


def process_issue(issue, repo_path=None, fork_slug=None):
    """Main issue processing function — AI-driven, with heuristic fallback."""
    issue_num = issue["number"]
    result = classify(issue)
    decision = issue.get("_ai_decision") or {}
    source = decision.get("source", "fallback")
    confidence = decision.get("confidence", issue.get("_confidence", 0))

    print(f"\n{'='*60}")
    print(f"Issue #{issue_num} → {result}  ({source}, confidence={confidence}/100)")
    print(f"Title: {issue.get('title', 'N/A')[:60]}")
    if decision.get("reasoning"):
        print(f"AI reasoning: {decision['reasoning'][:240]}")
    print(f"{'='*60}")

    _delete_previous_triage_comments(issue_num)

    # Ensure triaged label
    add_label(issue_num, "triaged")

    if result == "auto_fix":
        if repo_path:
            # We have a real cloned repo, so we can honestly attempt a PR.
            _post_comment(issue_num, _comment_for(issue, result))
            success = process_auto_fix_issue(issue, repo_path, fork_slug=fork_slug)
            if success:
                add_label(issue_num, "auto-fix-applied")
            else:
                add_label(issue_num, "auto-fix-attempted")
                _post_comment(
                    issue_num,
                    "⚠️ I classified this as auto-fixable but could not generate a PR "
                    "(either the target file/section wasn't found in "
                    "`MicrosoftDocs/learn-pr`, or the proposed change couldn't be "
                    "applied automatically). A human reviewer will take it from here.",
                )
        else:
            # No repo available (token missing or clone failed).
            # Down-grade to needs_human so we don't make false promises.
            print("⚠️ No learn-pr clone available — downgrading auto_fix → needs_human")
            _post_comment(issue_num, _comment_for(issue, "needs_human"))
            add_label(issue_num, "needs-review")

    elif result == "needs_human":
        _post_comment(issue_num, _comment_for(issue, result))
        add_label(issue_num, "needs-review")

    elif result == "skills_review_needed":
        _post_comment(
            issue_num,
            "🧰 **Skills Exercise Review Needed**\n\n"
            "This report concerns a GitHub Skills training or exercise. "
            "We are moving the complaint to the Skills exercise team to address.",
        )
        add_label(issue_num, "skills-review-needed")

    elif result == "needs_context":
        _post_comment(issue_num, _comment_for(issue, result))
        add_label(issue_num, "needs-context")
        gh(f'issue close {issue_num}')

    elif result == "spam":
        _post_comment(
            issue_num,
            _comment_for(
                issue, result,
                override=(
                    "🗑️ **Closed:** This issue appears to be the unfilled MS Learn "
                    "issue template (or otherwise lacks actionable content). Please "
                    "reopen with the template filled in if this was a mistake."
                ),
            ),
        )
        add_label(issue_num, "spam")
        gh(f'issue close {issue_num}')

    print(f"✅ Processed issue #{issue_num}")


# ==============================
# MAIN
# ==============================
def main():
    """Main entry point for batch processing.

    Behaviour:
      • In single-issue mode (TRIAGE_MODE=single, set by the workflow's
        `issues` event), we ALWAYS process the issue — a human just
        opened/edited it and wants fresh triage.
      • In batch mode (the default), we skip issues that already carry
        one of our triage labels, so the every-6-hours cron doesn't
        spam comments / try to re-open PRs for the same issue.
      • The user can override the skip with FORCE_RETRIAGE=1, useful
        when iterating on the analyzer.
    """
    if len(sys.argv) < 2:
        print("Usage: triage_batch.py <issues_json_file>")
        sys.exit(1)

    issues_file = sys.argv[1]
    if not os.path.exists(issues_file):
        print(f"❌ File not found: {issues_file}")
        sys.exit(1)

    with open(issues_file, "r") as f:
        issues = json.load(f)

    mode = os.environ.get("TRIAGE_MODE", "batch").lower()
    force = os.environ.get("FORCE_RETRIAGE", "").lower() in {"1", "true", "yes"}
    skip_already_triaged = (mode == "batch") and not force

    print(f"🔄 Processing {len(issues)} issue(s) — mode={mode}, "
          f"skip_already_triaged={skip_already_triaged}")

    # ── Filter step: drop issues we've already handled ────────────────
    if skip_already_triaged:
        kept, skipped = [], []
        for issue in issues:
            (skipped if already_triaged(issue) else kept).append(issue)
        if skipped:
            preview = ", ".join(f"#{i.get('number','?')}" for i in skipped[:10])
            more = "" if len(skipped) <= 10 else f" (+{len(skipped) - 10} more)"
            print(f"⏭️  Skipping {len(skipped)} already-triaged issue(s): "
                  f"{preview}{more}")
            print("   (set FORCE_RETRIAGE=1 to re-process them)")
        issues = kept

    if not issues:
        print("✅ Nothing new to process.")
        return

    # Only clone repo if we have auto-fix issues to act on.
    auto_fix_issues = [i for i in issues if classify(i) == "auto_fix"]
    repo_path, fork_slug = None, None

    if auto_fix_issues:
        print(f"\n📦 Found {len(auto_fix_issues)} auto-fix issues, cloning learn repo...")
        setup_git_config()
        repo_path, fork_slug = clone_learn_repo()

    # Process all (remaining) issues
    for i, issue in enumerate(issues, 1):
        try:
            process_issue(issue, repo_path, fork_slug=fork_slug)
        except Exception as e:
            issue_num = issue.get("number", "unknown")
            print(f"❌ Error processing issue #{issue_num}: {e}")
            try:
                _post_comment(
                    issue_num,
                    f"❌ Error during triage: {str(e)[:100]}",
                )
            except Exception:
                pass

    print(f"\n✅ Batch processing complete!")


if __name__ == "__main__":
    main()
