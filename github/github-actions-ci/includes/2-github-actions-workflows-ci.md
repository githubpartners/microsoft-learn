Here, you'll learn about GitHub Actions and workflows for CI. 

You'll learn to:

- Create a workflow from a template
- Understand the GitHub Actions logs
- Save and access build artifacts
- Automate reviews in GitHub using workflows
- Use partial re-runs
- Simplify using secrets with reusable workflows
- Discover code scanning partner integrations

## Create a workflow from a template

To create a workflow, you'll start by using a template. A template has common jobs and steps pre-configured for the particular type of automation you're implementing. If you're not familiar with workflows, jobs, and steps, check out the [Automate development tasks by using GitHub Actions](https://learn.microsoft.com/en-us/training/modules/github-actions-automate-tasks/) module.

On the main page of your repository, select the **Actions** tab to create a new workflow. You'll see that you can choose from many different templates. Two examples are the *Node.js* template, which does a clean install of node dependencies, builds the source code, and runs tests across different versions of Node. The second example is the *Python package* template, which installs Python dependencies and runs tests, including lint, across different versions of Python.

:::image type="content" source="../media/2-workflow-template.png" alt-text="GitHub Actions tab with the New Workflow button highlighted and the Node.js template selected." border="true":::

Take a look at the following Node.js template workflow.

```yml
name: Node.js CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:

    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [10.x, 12.x]

    steps:
    - uses: actions/checkout@v2
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v1
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm ci
    - run: npm run build --if-present
    - run: npm test
```

Notice the ```on:``` attribute. This workflow is triggered on a push to the repository, as well as when a pull request is made against the main branch.

There is one ```job``` in this workflow. Let's review what it does.

The ```runs-on:``` attribute specifies that, for the operating system, the workflow runs on ```ubuntu-latest```. The ```node-version:``` attribute specifies that there will be two builds, one for Node version 10.x and one for Node version 12.x. We'll describe the ```matrix``` portion in depth later, when we customize the workflow.

The ```steps``` in the job use the GitHub Actions [actions/checkout@v2](https://github.com/actions/checkout?azure-portal=true) action to get the code from your repository into the VM, and the [actions/setup-node@v1](https://github.com/actions/setup-node?azure-portal=true) action to set up the right version of Node.js. We specify that we're going to test two versions of Node.js with the ```${{ matrix.node-version }}``` attribute. This attribute points to the matrix we defined at the top of the file.

The last part of this step executes commands used by Node.js projects. The ```npm ci``` command installs dependencies from the *package-lock.json* file, ```npm run build --if-present``` runs a build script if it exists, and ```npm test``` runs the testing framework. Notice that this template includes both the build and test steps in the same job.

To learn more about npm, check out the npm documentation:

- [npm install](https://docs.npmjs.com/cli/install?azure-portal=true) 
- [npm run](https://docs.npmjs.com/cli/run-script?azure-portal=true) 
- [npm test](https://docs.npmjs.com/cli/test.html?azure-portal=true)

## Understand the GitHub Action logs 

When a workflow runs, it produces a log that includes the details of what happened and any errors or test failures.
If there is an error or if a test has failed, you see a red X rather than a green check mark ✔️ in the logs. You can examine the details of the error or failure to investigate what went wrong.

:::image type="content" source="../media/2-log-details.png" alt-text=" GitHub Actions log with details on a failed test." border="true":::

In the exercise, you identify failed tests by examining the details in the logs. You can access the logs from the **Actions** tab.

## Customize workflow templates

Recall that, at the beginning of this module, we described a scenario where you need to set up CI for your team. The Node.js template is a great start, but you want to customize it to better suit your own team's requirements. You want to target different versions of Node and different operating systems. You'll probably also want to separate the build and test steps into separate jobs.

Let's take a look at how you customize a workflow.

```yml
strategy:
matrix:
    os: [ubuntu-lastest, windows-2016]
    node-version: [8.x, 10.x]
```

Here, we configured a [build matrix](https://docs.github.com/enterprise-server@3.1/actions/learn-github-actions/managing-complex-workflows#using-a-build-matrix) for testing across multiple operating systems and language versions. This matrix will produce four builds, one for each operating system paired with each version of Node.

Four builds, along with all their tests, will produce quite a bit of log information. It might be difficult to sort through it all. In the sample below, we show you how to move the test step to a dedicated test job. This job tests against multiple targets. Making the build and test steps separate will make it easier to understand the log.

```yml
test:
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      os: [ubuntu-lastest, windows-2016]
      node-version: [8.x, 10.x]
  steps:
  - uses: actions/checkout@v1
  - name: Use Node.js ${{ matrix.node-version }}
    uses: actions/setup-node@v1
    with:
      node-version: ${{ matrix.node-version }}
  - name: npm install, and test
    run: |
      npm install
      npm test
    env:
      CI: true
```

### What are artifacts?

When a workflow produces something other than a log entry, it's called an *artifact*. For example, the Node.js build will produce a Docker container that can be deployed. This artifact, the container, can be uploaded to storage by using the action [actions/upload-artifact](https://github.com/actions/upload-artifact?azure-portal=true) and downloaded from storage by using the action [actions/download-artifact](https://github.com/actions/download-artifact?azure-portal=true).

Storing an artifact helps to preserve it between jobs. Each job uses a fresh instance of a VM, so you can't reuse the artifact by saving it on the VM. If you need your artifact in a different job, you can upload the artifact to storage in one job and download it for the other job.

## Save and access build artifacts

Artifacts are stored in storage space on GitHub. The space is free for public repositories and some amount is free for private repositories, depending on the account. GitHub stores your artifacts for 90 days. You can delete artifacts and logs sooner than the existing default of 90 days utilizing custom retention days. Additionally, for private, internal, and GitHub Enterprise repositories, you can retain artifacts and logs for over a year.

In the following workflow snippet, notice that in the ```actions/upload-artifact@main``` action there is a ```path:``` attribute. This is the path to store the artifact. Here, we specify *public/* to upload everything to a directory. If it was just a file that we wanted to upload, we could use something like *public/mytext.txt*.

```yml
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - name: npm install and build webpack
        run: |
          npm install
          npm run build
      - uses: actions/upload-artifact@main
        with:
          name: webpack artifacts
          path: public/
```

To download the artifact for testing, the build must have completed successfully and uploaded the artifact. In the following code, we specify that the test job depends on the build job.

```yml
test:
    needs: build
    runs-on: ubuntu-latest
```

In the following workflow snippet, we download the artifact. Now the test job can use the artifact for testing.

```yml
steps:
    - uses: actions/checkout@v1
    - uses: actions/download-artifact@main
      with:
        name: webpack artifacts
        path: public
```

For more information about using artifacts in workflows see [Persisting workflow data using artifacts](https://www.google.com/url?q=https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts&sa=D&source=docs&ust=1663854853049858&usg=AOvVaw12pVf7Z6YDukG5d3RqXyXL) in the GitHub documentation.

You can use images from private registries in job and service containers. Job and Service containers in GitHub Actions allow you to containerize your CI environment and make databases, caches, or other services available to your tests. Here’s an example of using private images from Docker Hub and GitHub Container Registry:

```
jobs:
  build:
    container:
      image: octocat/ci-image:latest
      credentials:
        username: mona
        password: ${{ secrets.docker_hub_password}}
    services:
      db:
        image:  ghcr.io/octocat/testdb:latest
        credentials:
          username: ${{ github.repository_owner }}
          password: ${{ secrets.ghcr_password }}
```

## Automate reviews in GitHub using workflows

So far, we've described starting the workflow with GitHub events such as *push* or *pull-request*. We could also run a workflow on a schedule or on some event outside of GitHub.

Sometimes, you may want to run a workflow after a person on your team does something. For example, you might only want to run a workflow after a reviewer has approved the pull request. For this scenario, you can trigger on ```pull-request-review```.

Another action we could take is to add a label to the pull request. In this case, we use the [pullreminders/label-when-approved-action](https://github.com/pullreminders/label-when-approved-action?azure-portal=true) action.

```yml
    steps:
     - name: Label when approved
       uses: pullreminders/label-when-approved-action@main
       env:
         APPROVALS: "1"
         GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
         ADD_LABEL: "approved"
```

Notice the block called ```env:```. This is where you set the environment variables for this action. For example, you can set the number of approvers needed. In this example we’ve set approvers to only one. 

The ```GITHUB_TOKEN``` variable is required because the action must make changes to your repository by adding a label. GitHub Actions lets you control the permissions granted to the GITHUB_TOKEN secret. 

A `permissions` key supported at the workflow and job level enables you to specify which permissions you want for the token. Any permission that is absent from the list will be set to `none`. Finally, you supply the name of the label to add.

GitHub actions now requires a collaborator with write access to take action to run workflows from first time users in pull requests.

Adding a label could be an event that starts another workflow, such as a merge. We'll cover this in the next module on continuous delivery with GitHub Actions.

## Use partial re-runs

You have the ability to re-run only the failed jobs or a single job in GitHub Actions. In addition, navigation improvements enable you to see the full results of previous runs. You save time by re-running only failed jobs, skipping work that’s already been done. You’ll now see a new drop-down menu if you have failing jobs in a workflow run, where you can choose **Re-run failed jobs** in addition to the existing **Re-run all jobs**. Each job listed in the sidebar has a re-run icon when you hover over it for a completed run. Also, jobs can be re-run directly from the logs view.

You’ll see a confirmation dialog that lists all the jobs that will be re-run, including all jobs that are downstream dependencies when you initiate a partial re-run. When you have more than one attempt at a workflow run, you’ll see a navigation drop-down to let you easily move between attempts. This is helpful for debugging what occurred across the various attempts of that run.

### Re-run jobs with debug logging

You can enable debug logging when you re-run jobs in a GitHub Actions workflow run. This gives you additional information about the job's execution and its environment which can help you diagnose failures. To enable debug logging, select **Enable debug logging** in the re-run dialog. Also, you can enable debug logging using the API or the command-line client.

## Simplify using secrets with reusable workflows

GitHub Actions simplifies using secrets with reusable workflows with the `secrets: inherit` keyword. You can simply pass the `secrets: inherit` to the reusable workflow and the secrets will be inherited from the calling workflow.

## Discover code scanning partner integrations

You can discover and configure Actions workflow templates for partner integrations straight from their repository's *Actions* tab under a category called **Security**.  Workflows are recommended based on the repository's content. GitHub will suggest analysis engines that are compatible with the source code in your repository. You can also configure code scanning for organization-owned private repositories where GitHub Advanced Security is enabled.

You can reference local reusable workflows easily. Reusable workflows that are in the same repository as the calling repository can be referenced with just the path and filename: `{path}/{filename}`.

Next, we'll cover how to use default and custom environment variables, custom scripts, cache dependencies, and pass artifact data between jobs. 
