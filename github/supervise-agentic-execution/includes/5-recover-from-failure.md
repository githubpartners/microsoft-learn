# Unit 5: Recover from Failure

Start with the requirement, the changed files, and the session or workflow log. Compare the expected result with the actual result. Identify the first specific error or incorrect result, because the agent's final summary may not explain the cause.

The following failure types help your team investigate. They aren't GitHub error codes.

| **Failure** | **What to look for** | **Corrective action** |
| --- | --- | --- |
| Context | A missing file, an outdated requirement, or the wrong source, such as the earlier draft instead of the figures file. | Point to the right source and state which version applies. |
| Permission | A denied action, an unavailable repository, or a blocked network request. | Check that the task needs the action and that the agreement permits it. In the repository's settings, the repository administrator grants only the access that the task really needs. |
| Tool or environment | A failed command, a missing component, or an unsupported setting. | The setup fix needs administrator or technical reviewer access. Then repeat the check. |
| Instruction | The agent overlooked an agreed limit, or two instructions conflict. | Name the conflict, restate the limit, and request a specific correction. |
| Model or output | An incorrect figure, a statement the source doesn't support, or a claim of success without evidence. | Check the output against the source and request a specific revision. |
| Business requirement | The result matches the figures but doesn't serve the intended reader, such as a summary leadership can't use. | Clarify the acceptance criteria with the task owner. |

Fix the cause and keep the controls that detected the problem. Granting every permission to bypass a denial, or relaxing a check so the result passes, hides the problem instead of fixing it.

## Find the error in the run

When a Copilot session runs on GitHub Actions, the run records errors as **annotations**. A cloud session has no Actions run, so read its session log instead. To find the annotations:

1. In the repository, select the **Actions** tab.

2. In the left sidebar, select **Copilot cloud agent**, and then open the run. The separate **Copilot** workflow is Copilot code review.

3. On the run's **Summary** page, read the **Annotations** list. Select **Show more** to read a long error in full.

Here's a real example. The run stopped with this error: "Reasoning effort 'medium' is not supported for model 'gemini-3.8-flash'." This is a tool or environment failure. Reasoning effort is how much the model analyzes before it answers, and the selected model doesn't support that setting.

Retrying with the same settings would fail again, so the session operator restarts the task with a supported model or setting.

![The Annotations list of a cancelled run, ending with the unsupported reasoning effort error.](../media/workflow-run-error-annotations.png)

The Annotations list on a run's Summary page. The last error names the real cause.

A **firewall** restricts network connections. When the agent's firewall blocks a request, a warning shows the address the agent tried to reach. Share that evidence with the right owner.

If the task really needs that address, someone with the administrator role allows only that address in the agent's internet access settings. Keep the firewall enabled. For session logs, access checks, and firewall warnings, see [Troubleshooting GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/troubleshoot-cloud-agent).

## Work through a failed requirement

1. **Check the result against the source.** For example, an agent corrects a report's revenue to $16.8 million USD. Its pull request description says "All figures now match the source." But the report still says North had the highest operating margin, at 16.8%. East's margin is higher, at 17.3%.

2. **Identify what the check missed.** The agent checked each number it changed, but not the statements that compare regions.

3. **Request a targeted correction.** State the requirement, what you found, the change, and how to check it. For example: "East has the highest operating margin, 17.3%. Correct the North sentence and add East as the highest. Check every comparison against the figures."

4. **Read the whole summary again.** Include the lines the agent didn't change, because a fix in one place can leave another statement wrong.

5. **Resolve unclear requirements before accepting the result.** The rules don't specify how to round South's revenue of 3,950 thousand, which reads as $4.0 million USD. The report owner decides that before you accept the result.

## Decide whether to retry or escalate

Retry when you understand the cause, the fix stays within the approved scope, and you can check it. To escalate means to refer the decision to someone with the authority to make it.
Escalate when requirements conflict, when access needs an owner's decision, or when repeated attempts show nothing new.

Post the escalation as a comment on the issue or the pull request and mention the owner. Include the requirement, the failure, the evidence, and the decision you need. A practical trigger: when the same check fails twice with the same error, stop the attempts and escalate with that short report.

### Before you restart

Restarting a task needs repository write access.

- The task owner confirms what failed and which fix the team permits.

- Save the link from the earlier attempt and check its changes before you choose the base branch for the new attempt.

In the new prompt, summarize what failed, the evidence, and the permitted fix. Don't paste the whole earlier session: it can hide the correction among other text.
