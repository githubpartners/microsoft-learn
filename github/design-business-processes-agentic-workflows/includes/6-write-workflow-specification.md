## **Unit 6 — Write the Workflow Specification**

A workflow specification turns your design into an agreement that an implementer and reviewer can use. It explains what the workflow must do, what it must not do, and how its result will be evaluated.

You don't need to write configuration syntax first. Begin with the business requirement, then work with an implementer or coding agent to express it using supported capabilities.

### **Connect the specification to the workflow files**

GitHub's creation guidance describes an agentic workflow source file in .github/workflows/. The Markdown source contains configuration at the top, called frontmatter, followed by natural-language instructions.

The source is compiled into an Actions .lock.yml file. Review and commit both files. The Markdown describes the workflow; the compiled file enables its execution through Actions. Ordinary Actions doesn't directly execute the Markdown body.

Recognize the main configuration concepts:

| **Setting** | **Design question it helps answer** |
| --- | --- |
| on | What starts the workflow? |
| permissions | What access is configured? |
| tools | Which supported capabilities are available? |
| safe-outputs | Which supported output actions are allowed? |
| engine | Which supported agent engine executes the work? |

These aren't a complete configuration. Use current agentic workflow guidance rather than copying arbitrary Actions syntax into the source.

### **Write instructions that can be tested**

Compare "Review the issues and make a useful report" with:

Review issue activity for the agreed repository and period. Calculate the defined measures, summarize recurring themes, and identify unresolved questions using the approved criteria. Link significant findings to source issues. Separate recommendations from facts, identify unavailable information, and don't assign work or promise completion dates.

The second instruction identifies work, evidence, boundaries, and output expectations. It can be checked against representative inputs.

Define terms such as important, blocked, or ready. For example, an open issue isn't necessarily blocked. If unresolved ownership is the condition you care about, specify the evidence that establishes it and what to do when discussion is inconclusive.

### **Specify the agent, model strategy, tools, and permissions**

The model supplies reasoning and generation capability. The agent uses that capability with instructions, tools, and an execution environment. GitHub's engine setting selects a supported agent engine; it isn't interchangeable with a model selector in every Copilot experience.

For your model strategy, identify the required quality, source volume, response time, cost, and organizational restrictions. Compare supported configurations using the same representative cases. A more fluent model isn't better if it invents facts or misses required limits.

Describe tools by operation: reading scoped issues, reading approved guidance, or delivering the report. Don't infer that reading an issue requires permission to edit it.

Keep permissions separate from instructions. "Don't modify source issues" is useful guidance, but access and allowed outputs must also support that limit. Use supported authentication and secret management; never place credentials in prompts or workflow documents.

### **Assemble the specification**

GitHub's documented weekly report provides a useful starting point. The following design extends that example with illustrative business requirements; it isn't a complete or runnable configuration.

| **Section** | **Example requirement** |
| --- | --- |
| Business objective | Prepare a concise issue activity report so maintainers can review themes and unresolved questions before planning. Planning decisions remain outside scope. |
| Trigger | Run on the agreed weekly schedule. Define the reporting cutoff and date range separately from the execution time. |
| Inputs and context | Read issue activity from the named repository and period, plus approved report criteria. Identify mandatory sources and their locations. |
| Instructions | Calculate measures, group themes, explain notable unresolved questions, and propose follow-up. Support findings with links. |
| Model strategy | Evaluate supported, approved configurations for source accuracy, coverage, latency, and cost using representative issue sets. Record the accepted selection. |
| Agent | Use the selected supported engine with the bounded role of preparing reports for maintainer review. |
| Tools | Retrieve scoped issue records and required guidance. Use a supported output mechanism to deliver the report. |
| Permissions | Grant only required source access and the declared report-creation output. Don't permit unrelated issue edits or assignments. |
| Outputs | Create a report issue with the period, activity measures, themes, unresolved questions, recommendations, limitations, and source links. |
| Validation | Check required sections, date selection, counts, source support, and authority boundaries. |
| Escalation | Refer conflicting criteria or decisions outside scope to the named process owner, with evidence and the unresolved question. |
| Failure handling | Stop on mandatory-source failure, report denied access, limit retries, and confirm the destination before repeating uncertain publication. |
| Approval | Maintainers review recommendations before making commitments. If publication itself needs prior approval, redesign delivery with an enforceable gate or a manual publishing step. |
| Completion criteria | A validated report is delivered to the approved destination, or an explicit failure or referral is recorded. Business follow-up remains separately tracked. |

Replace general phrases such as "named repository" and "approved criteria" with actual agreed values before implementation. A design draft may leave questions open; an operational workflow must not rely on guessing.

### **Read the documented report example as a business designer**

GitHub's creation guidance describes a weekly issue activity report that includes opened and closed counts, recurring themes, notable unresolved issues, and recommendations. Read its instructions and configuration as two connected parts of the design.

First, identify the content requirements. Counts require selection rules and reliable calculation. Themes require interpretation of descriptions. Recommendations require a clear distinction between an observed concern and a proposed next step.

Then inspect delivery. The example's declared issue-creation output means the report is posted in the repository. If your requirement is "a private draft reviewed before publication," copying that example unchanged wouldn't meet it.

Finally, identify local decisions the simplified example leaves to you: what makes an issue notable, which audience reads the report, how source failures are handled, and who accepts recommendations. Product documentation demonstrates a capability; your specification makes that capability usable for your process.

This reading approach helps nontechnical designers contribute to implementation reviews. You don't have to interpret every configuration line, but you should be able to explain how its schedule, source access, and output relate to the requirement.

### **Turn quality criteria into concrete test cases**

Write each test with an input condition, expected behavior, and evidence to inspect. Avoid asking only whether the result "looks right."

| **Test condition** | **Expected behavior** | **Evidence** |
| --- | --- | --- |
| No issues match the agreed period. | Report no matching activity without inventing themes. | The selection result and report text. |
| A description reports a problem without confirming its cause. | Preserve the distinction between the report and a verified diagnosis. | Source wording compared with the summary. |
| Two approved references give incompatible instructions. | Identify the conflict and refer the unresolved decision. | Both references and the referral record. |
| Delivery may have succeeded before a timeout. | Check the destination before a repeat publication. | Destination record and retry outcome. |

Have a reviewer inspect expected behavior before running the tests. Otherwise, a plausible generated answer can influence what everyone retrospectively decides was acceptable.

For factual checks, verify the meaning of the linked source, not just whether a link exists. A source may support part of a statement while the summary adds an unsupported conclusion.

For model comparisons, reuse the agreed test set and output checks. Record material differences in coverage, corrections, and review effort. Select the supported configuration that meets the task's requirements; don't compare only writing style.

### **Agree on the first operational trial**

Passing sample tests supports a limited trial, not unrestricted adoption. Define the first trial's repository, audience, duration, and allowed actions with the process owner. Use authorized material and make clear which outputs are still being evaluated.

Identify who checks each result and how they record corrections. Separate factual errors, missing coverage, formatting issues, and inappropriate recommendations so you can see what needs improvement. Capture review time as well as generation time.

Agree on the conditions for continuing, revising, or stopping the trial. For example, an unauthorized output should trigger immediate review rather than wait for an average quality score at the end.

At the review point, compare the observed results with the original objective. A workflow may be useful with narrower sources or a manual delivery step even if the initial design wasn't acceptable. Record that revised scope before expanding use.

### **Choose an output and verify the handoff**

GitHub's report example creates an issue through a safe output. That makes the report visible to the repository's audience; it isn't a private draft awaiting publication.

Another design might save a file as an Actions artifact, a file or collection of files retained from a run, if an appropriate mechanism is configured.

The outlined link downloads a saved artifact. This generic image doesn't show an agentic report or imply that reports are saved automatically. Source:[ ](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/downloading-workflow-artifacts?utm_source=chatgpt.com)[GitHub Docs: Downloading workflow artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/downloading-workflow-artifacts?utm_source=chatgpt.com).

For an artifact route, confirm access, retrieval instructions, and retention because artifacts can expire. For any route, specify the audience and confirm successful delivery from the resulting record, not just the agent's statement.

### **Validate ordinary, boundary, and failure cases**

Test the agreement with a normal set of issues, an empty period, incomplete descriptions, conflicting guidance, an unavailable source, and a repeated run.

An empty reporting period and a failed retrieval must produce different outcomes. One can be a valid no-activity result; the other means coverage couldn't be established.

An agent can check its draft, but self-checking isn't independent proof of correctness. Use repeatable checks for structure and counts, source comparison for factual claims, and human review where judgment or authority requires it. Limit correction attempts and define who receives unresolved failures.

Before handing the design to an implementer, ask a reviewer to explain what success, failure, approval, and completion would look like. If the answers differ from yours, resolve the specification first.

### **Review the generated implementation against the agreement**

GitHub documents agent-assisted authoring through supported development tools. The authoring agent helps create and compile workflow files; that interactive authoring session isn't the same as the later scheduled or event-triggered run.

Before accepting generated files, ask the implementer to demonstrate the trace from each important requirement to the implementation or test evidence. Where is the repository scope set? Which operation delivers the output? How does a mandatory-source failure become visible?

Keep unresolved requirements explicit. If the chosen configuration can't enforce a required approval boundary or produce the intended output, revise the implementation or reduce the scope. Don't quietly replace the requirement with a prompt that merely asks for the desired behavior.


s