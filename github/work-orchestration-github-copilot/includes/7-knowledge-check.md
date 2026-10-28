# **7.** **Knowledge check**
### YamlMime:ModuleUnit

uid: learn.github.work-orchestration-with-github-copilot.knowledge-check

title: Knowledge Check

metadata:

  title: Knowledge check

  description: Check what you've learned about orchestrating work with GitHub Copilot.

  ms.topic: unit

durationInMinutes: 5

content: |

quiz:

  questions:

  - content: "A stakeholder asks the team to 'improve the checkout experience.' What should you do before asking GitHub Copilot to implement the work?"

    choices:

    - content: "Ask Copilot to redesign the checkout immediately."

      isCorrect: false

      explanation: "Incorrect. A vague business request needs to be translated into actionable work before an agent can reliably execute it."

    - content: "Create a clear work item with an outcome, acceptance criteria, ownership, and constraints."

      isCorrect: true

      explanation: "Correct! Defining the expected outcome, acceptance criteria, ownership, and constraints turns a business request into executable work."

    - content: "Select the most powerful available model."

      isCorrect: false

      explanation: "Incorrect. Model selection comes after you understand the work and determine what capabilities the task requires."

    - content: "Start an Autopilot session and let Copilot determine the requirements."

      isCorrect: false

      explanation: "Incorrect. Copilot can help refine requirements, but the intended outcome and constraints should be established before delegating the work."

  - content: "You need to modify a repository using local files, run commands, and work directly in the local development environment. Which Copilot working surface is the best fit?"

    choices:

    - content: "GitHub.com"

      isCorrect: false

      explanation: "Incorrect. GitHub.com is useful for GitHub-hosted work, but this scenario specifically requires direct interaction with the local development environment."

    - content: "GitHub Copilot app"

      isCorrect: false

      explanation: "Incorrect. The Copilot app can support agent sessions, but this scenario specifically calls for local command-line and development environment access."

    - content: "Copilot CLI"

      isCorrect: true

      explanation: "Correct! Copilot CLI is well suited to local workflows where the agent needs to work with files, commands, and the development environment."

    - content: "GitHub Projects"

      isCorrect: false

      explanation: "Incorrect. Projects is used to plan and track work, not to provide a local development environment."

  - content: "A task is complex and has several possible implementation approaches. You want Copilot to develop an implementation approach that you can review before changes are made. Which session mode is most appropriate?"

    choices:

    - content: "Interactive"

      isCorrect: false

      explanation: "Incorrect. Interactive mode provides close human involvement, but this scenario specifically emphasizes developing and reviewing an implementation approach first."

    - content: "Plan"

      isCorrect: true

      explanation: "Correct! Plan mode is appropriate when you want to develop and review an approach before implementation."

    - content: "Autopilot"

      isCorrect: false

      explanation: "Incorrect. Autopilot provides a higher level of autonomy and is better suited to well-defined, lower-risk work."

    - content: "No session mode"

      isCorrect: false

      explanation: "Incorrect. Choosing an appropriate session mode is part of determining how much autonomy and human control the task requires."

  - content: "Which statement best describes the relationship between a Copilot agent and an AI model?"

    choices:

    - content: "An agent and a model are two names for the same capability."

      isCorrect: false

      explanation: "Incorrect. An agent and a model provide different parts of the Copilot experience."

    - content: "The model determines permissions and tools, while the agent provides reasoning."

      isCorrect: false

      explanation: "Incorrect. The agent provides capabilities such as tools, environment, instructions, and permissions. The model provides the intelligence used to perform the work."

    - content: "The agent determines how work is carried out, while the model provides the intelligence used to carry it out."

      isCorrect: true

      explanation: "Correct! The agent defines the capabilities and working environment, while the model provides the reasoning and generation capabilities."

    - content: "Agents are only used for GitHub Issues, while models are only used for pull requests."

      isCorrect: false

      explanation: "Incorrect. Agents and models can be used together across different Copilot workflows and tasks."

  - content: "Copilot has completed a change that appears to satisfy the original request. What should you do before considering the work complete?"

    choices:

    - content: "Merge the changes immediately."

      isCorrect: false

      explanation: "Incorrect. Copilot output should be reviewed and validated before it becomes an approved change."

    - content: "Start another autonomous session without reviewing the result."

      isCorrect: false

      explanation: "Incorrect. Increasing autonomy does not remove the need for human oversight and validation."

    - content: "Validate the result against the acceptance criteria and review the resulting changes."

      isCorrect: true

      explanation: "Correct! Validate the result against the original requirements and use the appropriate GitHub review workflow before approving the work."

    - content: "Delete the original work item because Copilot completed the task."

      isCorrect: false

      explanation: "Incorrect. The original work item provides important context and traceability and should normally remain connected to the completed work."

