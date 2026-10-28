# Unit 7: Knowledge check

Check what you learned, then compare your answers with the explanations. Choose one answer for each question. The questions use fictional business tasks.

## Main questions

### 1. Understand what drives Copilot costs

After a long chat about a report, with the figures file and two drafts attached, the report owner types "Check it again." Why might this short request use many tokens?

•  A. GitHub bills short prompts at a higher rate per token.

•  B. The input includes the earlier conversation, the attached files, and any tool results, not only the new message.

•  C. Every message costs a fixed minimum number of credits.

### 2. Read and manage usage

This fictional report compares two weeks of the same length, in AI credits:

•  Issue summaries: 80 in the prior week, 90 in the current week.

•  Draft comparisons: 120, then 130.

•  Report updates: 100, then 260.

•  Total: 300, then 480.

Which work should you investigate first, and what do you check?

•  A. Report updates, because they explain 160 of the 180-credit increase. Check the number of tasks, the model, the context, and the retries.

•  B. Draft comparisons, because they used the most credits in the prior week.

•  C. All three equally, because every line went up.

### 3. Choose a model for the task

A summary update has clear requirements, one summary, and one approved figures file. What is the best evidence-backed model-choice approach?

•  A. Start with the most powerful model because the summary goes to leadership.

•  B. Change models after every response, even when the result has not been checked.

•  C. Start with Auto on Balance and the default effort, verify the result against the approved figures and requirements, and step up only if checked evidence shows a need.

### 4. Apply risk controls to agentic work

The repository's instructions say "Never change files in data/," and the agent can still edit any file in the repository. Which control makes sure a change to the figures can't go in unreviewed?

•  A. Repeat the instruction in every prompt, because the agent always follows instructions.

•  B. Make the data owner a code owner of data/ and require code owner review in a ruleset, so no change to the figures merges without that person.

•  C. Write a longer, more detailed instruction.

### 5. Responsible AI for operational workflows

The agent reports that every figure in a summary matches the data. The list of changed files shows that it changed the Total row in data/13-figures.csv. What do you do?

•  A. Approve, because the summary and the data now agree.

•  B. Raise the reasoning effort and approve the next attempt.

•  C. Request changes: restore the figures file and correct the summary instead.

## Additional checks

### 6. What do you attach for a business check?

You want Copilot to check a summary against its source figures. What do you attach?

•  A. The summary and the figures file only.

•  B. Every earlier draft and the whole client folder, so Copilot doesn't miss anything.

•  C. The summary, the figures file, and the client's contract for extra context.

### 7. Choose the right customization

A team wants a repeatable release-note workflow that Copilot should load only for release tasks. Which option fits?

•  A. Put the whole workflow in every prompt.

•  B. Create a skill for the release-note workflow.

•  C. Add an MCP server, even though no external system is needed.

### 8. Decide whether MCP is appropriate

A reviewer needs to compare one report with a current, approved policy export from a system outside the repository. The task needs no live updates or actions. What is the best starting point?

•  A. Attach the approved export and limit the task to that file.

•  B. Configure a persistent MCP connection with every available tool.

•  C. Ask the model to recall the policy.

### 9. Treat explanations as evidence

A more capable model gives a confident explanation for a changed figure but does not identify the source row. What should the reviewer do?

•  A. Accept it because the explanation is detailed.

•  B. Ask to see the model’s private reasoning.

•  C. Require the source row, verify the figure, and record uncertainty if the source is incomplete.

### 10. Protect the approved shared version

A report update is approved as one task, but the agent also finds an unrelated formatting issue. Which branch strategy provides the strongest control?

•  A. Make both changes directly on the default branch.

•  B. Put both changes on one branch so reviewers see everything together.

•  C. Use a separate task branch and reviewed pull request for the approved report update, and handle the unrelated issue separately.

## Answers and explanations

**B.** The visible message is only part of the input. Earlier messages, attached files, and tool results add context to every request.

**A.** Report updates increased by 160 credits of the 180 total. Divide by the number of tasks to see whether the team did more work or each task cost more.

**C.** Start with settings that fit the clear, well-scoped task. Verify the output against the approved figures and requirements, then step up only when checked evidence—such as missing facts, unresolved ambiguity, or repeated discrepancies—shows that the starting choice cannot meet them.

**B.** An instruction guides the agent, but it doesn't remove access. A required code owner review blocks the merge until that person approves.

**C.** The figures file is the source. Changing the source to match the summary hides the error instead of fixing it.

**A.** Attach only the sources the task needs. Extra drafts add input tokens, and confidential files the task doesn't need add risk.

**B.** A skill packages task-specific instructions and supporting resources for a repeatable workflow that is loaded when relevant. A prompt is immediate, and MCP is for external tools or context.

**A.** A current approved file is sufficient for a one-time read-only comparison. Use MCP when repeated access to current external information or approved tool actions justifies a governed connection.

**C.** A convincing explanation is not proof. The reviewer needs source-linked evidence and explicit uncertainty, not access to private model reasoning.

**C.** A separate task branch keeps the approved scope isolated and lets reviewers verify the exact changes, checks, and evidence before merging. Direct default-branch changes bypass that review point, and unrelated work on the same branch obscures scope and makes rollback and approval harder.

For guidance on supervising Copilot agents, see GitHub Copilot Agents application card.
