Here, you'll learn some common configurations within a workflow file. You'll also explore the categories of event types, disabling and deleting workflows, and using specific versions of an action for security best practices. 

## Configure workflows to run for scheduled events

As mentioned previously, you can configure your workflows to run when specific activity occurs on GitHub, when an event outside of GitHub happens, or at a scheduled time. The `schedule` event allows you to trigger a workflow to run at specific UTC times using [POSIX cron syntax](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07). This cron syntax has five `*` fields, and each field represents a unit of time.

:::image type="content" source="../media/scheduled-events.png" alt-text="Image showing the five unit-of-time fields for scheduling an event in a workflow file." border="false":::

For example, if you wanted to run a workflow every 15 minutes, the `schedule` event would look like the following:

```yml
on:
  schedule:
    - cron:  '*/15 * * * *'
```

And if you wanted to run a workflow every Sunday at 3:00am, the `schedule` event would look like this:


```yml
on:
  schedule:
    - cron:  '0 3 * * SUN'
```

You can also use operators to specify a range of values or to dial in your scheduled workflow. The shortest interval you can run scheduled workflows is once every five minutes, and they run on the latest commit on the default or base branch.

## Configure workflows to run for manual events

In addition to scheduled events, you can manually trigger a workflow by using the `workflow_dispatch` event. This event allows you to run the workflow using the GitHub REST API or by selecting the **Run workflow** button in the **Actions** tab within your repository on GitHub. Using `workflow_dispatch`, you can choose on which branch you want the workflow to run, as well as set optional `inputs` that GitHub will present as form elements in the UI.

```yml
on:
  workflow_dispatch:
    inputs:
      logLevel:
        description: 'Log level'     
        required: true
        default: 'warning'
      tags:
        description: 'Test scenario tags'  
```

In addition to `workflow_dispatch`, you can use the GitHub API to trigger a webhook event called `repository_dispatch`. This event allows you to trigger a workflow for activity that occurs outside of GitHub, and essentially serves as an HTTP request to your repository asking GitHub to trigger a workflow off an action or webhook. Using this manual event requires you to do two things: send a `POST` request to the GitHub endpoint `/repos/{owner}/{repo}/dispatches` with the webhook event names in the request body, and configure your workflow to use the `repository_dispatch` event.

```bash
curl \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/octocat/hello-world/dispatches \
  -d '{"event_type":"event_type"}'
```

```yml
on:
  repository_dispatch:
    types: [opened, deleted]
```

## Configure workflows to run for webhook events

Lastly, you can configure a workflow to run when specific webhook events occur on GitHub. Most webhook events can be triggered from more than one activity for a webhook, so if multiple activities exist for a webhook, you can specify an activity type to trigger the workflow. For example, you can run a workflow for the `check_run` event but only for the `rerequested` or `requested_action` activity types.

```yml
on:
  check_run:
    types: [rerequested, requested_action]
```

## Use conditional keywords

Within your workflow file, you can access context information and evaluate expressions. Although expressions are commonly used with the conditional `if` keyword in a workflow file to determine whether a step should run or not, you can use any supported context and expression to create a conditional. It's important to know that when using conditionals in your workflow, you need to use the specific syntax `${{ <expression> }}`, which tells GitHub to evaluate an expression rather than treat it as a string.

For example, a workflow that uses the `if` conditional to check if the `github.ref` (the branch or tag ref that triggered the workflow run) matches `refs/heads/main` in order to proceed with the following steps in the workflow would look something like this:

```yml
name: CI
on: push
jobs:
  prod-check:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      ...
```

Notice that in this example, the `${{ }}` are missing from the syntax. With some expressions, as in the case of the `if` conditional, you may omit the expression syntax. GitHub automatically evaluates some of these common expressions, but you can always include them in case you forget which expressions GitHub automatically evaluates.

For more information about workflow syntax and expressions, check out [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idstepsif).


## Disable and delete workflows

After adding a workflow to your repository, you may find a situation where you want to temporarily disable the workflow. You can stop a workflow from being triggered without having to delete the file from the repo, either on GitHub or through the GitHub REST API. When you wish to enable the workflow again, you can easily do it using the same methods.

:::image type="content" source="../media/disable-workflow.png" alt-text="Picture of disabling a workflow on GitHub.":::

Disabling a workflow can be useful in some situations, for example:

- An error on a workflow is producing too many or wrong requests impacting external services negatively.
- You want to temporarily pause a workflow that is not critical and is consuming too many minutes on your account.
- You want to pause a workflow that is sending requests to a service that is down.
- You are working on a fork and you don't need all the functionality of some workflows it includes (like scheduled workflows).

You can also cancel a workflow run that is in progress in the GitHub UI from the **Actions** tab or using the GitHub API endpoint `DELETE /repos/{owner}/{repo}/actions/runs/{run_id}`. Keep in mind that when you cancel a workflow run, GitHub will cancel all of its jobs and steps within that run.

## Use an organization's templated workflow

If you have a workflow that multiple teams use within an organization, instead of re-creating the same workflow for each repository, you can promote consistency across your organization by using a workflow template that's defined in the organization's `.github` repository. Any member within the organization can use an organization template workflow, and any repository within that organization has access to those template workflows.

You can find these workflows by navigating to the **Actions** tab of a repository within the organization, selecting **New workflow**, and then finding the organization's workflow template section titled "Workflows created by *organization name*". For example, the organization called Mona has a template workflow as shown below.

:::image type="content" source="../media/mona-workflow.png" alt-text="Picture of a template organization workflow called greet and triage by Mona.":::

## Use specific versions of an action

When referencing actions in your workflow, we recommended that you refer to a specific version of that action rather than just the action itself. By referencing a specific version, you are placing a safeguard from unexpected changes pushed to the action that could potentially break your workflow. Below are several ways you can reference a specific version of an action.

```yml
steps:    
  # Reference a specific commit
  - uses: actions/setup-node@c46424eee26de4078d34105d3de3cc4992202b1e
  # Reference the major version of a release
  - uses: actions/setup-node@v1
  # Reference a minor version of a release
  - uses: actions/setup-node@v1.2
  # Reference a branch
  - uses: actions/setup-node@main
```

Some references are safer than others. For example, referencing a specific branch will run that action off of the latest changes from that branch, which you may or may not want. By referencing a specific version number or commit SHA hash, you're being more specific about the version of the action you're running. For more stability and security, we recommend that you use the commit SHA of a released action within your workflows. 

## Prevent GitHub Actions from creating and approving pull requests

To further reduce the risk of a user using Actions to merge a change into a protected branch that was not reviewed by another person, the organization setting to disallow Actions from approving pull requests has been extended to also limit Actions from creating pull requests. The Allow GitHub Actions to create and approve pull requests setting can be managed by admins in organization settings under **Actions** > *General* > *Workflow permissions*.

## Helping maintainers

One of the best things about GitHub Actions is that it gives developers the ability to automate all of their software workflows. Unfortunately, as GitHub Actions has grown, there has been a wide variety of bad actors abusing Actions, affecting service performance, and causing denial of service to open source projects. 

To help prevent this, GitHub has made two changes to how they treat pull requests from public forks in Actions to help maintainers.

- First, if GitHub determines an Actions run to be abusive or against our terms, GitHub's enforcement will be directed at the account hosting the fork and not the account associated with the upstream repository. The result of this process is to prevent maintainer accounts from being flagged and blocked due to these bad actors. 

- Second, pull requests from first-time contributors require manual approval from a repository collaborator with write access before any Actions workflows run. A first-time contributor will see a message that a maintainer must approve their Actions workflow when they opens a pull request before it will run. After a collaborator with write access has reviewed the changes, they can approve the workflows to run for the current commit only. If the pull request is updated to a new commit, a new approval will be required. These steps are a good balance between manual approval and existing automated workflows.
