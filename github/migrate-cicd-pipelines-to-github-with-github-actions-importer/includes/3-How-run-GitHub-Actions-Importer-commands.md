There are four commands that you can utilize with GitHub Actions Importer to assess, plan, test, and migrate your CI/CD environment into GitHub.

There commands are:

- **Audit**: Fetches all of the pipelines defined in a specified scope of the existing CI/CD environment, attempt a conversion of these pipelines to their equivalent workflow, and write a summary report with statistics gathered from the audit.
- **Forcast**: Fetches jobs that have been completed over a specified time period and uses that data to calculate usage metrics.
- **Dry Run**: Provide existing pipelines with their equivalent GitHub Actions workflow and highlight ones that will need to potentially migrate manually.
- **Migrate**: Convert an existing pipeline to its equivalent action and open a pull request with the converted workflows and associated files

In this unit we will be walking through the following:
- [How to audit your pipelines](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#how-to-audit-your-pipelines)
- [How to run the forecast command](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#how-to-run-the-forecast-commmand)
- [How to run a dry-run migration](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#how-to-execute-a-dry-run-command)
- [How to run your migration](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#learn-how-to-migrate-your-environment)
- [What is not automatically migrated](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#understand-what-is-not-migrated-automatically)

Now let's get started with how to execute an ```audit``` command. 

## How to audit your pipelines
In this section we’ll be going over how to run the ```audit``` command with GitHub Actions Importer and how to interpret your Audit summary. 

### How to run the audit command

GitHub Actions Importer provides an ```audit``` command that is designed to help analyze the complexity of a potential migration, which can be used to formulate a migration plan. This command will fetch all of the pipelines defined in a specified scope of the existing CI/CD environment, attempt a conversion of these pipelines to their equivalent workflow, and write a summary report with statistics gathered from the audit.

Running an audit on the command line will look something like this:
```
$ gh actions-importer audit jenkins --output-dir 
```

Once you initiate the command it will provide an Audit Summary report.

Let’s go over the details the Audit Summary report will provide you. 

### How to interpret your Audit summary

There are 4 sections of the Audit summary: 

- [Pipelines](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#pipelines)
- [Build steps](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#build-steps)
- [Manual tasks](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#manual-tasks)
- [File manifest](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#file-manifest)

Now, let’s break down what each of these sections will provide you and how to interpret the results.

#### Pipelines

This section contains high-level aggregated statistics on GitHub Actions Importer’s ability to migrate the targeted pipeline automatically.

image

The Pipelines section provides the following key metrics:

- **Successful**: identifies the number of pipelines that had all of their constructs and individual items converted automatically to their GitHub Actions equivalent.
- **Partially successful**: identifies the number of pipelines that had all of their constructs converted, however, there were some individual items (for example,build tasks or build triggers) that could not be converted automatically.
- **Unsupported**: identifies the number of pipeline definitions that use constructs that are unsupported by GitHub Actions Importer. Please refer to the platform-specific documentation to learn which pipeline types are supported.
- **Failed**: identifies the number of pipelines where GitHub Actions Importer had a fatal error during an attempt at conversion. This can occur for one of three reasons:
  - The pipeline was misconfigured and not valid in its existing CI/CD platform.
  - GitHub Actions Importer encountered an internal error when converting it.
  - There was an unsuccessful network response, often due to invalid credentials, that caused the pipeline to be inaccessible.

The **Job types** section summarizes which pipeline types are being used and whether they are supported or unsupported. Please refer to the platform-specific documentation to learn which pipeline types are supported.

Next, let’s go over Build steps.

#### Build steps

This section presents an aggregated summary of the individual build steps that are used across all of the target pipelines and how many could be converted automatically.

image

The Build steps section provides the following details:

- A known build step is one that GitHub Actions Importer can automatically convert to an equivalent action.
- An unknown build step is one that cannot be automatically converted to an equivalent action.
- An unsupported build step is either:
  - Fundamentally not supported by GitHub Actions.
  - Configured in a way that is incompatible with GitHub Actions.
- Actions provides a comprehensive list of actions that would be used in all of the converted workflows. This is important in these scenarios:
  - When you are migrating to GHES and need to sync these actions to your GHES instance.
  - When you are defining an organization-level allowlist.
  - When you need to provide a comprehensive list of actions for your security and/or compliance teams to review and approve.
- In addition, the audit summary report includes an equivalent summary of build triggers, environment variables, and other uncategorized items.

Next up, we’ll cover the Manual tasks section. 

#### Manual tasks

This section presents an overview of the manual tasks that can be identified.

image

The Manual tasks section can provide the following details:
- Secrets includes a summarized list of the secrets used in the converted pipelines. Because secrets cannot be migrated automatically, they will need to be created manually in order for these workflows to function properly.
- Self-hosted runners summarizes and identifies the labeled runners referenced in the source pipelines. You will need to decide whether a GitHub-hosted or self-hosted runner is appropriate to run these workflows within GitHub Actions.

Next, to round things out, we’ll discuss the File manifest.

#### File manifest

The final section of the audit summary report provides a manifest of all the files generated during the audit. These files can include:
- The original pipeline as it was defined in the source CI/CD platform.
- A log of the network responses used to convert a pipeline.
- The converted workflow file(s).
- A log of any error messages to troubleshoot a failed pipeline conversion.

In the next section we’ll be going over the ```Forecast``` command.

## How to run the forecast commmand

In this section we’ll be reviewing how to run the ```forecast``` command and a rundown of the Forecast report. 

### How to run the forecast command

The ```forecast``` command is designed to help you understand the compute capacity you’re currently using within your CI/CD environment. This command fetches jobs that have been completed over a specified time period and uses that data to calculate usage metrics.

Running a forecast on the command line will look something like this:
```
$ gh actions-importer audit jenkins –start-date 7/1/22 --output-dir  
```

Image 

#### What is in a Forecast report?

The Forecast report includes these metrics:

- Job count: the total number of completed jobs.
- Pipeline count: the number of unique pipelines used.
- Execution time: the amount of time a runner spent on a job. This metric can be used to help set expectations for the cost of GitHub-hosted runners.
- Queue time: the amount of time a job spent waiting for a runner to be available.
- Concurrent jobs: the number of jobs running at any given time. This metric can be used to understand the number of concurrent runners necessary at current levels.

Additionally, these metrics are presented for each runner queue defined in the source CI/CD system. This is useful if you will need a mix of hosted and self-hosted runners and/or if you use a mix of platforms.

In the next section, we’ll be diving into how to utilize the ```dry-run``` command. 

## How to execute a dry-run command

In this section we will review how to use the ```dry-run``` command and provide an example of what the converted workflow will look like. 

### How to run a dry-run command 

You can use the ```dry-run``` command to convert an existing pipeline to its equivalent GitHub Actions workflow. The console output of the command will list the path to the file or files that GitHub Actions Importer generated. Before migrating, you should perform a dry run of a pipeline and validate the contents are suitable.

If the conversion of a pipeline was only “partially successful” (that is, it included tasks that could not be converted automatically), the task that was not converted will be included in a commented section. For example, if you were to run the following CLI command:

```
$ gh actions-importer dry-run jenkins --source-url $SOURCE_URL --output-dir 
```

### An example of the converted workflow 

```
name: ethanis/universe
on:
  workflow_dispatch:
jobs:
  Build:
    runs-on:
      - self-hosted
      - main
    steps:
    - name: checkout
      uses: actions/checkout@v3
#     # This item has no matching transformer
#     - buildJavascriptApp:
#       - key: deploy
#         value:
#           isLiteral: true
#           value: false’ 
```

In this situation, you will need to decide how to implement this functionality. If this task is used within multiple pipelines, the recommended approach is to implement a custom transformer that can handle this scenario in every pipeline. If this is a one-off scenario, you can edit the converted workflow file manually.
Let’s assume in this example that the buildJavascriptApp build step is used in multiple workflows and could be easily replicated with a single shell command. This is what that custom transformer would look like:

```
transform “buildJavascriptApp” do |item|
  {
    name: “Build Javascript App”,
    run: “npm install && npm run build”
  }
End
```

If you were to add these contents to a file named transformers.rb, they can be provided to GitHub Actions Importer on the command line. For example:

```
$ gh actions-importer dry-run jenkins --source-url $SOURCE_URL --output-dir --custom-transformers transformers.rb
```

In the next section, we’ll provide the command line for migration and provide other resources for specific CIs. 

## Learn how to migrate your environment 

You can use the migrate command to convert an existing pipeline to its equivalent action and open a pull request with the converted workflows and associated files.

```
$ gh actions-importer migrate jenkins --source-url $SOURCE_URL –target-url $TARGET_URL --output-dir 
```

Any necessary manual tasks will be included in the description of the pull request. Once these manual tasks and the code reviews are complete, the pull request can be merged and the workflow will have been successfully migrated to GitHub Actions.

image

For specific differences for supported CI platforms please reference the following links:

- Azure DevOps
- CircleCI
- GitLab
- Jenkins
- Travis CI

Now let’s take a moment to review what is not automatically migrated. 

## Understand what is not migrated automatically

GitHub Actions Importer cannot migrate everything. It’s important to be mindful of its limitations, which include:

- Secrets and encrypted values are not automatically converted to repository secrets. References to secrets will be converted into context expressions and populating these values will be a manual task.
- Self-hosted build agents are not automatically converted to self-hosted runners. Determining whether to use GitHub-hosted runners or create equivalent self-hosted - runners will be a manual task. References to these self-hosted runners will be converted to the same set of labels in a needs statement in the resulting workflow.
- Historical packages are not migrated to GitHub Packages. Any steps that publish or consume pipeline artifacts and caches will be converted using the equivalent actions.
- Permissions for CI/CD pipelines are not migrated automatically and will need to be manually configured.
- Build steps or build triggers that are less commonly used may not be automatically converted by GitHub Actions Importer. This can be a factor for migrations involving Azure DevOps, Jenkins, and CircleCI, all of which can be extended through marketplace customizations.

Now let’s check your knowledge on what we just learned!
