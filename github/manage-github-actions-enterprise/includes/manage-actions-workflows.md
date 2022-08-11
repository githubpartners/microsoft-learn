Here, you explore the different tools and strategies available to you in GitHub Enterprise Cloud and GitHub Enterprise Server in order to share GitHub actions and workflows and manage their use within your enterprise.

The content is structured around the level at which the tools presented are available: _enterprise level_ or _organizational level_.

## At enterprise level

### Configure a GitHub Actions use policy

GitHub Actions workflows often contain actions, which are sets of standalone commands to be executed within the workflow. When creating a workflow, you can create your own actions to use or reference public community actions available from GitHub Marketplace. For this reason, configuring a use policy for workflows and actions in your enterprise is essential to prevent users from using malicious third-party actions.

Several options are available to you in Enterprise Cloud to configure a policy, as well as in Enterprise Server if GitHub Connect is enabled in your enterprise settings.

To configure a GitHub Actions use policy for your enterprise, navigate to your enterprise account and then to **Policies > Actions** in the sidebar. The options presented below should appear.

:::image type="content" source="../media/policies.png" alt-text="Actions screen with default options selected.":::

The dropdown at the top labeled **Enable for all organizations** enables you to decide which organizations in your enterprise can use GitHub Actions (all of them, some of them or none of them), while the three options underneath enable you to define the restriction level of GitHub Actions within these organizations.

If you want to enable only specific actions to be used within your enterprise, select **Allow select actions** and choose the option corresponding to your use case, as shown below.

:::image type="content" source="../media/policies-2.png" alt-text="Actions screen with Allow select actions option selected.":::

### Share GitHub Actions within your enterprise

You can innersource automation by sharing Actions only within your enterprise without publishing them publicly. You do this by storing the Action in an internal repository and then configure the repository settings to allow access to workflows in other repositories. The other repositories can be in the same organization or other organizations in the enterprise. These Actions can only be used by workflows defined in other private and internal repositories but cannot be used in workflows defined within any public repositories.

### Manually sync public actions for Enterprise Server

Most official GitHub-authored actions come automatically bundled with Enterprise Server, and are captured at a point in time from the GitHub Marketplace. They include `actions/checkout`, `actions/upload-artifact`, `actions/download-artifact`, `actions/labeler` and various `actions/setup-` actions, among others. To see all the official actions included on your enterprise instance, browse to the actions organization on your instance: https://HOSTNAME/actions.

As mentioned in the [Configure a GitHub Actions use policy](#configure-a-github-actions-use-policy) section, it is possible to configure Enterprise Server to automatically access the public actions available in the GitHub Marketplace and to configure a use policy for them. However, if you want stricter control over the public actions that should be made available in your enterprise, you have the possibility to manually download and sync actions into your enterprise instance using the `actions-sync` tool.

### View cache usage

Dependency caching is one of the most effective ways to make jobs faster on GitHub Actions. This gives you greater control over cache availability for your action workflows and monitor the storage usage of your existing caches. Actions users can use actions/cache to speed up their workflow execution times through GitHub's cache usage APIs. Doing so allows you to query the cache usage within each repository and monitor if the total size of all caches is reaching the upper limit of 10 GB. Additionally, you can monitor aggregate cache usage at organization level and at enterprise level, if your GitHub organization is owned by an enterprise account.

## At organization level

### Document corporate standards

Creating a GitHub Actions workflow often involves writing multiple files and creating several repositories to specify the workflow in itself, as well as the actions, containers and/or runners to use in the workflow. Depending on the number of users in your Enterprise Cloud or Enterprise Server instance, things can get messy pretty quickly if you do not have corporate standards in place for creating GitHub Actions workflows.

As a best practice, we recommend you document the following in a GitHub wiki or as a markdown file in a repository accessible to all within an organization:

- Repositories for storage
- Files/folders naming conventions
- Location of shared components
- Plans for ongoing maintenance
- Contribution guidelines

### Create workflow templates

Workflow templates are a great way to ensure automation is reused and maintained in your enterprise. Both in Enterprise Cloud and Enterprise Server, users with write access to an organization's `.github` repository can create workflow templates that will be available for use to the other organization's members with the same write access. Workflow templates can then be used to create new workflows in the public and private repositories of the organization.

Creating a workflow template is done in two steps:

1. Create a `yml` workflow file.
2. Create a `json` metadata file that describes how the template should be presented to users when they are creating a workflow.

    > [!Note]
    > The metadata file must have the same name as the workflow file. Instead of the `.yml` extension, it must be appended with `.properties.json`. For example, a file named `octo-organization-ci.properties.json` contains the metadata for the workflow file named `octo-organization-ci.yml`.

Both files must be placed in a public `.github` repository and in a directory named `workflow-templates`. You might have to create these if they don't already exist in your organization.

Below is an example of a basic workflow file:

```yml
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
      - uses: actions/checkout@v2

      - name: Run a one-line script
        run: echo Hello from Octo Organization
```

Note that the above file uses a `$default-branch` placeholder. When a workflow is created using your template, this placeholder is automatically replaced with the name of the repository's default branch.

Below is the metadata file you would create for the above workflow file:

```json
{
    "name": "Octo Organization Workflow",
    "description": "Octo Organization CI workflow template.",
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

Metadata files use the following parameters:

|   Parameter    |                                                                                                                   Description                                                                                                                   |      Required      |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
|     `name`     |                                                                                   Name of the workflow template displayed in the list of available templates                                                                                    | Yes |
| `description`  |                                                                                Description of the workflow template displayed in the list of available templates                                                                                | Yes |
|   `iconName`   | Defines an icon for the workflow's entry in the template list. Must be an SVG icon of the same name, and must be stored in the `workflow-templates` directory. For example, an SVG file named `example-icon.svg` is referenced as `example-icon`. | Yes |
|  `categories`  |                                      Defines the language category of the workflow. When a user views the available templates, the templates that match the same language will feature more prominently.                                      |        No         |
| `filePatterns` |                                                       Enables the template to be used if the user's repository has a file in its root directory that matches a defined regular expression.                                                       |        No         |

Once a workflow template is created, users in your organization can find it under **Actions > New workflow > Workflows created by _your_organization_name**.

:::image type="content" source="../media/workflow-template.png" alt-text="Workflow template example." border="false":::
