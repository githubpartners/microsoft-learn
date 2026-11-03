
# **Unit 4: Measure Operational Quality**

A batch of agent requests can include outputs that are incomplete or need corrections, so a team needs consistent quality measures. With this unit, you can turn ten requests into rates that anyone on the team can check, so quality becomes a number instead of an impression.

Assess each output on four dimensions:

- **Accuracy:** every figure and claim matches approved evidence.

- **Relevance:** the output addresses the specific request.

- **Completeness:** every required part is there.

- **Boundaries:** the workflow stays within permitted data and actions.

Agree on how to count people's time. Track two kinds of review time. **Planned review** is the normal check against the checklist. **Additional review** is any extra correction or review after a problem.

Count each person's minutes only once in total human effort. Separating the two kinds shows whether the workflow saves time overall or only moves it into corrections. Use the same checklist and counting rules throughout, and record any uncertainty or disagreement.

## Combine quality and security signals

For code tasks, record Copilot code review comments and GitHub Code Quality findings, noting the pull request or commit, finding or comment, and its status; for code-scanning security alerts, record open alert counts by severity at the same scope before and after the trial. Map each recorded item to the checklist dimension it actually tests—typically **Accuracy** or **Completeness** for code-quality issues, and **Boundaries** for security issues. These signals do not establish **Relevance** unless an item explicitly identifies an out-of-scope result, and they do not validate non-code facts such as financial figures. Product navigation labels may change; see the [Copilot code review](https://docs.github.com/copilot/code-review), [GitHub Code Quality](https://docs.github.com/code-security/code-quality), and [code scanning alerts](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts) documentation. A person still decides acceptance against the complete checklist.

## Classify each request

At the reporting cutoff, assign each request to exactly one bucket. Use **Unresolved** for requests that are still open; classify closed requests by their final output and acceptance decision.

- **Accepted:** a person accepts the output.

- **Partial:** the output exists but doesn't meet every requirement and hasn't been accepted.

- **Failed:** the request produced no usable output.

- **Unresolved:** the request is still open. Track it separately.

For the recovery rate, divide the exceptions the team resolved by all exceptions. For example, two recovered exceptions out of three is a 66.7% recovery rate.

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

- A person accepted 7 on the first attempt.

- 2 had a verified defect in the first output, such as a wrong figure. The team corrected them, and a person then accepted them.

- 1 asked for a comparison with a draft nobody attached. It ended with an incomplete output and was classified as Partial, with no verified defect.

The three requests that weren't accepted on the first attempt used the other five attempts. Each one had an exception, needed rewording, and needed an additional review. A person reviewed all ten first outputs. The rates use the ten requests, not the twelve attempts.

The final buckets are 9 Accepted, 1 Partial, 0 Failed, and 0 Unresolved. The other measures overlap these buckets; they aren't additional classifications. The mappings below describe this trial, not fixed rules for future trials.

| **Measure** | Count | **Rate** | **Classification mapping in this trial** |
| --- | --- | --- | --- |
| Accepted requests | 9 of 10 requests | 90% | All 9 requests classified as Accepted, including 2 accepted after correction. |
| First-pass acceptance | 7 of 10 requests | 70% | 7 of the 9 Accepted requests were accepted on the first attempt. |
| Partial requests | 1 of 10 requests | 10% | The 1 request classified as Partial; its output wasn't accepted. |
| Requests needing rework | 3 of 10 requests | 30% | 2 requests classified as Accepted and 1 as Partial. |
| Requests with exceptions | 3 of 10 requests | 30% | 2 requests classified as Accepted and 1 as Partial. |
| Recovered exceptions | 2 of 3 exceptions | 66.7% | The resolved exceptions on 2 Accepted requests, out of all 3 exceptions; the exception on the Partial request wasn't resolved. |
| Additional review (Human in the loop) | 3 of 10 requests | 30% | 2 requests classified as Accepted and 1 as Partial. |
| First outputs with verified defects | 2 of 10 outputs | 20% | The first outputs of 2 requests later classified as Accepted after correction. |

Read related measures in pairs, and treat what they suggest as a question to check, not a conclusion. Steady acceptance with a rising rework rate suggests quality slipped. Before you conclude that, check three things: the types of errors behind the rework, how hard the tasks were compared with the last period, and how many requests the team sent. A harder mix of tasks can raise rework without any change in the workflow, and a busier week can raise accepted requests without any change in quality.