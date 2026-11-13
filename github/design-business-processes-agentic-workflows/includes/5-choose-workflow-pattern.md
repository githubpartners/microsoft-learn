## **Unit 5 — Choose the Workflow Pattern**

A workflow pattern is a reusable way to organize work. Choose it from the question the process needs to answer, not from the tools you want to try.

The following six patterns help describe business requirements. They aren't a menu of GitHub workflow types.

### **Match the pattern to the need**

| **Pattern** | **When it fits** | **Expected result** |
| --- | --- | --- |
| Triage | New work needs initial handling. | A request summary, missing information, and a proposed next step. |
| Reporting | An audience needs an overview of activity. | A bounded summary with measures, findings, and source links. |
| Monitoring | A defined condition needs repeated checking. | A relevant alert or a clear no-action result. |
| Review | An existing artifact needs comparison with criteria. | Specific findings supported by evidence. |
| Classification | Items need consistent grouping. | Categories with reasons and uncertainty handling. |
| Escalation | An exception requires another person's decision. | A useful handoff to an authorized role. |

GitHub documents issue triage and reporting as agentic workflow use cases. Its development tutorial also demonstrates a pull request reviewer checking test coverage. The transferable review principle is comparison with explicit criteria; a business reviewer might instead check required sections or consistency with approved guidance.

### **Understand the important differences**

Triage prepares work for handling. Classification may be one part of triage, but assigning a category doesn't necessarily establish the next action. A request can be correctly classified and still lack essential details.

Reporting explains a selected set of activity for a particular audience. Define the period and measures. "Issues opened this week" and "issues still open" answer different questions. State which one you mean, and calculate counts with repeatable operations.

Monitoring looks for a condition, not simply something new to summarize. Specify what triggers an alert, what clears it, and when another alert is justified. If repeat suppression requires a record of earlier alerts, the implementation must maintain that record; don't assume the agent remembers previous runs.

Review identifies where an artifact doesn't meet a requirement. A useful finding names the location, criterion, and evidence. "This needs improvement" doesn't tell the recipient what to inspect.

Classification depends on category definitions. Decide whether one category, several categories, or an uncertain result is allowed. On GitHub, labels can represent categories, but a proposed category doesn't automatically create or apply a label.

Select Labels to inspect the repository's categories and descriptions. Use them to understand that repository's classification scheme, not as a required set of categories. Source: [GitHub Docs: Managing labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels?utm_source=chatgpt.com).

Escalation handles exceptions requiring authority or expertise. It shouldn't become the default route for every missing fact when a clarification question would suffice.

### **Define success and exit conditions**

Success should match the pattern. Triage should reduce the effort needed to understand and route a request. Reporting should provide accurate, traceable information for its audience. Monitoring should surface relevant conditions without repeated noise. Review findings should be specific enough to act on.

An exit condition states when a run ends. Examples include a validated report being delivered, an escalation being recorded, or a monitor finding no qualifying condition. Also define unsuccessful exits, such as unavailable mandatory information. Don't let the workflow continue indefinitely until it produces an answer.

### **Avoid common anti-patterns**

- One workflow for everything: Different purposes acquire broad access and unclear completion criteria.

- AI for fixed checks: A predictable rule is replaced by unnecessary interpretation.

- Forced certainty: Every item receives a category even when evidence is insufficient.

- Review without criteria: The result is opinion rather than a checkable finding.

- Automatic commitments: A suggestion becomes an assignment or promise without authorization.

Combine patterns only when their purpose is clear. Triage may classify requests and escalate exceptions, but scheduled reporting usually deserves its own scope, audience, and completion criteria.

### **Choose between patterns that use the same information**

The same repository can support several workflows, each answering a different question. Start by completing the sentence "The recipient needs to know..." rather than selecting a pattern from its name.

Consider these needs:

- "What happened across our requests this week?" points to reporting.

- "Which requests now meet the condition for attention?" points to monitoring.

- "What is this new request asking for, and what is missing?" points to triage.

- "Does this proposed guide meet our publishing checklist?" points to review.

A weekly report might mention an unanswered request, but it doesn't replace monitoring if the team needs an earlier alert. Conversely, a stream of alerts doesn't provide the coherent overview needed for a planning meeting.

Choose the smallest combination that answers the business question. If one workflow only needs to recommend categories, don't add assignment and publication actions merely because they could follow classification.

### **Define categories with examples and boundaries**

Classification becomes more dependable when category definitions explain intent. For example, a question asks how existing guidance works; a change request asks for different guidance. Both might mention the same page or feature.

Provide examples that distinguish the boundary, not just obvious examples of each category. "Where is the access procedure?" and "The access procedure needs a new approval step" contain similar vocabulary but ask for different responses.

Also define how to handle mixed intent. A request may ask a question and propose an improvement. Decide whether multiple categories are allowed or whether a reviewer should choose the next handling path. This is an illustrative design choice, not a GitHub default.

### **Use measures that reveal the pattern's weaknesses**

For classification, examine incorrectly assigned items and items that should have remained uncertain. For review, check both unsupported findings and missed problems. For monitoring, examine unnecessary alerts and qualifying cases that weren't surfaced.

These paired measures matter. A monitor can reduce noise by sending almost nothing while missing important work. A reviewer can find more possible concerns while creating an unreasonable checking burden.

Agree on the acceptable balance with the recipient before the pilot. Don't use the number of generated comments, categories, or reports as proof of value. The output should make the next decision easier or more reliable.