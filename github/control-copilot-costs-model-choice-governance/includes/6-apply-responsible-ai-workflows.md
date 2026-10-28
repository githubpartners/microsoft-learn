# Unit 6: Responsible AI for operational workflows

An agent's output isn't ready just because it reports that it meets the requirements. Accept an agent's work on evidence, and stop it the moment something looks wrong. You stay accountable for every deliverable, so you accept AI-assisted work only after you check it against its sources.

Before the agent starts, the task owner defines the requirements, limits, reviewers, escalation contacts, and evidence used to accept the result.

## Choose the right form of guidance or connection

| **Option** | **Purpose** |
| --- | --- |
| Prompt | The immediate request for this task and this run. |
| Instructions | Reusable guidance that applies within a defined scope. |
| Skill | A reusable workflow or capability for a specific kind of task. |

These options serve different purposes. None automatically authorizes a task, grants access beyond its configured permissions, guarantees correctness, or replaces evidence-based human review.

## Prepare the task requirements record

Before live work, the task owner records:

•  The approved repository and the files the agent may change.

•  The files the agent must not change.

•  The allowed changes.

•  The attempt limit.

•  The reviewers.

•  The escalation contacts.

•  The stop triggers and immediate actions the team will follow.

Write the record in the task's issue description so the reviewers and the agent read the same text. For example:

Task requirements

Repository: approved reporting repository

Files the agent may change: report/q3-summary.md

Files the agent must not change: everything in data/

Allowed change: make every figure and statement match data/13-figures.csv

Attempt limit: 2, then the report owner decides

Reviewers: report reviewer and second eligible reviewer

Escalation contacts: report owner and security team

## Set boundaries before the agent starts

For **risk-based autonomy**, the task owner chooses the permitted autonomy and records the file, attempt, and spending limits. The billing and repository administrators apply the enforceable controls, while named people monitor team agreements. Record a contact and action for each stop trigger; see “Stop and escalate problems” for examples.

### Choose a branch strategy

Use a separate branch for each approved task and bring the change back through a reviewed pull request. This protects the approved shared version while reviewers compare the changes, checks, and source evidence. Direct changes to the default branch bypass that review point, while mixing unrelated work into one branch makes scope, evidence, rollback, and approval harder to verify.

## Validate against the original requirements

Compare what the owner asked for with the actual change:

1. Read the **diff**, the view that shows what changed line by line, before you rely on the agent's summary. On the pull request, select **Files changed**: lines that start with + show added text, and lines that start with - show removed text ([review the changes](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request#starting-a-review)).

1. Connect each requirement to the evidence that supports it.

1. List changes outside the approved files, including the figures file and any workflow or configuration files. If there are none, record that.

1. For a code change, the approved tests run under the code owner's access, or you open the linked test result. Request any missing setup or evidence.

1. Give unresolved findings to the person who can decide.

For a report correction, acceptance criteria should cover the figures, comparisons, supported claims, and permitted files. Ask the owner about any missing rule, such as rounding; don't invent one.

**Worked review example:** two fictional proposals both report "every figure matches." One corrects the summary to $16.8 million. The other changes the Total row in the figures file to 16,900, so the summary matches the data. Only the first keeps the approved figures as the source. Inspect each list of changed files before you approve, and request changes on the second: restore the figures file and fix the summary.

The same method works for every deliverable: check the draft against the approved sources, required content, and privacy rules, however cheaply Copilot produced it.

## Review and approve the change

The accountable reviewer withholds approval for unmet requirements or unchecked changes. Ask for a correction that names the evidence, permitted files, and checks to keep. Workflow execution, pull request approval, and business acceptance are separate decisions.

A draft pull request can't merge. Marking a draft as ready for review is a separate step from approving it.

For training-only practice, choose Comment, keep the pull request as a draft, and don't collect approvals or merge.

## Show the reviewer what happened

**Transparency** means anyone can see what the agent did, with what information, and who decided what. Leave a record that someone can follow without reconstructing the chat. Include:

•  The business purpose, the allowed work, the Copilot feature used, and how AI helped.

•  The sources and files given to the agent, and the actions it performed.

•  The changes, checks, results, and unresolved failures.

•  Assumptions and cases no one checked.

•  The review and approval decisions, and who made them.

•  The known-good version, identified by the recovery owner, and the approved recovery procedure.

Write the record in the pull request description, and link the agent session there. Withhold the merge when no one can check the evidence. A **commit** is a saved set of changes.

On an agent commit, the **Verified** badge means GitHub verified the agent's signature for that exact commit. If its contents changed, it would be a different commit and need a new signature. The badge doesn't mean the change is correct.

## Stop and escalate problems

Use your organization's existing contacts and response processes.

| **Trigger** | **Immediate action** | **Contact** |
| --- | --- | --- |
| Unclear requirement, owner, or authority | Pause the task or session, and record the question. | Manager or process owner. |
| Unrelated edit or a request for broader access | Withhold the merge or the access, and keep the evidence. | System owner or security team. |
| Possible exposure of secrets or personal data, including a push protection alert, where GitHub blocks a change that contains a password or key | Stop the affected action, and describe it without copying sensitive values. | Security or privacy team. |
| Repeated failure or the agreed usage limit | Stop the attempts, and summarize the attempts, the cost, and the failure evidence. | Task owner. |
| Unexpected change to a live system | Stop the agent's actions, and follow the approved restore process. | Recovery owner and change or incident manager. |

Stopping doesn't undo existing changes. Follow the session management instructions to stop the session, and check separately for other workflows or outside activity.

Keep the evidence without secrets, and make no further changes while the owner assesses the issue. The recovery owner decides whether to restore the known-good version through the approved recovery process.

