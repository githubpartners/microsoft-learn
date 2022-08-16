### Use reusable workflows

Hey, wouldn't it be nice not to have to do the same workflow for all of your repos manually, let's use reusable workflows. Reusable workflows offer a simple and powerful way to avoid copying and pasting workflows across your repositories. Here, you'll learn about resuable workflows.

### Reusable workflow uses

Reusable workflows let you DRY (don’t repeat yourself) your Actions configurations. This means that you don’t need to copy and paste your workflows from one repository to another.  You can use one reusable workflow if you have three different Node applications and you’re building them all the same way.

Additionally, reusable workflows allow you to require certain tests to be run before code can be deployed to production when combined with OpenID Connect.

### Make any GitHub Actions workflow reusable

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

Next you need to make sure that your organization's repositories have access to the `workflow_call` trigger. To do this, go to your repository settings, select **Actions**, and enable access to repositories in your organization.

Reusable workflows allow you to specify any number of things and customize them more to your liking. You can have multiple jobs and that gives you a lot of more granular control and power. The reusable workflow can be used in and across public repositories or within a single private repository. Reusable workflows from public repositories can be referenced using a SHA, a release tag, or a branch name. Re-running all jobs in a workflow will use the reusable workflow from the specified reference. You can have a reusable workflow call one reusable workflow. Reusable workflows don’t require individual folders for each workflow like composite actions do.

### Call a reusable workflow

You call a reusable workflow using the `uses` keyword. You can call reusable workflows directly within a job, not from within job steps. This is unlike when using actions within a workflow. These two syntaxes reference reusable workflow files: 
- `{owner}/{repo}/.github/workflows/{filename}@{ref}` for reusable workflows in public repositories
- `./.github/workflows/{filename}` for reusable workflows in the same repository

Using the commit SHA is the safest for stability and security. `{ref}` can be a SHA, a release tag, or a branch name. Using the second syntax option (without `{owner}/{repo}` and `@{ref}`) the called workflow is from the same commit as the caller workflow.

### Monitor workflows in use

You can use the GitHub REST API to monitor reusable workflows in use. The `prepared_workflow`_job audit log action is triggered when a workflow job is started. 

### Compare with composite actions

Composite actions enable you to combine multiple actions into a single action that you can then insert into any workflow. This means you can refactor long YAML workflow files into much smaller files. This saves a fair amount of copying and pasting. Composite actions are intended to be more isolated and generic.

|   Reusable workflows    |                                                                                                                   Composite actions                                                                                                                  
|--------------|------------------|
|     Cannot call another reusable workflow     |                                                                                   Can be nested to have up to 10 composite actions in one workflow                                                                                    
| Can use secrets  |                                                                                Cannot use secrets                                                                                
|   Can use if: conditionals   | Cannot use if: conditionals
|  Can be stored as normal YAML files in your project  |                                      Requires individual folders for each composite action                                      
| Can use multiple jobs |                                                       Cannot use multiple jobs
| Each step is logged in real-time |                                                      Logged as one step even if it contains multiple steps

