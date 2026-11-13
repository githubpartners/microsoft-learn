## **Unit 4 — Define Decision Rights**

Decision rights describe who may decide and who remains accountable. They prevent a recommendation from silently becoming an authorized action.

Use three categories to discuss the design with stakeholders. These categories aren't GitHub permission settings; implementation must use appropriate controls to support them.

### **Assign agent-owned, human-approved, and human-only decisions**

| **Category** | **Meaning** | **Example** |
| --- | --- | --- |
| Agent-owned | The agent may complete a bounded decision without case-by-case approval. | Group issue descriptions into draft report themes using agreed criteria. |
| Human-approved | The agent prepares a proposal, but a person authorizes the controlled action. | Propose documentation changes in a pull request for required review before merging. |
| Human-only | An authorized person makes the decision; the agent may organize supporting information. | Approve a policy exception or commit a team to a deadline. |

Assign rights by consequence, evidence, and reversibility. A low-impact draft is easier to review and correct than a public commitment. An agent's confidence isn't a substitute for delegated authority.

Be precise about the action. Recommending a category, applying a label, assigning an owner, and promising a response are different activities. Permission to do one doesn't imply permission to do the others.

### **Place approval before the controlled action**

An approval point needs four things:

1. The exact action being authorized.

1. The person or role allowed to authorize it.

1. The evidence that person reviews.

1. What happens after approval, rejection, or no response.

A pull request proposes changes to repository files. It provides a review surface, but opening one doesn't itself establish every approval requirement. Required reviews and other applicable repository controls must be configured to enforce the intended boundary.

Likewise, a prompt that says "wait for approval" isn't an approval mechanism. Ask the implementer to show how the controlled action is blocked while approval is pending. If no suitable mechanism exists, retain that action as a manual step.

### **Distinguish clarification, escalation, and stopping**

These responses address different problems:

- Clarification requests a missing fact. For example, ask which page a documentation issue concerns.

- Escalation refers a decision beyond the workflow's authority or expertise. For example, send a conflict between approved instructions to the policy owner.

- Stopping prevents the affected work from proceeding when a mandatory condition isn't met. For example, don't publish a complete report if its mandatory source couldn't be read.

An escalation should include the source item, unresolved question, reason for referral, and action taken or withheld. Name the receiving role and how the handoff will be recorded. Notification isn't the same as resolution.

Define stop conditions in advance, including denied access, unavailable mandatory sources, failed validation after the allowed correction attempts, or a requested action outside the authorized scope. Stopping safely should produce an explicit failure or pending state, not a success message.

### **Match authority boundaries to technical access**

GitHub documents read-only access by default for agentic workflows and controlled writes through declared safe outputs. These provide supported output actions, such as creating an issue, without granting unrestricted agent write access.

A safe output doesn't guarantee that content is accurate or human-approved. Creating a report issue still publishes information to that repository's audience.

Review instructions, tool access, permissions, and allowed outputs together. The design should give the workflow only the capabilities it needs, with a person accountable for reviewing consequential results.

### **Give reviewers a decision they can actually make**

Human involvement is useful when the person receives enough information to judge the proposal. An approval request containing only "the agent recommends this change" transfers little more than the agent's confidence.

For a proposed documentation change, the reviewer should be able to inspect the original concern, the proposed wording, the relevant guidance, and any unresolved assumptions. The reviewer can then accept the proposal, request a revision, or reject it for a stated reason.

Keep the review proportional to the decision. Someone checking whether a summary preserves source meaning doesn't necessarily have authority to change policy. Route policy decisions to the appropriate owner rather than treating every reviewer as interchangeable.

When a proposal changes after review, establish whether it needs renewed approval. An earlier acceptance shouldn't silently authorize a materially different action. Ask the technical maintainer how the chosen controls handle that situation.

### **Resolve competing instructions without expanding authority**

An issue may request behavior that conflicts with the workflow's agreed scope. For example, a requester might ask the reporting agent to assign work immediately, although its role is limited to preparing recommendations.

The submitted request is information to evaluate, not permission to expand the workflow's role. The appropriate result is to identify the request and preserve the authority boundary. If an exception is needed, refer it to the owner.

Likewise, a claim of urgency doesn't remove approval requirements. A time-sensitive case may justify faster escalation, but not a different decision-maker unless the organization has explicitly defined that arrangement.

### **Define what pending means**

A workflow can finish its contribution while the business decision remains open. For example, it may record a complete referral and stop; the policy owner still needs to decide.

Distinguish completed preparation, awaiting a human decision, and failed execution in the design. If review receives no response, specify a reminder or referral route where appropriate. Don't treat silence as approval.

These states help people understand what requires attention without reading every run log. They also prevent a successful automated step from being mistaken for acceptance of the underlying business recommendation.
