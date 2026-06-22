"""Smoke-test the AI triage pipeline.

Locally there is no GITHUB_TOKEN with models:read scope, so the AI call
raises and we exercise the heuristic fallback path. The point of this test
is to prove the fallback returns sensible classifications + comments.
"""
import os
import sys

os.environ.pop("GITHUB_TOKEN", None)  # force the fallback path

from ai_triage import ai_or_fallback

ISSUES = [
    {
        "number": 7,
        "title": "MS Learn Module Update Request: [REPLACE_WITH_MODULE_TITLE]",
        "body": (
            "Which of the MS Learn modules from the dropdown are you submitting an update request?\n"
            "None\n\nAdditional information\n\n"
            "Fix a broken user experience (broken links, exercise error, etc.)\n\n"
            "Update incorrect information\n\nAdd new content to the module\n\n"
            "Some other request\nInformation about the requested update\nNo response"
        ),
        "expected": "spam",
    },
    {
        "number": 4,
        "title": "MS Learn Module Update Request: Manage your work with GitHub Projects",
        "body": (
            "Information about the requested update\n"
            "https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/7-knowledge-check\n\n"
            "In Module assessment/Check your knowledge\n\n"
            "What Project descriptor automatically saves when you change it?\n\n"
            "Project name (Correct)\n\n\nProject description\n\n\nProject README\n\n"
            "first answer is marked as correct, should be: None of them."
        ),
        "expected": "auto_fix",
    },
]

lines = []
for issue in ISSUES:
    r = ai_or_fallback(issue)
    lines.append(
        f"#{issue['number']:>3}  expected={issue['expected']:<13}  "
        f"got={r['classification']:<13}  ({r['source']}, conf={r['confidence']})"
    )
    lines.append(f"     comment[:140] = {r['comment'][:140]!r}")
    if r.get("fix_plan"):
        fp = r["fix_plan"]
        lines.append(f"     fix_plan = current={fp.get('current_text')!r}  desired={fp.get('desired_text')!r}")

text = "\n".join(lines) + "\n"
sys.stdout.write(text)
sys.stdout.flush()
with open("_smoke_result.txt", "w") as fh:
    fh.write(text)
