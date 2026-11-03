# Unit 2: Understand what drives Copilot costs

Before you start AI-assisted work, estimate its cost in AI credits and Actions minutes.

Every Copilot interaction sends information to an AI **model** and gets a response back. A model is the AI system that reads the input and generates the response. Models differ in capability, speed, and price.

> [!NOTE]
> The AI credit calculation stays the same across platforms (meaning the environments where you use Copilot, such as GitHub.com, the GitHub Copilot app, and an editor such as VS Code): you pay for the tokens processed at the selected model's rate. However, each platform can add other meters, such as GitHub Actions minutes, and offers different models, settings, and governance controls that affect the total cost.

## What a model reads: tokens and context

A **token** is a small piece of text that a model reads or writes. A token can be a whole word, part of a word, a symbol, or a space. Both your input and the model's output count in tokens.

- **Input tokens:** your message, attached files, conversation history, and tool results, at the model's base price.

- **Cached input tokens:** input the model already processed in an earlier request and can reuse. They usually cost about one tenth of the input price.

- **Output tokens:** the text, code, and tests the model writes. They usually cost several times the input price.

Some models also charge for writing to the cache.

A model's **context** is all the information it receives for one request. Context includes much more than the message you type:

- Your written instructions.

- Files, pages, or images you attach.

- Earlier messages in the same conversation.

- An instructions file that the repository keeps for Copilot.

- Descriptions of the tools the agent can use, and the results of those tools.

For each new message in a conversation, Copilot sends the earlier messages again, so a long conversation sends more context with every request. The longer the chat, the more each new message costs, even a short one.

## How tokens become AI credits

On usage-based billing, Copilot measures AI usage in **GitHub AI Credits**. One AI credit equals \$0.01 USD. GitHub counts tokens in each interaction and turns them into credits.

GitHub multiplies each count by the model's price for that kind of token and adds the results to get the cost in US dollars. Then it converts the cost to AI credits and deducts them from your allowance.

An AI credit measures cost, not a number of prompts. A small question can use part of one credit, and a long agent task can use dozens.

Here's a worked example with a model priced at \$2.00 per million input tokens and \$10.00 per million output tokens:

- A request to "summarize this short policy in two sentences" processes 1,000 input and 200 output tokens: \$0.002 + \$0.002 = \$0.004, or **0.4 credits**.

- A request to "review these service requests, find policy exceptions, draft follow-up actions, and check the results" processes 10,000 input and 2,000 output tokens: \$0.02 + \$0.02 = \$0.04, or **4 credits**.

The second request processes ten times more tokens, so it costs ten times more.

> [!NOTE]
> The prices in this module are for illustrative purposes. Check [Models and pricing for GitHub Copilot](https://docs.github.com/copilot/reference/copilot-billing/models-and-pricing) for the latest pricing information.

### Understand GitHub Actions minutes

GitHub Actions minutes measure how long workflows run, separately from AI credits. Beyond the plan allowance, GitHub bills each minute at a rate that depends on the runner's operating system and size, and larger runners cost more. Failed runs and reruns count toward the total. See official [GitHub Actions runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing) for current values.

## Code completions and next edit suggestions

As you type in an **editor**, such as Visual Studio Code (VS Code), Copilot suggests the rest of the line or the next related edit. An editor is an application for opening and changing files. These suggestions don't use AI credits and stay unlimited on paid subscriptions. They also keep working when a budget blocks the features that use credits.

## Copilot code review

GitHub chooses the model for each review and doesn't disclose it, so the cost per review varies. In usage reports, reviews appear on their own line, **Code Review model**. Copilot code review also uses GitHub Actions minutes.

Automatic review triggers can start additional paid reviews, so check both meters before turning them on.

## Options that change the cost of each request

While you work with Copilot, these settings change how much each request costs:

- **Model** (the model menu below the prompt): the price per token, and the quality and speed of the answer.

- **Copilot Fusion** (**Standard**, **High**, or **Max**, in the model menu): Copilot orchestrates multiple models for each request and can combine more than one. Standard provides a balanced approach; High and Max favor deeper reasoning for more demanding tasks. Because each model step contributes to usage, higher tiers can use more AI credits.

- **Reasoning effort** and **context window** (the model menu in the Copilot app): more effort, or a long-context tier, can use more tokens and cost more.

- **Attached context** (the **+** button and the repository selector): changes the amount of input sent.

- **Mode and tool permissions** (the mode menu): how much the agent does on its own, and whether it asks before it runs a tool.

- **Review triggers and effort** (your Copilot settings, **Code review** page): how often and how deeply Copilot reviews pull requests.

If an option doesn't show up:

- **Update the app.** New options reach the latest version of the Copilot app and VS Code first.

- **Check feature availability.** Copilot Fusion tiers and model options can vary by plan, client, rollout, and organization policy. Check [GitHub's current Copilot documentation](https://docs.github.com/en/copilot) for availability and usage details.

- **A policy may hide it.** Organization and enterprise policies can hide models and preview features, and your administrator sets those policies.

## Included usage and additional usage

**Included usage** is the AI credit allowance that comes with your plan. **Additional usage** is any usage beyond that allowance. Additional usage creates charges only while the paid usage setting is enabled.

- **Individual plans** (Copilot Pro, Copilot Pro+, and Copilot Max) come with a monthly allowance. Paid usage beyond the allowance becomes available only after you set a budget for it.

- **Copilot Business and Copilot Enterprise**: each license adds a fixed number of credits to one shared pool every month, and everyone in the organization or enterprise uses credits from that pool. For example, 100 licenses that each add 1,000 credits share a pool of 100,000 credits. An authorized administrator can disable **AI credits paid usage** to prevent charges beyond the included credits.

Allowances differ by plan, and GitHub can change them. Check your plan's current allowance in billing settings. For organization and enterprise billing, see [Usage-based billing for organizations and enterprises](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing).

On individual plans, part of the allowance is a flexible amount that GitHub can change over time. Copilot Free has a smaller allowance and can use models only through Auto.

Unused credits don't carry over. Allowances reset on the first day of each calendar month at 00:00 UTC.

When you run out of credits:

- **On an individual plan**, you can upgrade and pay only the price difference, set a budget to pay for more usage, or wait for the monthly reset.

- **On Copilot Business or Copilot Enterprise**, a banner on GitHub.com lets you request more budget from your administrator.

> [!NOTE]
> If you see "premium requests": before June 1, 2026, Copilot billed **premium requests**, also called **premium request units (PRUs)**. Each interaction counted as one or more requests, depending on a model multiplier. Usage-based billing with AI credits replaced that approach.

You can still see the old terms in older screens and on annual Copilot Pro and Copilot Pro+ plans that still use the old billing system. Model multipliers don't apply to AI credits.
