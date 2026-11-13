
# **Unit 4: Measure Operational Quality**

A batch of agent requests can include outputs that are incomplete or need corrections, so a team needs consistent quality measures. With this unit, you can turn ten requests into rates that anyone on the team can check, so quality becomes a number instead of an impression.

Assess each output on four dimensions:

- **Accuracy:** every figure and claim matches approved evidence.

- **Relevance:** the output addresses the specific request.

- **Completeness:** every required part is there.

- **Boundaries:** the workflow stays within permitted data and actions.

Agree on how to count people's time. Track two kinds of review time. **Planned review** is the normal check against the checklist. **Additional review** is any extra correction or review after a problem. Both are human-in-the-loop work, because a person checks the output and decides what happens next. The share of requests that need additional review shows how often people had to step in beyond the planned check.

Assign each person's review or correction minutes to one bucket, not both. A person can contribute different minutes to both buckets.

**Total review and correction time = planned review minutes + additional review minutes**, summed across everyone involved. Count each person's time even if they work simultaneously.

For example, two reviewers each spend 10 minutes on planned review, and one spends another 5 minutes on corrections. Record 20 planned + 5 additional = 25 human minutes, even if the planned reviews happen at the same time.

Add any other human time included in the measurement boundary, such as setup time or time spent deciding how to handle an exception, to get **total human effort**. Separating the two review buckets shows whether the workflow saves time overall or only moves it into corrections. Use the same checklist and counting rules throughout, and record any uncertainty or disagreement.

## Combine quality signals

For code tasks, record Copilot code review comments and GitHub Code Quality findings, noting the pull request or commit, finding or comment, and its status. Map each recorded item to the checklist dimension it actually tests, typically **Accuracy** or **Completeness** for code-quality issues. These signals do not establish **Relevance** unless an item explicitly identifies an out-of-scope result, and they do not validate non-code facts such as financial figures. Product navigation labels may change; see the [Copilot code review](https://docs.github.com/en/copilot/code-review) and [GitHub Code Quality](https://docs.github.com/en/code-security/code-quality) documentation. A person still decides acceptance against the complete checklist.

## Classify each request

At the reporting cutoff, assign each request to exactly one bucket. Use **Unresolved** for requests that are still open; classify closed requests by their final output and acceptance decision.

- **Accepted:** a person accepts the output.

- **Partial:** the output exists but doesn't meet every requirement and hasn't been accepted.

- **Failed:** the request produced no usable output.

- **Unresolved:** the request is still open. Track it separately.

A run can succeed while its output fails the requirements.

## Apply the quality check to a draft comparison

Suppose an agent lists what changed between two report drafts, as a comment on the issue. The list reads well, and the run succeeded. But it leaves out that West's statement changed from "declined slightly" to "grew 2.5%," and it says "all figures checked" without showing which ones.

The business reviewer checks four things:

- **Accurate figures:** compare each listed old and new value with the two files. If a value is wrong, request a correction instead of fixing it silently.

- **Complete list:** compare both drafts yourself for changes the list missed. If something is missing, keep the list partial and unaccepted.

- **Permitted data and actions:** check that the agent only commented and changed no file, as the issue's limits say. Escalate disallowed data or actions, and withhold acceptance.

- **Claimed checks:** look for the record behind "all figures checked": which figures, against which version. If it's missing, mark the claim unverified and request the evidence.

Request one specific correction: add the West statement change, and name the file and line for each listed figure. Keep the request's agreed limits, and record the instruction version.

The missing West change matters more than its size suggests. The current summary says West grew, and the figures show it declined, so a reader who trusts the list never learns that this statement changed at all.

## Read the trial results

Suppose the trial had ten requests and twelve attempts over five business days. Here's what happened to the ten requests:

- A person accepted 7 on the first attempt. During one of them, the agent asked for access to a spreadsheet outside the agreed sources. The report owner declined, the agent finished with the approved sources, and the output passed the planned review without corrections.

- 2 had a verified defect in the first output, such as a wrong figure. The team corrected them, and a person then accepted them.

- 1 asked for a comparison with a draft nobody attached. The agent asked for the missing draft, but nobody supplied it before the cutoff. The request ended with an incomplete output and was classified as Partial, with no verified defect.

The three requests that weren't accepted on the first attempt used the other five attempts. Each one needed rework and an additional review. Only two requests had an exception: the access request and the missing draft. The wrong figures needed rework but weren't exceptions, because the work didn't need a person's decision to continue, and the reviewer caught the errors at the planned review. A person reviewed all ten first outputs. Request-based rates use the ten requests, not the twelve attempts; the recovery rate uses the two exceptions.

The final buckets are 9 Accepted, 1 Partial, 0 Failed, and 0 Unresolved. The other measures overlap these buckets. They aren't additional classifications. The mappings below describe this trial, not fixed rules for future trials.

| **Measure** | Count | **Rate** | **Classification mapping in this trial** |
| --- | --- | --- | --- |
| Accepted requests | 9 of 10 requests | 90% | All 9 requests classified as Accepted, including 2 accepted after correction. |
| First-pass acceptance | 7 of 10 requests | 70% | 7 of the 9 Accepted requests were accepted on the first attempt. |
| Partial requests | 1 of 10 requests | 10% | The 1 request classified as Partial; its output wasn't accepted. |
| Requests needing rework | 3 of 10 requests | 30% | 2 requests classified as Accepted after correction and 1 as Partial. |
| Requests with exceptions | 2 of 10 requests | 20% | 1 request accepted on the first attempt without rework (the declined access request) and 1 as Partial (the missing draft). The 2 corrected requests had defects, not exceptions. |
| Resolved exceptions (recovery rate) | 1 of 2 exceptions | 50% | The access request's exception was resolved, because the work continued within the agreed limits. The missing draft never arrived, so the Partial request's exception stays unresolved, even though the request is closed. |
| Requests needing additional review | 3 of 10 requests | 30% | The same 3 requests as rework, because every correction needs another review. The access request needed only a decision and the planned review. |
| Requests where the first output had a verified defect | 2 of 10 requests | 20% | 2 requests classified as Accepted after correction; the Partial request had no verified defect. |

Read related measures in pairs, and treat what they suggest as a question to check, not a conclusion. Steady acceptance with a rising rework rate suggests quality slipped. Before you conclude that, check three things: the types of errors behind the rework, how hard the tasks were compared with the last period, and how many requests the team sent. A harder mix of tasks can raise rework without any change in the workflow, and a busier week can raise accepted requests without any change in quality.