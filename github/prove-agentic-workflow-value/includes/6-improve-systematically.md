# **Unit 6: Improve Systematically**

When reports repeatedly include unsupported outlook statements, a team can use run evidence to investigate the cause. With this unit, you can make a workflow better one small, measured change at a time, so you know which change helped.

When a workflow fails repeatedly, use the data and the run records to look for the cause. Check its context, permissions, tools, instructions, model output, and business requirements. Treat your explanation as something to test, not a proven cause.

## Group failures into a pattern first

Recurring failures can indicate a systematic improvement opportunity. A **pattern** is a problem that recurs across requests and shares one cause. Before changing the workflow for routine quality problems, check that the evidence points to a common cause and that the cause maps to one thing you can change, such as the instructions, attached context, or a tool.

When failed requests point to different causes, split them into separate patterns, each with its own change and measurement. A single high-impact incident, such as exposing sensitive information or taking a disallowed action, can justify immediate containment or a change to permissions, boundaries, or approval gates. Record the intervention, then measure its effects afterward.

## Match the change to the cause

Fix each recurring problem at its cause, and then check the matching measure on the next similar requests:

- **Claims without a source**, such as an unsupported forecast: add "Name the source for every claim, or mark it as unsupported" to `.github/copilot-instructions.md`. This requires a commit and write access to the repository. Check accuracy.

- **Missing context**, such as a draft nobody attached: attach it in the issue or the prompt. Check completeness.

- **A tool that fails or times out**: check the tool's setup before you switch models. Check the recovery rate and the running time.

- **Denied permissions**: the access owner decides whether the task needs that access, or you narrow the task. Check the exception rate.

- **Weak answers with the right sources**: compare models in a small approved trial, using the same model for every request in that trial. Check quality and cost per accepted summary.

- **An unclear requirement**, such as how to round revenue figures: post the question in a comment on the issue and mention the report owner, who decides. Check the rework rate.

Keep every check enabled. Turning a check off improves the numbers by **hiding** problems.

## Set gates, boundaries, and escalation rules

- An **approval gate** requires a person's authorization before a significant action. The task owner decides in advance which actions need it.

- A **workflow boundary** defines the permitted data, files, actions, time limits, and spending. GitHub settings cover part of it: passwords and keys, connected tools, and budgets. Write the rest, such as "never change files in data/," as a team agreement in the workflow's issue.

- An **escalation rule** names who handles exceptions and when the work must stop.

- A **rollback plan** states who can restore the previous approved version and when. Team agreement: write it next to the escalation rule.

Use trial evidence, rather than adding approvals everywhere, to decide which control needs to change:

- Did a request exceed its approved files, access, or spending before anyone intervened? Tighten the boundary or add approval before that action.

- Did an unclear requirement or recurring exception delay the work? Name who decides and when the agent must stop and ask.

Record the change and its owner, then measure whether it reduces exceptions and rework without weakening quality.

## Change one thing and measure again

Where you can, change one main factor at a time. If you change two things and the numbers move, you can't tell which change did it. Keep a change record in the workflow's issue, so the next person sees what changed and why:

- The original version and the suspected cause.

- The prompt or instructions, and the approved context.

- The tool and model versions, if known.

- The permissions, the gates, and the owner.

- The date and configuration commit; the technical reviewer records the commit.

- The acceptance criteria and the rollback plan.

Then test new, similar requests with the same definitions, time period, checklist, groups, and costs across all attempts.

Keep a small **regression set**: five to ten past requests with accepted answers. After each change, run them again and compare the outputs with the accepted ones. If a change improves the new requests but breaks the old ones, you find out before the team does.

Inputs change too. For example, if a data owner revises a report's source figures, check the report again with the same checklist as the first review, and record which version of the figures you checked by identifying its commit. Acceptance against the old figures doesn't carry over to the new ones.

For a code review trial, record the review effort, the automatic triggers, and the number of reviews that actually ran. Copilot code review settings are at **profile picture > Settings > Copilot > Code review**. A lower total can mean fewer reviews ran, not that reviews became more efficient, so compare cost per accepted outcome with the same quality requirements.

For scheduled work, record the actual runs over the same period, including runs that produced no accepted result. The technical reviewer needs access to change repository configuration. The owner decides whether to keep, revise, stop, or escalate each change.