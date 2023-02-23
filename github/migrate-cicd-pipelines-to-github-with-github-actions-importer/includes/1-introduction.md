GitHub Actions Importer is designed to help you forecast, plan, and facilitate migrations from your current CI/CD tool to GitHub Actions. 

Doing individual migrations is relatively easy in isolation. However, if you have a large and established CI/CD footprint, having a tool capable to assist with migrations is key to your ability to adopt GitHub Actions at scale.

## Learning objectives

In this module you will:

- Review how to install the GitHub Actions Importer CLI extension and ensure it's up to date
- Understand the GitHub Actions Importer commands: audit, forecast, dry-run, and migrate as well as learn what cannot be migrated automatically 
- Run through a mock migration lab exercise for one of the supported CI/CD platforms listed below

## Prerequisites

- A GitHub account
- Prior working knowledge of GitHub Actions
- Organizational access to one of the supported CI/CD platforms below 

## Important notes

As you'll learn from this module, you can use GitHub Actions Importer to plan and automatically migrate your CI/CD pipelines to GitHub Actions from the following supported platforms: 

- Azure DevOps
- CircleCI
- GitLab
- Jenkins
- Travis CI

It is imperative to review every workflow that is converted by the GitHub Actions Importer for correctness before using it as a production workload. 

The goal is to achieve an 80% conversion rate for every workflow, but like all things, the actual conversion rate will depend on your specific makeup of your pipelines. 

To set expectations, it is important to note that there are a couple of things that won't be automatically migrated when you use GitHub Actions Importer.

#### What is *not* automatically migrated:

- Secrets and encrypted values 
- Self-hosted build agents
- Historical packages
- Permissions for CI/CD pipelines
- Less commonly used build steps or build triggers

Now, let's dive into how to install GitHub Actions Importer and ensure it is up to date. 