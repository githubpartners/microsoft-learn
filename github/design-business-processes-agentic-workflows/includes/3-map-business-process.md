## **Unit 3 — Map the Business Process**

A process map describes how work moves from a starting event to a result. A table or numbered sequence is enough; you don't need a diagram or technical workflow file.

Start by examining how a person completes the task today. "Prepare a report" may hide several activities: select records, read discussion, calculate measures, interpret themes, check claims, and deliver the result. Mapping them reveals what the agent needs and where people remain involved.

### **Identify the trigger, inputs, and context**

A trigger starts the workflow. GitHub Actions supports repository events, schedules, and manual starts. A new issue might start triage; a schedule might start reporting.

Specify what should and shouldn't cause another run. Opening an issue, editing it, and adding a comment are different events. Enabling all of them without a purpose can create repeated work.

Then separate:

- Inputs: The records being processed, such as issue descriptions and selected comments.

- Context: The instructions used to interpret them, such as reporting requirements or approved categories.

Open a repository's Issues tab and inspect descriptions and discussion before deciding what the process can rely on.

Define the scope explicitly. A report about recent issue activity may need different records from a list of all unresolved issues. An older issue can remain open without having been created in the reporting period.

### **Describe steps, transformations, and decisions**

A transformation changes information into a more useful form. Grouping descriptions into themes and condensing a discussion into a summary are transformations. Counting records and selecting dates can often use fixed operations rather than model judgment.

A decision selects the next path. For example, "Are all mandatory sources available?" determines whether the workflow continues or records a failure.

The following illustrative map applies to the reporting use case documented by GitHub:

| **Step** | **Work and transformation** | **Decision or exception** | **Responsibility** |
| --- | --- | --- | --- |
| Start | Establish the repository and reporting period. | Is the requested scope authorized? | Configured workflow; owner approves scope. |
| Retrieve | Obtain the selected issue records. | If a mandatory source is unavailable, stop and report the gap. | Tools retrieve information. |
| Measure | Calculate agreed activity counts. | Apply the same date and inclusion rules each time. | Repeatable operations. |
| Analyze | Turn descriptions into themes and unresolved questions. | Mark unsupported or conflicting information. | Agent interprets evidence. |
| Validate | Compare the draft with reporting criteria. | Correct bounded problems or route unresolved failures. | Checks and reviewer, as designed. |
| Deliver | Create the report in the approved destination. | Confirm delivery; don't blindly duplicate a failed attempt. | Configured output mechanism. |
| Use | Consider recommendations during planning. | Accept, reject, or request more information. | Responsible people. |

This is a business map, not a one-to-one list of technical jobs. GitHub Actions uses jobs and steps to organize execution on a runner, the environment performing the work. An implementer translates your process into those structures.

### **Include tools, outputs, and human boundaries**

A tool gives the agent a capability, such as retrieving issue information. Name the required operation, not just a product: "read issues from the selected repository" is clearer than "use GitHub."

Define the output as a deliverable: its contents, recipient, destination, and evidence. A report needs more than "summary completed." Readers should know what it covers and where its claims came from.

Finally, mark the boundary between preparing information and making commitments. The agent may identify unresolved questions; the planning team decides which work to undertake. Include human review as a process step with a named role, not an assumption outside the map.

Exceptions belong in the same design. Missing facts may require clarification; denied access requires a failure path; a disputed policy may require escalation. Without these paths, an implementation may appear successful while delivering incomplete work.

### **Trace one item through the map**

Use a real, authorized example to check whether the map is complete. For a documentation request, begin with the submitted title and description, not an idealized version containing every fact.

Suppose the description identifies a confusing instruction but doesn't link to its page. The first useful result may be a missing-information finding rather than a recommended edit. Your map should show who prepares the question, whether sending it is authorized, and how the response enters the process.

Continue the walkthrough after the missing fact is supplied. Does the process re-read the updated issue? Does a person restart it? Which information from the previous attempt is still relevant? These are design questions for the trigger and handoff, not details the agent should invent.

Now compare the normal route with an exception:

| **Situation** | **Appropriate next step** | **Evidence to retain** |
| --- | --- | --- |
| Required details are present. | Prepare the defined analysis. | Source links and the input scope. |
| A requester omitted a necessary fact. | Prepare or send an authorized clarification. | The missing fact and pending question. |
| The workflow can't read a mandatory source. | Record an operational failure. | The unavailable source and affected work. |
| Approved references conflict. | Refer the conflict to the responsible owner. | Both references and the unresolved decision. |

The distinction matters because "needs more information" can hide very different responsibilities. A requester can supply a page link; they can't necessarily resolve a denied permission or decide which organizational policy takes precedence.

### **Make handoffs visible**

A handoff transfers work between the agent, a tool, or a person. For each handoff, identify what is passed, who receives it, and how the receiver knows action is needed.

A report stored successfully but never brought to the intended reviewer's attention may not support the business process. Similarly, an escalation that reaches an unmonitored destination doesn't establish useful human involvement.

Walk through the map with the people who perform the work. Ask them to identify hidden checks, likely exceptions, and the point where they consider their part complete. Resolve disagreements before translating the map into configuration.

