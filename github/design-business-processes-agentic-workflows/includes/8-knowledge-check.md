
## **Unit 8 — Knowledge check**

### **Question 1**

A team receives many requests, but members disagree about what makes one urgent. What should happen before automating priority decisions?

- Correct: Keep priority decisions human-led while agreeing on criteria and exception ownership.

- Incorrect: Use a more capable model to infer a policy from previous discussions.

- Incorrect: Treat the requester's use of "urgent" as the final priority.

- Incorrect: Automate priority decisions first and resolve disagreements during the pilot.

Explanation: Repeated work isn't ready for delegated priority decisions until the criteria and authority are clear. A model can summarize previous discussions, but it can't establish an agreed priority policy on the team's behalf.

### **Question 2**

A report must cover activity from the past seven days. The agent groups issue descriptions into recurring themes. Which statement correctly describes the process?

- Incorrect: The themes are the inputs, and the reporting period is the output.

- Incorrect: The schedule defines which issues count, so a separate selection rule isn't needed.

- Correct: Issue records are inputs, grouping is a transformation, and the date range constrains selection.

- Incorrect: The agent should infer the reporting period from the issue descriptions.

Explanation: Inputs are the records being processed, transformations change their form, and selection rules define coverage. A schedule determines when the workflow runs, not which period or records the report covers.

### **Question 3**

A workflow may propose documentation edits, but an authorized reviewer must accept them before merging. Which design best supports this requirement?

- Incorrect: Give the agent merge access and tell it to wait until it believes the changes are acceptable.

- Correct: Have it propose a pull request and configure the applicable review controls before merging.

- Incorrect: Merge the changes automatically and ask for approval afterward.

- Incorrect: Treat the creation of a pull request as evidence that a reviewer approved the changes.

Explanation: The agent prepares a proposal while the controlled action remains subject to enforced review. Agent confidence doesn't replace human authorization, and a prompt alone isn't an approval gate.

### **Question 4**

A team wants to find requests that lack an intake response after an agreed period, without sending the same alert on every run. Which pattern fits best?

- Incorrect: Reporting, because a weekly narrative alone prevents repeated alerts.

- Incorrect: Classification, because applying a category resolves the unanswered request.

- Incorrect: Review, using a publishing checklist to assess each request.

- Correct: Monitoring, with a defined condition, clearing rule, and repeat-alert handling.

Explanation: Monitoring detects a defined condition. Avoiding repeated alerts also requires explicit state or another supported suppression mechanism.

### **Question 5**

A mandatory issue source can't be retrieved during report generation. What should the specification require?

- Correct: Record the failure, notify the owner, and don't claim complete coverage.

- Incorrect: Treat the missing source as having no activity so the schedule is maintained.

- Incorrect: Publish a full report based on earlier themes without identifying the gap.

- Incorrect: Retry indefinitely until the source becomes available.

Explanation: Failed access isn't evidence of no activity. Failure handling must preserve that distinction and provide an actionable notification. Retries need limits and a failure path.

### **Question 6**

A report update is technically successful, but the resulting report no longer includes required limitations. What is the best response?

- Incorrect: Accept the change because the Actions run succeeded.

- Correct: Treat it as a regression, review the change, and restore or correct the accepted behavior.

- Incorrect: Change the acceptance criteria to match the new output.

- Incorrect: Switch models immediately without reviewing the update.

Explanation: Regression checks protect previously accepted requirements after a change. Execution success doesn't prove that the output meets its business requirements. First inspect the changed configuration and evidence.


