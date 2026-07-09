import os
import sys
import json
import subprocess
import re
from issue_analyzer import intelligent_classify, generate_context_aware_comment

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def ensure_label(label_name):
    # create label safely if it doesn't exist
    run(f'gh label create "{label_name}" --repo "$GITHUB_REPOSITORY" || true')


def add_label(issue_number, label_name):
    ensure_label(label_name)
    gh(f'issue edit {issue_number} --add-label "{label_name}"')

def run(cmd):
    """Run shell commands safely"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR:", result.stderr)
    return result.stdout.strip()


def gh(cmd):
    """GitHub CLI wrapper with auth"""
    return run(f'gh {cmd} --repo "$GITHUB_REPOSITORY"')


def extract_urls(text):
    return re.findall(r'https?://\S+', text)


def extract_module_mentions(text):
    """
    Detect MS Learn module references (basic heuristic)
    """
    patterns = [
        r"module",
        r"learn.microsoft.com",
        r"knowledge check",
        r"check your knowledge",
        r"github copilot"
    ]

    return any(p.lower() in text.lower() for p in patterns)


def classify(issue):
    """Use intelligent AI-powered analysis for classification"""
    category, confidence, analysis = intelligent_classify(issue)
    issue['_analysis'] = analysis
    issue['_confidence'] = confidence
    return category




def comment(issue_number, message):
    gh(f'issue comment {issue_number} --body "{message}"')


def close(issue_number):
    gh(f'issue close {issue_number}')


def process(issue):
    issue_number = issue["number"]
    result = classify(issue)
    analysis = issue.get("_analysis", {})

    print(f"Issue #{issue_number} classified as: {result}")
    print(f"Specificity Score: {analysis.get('specificity_score', 0)}/100")

    # ALWAYS ensure label exists first
    add_label(issue_number, "triaged")

    if result == "auto_fix":
        comment_text = generate_context_aware_comment(analysis, result)
        comment(issue_number, comment_text)
        add_label(issue_number, "auto-fix")

    elif result == "needs_human":
        comment_text = generate_context_aware_comment(analysis, result)
        comment(issue_number, comment_text)
        add_label(issue_number, "needs-review")

    elif result == "needs_context":
        comment_text = generate_context_aware_comment(analysis, result)
        comment(issue_number, comment_text)
        add_label(issue_number, "needs-context")

    elif result == "spam":
        comment(issue_number,
            "🗑️ **Closed:** Insufficient actionable content to triage.")
        add_label(issue_number, "spam")
        close(issue_number)

def main():
    if len(sys.argv) < 2:
        print("Usage: triage.py '<issue_json>' or triage.py '<issue_number>'")
        sys.exit(1)

    raw = sys.argv[1]

    # Try to parse as JSON first
    try:
        issue = json.loads(raw)
    except json.JSONDecodeError:
        # If not valid JSON, try to treat as issue number and fetch it
        try:
            issue_number = int(raw)
            print(f"📝 Fetching issue #{issue_number} from GitHub...")
            issue_json = run(f'gh issue view {issue_number} --json number,title,body,labels --repo "$GITHUB_REPOSITORY"')
            issue = json.loads(issue_json)
        except (ValueError, json.JSONDecodeError):
            print(f"❌ Invalid input: '{raw}' is neither valid JSON nor a valid issue number")
            sys.exit(1)

    process(issue)


if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("Missing GITHUB_TOKEN")
        sys.exit(1)

    main()
