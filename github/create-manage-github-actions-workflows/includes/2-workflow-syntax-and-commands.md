Understanding your workflow can seem challenging at first. In this unit, you'll learn more about the YAMl syntax and some common workflow commands.

## YAML syntax for workflows

Workflow files use YAML syntax, and must have either a `.yml` or `.yaml` file extension. You need to store workflow files in the `.github/workflows` directory of your repository.

To automatically trigger a workflow, use `on` to define which events can cause the workflow to run. You can define single or multiple events that can trigger a  workflow, or set a time schedule.

A workflow with the following `on` value will run when a push is made to any branch in the workflow's repository:

```
on:push
```

A workflow with the following `on` value will run when a push is made to any branch in the repository or when someone forks the repository:

```
on: [push, fork]
```

If you specify multiple events, only one of those events needs to occur to trigger your workflow.

### Activity types

![activity-types](https://user-images.githubusercontent.com/6351798/193733579-5140c49b-c183-4049-a604-be5f9ed1d703.png)

Some events have activity types that give you more control over when your workflow should run. Use `on.<event_name>.types` to define the type of event activity that will trigger a workflow run. If your workflow triggers on the `label` event, it will run whenever a label is `created`, `edited`, or `deleted`. If you specify the `created` activity type for the `label` event, your workflow will run when a label is created but not when a label is edited or deleted.

```
on:
  label:
    types:
      - created
```

If you specify multiple activity types, only one event activity type needs to occur to trigger your workflow. If multiple triggering event activity types occur at the same time, multiple workflow runs will be triggered. The following workflow triggers when an issue is opened or labeled. If an issue with two labels is opened, three workflow runs will start: one for the issue opened event and two for the two issue labeled events.

```
on:
  issues:
    types:
      - opened
      - labeled
```

When using the `pull_request` and `pull_request_target` events, you can configure a workflow to run only for pull requests that target specific branches. Use the `branches` filter when you want to include branch name patterns or when you want to both include and exclude branch names patterns. Use the `branches-ignore` filter when you only want to exclude branch name patterns. You cannot use both the `branches` and `branches-ignore` filters for the same event in a workflow.

The patterns defined in `branches` are evaluated against the Git ref's name. The following workflow would run whenever there is a `pull_request` event for a pull request targeting:

- A branch named `main` (`refs/heads/main`)
- A branch named `mona/octocat` (`refs/heads/mona/octocat`)
- A branch whose name starts with `releases/`, like `releases/10` (`refs/heads/releases/10`)

```
on:
  pull_request:
    # Sequence of patterns matched against refs/heads
    branches:    
      - main
      - 'mona/octocat'
      - 'releases/**'
```

### On schedule

If you want to define a time schedule for your workflows, you can use the `on.schedule` event type. Scheduled workflows run on the latest commit on the default or base branch. The shortest interval you can run scheduled workflows is once every 5 minutes. This is done by using POSIX cron syntax to run at specific UTC times. The below example will trigger the workflow to run every day at 5:30 and 17:30 UTC:

```
on:
  schedule:
    # * is a special character in YAML so you have to quote this string
    - cron:  '30 5,17 * * *'
 ```
 
## Workflow commands

Creating a workflow is simple as long as you can find the right actions for your steps. In some cases you may need to create your own actions to achieve your desired outcomes, but you can use workflow commands to add another level of customization to your workflows.

Workflow commands enable you to communicate with the GitHub Actions runner machine by printing formatted lines of text to the console. These workflow commands can be used with shell commands or within your custom actions. Workflow commands are useful because they enable you to share information between workflow steps, print debug or error messages to the console, set environment variables, set output parameters, or add to the system path.

Most workflow commands use the `echo` command in the below specific format, while others can be invoked by writing to a file.

```bash
echo "::workflow-command parameter1={data},parameter2={data}::{command value}"
```

Below are some basic message logging examples for printing a debug message, info message, error message, or warning message to the console.

```yml
- name: workflow commands logging messages
  run: |
    echo "::debug::This is a debug message"
    echo "This is an info message"
    echo "::error::This is an error message"
    echo "::warning::This is a warning message"
```

You can also create a message to print to the log with a filename (file), line number (line), and column (col) number where the error occurred. Warning messages will appear in a yellow highlight with the text "warning", and error messages will appear in a red highlight with the text "error".

```bash
echo "::error file=app.js,line=10,col=15::Something went wrong"
```

It's important that these workflow commands need to be on a single line. Characters that interfere with parsing such as commas and line breaks will need to be URL-encoded.

For example, the below text is a multi-line message.

```yml
This text spans
across multiple lines
```

This message should be encoded as shown below.

```yml
This text spans%0Aacross multiple lines
```

In addition to workflow commands, you can set exit codes to set the status of an action. This is important because when you're working with jobs in a workflow, a failed exit code will halt all concurrent actions and cancel any future actions. If you are creating a JavaScript action, you can use the actions toolkit `@actions/core` package to log a message and set a failure exit code. If you are creating a Docker container action, you can set a failure exit code in your `entrypoint.sh` script.

In the next unit, we'll cover how to create, use, and share starter workflows.
