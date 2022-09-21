Here you'll learn about GitHub Actions workflow triggers. Workflow triggers are events that cause a workflow to run. 

## Trigger a GitHub Actions workflow

Workflow triggers are events that cause a workflow to run. These events include the following.

- Events that occur in your workflow's repository
- Events that occur outside of GitHub and trigger a `repository_dispatch event` on GitHub
- Scheduled times
- Manual

### Events in your workflow's repository

You can configure your workflow to run when a push is made to the default branch of your repository, when a release is created, or when an issue is opened. Workflow triggers are defined with the `on` key.

Here are steps to trigger a workflow run.

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

When using the `workflow_dispatch` event, you have the option to specify inputs that are passed to the workflow. The triggered workflow receives the inputs in the `inputs` context.

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

### More workflow control

Looking for more granular control than what events, event activity types, or event filters provide? Using conditionals and environments give you more control over individual jobs or steps in your workflow.

Conditionals will further control whether jobs or steps in your workflow will run. For example, if you want the workflow to run when a specific label is added to an issue, you can trigger on the `issues labeled` event activity type and use a conditional to check what label triggered the workflow. The following workflow will run when any label is added to an issue in the workflow's repository, but the `run_if_label_matches` job will only execute if the label is named bug.

```
on:
  issues:
    types:
      - labeled

jobs:
  run_if_label_matches:
    if: github.event.label.name == 'bug'
    runs-on: ubuntu-latest
    steps:
      - run: echo 'The label was bug'
```

The following steps will give you the ability to use an environment that requires approval from a specific team or user to manually trigger a specific job in a workflow.

1. Configure an environment with required reviewers
2. Reference the environment name in a job in your workflow using the `environment:` key. Any job referencing the environment will not run until at least one reviewer approves the job

For example, the following workflow will run whenever there is a push to main. The `build` job will always run. The `publish` job will only run after the `build` job successfully completes (due to `needs: [build]`) and after all of the rules (including required reviewers) for the environment called `production` pass (due to `environment: production`).

```
on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: build
        echo 'building'

  publish:
    needs: [build]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: publish
        echo 'publishing'
```

You can use a conditional to check whether a specific event type exists in the event context. Use this if you want to run different jobs or steps depending on what event triggered the workflow.

For example, the following workflow will run whenever an issue or pull request is closed. If the workflow ran because an issue was closed, the `github.event` context will contain a value for `issue` but not for `pull_request`. Therefore, the `if_issue` step will run but the `if_pr` step will not run. Conversely, if the workflow ran because a pull request was closed, the `if_pr` step will run but the `if_issue` step will not run.

```
on:
  issues:
    types:
      - closed
  pull_request:
    types:
      - closed

jobs:
  state_event_type:
    runs-on: ubuntu-latest
    steps:
    - name: if_issue
      if: github.event.issue
      run: |
        echo An issue was closed
    - name: if_pr
      if: github.event.pull_request
      run: |
        echo A pull request was closed
```

We'll cover reusing workflows in the next unit.
