# **Unit 6: Improve Systematically**

For example, when reports repeatedly include unsupported outlook statements, a team can use run evidence to investigate the cause. With this unit, you can make a workflow better one small, measured change at a time, so you know which change helped.

When a workflow fails repeatedly, use the data and the run records to look for the cause. Check its context, permissions, tools, instructions, model output, and business requirements. Treat your explanation as something to test, not a proven cause.

## Group failures into a pattern first

Recurring failures can indicate a systematic improvement opportunity. A **pattern** is a problem that recurs across requests and shares one cause. Before changing the workflow for routine quality problems, check that the evidence points to a common cause and that the cause maps to one thing you can change, such as the instructions, attached context, or a tool.

When failed requests point to different causes, split them into separate patterns, each with its own change and measurement. A single high-impact incident—such as exposing sensitive information or taking a disallowed action—can justify immediate containment or a change to permissions, boundaries, or approval gates. Record the intervention, then measure its effects afterward.

## Match the change to the cause

Fix each recurring problem at its cause, and then check the matching measure on the next similar requests:

- **Claims without a source**, such as an unsupported forecast: add "Name the source for every claim, or mark it as unsupported" to .github/copilot-instructions.md. Adding it is a commit, so it needs write access. Check accuracy.

- **Missing context**, such as a draft nobody attached: attach it in the issue or the prompt. Check completeness.

- **A tool that fails or times out**: check the tool's setup before you switch models. That check needs the administrator role. Check the recovery rate and the running time.

- **Denied permissions**: the access owner decides whether the task needs that access, or you narrow the task. Check the exception rate.

- **Weak answers with the right sources**: compare models in a small approved trial, with one model for every request in it. Check quality and cost per accepted summary.

- **An unclear requirement**, such as how to round revenue figures: post the question in a comment on the issue and mention the report owner, who decides. Check the rework rate.

For a rule that applies only to some files, such as everything in report/, a path-specific instructions file (.github/instructions/NAME.instructions.md) keeps it next to those files. To set up the instructions file, add repository custom instructions.

For example, the file could tell Copilot to use only the figures in the data folder and to flag any figure that doesn't match.

Keep every check turned on. Turning a check off improves the numbers by hiding problems.

## Set gates, boundaries, and escalation rules

- An **approval gate** requires a person's authorization before a significant action. The person in charge decides in advance which actions need it. GitHub setting: require human approval for workflow runs, and approvals on the **pull request** before merge. Both need the administrator role.

- A **workflow boundary** defines the permitted data, files, actions, time limits, and spending. GitHub settings cover part of it: passwords and keys, connected tools, and budgets. Write the rest, such as "never change files in data/," as a team agreement in the workflow's issue.

- An **escalation rule** names who handles exceptions and when the work must stop. Team agreement: write it in the issue or in your team's written procedures.

- A **rollback plan** states who can restore the previous approved version and when. Team agreement: write it next to the escalation rule.

Use trial evidence, rather than adding approvals everywhere, to decide which control needs to change:

- Did a request exceed its approved files, access, or spending before anyone intervened? Tighten the boundary or add approval before that action.

- Did an unclear requirement or recurring exception delay the work? Name the person who decides and when the agent must stop and ask.

Record the change and its owner, then measure whether it reduces exceptions and rework without weakening quality.

## Change one thing and measure again

Where you can, change one main factor at a time. If you change two things and the numbers move, you can't tell which change did it. Keep a change record in the workflow's issue, so the next person sees what changed and why:

- The original version and the suspected cause.

- The prompt or instructions, and the approved context.

- The tool and model versions, if known.

- The permissions, the gates, and the owner.

- The date and the configuration commit. The technical reviewer has the commit.

- The acceptance criteria and the rollback plan.

Then test new, similar requests with the same definitions, time period, checklist, groups, and costs across all attempts.

Keep a small **regression set**: five to ten past requests with accepted answers. After each change, run them again and compare the outputs with the accepted ones. If a change improves the new requests but breaks the old ones, you find out before the team does.

Inputs change too. For example, if a data owner revises a report's source figures, check the report again with the same checklist as the first review, and record which version of the figures you checked, by its commit. Acceptance against the old figures doesn't carry over to the new ones.

For a code review trial, record the review effort, the automatic triggers, and the number of reviews that actually ran. Copilot code review settings are at profile picture > Settings > Copilot > Code review. A lower total can mean fewer reviews ran, not that reviews became more efficient, so compare cost per accepted outcome with the same quality requirements.

For scheduled work, record the actual runs over the same period, including runs that produced no accepted result. Repository configuration changes need the technical reviewer's access. The owner decides whether to keep, revise, stop, or escalate each change.