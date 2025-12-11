// ensureMonthlyTriage.js
const { Octokit } = require("@octokit/core");

const githubToken = process.env.GITHUB_TOKEN;
const repoOwner = process.env.REPO_OWNER;
const repoName = process.env.REPO_NAME;

if (!githubToken || !repoOwner || !repoName) {
  console.error("Missing required env: GITHUB_TOKEN, REPO_OWNER, REPO_NAME");
  process.exit(1);
}

const octokit = new Octokit({ auth: githubToken });

function getYearMonth(offset = 0) {
  const d = new Date();
  d.setMonth(d.getMonth() + offset);
  return d.toISOString().slice(0, 7); // YYYY-MM
}

async function findIssueByExactTitle(title) {
  for (let page = 1; page < 50; page++) {
    const resp = await octokit.request("GET /repos/{owner}/{repo}/issues", {
      owner: repoOwner,
      repo: repoName,
      state: "all",
      per_page: 100,
      page,
    });
    if (!resp.data.length) break;
    const hit = resp.data.find((i) => i.title === title);
    if (hit) return hit;
    if (resp.data.length < 100) break;
  }
  return null;
}

async function main() {
  const currentYM = getYearMonth(0);
  const previousYM = getYearMonth(-1);
  const currentTitle = `GitHub Triage: ${currentYM}`;
  const previousTitle = `GitHub Triage: ${previousYM}`;

  // Close previous month issue if open
  const prevIssue = await findIssueByExactTitle(previousTitle);
  if (prevIssue && prevIssue.state === "open") {
    await octokit.request(
      "PATCH /repos/{owner}/{repo}/issues/{issue_number}",
      {
        owner: repoOwner,
        repo: repoName,
        issue_number: prevIssue.number,
        state: "closed",
      }
    );
    console.log(`Closed previous triage issue #${prevIssue.number}`);
  } else {
    console.log(`No open previous triage issue (title: ${previousTitle})`);
  }

  // Ensure current month issue exists
  const currIssue = await findIssueByExactTitle(currentTitle);
  if (currIssue) {
    console.log(`Current triage issue already exists: #${currIssue.number}`);
    return;
  }

  const body = `
### Monthly GitHub Triage – ${currentYM}

Automatically generated tracking issue for ${currentYM}.

#### Purpose
- Collect newly opened issues for classification.
- Track placeholders (titles containing \`[REPLACE_WITH_MODULE_TITLE]\`).
- Identify consolidation / closure candidates.

#### Actions
- Apply governance labels.
- Escalate support or experience issues.
- Prepare weekly summaries (see companion workflow).

:octocat: :copilot: Created automatically.
  `.trim();

  const created = await octokit.request("POST /repos/{owner}/{repo}/issues", {
    owner: repoOwner,
    repo: repoName,
    title: currentTitle,
    body,
    labels: ["triage"],
  });
  console.log(`Created new triage issue #${created.data.number}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});