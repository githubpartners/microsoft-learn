# **5. Manage Session Context**

When you work with GitHub Copilot, the quality of the result depends heavily on the context available to the session. Copilot can work with information from your repository, files, issues, Projects, documentation, and other relevant sources, but more context isn't always better.

The goal is to provide **the right context for the task**. Too little context can lead to incomplete or incorrect results. Too much irrelevant, conflicting, or outdated context can make it harder for Copilot to determine what matters.

Managing context is therefore an important part of orchestrating work with Copilot.

## **Build the right context**

Start by identifying what Copilot needs to understand the task.

For example, if you're asking Copilot to update an authentication flow, the relevant context might include:

- The issue describing the required change

- The files that implement authentication

- Related tests

- Repository instructions or coding conventions

- Documentation describing the expected behavior

- Related pull requests or previous implementation decisions

You don't necessarily need to provide the entire repository or every issue related to the project. Focus on the information that helps Copilot understand the **goal, constraints, expected behavior, and implementation context**.

This makes the session more focused and helps Copilot make better decisions.

## **Add context with mentions and commands**

Depending on the Copilot experience you're using, you can explicitly provide context using mentions and slash commands.

Mentions can help you point Copilot to relevant resources, such as files, issues, or other GitHub content. This is useful when you already know which resource contains information that Copilot needs.

Slash commands provide shortcuts for common interactions with Copilot. They can help you control how you interact with the session without having to describe every action in natural language.

Together, these features make it easier to direct Copilot toward the information that matters.

## **Use instructions to establish expectations**

Context isn't only about the files and resources Copilot can access. Instructions also influence how Copilot approaches the work.

Repository custom instructions can provide persistent guidance about a codebase, such as:

- Coding conventions

- Testing requirements

- Project structure

- Preferred tools or frameworks

- Rules that Copilot should follow when making changes

This is particularly useful for teams because important project guidance doesn't have to be repeated in every session.

Think of instructions as part of the operating context for Copilot. They help establish **how the work should be done**, while task-specific context explains **what work needs to be done**.

## **More context isn't always better**

A common mistake is to assume that adding more context will always produce better results.

Consider a task that requires updating one API endpoint. Providing the relevant issue, implementation files, tests, and API documentation can give Copilot what it needs. Adding unrelated issues, obsolete documentation, and files from a different subsystem may introduce noise.

When managing context, ask:

- Is this information relevant to the task?

- Is it current?

- Does it provide a requirement, constraint, example, or useful implementation detail?

- Could it conflict with another source of information?

- Does Copilot actually need it to complete the task?

The objective is not to maximize the amount of context. It is to maximize the **relevance of the context**.

## **Watch for conflicting or outdated information**

Repositories often contain information that changes over time. Documentation, comments, issues, and implementation details can become inconsistent with one another.

For example, an issue might describe an older version of an API while the current implementation uses a newer version. If both are available as context, Copilot may have difficulty determining which behavior is expected.

Before relying on a source, consider whether it is:

- Current

- Authoritative

- Consistent with the task

- Consistent with the current implementation

When sources conflict, clarify the expected behavior instead of assuming Copilot will determine which source is correct.

## **Protect sensitive information**

Context management also includes deciding what information should not be provided to a Copilot session.

Avoid unnecessarily exposing sensitive information such as credentials, secrets, private data, or other information that isn't required for the task. Use the repository and organization's existing security and access controls when determining what Copilot should be able to access.

The principle is simple: **give Copilot the information it needs to complete the task, and avoid exposing information it doesn't need.**

## **Manage the session lifecycle**

A Copilot session is not necessarily a single prompt and response. You can build on the session as the work progresses, provide additional context, clarify requirements, and respond to questions or proposed changes.

For a complex task, you might:

1. Start with the issue and acceptance criteria.

1. Provide the relevant repository and files.

1. Ask Copilot to analyze the existing implementation.

1. Clarify assumptions or constraints.

1. Provide additional documentation if needed.

1. Review the proposed approach or changes.

1. Continue the session as the work evolves.

This creates a more deliberate workflow than repeatedly starting new sessions without carrying forward the relevant context.

## **A practical context checklist**

Before asking Copilot to perform a significant task, check that you have:

| **Context** | **Question** |
| --- | --- |
| **Goal** | What outcome am I trying to achieve? |
| **Requirements** | What must the solution do? |
| **Files** | Which files contain the relevant implementation? |
| **Issues** | What existing work or requirements provide background? |
| **Documentation** | What technical or business guidance applies? |
| **Instructions** | What project-specific rules should Copilot follow? |
| **Constraints** | What should Copilot avoid changing? |
| **Validation** | How will I know the result is correct? |

This checklist helps turn a vague request into a well-scoped Copilot session.

## **Benefits of effective context management**

Managing session context effectively helps you:

- Reduce irrelevant or conflicting information.

- Give Copilot a clearer understanding of the task.

- Maintain consistent project-specific behavior.

- Reduce the need to repeat instructions.

- Make complex tasks easier to break into manageable steps.

- Improve the traceability between requirements and implementation.

- Keep sensitive information out of the session when it isn't required.

The most effective Copilot workflows don't simply give the agent more information. They give it **the right information at the right time**.

## **Next unit: Close the loop in GitHub**