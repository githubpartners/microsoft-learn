In this unit we'll be introducing you to the four commands that GitHub Actions Importer offers. In the following [Lab exercise](https://github.com/actions/importer-labs) you will be provided step by step guidelines on how to run all four commands for each of the supported CI platforms. 

But for now, let's introduce you to the commands of GitHub Importer.

The commands are:

- **Audit**
- **Forecast**
- **Dry-run**
- **Migrate**

In this unit we will be walking through the following:
- [What is the audit command?](https://github.com/githubpartners/microsoft-learn/edit/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#what-is-the-audit-command)
- [What is the forecast command?](https://github.com/githubpartners/microsoft-learn/edit/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#what-is-the-forecast-command)
- [What is the dry-run command?](https://github.com/githubpartners/microsoft-learn/edit/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#what-is-the-dry-run-command)
- [How to run your migration?](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#learn-how-to-migrate-your-environment)
- [What is not automatically migrated?](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/3-How-run-GitHub-Actions-Importer-commands.md#understand-what-is-not-migrated-automatically)

Let's get started with getting to know the ```audit``` command. 

## What is the audit command?
In this section we’ll be going over the basics of the ```audit``` command with GitHub Actions Importer.

The ```audit``` command fetches all of the pipelines defined in a specified scope of the existing CI/CD environment, attempts a conversion of these pipelines to their equivalent workflow, and write a summary report with statistics gathered from the audit. It is designed to help analyze the complexity of a potential migration, which can be used to formulate a migration plan. 

Running an audit on the command line will look something like this:
```
$ gh actions-importer audit jenkins --output-dir 
```

Once you initiate the command it will provide an Audit Summary report.

Let’s go over the details the Audit Summary report will provide you. 

### What is in an Audit summary?

There are four sections of the Audit summary: 

- **Pipelines:** This section contains high-level aggregated statistics on GitHub Actions Importer’s ability to migrate the targeted pipeline automatically.
- **Build steps:** This section presents an aggregated summary of the individual build steps that are used across all of the target pipelines and how many could be converted automatically.
- **Manual tasks:** This section presents an overview of the manual tasks that can be identified.
- **File manifest:** The final section of the audit summary report provides a manifest of all the files generated during the audit. 

:::image type="content" source="../media/Audit_summary.jpg" alt-text="Audit summary for an Jenkins instance with sections of Pipelines and Job types.":::


## What is the Forecast command?

In this section we’ll be reviewing the ```forecast``` command and a rundown of the Forecast report. 

The ```forecast``` command fetches jobs that have been completed over a specified time period and uses that data to calculate usage metrics.

Running a forecast on the command line will look something like the image below. 

:::image type="content" source="../media/Forecast_report.jpg" alt-text="Forecast report for Jenkins with Job count, Pipeline count, Execution time, Queue time, and Concurrent jobs sections.":::


#### What is in a Forecast report?

The Forecast report includes these metrics:

- **Job count:** The total number of completed jobs.
- **Pipeline count:** The number of unique pipelines used.
- **Execution time:** The amount of time a runner spent on a job. This metric can be used to help set expectations for the cost of GitHub-hosted runners.
- **Queue time:** The amount of time a job spent waiting for a runner to be available.
- **Concurrent jobs:** The number of jobs running at any given time. This metric can be used to understand the number of concurrent runners necessary at current levels.

Additionally, these metrics are presented for each runner queue defined in the source CI/CD system. This is useful if you will need a mix of hosted and self-hosted runners and/or if you use a mix of platforms.

In the next section, we’ll be diving into the ```dry-run``` command. 

## What is the dry-run command?

In this section we will review how to use the ```dry-run``` command and provide an example of what the converted workflow will look like. 

You can use the ```dry-run``` command to convert an existing pipeline to its equivalent GitHub Actions workflow. The console output of the command will list the path to the file or files that GitHub Actions Importer generated. Before migrating, you should perform a dry-run of a pipeline and validate the contents are suitable.

If the conversion of a pipeline was only “partially successful” (that is, it included tasks that could not be converted automatically), the task that was not converted will be included in a commented section.

Next up, we'll be tackling how to migrate your environmment. 

## Learn how to migrate your environment 

You can use the ```migrate``` command to convert an existing pipeline to its equivalent action and open a pull request with the converted workflows and associated files.

```
$ gh actions-importer migrate jenkins --source-url $SOURCE_URL –target-url $TARGET_URL --output-dir 
```

Any necessary manual tasks will be included in the description of the pull request. Once these manual tasks and the code reviews are complete, the pull request can be merged and the workflow will have been successfully migrated to GitHub Actions.

:::image type="content" source="../media/PR_for_Migration.jpg" alt-text="New PR once a migration is completed.":::

For specific differences for supported CI platforms please reference the following links:

- [Azure DevOps](https://docs.github.com/en/actions/migrating-to-github-actions/migrating-from-azure-pipelines-to-github-actions)
- [CircleCI](https://docs.github.com/en/actions/migrating-to-github-actions/migrating-from-circleci-to-github-actions)
- [GitLab](https://docs.github.com/en/actions/migrating-to-github-actions/migrating-from-gitlab-cicd-to-github-actions)
- [Jenkins](https://docs.github.com/en/actions/migrating-to-github-actions/migrating-from-jenkins-to-github-actions)
- [Travis CI](https://docs.github.com/en/actions/migrating-to-github-actions/migrating-from-travis-ci-to-github-actions)

Now, let’s take a moment to review and dive a bit deeper into what is not automatically migrated with GitHub Actions Importer. 

## Understand what is not migrated automatically

GitHub Actions Importer cannot migrate everything. It’s important to be mindful of its limitations, which include:

- **Secrets and encrypted values** are not automatically converted to repository secrets. References to secrets will be converted into context expressions and populating these values will be a manual task.
- **Self-hosted build agents** are not automatically converted to self-hosted runners. Determining whether to use GitHub-hosted runners or create equivalent self-hosted - runners will be a manual task. References to these self-hosted runners will be converted to the same set of labels in a needs statement in the resulting workflow.
- **Historical packages** are not migrated to GitHub Packages. Any steps that publish or consume pipeline artifacts and caches will be converted using the equivalent actions.
- **Permissions for CI/CD pipelines** are not migrated automatically and will need to be manually configured.
- **Build steps or build triggers** that are less commonly used may not be automatically converted by GitHub Actions Importer. This can be a factor for migrations involving Azure DevOps, Jenkins, and CircleCI, all of which can be extended through marketplace customizations.

Now let’s check your knowledge on what we just learned!
