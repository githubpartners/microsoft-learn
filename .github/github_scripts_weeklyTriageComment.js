// weeklyTriageComment.js
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
function getStartDate(daysBack = 7) {
  const d = new Date();
  d.setDate(d.getDate() - daysBack);
  return d.toISOString().slice(0, 10); // YYYY-MM-DD
}

async function findIssue(title) {
  for (let page = 1; page < 50; page++) {
    const resp = await octokit.request("GET /repos/{owner}/{repo}/issues", {
      owner: repoOwner,
      repo: repoName,
      state: "open",
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
  const yearMonth = getYearMonth();
  const triageTitle = `GitHub Triage: ${yearMonth}`;
  const triageIssue = await findIssue(triageTitle);
  if (!triageIssue) {
    throw new Error(
      `Current triage issue "${triageTitle}" not found. Run monthly triage workflow first.`
    );
  }

  const startDate = getStartDate(7);
  const q = `repo:${repoOwner}/${repoName} is:issue is:open created:>=${startDate}`;

  let allItems = [];
  for (let page = 1; page < 10; page++) {
    const resp = await octokit.request("GET /search/issues", {
      q,
      per_page: 100,
      page,
    });
    const items = resp.data.items || [];
    allItems = allItems.concat(items);
    if (items.length < 100) break;
  }

  // Categorization
  const reTemplate = /\[REPLACE_WITH_MODULE_TITLE\]|N\/?A/i;
  const reGrammar = /\b(grammar|spelling|typo|misspell(ed)?|proofread)\b/i;
  const reDeprecated = /\b(deprecated|outdated|codeql|dependabot|projects?|security)\b/i;
  const reSuggested =
    /\b(update|improvement|improve|copilot|prompt|exercise|action|module|enterprise)\b/i;
  const reOther =
    /\b(broken|support|help|unable|issue|not issued|confused|experience|certificate)\b/i;

  function categorize(title) {
    if (reTemplate.test(title)) return "template";
    if (reGrammar.test(title)) return "grammar";
    if (reDeprecated.test(title)) return "deprecated";
    if (!reTemplate.test(title) && reSuggested.test(title)) return "suggested";
    if (reOther.test(title)) return "other";
    if (/update|request/i.test(title) && !reTemplate.test(title)) return "suggested";
    return "other";
  }

  const buckets = { grammar: [], deprecated: [], suggested: [], other: [], template: [] };
  for (const i of allItems) buckets[categorize(i.title)].push(i);

  const rep = (arr) => (arr.length ? `#${arr[0].number}` : "");
  const todayStr = new Date().toISOString().slice(0, 10);
  const allIssueLines = allItems.map((i) => `- #${i.number}`).join("\n");

  let md = `**${yearMonth} Weekly Triage Update (Issues opened since ${startDate})**\n`;
  md += `- Checked as of: ${todayStr} (UTC)\n\n`;
  md += `**Counts (last 7 days):**\n`;
  md += `- Grammar/Spelling: ${buckets.grammar.length} ${rep(buckets.grammar)}\n`;
  md += `- Deprecated/Outdated: ${buckets.deprecated.length} ${rep(buckets.deprecated)}\n`;
  md += `- Suggested Content Updates: ${buckets.suggested.length} ${rep(buckets.suggested)}\n`;
  md += `- Other: ${buckets.other.length} ${rep(buckets.other)}\n`;
  md += `- Template-Incomplete: ${buckets.template.length} ${rep(buckets.template)}\n\n`;
  md += `_Total new issues: ${allItems.length}_\n\n`;
  md += `**Issue References (Last 7 Days):**\n${allIssueLines}\n\n`;
  md += `:octocat: :copilot: Mona (Copilot) has reviewed these new issues.\n`;
  md += `<!-- Search query: repo:${repoOwner}/${repoName} is:issue is:open created:>=${startDate} -->\n`;

  await octokit.request(
    "POST /repos/{owner}/{repo}/issues/{issue_number}/comments",
    {
      owner: repoOwner,
      repo: repoName,
      issue_number: triageIssue.number,
      body: md,
    }
  );

  console.log(`Posted weekly triage update to #${triageIssue.number}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});