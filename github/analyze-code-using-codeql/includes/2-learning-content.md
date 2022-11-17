As a developer, you can perform code scanning externally and then display the results in GitHub. Alternatively, you can set up webhooks that listen to code scanning activity in your repository.

In this unit, you'll learn about:

- Integrate with code scanning: perform analysis elsewhere and upload the code scanning results to GitHub
- Integrate with webhooks: build or set up integrations that subscribe to code scanning events in your repository
- Use partner integrations: discover and configure GitHub Actions workflow templates

## Integrate with code scanning

You can perform analysis elsewhere and then upload the code scanning results to GitHub. The alerts for code scanning that you run externally are displayed in the same way as those for code scanning that you run within GitHub. When you use a third-party static analysis tool that can produce results as Static Analysis Results Interchange Format (SARIF) 2.1.0 data, you can upload the results to GitHub.

You can view the status of the alert for each analysis origin on the alert page if an alert has multiple analysis origins. This occurs when you run code scanning using multiple configurations.

## Integrate with webhooks

You can use code scanning webhooks to build or set up integrations that subscribe to code scanning events in your repository, such as GitHub Apps or OAuth Apps. For example, you could build an integration that creates an issue on GitHub or sends you a Slack notification when a new code scanning alert is added in your repository.

### Set up a webhook

You can install webhooks on an organization or on a specific repository. To set up a webhook, go to the settings page of your repository or organization. Then, click ***Webhooks***, then ***Add webhook***.

Webhooks require a few configuration options before you can make use of them. These webhooks settings include: payload URL, content type, secret, SSL verification, active, and events.

## Use partner integrations

You can discover and configure GitHub Actions workflow templates for partner integrations straight from their repository's **Actions** tab under a category called **Security**. Workflows are recommended based on the repository's content. GitHub suggests analysis engines that are compatible with the source code in your repository.

    <!-- @a-a-ron add image here: 
    https://github.blog/changelog/2022-02-22-discover-code-scanning-partner-integrations-on-the-github-actions-tab/
    The security image from the page link above.
    -->

Code scanning and GitHub's CodeQL analysis engine are freely available for public repositories. Analysis engines and services provided by partners might require a subscription. Additionally, you can configure code scanning for organization-owned private repositories when GitHub Advanced Security (GHAS) is enabled.

Next up, you will learn how to set up code scanning with GitHub Actions and how to perform bulk setup of code scanning for multiple repositories.
