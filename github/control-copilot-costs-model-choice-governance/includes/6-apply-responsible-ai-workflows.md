# Unit 6: Responsible AI for operational workflows

An agent's output isn't ready just because it reports that it meets the requirements. Accept an agent's work based on evidence, and stop it the moment something looks wrong. You stay accountable for every deliverable, so you accept AI-assisted work only after you check it against its sources.

Before the agent starts, the task owner defines the requirements, limits, reviewers, escalation contacts, and evidence the owner will use to accept the result.

## Prepare the task requirements record

Before live work, the task owner records:

- The approved repository and the files the agent may change.

- The files the agent must not change.

- The allowed changes.

- The attempt limit.

- The reviewers.

- The escalation contacts.

- The stop triggers and immediate actions the team will follow.

Write the record in the task's issue description so the reviewers and the agent read the same text. For example:

```text
Task requirements
Repository: approved reporting repository
Files the agent may change: report/q3-summary.md
Files the agent must not change: everything in data/
Allowed change: make every figure and statement match data/q3-figures.csv
Attempt limit: 2, then the report owner decides
Reviewers: report reviewer and second eligible reviewer
Escalation contacts: report owner and security team
```

## Set boundaries before the agent starts

For **risk-based autonomy**, the task owner chooses the permitted autonomy and records the file, attempt, and spending limits. The billing and repository administrators apply the enforceable controls, while named people monitor team agreements. Record a contact and action for each stop trigger.

## Validate against the original requirements

Compare what the owner asked for with the actual change:

1. Read the **diff**, the view that shows what changed line by line, before you rely on the agent's summary. On the pull request, select **Files changed**.

2. Connect each requirement to the evidence that supports it.

3. List changes outside the approved files, including the figures file and any workflow or configuration files. If there are none, record that.

4. Give unresolved findings to the task owner.

For a report correction, acceptance criteria should cover the figures, comparisons, supported claims, and permitted files. Ask the owner about any missing rule, such as rounding.

**Worked review example:** two fictional proposals both report "every figure matches." One corrects the summary to $16.8 million USD. The other changes the Total row in the figures file to $16.9 million USD, so the summary matches the data. Only the first keeps the approved figures as the source. Inspect each list of changed files before you approve, and request changes on the second: restore the figures file and fix the summary.

The same method works for every deliverable: check the draft against the approved sources, required content, and privacy rules, however cheaply Copilot produced it.

## Review and approve the change

The accountable reviewer withholds approval for unmet requirements or unchecked changes. Ask for a correction that names the evidence, permitted files, and checks to keep. Workflow execution, pull request approval, and business acceptance are separate decisions.

You can't merge a draft pull request. Marking a draft as ready for review is a separate step from approving it.

For training-only practice, choose Comment, keep the pull request as a draft, and don't collect approvals or merge.

## Show the reviewer what happened

**Transparency** means anyone can see what the agent did, with what information, and who decided what. Leave a record that someone can follow without reconstructing the chat. Include:

- The business purpose, the allowed work, the Copilot feature you used, and how AI helped.

- The sources and files you gave the agent, and the actions it performed.

- The changes, checks, results, and unresolved failures.

- Assumptions and cases no one checked.

- The review and approval decisions, and who made them.

- The known-good version that the recovery owner identifies, and the approved recovery procedure.

Write the record in the pull request description, and link the agent session there. Withhold the merge when no one can check the evidence.

## Stop and escalate problems

Use your organization's existing contacts and response processes.

| **Trigger** | **Immediate action** | **Contact** |
| --- | --- | --- |
| Unclear requirement, owner, or authority | Pause the task or session, and record the question. | Manager or process owner. |
| Unrelated edit or a request for broader access | Withhold the merge or the access, and keep the evidence. | System owner or security team. |
| Possible exposure of secrets or personal data, including a [Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection) alert when GitHub blocks a push containing a detected secret | Stop the affected action, and describe it without copying sensitive values. | Security or privacy team. |
| Repeated failure or the agreed usage limit | Stop the attempts, and summarize the attempts, the cost, and the failure evidence. | Task owner. |
| Unexpected change to a live system | Stop the agent's actions, and follow the approved restore process. | Recovery owner and change or incident manager. |

Stopping doesn't undo existing changes. Follow the session management instructions to stop the session, and check separately for other workflows or outside activity.

Keep the evidence without secrets, and make no further changes while the owner assesses the issue. The recovery owner decides whether to restore the known-good version through the approved recovery process.
