# **Unit 2: Define Value Before Automation**

Before a team sends its first Copilot request, it needs a starting point for comparison. In this unit, you'll learn how to set a baseline and define your targets before a trial starts, so you can show whether AI really saves your team time on a deliverable.
For example, a reporting trial could include requests to update a summary so it matches approved figures.

## Set up the trial

Before the trial, follow these steps:

1. **Measure today's work.** Record how the team does the work now. This is your **baseline**: the starting point for comparison.

1. **Set a target outcome.** Write down the improvement you want.

1. **Define acceptance criteria.** List the requirements each output must meet. Example: every figure matches the approved figures file, and no claim goes beyond the figures.

1. **Put the criteria in one checklist.** Name the reviewer, and write the criteria as a checklist in the workflow's **GitHub issue**, so every reviewer uses the same list before and after the trial. To set it up, create an issue and add a task list to its description.

1. **Record the plan and its boundary.** **The trial plan** is a shared spreadsheet the reviewer can open. In it, record the amount of work (for example, ten requests), the time period, who accepts the result, and the evidence sources. In this example, the team member who owns the report accepts each summary. Also state your measurement boundary: which work, time, and costs you'll count. When you set the boundary now, nobody can change which costs count after the results arrive.

Count requests and attempts separately. A request is one piece of work. An **attempt** is one try at doing it. Example: retrying one summary is one request and two attempts. Counting attempts as requests inflates throughput and hides retries.

## Choose consistent measures

- **Cycle time:** the time from when a request is ready for work until a person accepts it, including waiting time.

- **Human effort:** the total minutes people spend on setup, monitoring, review, and corrections.

- **Throughput:** the number of accepted outcomes in a stated period.

- **Error rate:** outputs with at least one verified defect, such as a wrong figure, divided by all outputs inspected.

- **Rework rate:** requests that needed correction, divided by all requests attempted.

- **Exception rate:** requests with an **exception**, a situation outside the agreed plan such as a request for broader access, divided by all requests attempted.

- **Cost:** the combined value of people's time and resources inside the measurement boundary you chose and documented.

Setup time may cover several requests. Decide how to count it. For example, divide 30 setup minutes across ten requests: three minutes each. Compare similar tasks over the same length of time.

Keep each measure the same as before and during the trial: the same definition, the same checklist, the same time period, and the same reviewers where you can. If a definition changes partway through, record the date in the trial spreadsheet and do not compare results across that date. Count throughput in one fixed period, for example accepted summaries in five business days, so a longer trial doesn't look more productive than a shorter baseline.

## Ask these questions before you start a trial

Before you measure anything, answer these questions with the people who own the work. Each question comes with an example answer for the team's summary requests.

- **Which costs will I count, and who gives me the numbers?** Example: 
    - People's time, including review and corrections
    - AI credits, and GitHub Actions minutes, plus the AI credits and GitHub Actions minutes supplied by the **billing manager**. The billing manager is the GitHub role that handles Copilot billing for your organization.

- **Where will the evidence come from?** You can't measure a claim that has no evidence. Example: the summary version, the figures file version, the agent's **session** (its record of one stretch of work on a task), the run records, and the reviewer's record of the figure checks.

## Baseline and targets

This baseline covers ten similar summary requests over five business days. The 300 minutes of human effort include 30 minutes of rework. The team records its baseline and targets before the trial:

| **Measure** | **Baseline (today)** | **Target (trial)** |
| --- | --- | --- |
| Accepted summaries | 10 of 10 accepted | At least 9 of 10 accepted |
| Median cycle time, accepted requests | 60 min | 45 min or less |
| Total human effort | 300 min (30 min of rework) | 200 min or less |
| Unsupported claims or disallowed data | None in the ten accepted outputs | None in any accepted output |
| Cost inside the measurement boundary | $150 (people's time) | \$120 or less (the approved budget) |

Report any unsupported claim or disallowed data as its own finding, so an average doesn't hide it.