
# **Unit 4: Measure Operational Quality**

A batch of agent requests can include outputs that are incomplete or need corrections, so a team needs consistent quality measures. With this unit, you can turn ten requests into rates that anyone on the team can check, so quality becomes a number instead of an impression.

Assess each output on four dimensions:

- **Accuracy:** every figure and claim matches approved evidence.

- **Relevance:** the output addresses the specific request.

- **Completeness:** every required part is there.

- **Boundaries:** the workflow stays within permitted data and actions.

Check the version of the output you're reviewing. If a required part is missing, keep the output partial and unaccepted, even if the run succeeded.

Agree on how to count people's time. Track two kinds of review time. **Planned review** is the normal check against the checklist.

**Additional intervention** is any extra correction or review after a problem.

Count each person's minutes only once in total human effort. Separating the two kinds shows whether the workflow saves time overall or only moves it into corrections. Use the same checklist and counting rules throughout, and record any uncertainty or disagreement.

## Combine quality and security signals

Copilot code review and, on GitHub Team and GitHub Enterprise Cloud, GitHub Code Quality can provide useful evidence for the checks they actually run. When the repository also holds code, open security alerts provide another signal: the technical reviewer records the count by severity under **Security and quality > Findings**, before and after the trial. These checks can identify code-quality or security issues, but they don’t validate financial figures or determine whether a summary is suitable for leadership. A person still decides acceptance against the complete checklist.

## Classify each request

- **Successful:** a person accepts the output.

- **Partial:** the output exists but doesn't meet every requirement.

- **Failed:** the request produced no usable output.

- **Unresolved:** the request is still open. Track it separately.

For the request failure rate, divide failed requests by all requests attempted. For the execution failure rate, divide failed attempts, the tries that produced no usable output, by all attempts. For example, two failed requests out of ten is a 20% request failure rate.

A run can succeed while its output fails the requirements.

## Apply the quality check to a draft comparison

In this fictional request, an agent lists what changed between two report drafts, as a comment on the issue. The list reads well, and the run succeeded. But it leaves out that West's statement changed from "declined slightly" to "grew 2.5%," and it says "all figures checked" without showing which ones.

The business reviewer checks four things:

- **Accurate figures:** compare each listed old and new value with the two files. If a value is wrong, request a correction instead of fixing it silently.

- **Complete list:** compare both drafts yourself for changes the list missed. If something is missing, keep the list partial and unaccepted.

- **Permitted data and actions:** check that the agent only commented and changed no file, as the issue's limits say. Escalate disallowed data or actions, and withhold acceptance.

- **Claimed checks:** look for the record behind "all figures checked": which figures, against which version. If it's missing, mark the claim unverified and request the evidence.

Request one specific correction: add the West statement change, and name the file and line for each listed figure. Keep the request's agreed limits, and record the instruction version. Then test new, similar requests the same way as before.

The missing West change matters more than its size suggests. The current summary says West grew, and the figures show it declined, so a reader who trusts the list never learns that this statement changed at all.

## Read the fictional trial results

The fictional trial had ten requests and twelve attempts over five business days. Here's what happened to the ten requests:

- A person accepted 7 on the first attempt.

- 2 had a verified defect in the first output, such as a wrong figure. The team corrected them, and a person then accepted them.

- 1 asked for a comparison with a draft nobody attached. It lacked enough context and stayed unaccepted, with no verified defect.

The three requests that weren't accepted on the first attempt used the other five attempts. Each one had an exception, needed rework, and needed extra help from a person.

A person reviewed all ten first outputs. Count each request only once when you measure accepted outcomes, because a retry isn't another completed request.

| **Measure** | Count | **Rate** |
| --- | --- | --- |
| Accepted requests | 9 of 10 requests | 90% |
| First-pass acceptance | 7 of 10 requests | 70% |
| Partial, unaccepted requests | 1 of 10 requests | 10% |
| Requests needing rework | 3 of 10 requests | 30% |
| Requests with exceptions | 3 of 10 requests | 30% |
| Recovered exceptions | 2 of 3 exceptions | 66.7% |
| Normal human review | 10 of 10 requests | 100% |
| Extra human intervention | 3 of 10 requests | 30% |
| First outputs with verified defects | 2 of 10 outputs | 20% |

Read two measures together, and treat what they suggest as a question to check, not a conclusion. More accepted requests with a steady rework rate suggests the workflow handled more work at the same quality. Steady acceptance with a rising rework rate suggests quality slipped. Before you conclude either, check three things: the types of errors behind the rework, how hard the tasks were compared with the last period, and how many requests the team sent. A harder mix of tasks can raise rework without any change in the workflow, and a busier week can raise accepted requests without any change in quality.