Here you'll learn about GitHub Actions workflow triggers. Workflow triggers are events that cause a workflow to run. 

## Trigger a GitHub Actions workflow

Workflow triggers are events that cause a workflow to run. These events include the following.

- Events that occur in your workflow's repository
- Events that occur outside of GitHub and trigger a `repository_dispatch event` on GitHub
- Scheduled times
- Manual

### Events in your workflow's repository

You can configure your workflow to run when a push is made to the default branch of your repository, when a release is created, or when an issue is opened. Workflow triggers are defined with the `on` key.

Use the following steps to trigger a workflow run.

1. An event occurs on your repository. The event has an associated commit SHA and Git ref
2. GitHub searches the `.github/workflows` directory in your repository for workflow files that are present in the associated commit SHA or Git ref of the event
3. A workflow run is triggered for any workflows that have `on:` values that match the triggering event. Some events also require the workflow file to be present on the default branch of the repository in order to run

Each workflow run uses the version of the workflow that is present in the associated commit SHA or Git ref of the event. When a workflow runs, GitHub sets the `GITHUB_SHA` (commit SHA) and `GITHUB_REF` (Git ref) environment variables in the runner environment.

### Available events and activity types

Some events have multiple activity types. For these events, you can specify which activity types will trigger a workflow run.

`branch_protection_rule`: Runs your workflow when branch protection rules in the workflow repository are changed. Activity types include.

- created
- edited
- deleted

For example, you can run a workflow when a branch protection rule has been `created` or `deleted`:

```
on:
  branch_protection_rule:
    types: [created, deleted]
```

`fork`: Runs your workflow when someone forks a repository. The activity types are N/A.

For example, you can run a workflow when the `fork` event occurs:

```
on:
  forkon:
  fork
```

`issues`: Runs your workflow when an issue in the workflow's repository is created or modified. Activity types include.

- opened
- edited
- deleted
- transferred
- pinned
- unpinned
- closed
- reopened
- assigned
- unassigned
- labeled
- unlabeled
- locked
- unlocked
- milestoned
- demilestoned

For example, you can run a workflow when an issue has been `opened`, `edited`, or `milestoned`:

```
on:
  issues:
    types: [opened, edited, milestoned]
```

`workflow run`: This event occurs when a workflow run is requested or completed. The event allows you to execute a workflow based on execution or completion of another workflow. The workflow started by the `workflow_run` event can access secrets and write tokens, even if the previous workflow could not. This is useful in cases where the previous workflow is intentionally not privileged, and now you need to take a privileged action in a later workflow.

For example, a workflow is configured to run after the separate *Run Tests* workflow completes:

```
on:
  workflow_run:
    workflows: [Run Tests]
    types:
      - completed
 ```
 
### Use filters

Some events have filters that give you more control over when your GitHub Actions workflow should run. The `push` event has a `branches` filter that causes your workflow to run only when a push to a branch that matches the `branches` filter occurs, instead of when any push occurs.

For example:

```
on:
  push:
    branches:
      - main
      - 'releases/**'
```

You can use filters to target specific branches for pull request events. You can use the `pull_request` and `pull_request_target events` to configure a workflow to run only for pull requests that target specific branches. The `branches` filter can be used to include branch name patterns or when you want to both include and exclude branch names patterns. You can use the `branches-ignore` filter when you only want to exclude branch name patterns. You cannot use both the `branches` and `branches-ignore` filters for the same event in a workflow.

The patterns defined in `branches` are evaluated against the Git ref's name. For example, the following workflow would run whenever there is a `pull_request` event for a pull request targeting.

```
on:
  pull_request:
    # Sequence of patterns matched against refs/heads
    branches:    
      - main
      - 'mona/octocat'
      - 'releases/**'
```

### Manually triggered workflows

When using the `workflow_dispatch` event, you can optionally specify inputs that are passed to the workflow. The triggered workflow receives the inputs in the `inputs` context.

For example:

```
on:
  workflow_dispatch:
    inputs:
      logLevel:
        description: 'Log level'
        required: true
        default: 'warning' 
        type: choice
        options:
        - info
        - warning
        - debug 
      print_tags:
        description: 'True to print to STDOUT'
        required: true 
        type: boolean 
      tags:
        description: 'Test scenario tags'
        required: true 
        type: string
      environment:
        description: 'Environment to run tests against'
        type: environment
        required: true 

jobs:
  print-tag:
    runs-on: ubuntu-latest
    if:  ${{ inputs.print_tags }} 
    steps:
      - name: Print the input tag to STDOUT
        run: echo  The tags are ${{ inputs.tags }} 
```

### Further control how your workflow will run



We'll cover reusing workflows in the next unit.

<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->

<!-- Do not add a unit summary or references/links -->
