:::image type="content" source="../media/github.png" alt-text="An image of the GitHub logo with circles in the background":::

GitHub Actions Importer is designed to help you forecast, plan, and facilitate migrations from your current CI/CD tool to GitHub Actions. Doing individual migrations is relatively easy in isolation. However, if you have a large and established CI/CD footprint, having tooling available to assist with migrations is key to your ability to adopt GitHub Actions at scale.

You can use GitHub Actions Importer to plan and automatically migrate your CI/CD pipelines to GitHub Actions from Azure DevOps, CircleCI, GitLab, Jenkins, and Travis CI.

Any workflow that is converted by the GitHub Actions Importer should be inspected for correctness before using it as a production workload. The goal is to achieve an 80% conversion rate for every workflow, however, the actual conversion rate will depend on the makeup of each individual pipeline that is converted.

## Learning objectives

In this module you will:

- Review how to install the GitHub Actions Importer CLI Extension, ensure it's up-to-date, and learn about supported CI platforms
- Comprehend how to execute the audit, forecast, dry-run, and migrate commands and learn what is not automatically migrated

## Prerequisites:

- You must have been granted access to the public preview for the GitHub Actions Importer
- You must have credentials to authenticate to the GitHub Packages Container registry. For more information, see "Working with the Container registry"
- An environment where you can run Linux-based containers, and can install the necessary tools
    - Docker is installed and running
    - GitHub CLI is installed
