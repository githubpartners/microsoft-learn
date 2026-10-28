# **Unit 7: Knowledge Check**

Choose one answer per question before you read the feedback. Every question uses the team's trial.

## Main questions

### 1. Define Value Before Automation

The team wants to start the Copilot trial on Monday. Which step must happen before the first request goes to the agent?

- A. Pick the most capable model, so the first results look strong.

- B. Record the baseline for ten similar summary requests and write the acceptance checklist in the workflow's issue.

- C. Run the trial for a week, and then set targets that fit the results.

### 2. Inspect Run Evidence

The agent's run shows **Success**, and its description says "all figures checked against data/13-figures.csv." No record shows which figures it checked. What do you do?

- A. Accept the summary, because the run succeeded and the description names the right file.

- B. Reject the summary, because missing evidence means the figures are wrong.

- C. Mark the claim unverified, and check the figures yourself against the version of the file you're reviewing.

### 3. Measure Operational Quality

Ten summary requests took twelve attempts. A person accepted nine of the requests. What's the acceptance rate?

- A. 90%

- B. 75%

- C. 9 of 12 attempts, so 75% for the trial

### 4. Connect Cost to Value

The trial's batch cost $97, including two retries and one request nobody accepted. A person accepted nine requests. What's the fair cost per accepted outcome?

- A. $97 divided by 12 attempts, about $8.08.

- B. $97 divided by 9 accepted requests, about $10.78.

- C. $97 minus the cost of the unaccepted request, divided by 9.

### 5. Improve Systematically

Three summaries in a trial kept an outlook sentence that the figures don't support. What change addresses the cause?

- A. Add a rule to the instructions file to source every claim or mark it as unsupported, and then test similar requests with the same checklist.

- B. Switch to a larger model and change the instructions at the same time, to fix it faster.

- C. Correct each of the three summaries by hand and keep the workflow as it is.

## Additional checks

### 6. Report a business result

Nine of ten summaries match their sources. One has a figure that doesn't match its source row. How do you report the result?

- A. Report 100% accuracy, because the wrong figure is small.

- B. Leave that summary out as an outlier.

- C. Report the unsupported figure as its own finding, and count that summary as partial.

### 7. Decide what to do next

The trial reduced human effort, measured cost, and median time to acceptance, but accepted 9 of 10 summaries compared with 10 of 10 at baseline. What should the team do next, and which evidence supports that decision?

- A. Expand immediately, because lower cost and faster delivery prove ROI and preserved quality.

- B. Revise or continue the limited trial while investigating the unaccepted request, checking final-output quality, and confirming the agreed limits.

- C. Stop permanently, because one unaccepted request proves the workflow has no value.

## Answers and explanations

1. **B.** Without a baseline and criteria set in advance, any result looks good. Targets set after the trial tend to match the results. Review <u>Questions to ask before you start a trial</u>.

1. **C.** A successful run shows that the run ended, not that the figures are right. Missing evidence makes the claim unverified, not false.

1. **A.** Acceptance rate divides accepted requests by all requests: 9 / 10 = 90%. Dividing by attempts mixes two groups. Review <u>Choose consistent measures</u>.

1. **B.** Retries and unaccepted work still cost money, so they stay in the batch, and you divide by the outcomes a person accepted. Review <u>Include the whole cost boundary</u>.

1. **A.** The same problem recurs with one cause, so one change to the instructions addresses it. Changing two things at once hides which one helped, and fixing by hand leaves the cause in place. Review <u>Match the change to the cause</u>.

1. **C.** One unsupported figure makes the output partial, however well the rest reads. Report it separately so an average doesn't hide it. Review <u>Apply the quality check to a draft comparison</u>.

1. **B.** The measured improvements are promising, but the unaccepted request remains unresolved. Investigate it, inspect final-output quality and boundary evidence, and then decide whether to expand, revise, or stop. The current evidence doesn’t prove ROI or preserved quality.
