Here, you'll learn the basics about creating, using, and sharing GitHub Actions workflows.

## Create a GitHub Actions workflow

Workflows can be created by users with *write* access to the organization's `.github` repository. Those workflows can then be used by organization members who have permission to create workflows. Workflows created by users can only be used to create workflows in public repositories. Organizations using GitHub Enterprise Cloud can also use workflows to create workflows in private repositories.

Use these steps to create a starter workflow and metadata file. The metadata file describes how the starter workflows will be presented to users when they are creating a new workflow.
1. Create a new public repository named `.github` in your organization, if it doesn't already exist
2. Create a directory named `workflow-templates`
3. Create your new workflow file inside the `workflow-templates` directory

You can use the `$default-branch` placeholder to refer to a repository's default branch. When a workflow is created, the placeholder will be automatically replaced with the name of the repository's default branch.

For example, this file named `octo-organization-ci.yml` demonstrates a basic workflow.

```
name: Octo Organization CI

on:
  push:
    branches: [ $default-branch ]
  pull_request:
    branches: [ $default-branch ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run a one-line script
        run: echo Hello from Octo Organization
```

4. Create a metadata file inside the `workflow-templates` directory
  - The metadata file must have the same name as the workflow file, but instead of the `.yml extension` it must be appended with `.properties.json`

For example, this file named `octo-organization-ci.properties.json` contains the metadata for a workflow file named `octo-organization-ci.yml`.

```
{
    "name": "Octo Organization Workflow",
    "description": "Octo Organization CI starter workflow.",
    "iconName": "example-icon",
    "categories": [
        "Go"
    ],
    "filePatterns": [
        "package.json$",
        "^Dockerfile",
        ".*\\.md$"
    ]
}
```

- `name` - Required: is the name of the workflow and is displayed in the list of available workflows
- `description` - Required: is the description of the workflow and is displayed in the list of available workflows
- `iconName` - Optional: specifies an icon for the workflow that is displayed in the list of workflows. The `iconName` must be the name of an SVG file, without the file name extension, stored in the `workflow-templates` directory
- `categories` - Optional: defines the language category of the workflow. When a user views the available starter workflows for a repository, the workflows that match the identified language for the project are featured more prominently
- `filePatterns` - Optional: allows the workflow to be used if the user's repository has a file in its root directory that matches a defined regular expression

### Add an action to your workflow

You can add an action to your workflow by referencing the action in your workflow file. Additionally, you can view the actions referenced in your GitHub Actions workflows as dependencies in the dependency graph of the repository containing your workflows.

Example repository file structure to add an action from the same repository:

```
|-- hello-world (repository)
|   |__ .github
|       └── workflows
|           └── my-first-workflow.yml
|       └── actions
|           |__ hello-world-action
|               └── action.yml
```

Example workflow file:

```
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # This step checks out a copy of your repository.
      - uses: actions/checkout@v3
      # This step references the directory that contains the action.
      - uses: ./.github/actions/hello-world-action
```

The `action.yml` file is used to provide metadata for the action.

## Use a GitHub Actions workflow

When you set up workflows in your repository, GitHub analyzes the code in your repository and recommends workflows based on the language and framework in your repository. If an action is defined in the same repository where your workflow file uses the action, you can reference the action with either the ‌`{owner}/{repo}@{ref}` or `./path/to/dir` syntax in your workflow file.

GitHub provides ready-to-use workflows for the following high level categories:

- Deployment (CD)
- Security
- Continuous Integration (CI)
- Automation
  - Automation workflows offer solutions for automating workflows, such as triaging pull requests and applying a label based on the paths that are modified in the pull request, or greeting users who are first time contributors to the repository

You can also create your own workflows to share with your organization. These workflows will appear alongside the GitHub-provided workflows.

Anyone with write permission to a repository can set up GitHub Actions starter workflows for CI/CD or other automation.
1. On GitHub.com, navigate to the main page of the repository
2. Under your repository name, click **Actions**
3. Click **New workflow**
4. The *Choose a workflow* page shows a selection of recommended workflows. Find the workflow that you want to use, then click **Configure**
  - If the workflow contains comments detailing additional setup steps, follow these steps. Many of the workflow have corresponding guides
  - Some workflows use secrets. For example, `${{ secrets.npm_token }}`. If the workflow uses a secret, store the value described in the secret name as a secret in your repository
  - Optionally, make additional changes. For example, you might want to change the value of `on` to change when the workflow runs
5. Click **Start commit**
6. Write a commit message and decide whether to commit directly to the default branch or to open a pull request

## Share a GitHub Actions workflow

You can create starter workflows in the .github repository and share them with other users in your organization. Your organization can also share workflows by reusing the workflows exactly or by creating workflows that provide templates for new workflows.

We'll cover how to trigger a workflow in the next unit.

<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->

<!-- Do not add a unit summary or references/links -->
