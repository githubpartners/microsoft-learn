## Getting Started Resources

- **Quickstart guide**: https://skills.github.com/quickstart#planning-your-course
- **GitHub Skills “private” repo for skills.github.com**: https://github.com/github/skills
- **GitHub Skills public org**: https://github.com/skills
- **Exercise template**: https://github.com/skills/template-template

## Setup

- **Codebase: Basic codebase**. Something to populate the repository so it’s not blank
- **Existing workflow**: Create an existing workflow for the purpose of being used in another workflow. Nothing fancy, but a workflow that makes sense to use in another workflow

## Step 1: Make a GitHub Actions workflow reusable

- **Learning content**: Brief introduction to reusable workflows and how to make one reusable 
- **Activity: Add the workflow_call trigger to the existing workflow**
  - Prompt the learner to add the workflow_call: trigger to the existing workflow by making a change to the workflow file and committing it to a new branch and opening a PR

## Step 2: Reference a reusable workflow in a new workflow

- **Learning content**: Talk about [some limitations](https://github.blog/2022-02-10-using-reusable-workflows-github-actions/#some-limitations-with-reusable-workflows) to using reusable workflows and then how to reference the reusable workflow. `USER_OR_ORG_NAME/REPO_NAME/.github/workflows/REUSABLE_WORKFLOW_FILE.yml`
- **Activity: Reuse the existing workflow in a new workflow**
  - Include a code snippet of a new workflow for the learner to copy and paste and prompt the learner to add that new workflow to the same PR. This new workflow needs to reference the existing workflow

Merge the PR

## Step 3: Trigger the event for the new workflow

- **Learning content**: Brief explanation of what will happen when the learner triggers the new workflow 
- **Activity: Trigger the workflow**
  - Prompt the learner to trigger the workflow

## Step 4: Make your workflows accessible across your organization

- **Learning content**: Brief explanation of why you would want to make your reusable workflows accessible to other repositories in your organization
- **Activity: Allow other repositories in your organization to use the reusable workflow**
  - Prompt the learner to enable access to repositories in the organization in the repository settings under Action/Access
