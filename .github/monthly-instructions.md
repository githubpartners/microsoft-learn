# Below is a consolidated, step-by-step guide and the complete, updated code to implement an automated process that:

- Ensures a monthly “GitHub Triage: YYYY-MM” issue exists and closes last month’s issue if still open
- Posts weekly comments to the current month’s triage issue, listing and categorizing issues opened in the last 7 days, with each issue reference on its own line
- Provides a reusable composite action for triage issue creation/closing
- Offers a workflow that uses the composite action
- Follow the steps and use the files exactly as provided.

# Step-by-step implementation guide

1. Choose your branch and prepare directories
- Decide your branch (example: update-monthly-review).
- Ensure you have the following directories:
   - .github/workflows
   - .github/actions/triage-issue

2. Add the monthly triage workflow (creates current month’s triage issue and closes previous)
- This workflow runs monthly. It ensures an issue titled “GitHub Triage: YYYY-MM” exists and closes last month’s triage issue if it is still open.

3. Add the weekly triage comment workflow
- This runs weekly and posts a comment to the current month’s triage issue with:
   - Counts by category
   - A list of each new issue in the last 7 days with one line per issue (e.g., “- #223”)
   - A note that Mona (Copilot) reviewed
- It uses JavaScript via actions/github-script and the GitHub Search API (created:>=YYYY-MM-DD).

4. Add the reusable composite action
- Encapsulates logic to:
  - Optionally close last month’s triage issue
  -Create the current month’s triage issue
- This makes future reuse and refactoring easier.

5. Add a workflow that uses the composite action
- Example monthly workflow that calls the composite action instead of embedding the logic directly.
- Useful for decoupling and reusability.

6. Commit and push
- Add all files.
- Commit with a message, such as: add monthly triage + weekly review workflows
- Push to your branch.

7. Validate and optionally trigger
- Go to the GitHub repository’s Actions tab.
- Confirm workflows are present.
- Manually trigger them if desired via workflow_dispatch.
- Confirm labels and issue creation/comments work.

8. Future enhancements
- Pagination beyond 1000 items if needed.
- Slack/Teams notifications.
- GraphQL query optimization for exact-title lookups.
- NLP-based categorization improvements.
- JSON artifact uploads for reports and dashboards.
- Templating: externalize comment templates into env vars or repository files.
