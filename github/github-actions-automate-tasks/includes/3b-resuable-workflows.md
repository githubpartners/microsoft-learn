From automating repetitive tasks to building continuous integration and continuous deployment pipelines, you can do a lot with GitHub Actions. But until recently, you had to copy and paste YAML files from one repository to another if you wanted to use them in more than one place.

Reusable workflows let you DRY (don’t repeat yourself) your Actions configurations. This means that you don’t need to copy and paste your workflows from one repository to another. As an example, if you have three different Node applications and you’re building them all the same way, you can use one reusable workflow for all three.

Additionally, when combined with OpenID Connect (OIDC), reusable workflows let you enforce consistent deployments across your repository, organization, or enterprise. You can do this by defining trust conditions on cloud roles based on reusable workflows.

## Make any GitHub Actions workflow reusable

### Step 1: Add a workflow_call trigger

A reusable workflow is just like any GitHub Actions workflow with one key difference: it includes a `workflow_call` trigger. That means you need to add in the following syntax to any action’s YAML workflow file:
```
on:
  workflow_call:
```

Then reference this workflow in another workflow by adding in this syntax:
```
Uses:
  USER_OR_ORG_NAME/REPO_NAME/.github/workflows/REUSABLE_WORKFLOW_FILE.yml@TAG_OR_BRANCH
```

You can pass data such as job information or passwords to a reusable workflow by using inputs and secret triggers. Inputs are used to pass non-sensitive information while secrets are used to pass along sensitive information such as passwords and credentials.

### Step 2: Make your actions accessible across your organization

  After you've added the `workflow_call` trigger, you need to make sure that your organization's repositories have access to the trigger. To do this, go to your repository settings, select **Actions**, and enable access to repositories in your organization.

## A real-world example with reusable workflows

A developer used reusable workflows while developing hot.opensauced.pizza. The developer needed to centralize the GitHub Actions compliance workflows but they didn't want to copy and paste everything several times. The developer added the `workflow_call` trigger to the original YAML workflow file in their open-sauced repository.

```
name: Compliance

on:
  pull_request_target:
    types:
      - opened
      - edited
      - synchronize
      - reopened
  workflow_call:
```

The developer then built a new YAML workflow in the hot.opensauced.pizza repository and had it call back to the reusable compliance workflow.

```
name: "Compliance"

on:
  pull_request_target:
    types:
      - opened
      - edited
      - synchronize

permissions:
  pull-requests: write

jobs:
  compliance:
    uses: open-sauced/open-sauced/.github/workflows/compliance.yml@main
```

Reusable workflows helped provide consistency across the developer's projects and made life easier by not having to duplicate work. By copying and pasting a few key YAML files from one project to another, they could immediately be good to go on day one.

## Access resuable workflows

Before a reusable workflow can be used by another workflow, at least one of the below conditions must be true:

- Both workflows are in the same repository.
- The called workflow is stored in a public repository.
- The called workflow is stored in an internal repository and the settings for that repository allow it to be accessed.

### Call a reusable workflow

You can also call a reusable workflow using the `uses` keyword. Unlike when you are using actions within a workflow, you call reusable workflows directly within a job, and not from within the job steps. You can even call multiple workflows by referencing each workflow in a separate job.

- `{owner}/{repo}/.github/workflows/{filename}@{ref}` for reusable workflows in public repositories
- `./.github/workflows/{filename}` for reusable workflows in the same repository

```
jobs:
  call-workflow-1-in-local-repo:
    uses: octo-org/this-repo/.github/workflows/workflow-1.yml@172239021f7ba04fe7327647b213799853a9eb89
  call-workflow-in-another-repo:
    uses: octo-org/another-repo/.github/workflows/workflow.yml@v1
```

Using the commit SHA is the safest for stability and security. `{ref}` can be a SHA, a release tag, or a branch name. Using the second syntax option (without `{owner}/{repo}` and `@{ref}`) the called workflow is from the same commit as the caller workflow.

### Limitations with using resuable workflows

As you think about using resuable workflows, keep in mind that there are a couple limitations that you should be aware of. 

- You can’t reference a reusable workflow that’s in a private repository. If you have a reusable workflow in a private repository, only other workflows in that private repository can use it.
- Reusable workflows can’t be stacked on top of one another. You can only have a reusable workflow call another reusable workflow, but you can’t have it reference more than one.

## Monitor workflows in use

You can use the GitHub REST API to monitor reusable workflows in use. The `prepared_workflow_job` audit log action is triggered when a workflow job is started. 

- `repo` - the organization/repository where the workflow job is located. For a job that calls another workflow, this is the organization/repository of the caller workflow.
- `@timestamp` - the date and time that the job was started, in Unix epoch format.
- `job_name` - the name of the job that was run.
- `job_workflow_ref` - the workflow file that was used, in the form {owner}/{repo}/{path}/{filename}@{ref}. For a job that calls another workflow, this identifies the called workflow.

## How do resuable workflows compare to composite actions

Composite actions enable you to combine multiple actions into a single action that you can then insert into any workflow. This means you can refactor long YAML workflow files into much smaller files. This saves a fair amount of copying and pasting. For example, if your job needs to run on a specific runner or machine, you need to use reusable workflows. Composite actions don’t specify this type of thing. Composite actions are intended to be more isolated and generic.

Below are some key differences between resuable workflows and composite actions.

|   Reusable workflows    |                                                                                                                   Composite actions                                                                                                                  
|--------------|------------------|
|     Cannot call another reusable workflow     |                                                                                   Can be nested to have up to 10 composite actions in one workflow                                                                                    
| Can use secrets  |                                                                                Cannot use secrets                                                                                
|   Can use if: conditionals   | Cannot use if: conditionals
|  Can be stored as normal YAML files in your project  |                                      Requires individual folders for each composite action                                      
| Can use multiple jobs |                                                       Cannot use multiple jobs
| Each step is logged in real-time |                                                      Logged as one step even if it contains multiple steps

Reusable workflows allow you to specify any number of things and customize them more to your liking. You can have multiple jobs and that gives you a lot more granular control and power. The reusable workflow can be used in and across public repositories or within a single private repository, and reusable workflows from public repositories can be referenced using a SHA, a release tag, or a branch name. 

Re-running all jobs in a workflow will use the reusable workflow from the specified reference. You can have a reusable workflow call one reusable workflow and reusable workflows don’t require individual folders for each workflow like composite actions do.
