# Unit 8: Knowledge Check

Select the best response for each question before you read the answers. The questions use fictional examples of report reviews.

## Main questions

### 1. Human control points

The agent opened a pull request that updates a summary, and the reviewer approved it. Who decides whether the summary is ready for leadership?

- **A. The reviewer, because the approval completes the review.**

- **B. The report owner named in the issue, after checking the result against the acceptance criteria.**

- **C. Copilot, because its pull request description says every figure matches.**

### 2. Approve, reject, revise

The agent's pull request keeps the sentence "The team expects all four regions to grow next quarter." The figures file has no data for that quarter, and the issue doesn't say whether the outlook stays. What's your first response?

- **A. Request a revision that deletes the sentence, because the figures don't support it.**

- **B. Approve, because the sentence was in the summary before the agent started.**

- **C. Ask the report owner whether the outlook stays, and how to label it, before you approve or request a revision.**

### 3. Steer a running workflow

During an approved report update, the agent proposes an unfamiliar tool. You check that it would upload the approved figures to an external service, outside the agreed scope. The upload is awaiting authorization, and no information has been sent. What do you do?

- A. Withhold authorization, steer the agent back to the approved source, and escalate the broader access request. Stop if continuing could expose information or cause harm.

- B. Authorize the tool because the report update is already approved.

- C. Stop every session that proposes an unfamiliar tool, regardless of what the tool does or whether it is in scope.

### 4. Recover from failure

The agent's pull request description says "All figures now match the source." You find that it still calls North the region with the highest margin, although East's is higher (17.3% against 16.8%). What's the best next step?

- **A. Ask the agent to double-check its work, and approve if it confirms.**

- **B. Post a correction that names the requirement, what you found, the change, and how to check it, and then read the whole summary again.**

- **C. Edit the sentence yourself and approve the pull request.**

### 5. Stop and contain

You stopped a session after the agent pushed a commit that changed data/13-figures.csv. What's true now?

- **A. Stopping the session undid the commit.**

- **B. The pull request closed, so you have nothing more to do.**

- **C. The commit is still there and needs review, and other runs the agent started need their own check.**

### 6. Validate output

Copilot code review found no issues, and every figure in the summary matches the figures file. What else must a person check before accepting?

- **A. That the comparisons and growth statements are right, nothing outside the agreed file changed, and the summary works for leadership.**

- **B. Nothing, because the review and the figures agree.**

- **C. That the agent's description of its own work sounds confident and complete.**

## Additional checks

### 7. Check a business deliverable

The agent listed five figures that changed between draft 1 and the current summary. You checked three, and they match. What do you do before the list goes to the meeting organizer?

- **A. Send the list, because every figure you checked matches.**

- **B. Check the other two, and compare both drafts yourself for changes the list missed.**

- **C. Ask Copilot to confirm that its list is complete.**

## Answers and explanations

**B.** Review and acceptance are separate gates. The reviewer's approval lets the change merge, and the named owner accepts the result using evidence. Review Name the human owner.

**C.** The requirement doesn't say what happens to the outlook, so clarify before you judge the agent's work. Deleting it could remove content the owner wants. Review Choose the response that resolves the problem.

**A.** Approval of the report update doesn't authorize an out-of-scope upload. Because the action is waiting and no information has been sent, withhold authorization and steer back within scope while the owner considers the access request. Stop and escalate if continuing could cause harm. An unfamiliar tool alone isn't a stop trigger. Review Check unexpected tool use.

**B.** The agent's confirmation isn't evidence, and editing it yourself makes you a collaborator, so your approval no longer counts as independent. A specific correction fixes the cause, and a full reread catches other wrong statements. Review Work through a failed requirement.

**C.** Stopping keeps pushed commits and doesn't prove that separate processes stopped. Review Stop a Copilot session on GitHub.

**A.** Matching numbers and a clean automated review don't cover comparisons, scope, or business fit. A person checks those. Review Connect each requirement to evidence.

**B.** A list that reads well can still leave out a change, and Copilot's confirmation isn't evidence. Check each figure against its source, and check for omissions. Review Tell supported output from plausible output.
