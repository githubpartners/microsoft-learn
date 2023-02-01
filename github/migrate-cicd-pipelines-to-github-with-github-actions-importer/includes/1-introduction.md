GitHub Actions Importer is designed to help you forecast, plan, and facilitate migrations from your current CI/CD tool to GitHub Actions. Doing individual migrations is relatively easy in isolation. However, if you have a large and established CI/CD footprint, having tooling available to assist with migrations is key to your ability to adopt GitHub Actions at scale.

You can use GitHub Actions Importer to plan and automatically migrate your CI/CD pipelines to GitHub Actions from these supported platforms below. We will be diving deeper into each specific CI platform in the exercise later in the module, but here are the links to them for reference. 

- [Azure DevOps](https://github.com/valet-customers/labs/blob/main/azure_devops/readme.md)
- [CircleCI](https://github.com/valet-customers/labs/blob/main/circle_ci/readme.md)
- [GitLab](https://github.com/valet-customers/labs/blob/main/gitlab/readme.md)
- [Jenkins](https://github.com/valet-customers/labs/blob/main/jenkins/readme.md)
- [Travis CI](https://github.com/valet-customers/labs/blob/main/travis/readme.md)

It is imperative to review every workflow that is converted by the GitHub Actions Importer for correctness before using it as a production workload. 

The goal is to achieve an 80% conversion rate for every workflow, but like all things, the actual conversion rate will depend on your specific makeup of your  pipelines. 

To set expectations it is important to note that there are a couple of things that won't be autmatically migrated when you use GitHub Actions Importer.

#### What is not automatically migrated

- Secrets and encrypted values 
- Self-hosted build agents
- Historical packages
- Permissions for CI/CD pipelines
- Build steps or build triggers

We'll dive deeper into this in the module, for now let's review the learning objectives for this module.

## Learning objectives

In this module you will:

- Review how to install the GitHub Actions Importer CLI Extension, ensure it's up-to-date, and learn about supported CI platforms
- Comprehend how to execute the audit, forecast, dry-run, and migrate commands and learn what is not automatically migrated

## Prerequisites:

- You must have credentials to authenticate to the GitHub Packages Container registry. For more information, see "Working with the Container registry"
- An environment where you can run Linux-based containers, and can install the necessary tools
    - Docker is installed and running
    - GitHub CLI is installed
