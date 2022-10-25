## What are GitHub Actions?

*GitHub Actions* are packaged scripts to automate tasks in a software development workflow in GitHub. You can configure GitHub Actions to trigger complex workflows that meet your organization's needs; each time developers check new source code into a specific branch, at timed intervals, or manually. The result is a reliable and sustainable automated workflow, which leads to a significant decrease in development time.

## Where can you find GitHub Actions?

GitHub Actions are scripts that adhere to a yml data format. Each repository has an **Actions** tab that provides a quick and easy way to get started with setting up your first script. If you see a workflow that you think would be a great starting point, just select the **Configure** button to add the script and begin editing the source yml.

:::image type="content" source="../media/github-actions-automate-development-tasks-01.png" alt-text="Screenshot of the *Actions tab* in GitHub Actions displaying a simple workflow and a button to set up this workflow.":::

However, beyond those GitHub Actions featured on the Actions tab, you can:

- Search for GitHub Actions in the [GitHub Marketplace](https://github.com/marketplace?type=actions&azure-portal=true). The GitHub Marketplace allows you to discover and purchase tools that extend your workflow.
- Search for open-source projects. For example, the [GitHub Actions](https://github.com/actions?azure-portal=true) organization features many popular open-source repos containing GitHub Actions you can use.
- Write your own GitHub Actions from scratch. Furthermore, if you want, you could make them open source, or even publish them to the GitHub Marketplace.

## New workflow experience

When you want to create an Actions workflow in the Actions tab of your repository, the recommendations will be based on an analysis of repository content. The workflow recommendations are based on repository analysis that detects elements, such as programming language, build tools, frameworks, and package managers. If a repository contains a Node.js application that has been containerized, then the repository analysis will prioritize showing you both container and Node related workflows, as one example.

Also recommendations have been extended to the deployment category. If a repository contains a Dockerfile, we’ll suggest a workflow that builds these containers and deploys them to a container-compatible cloud service, as an example. This enables our cloud partners to contribute workflows for each of their services and helps them recommend the right workflows to end users based on the language and framework used in the repository code.

Get started by going to the **Actions** tab in your repository and select **New Workflow**.

## Using open-source GitHub Actions

Many GitHub Actions are open source and available for anyone who wants to use them. However, just like with any open-source software, you need to carefully check them before using them in your project. Similar to recommended community standards with open-source software, such as including a README, code of conduct, contributing file, and issue templates, just to name a few, you can follow the following recommendations when using GitHub Actions:

- Review the action's `action.yml` file for inputs, outputs, and to make sure the code does what it says it does.
- Check if the action is in the GitHub Marketplace. This is a good check, even if an action does not have to be on the GitHub Marketplace to be valid.
- Check if the action is verified in the GitHub Marketplace. This means that GitHub has approved the use of this action. However, you should still review it before using it.
- Include the version of the action you're using by specifying a Git ref, SHA, or tag.

## Two types of GitHub actions

There are two types of GitHub actions: container actions and JavaScript actions.

With **container actions**, the environment is part of the action's code. These actions can only be run in a Linux environment that GitHub hosts. Container actions support many different languages.

**JavaScript actions** don't include the environment in the code. You'll have to specify the environment to execute these actions. You can run in a VM in the cloud or on-premises. JavaScript actions support Linux, macOS, and Windows environments.

### The anatomy of a GitHub action

Here's an example of an action that performs a git checkout of a repository. This action, [actions/checkout@v1](https://github.com/actions/checkout?azure-portal=true), is part of a step in a workflow. This step also builds the Node.js code that was checked out. We'll talk about workflows, jobs, and steps in the next section.

```yml
steps:
  - uses: actions/checkout@v1
  - name: npm install and build webpack
    run: |
      npm install
      npm run build
```

Suppose you want to use a container action to run containerized code. Your action might look like this:

```yml
name: "Hello Actions"
description: "Greet someone"
author: "octocat@github.com"

inputs:
    MY_NAME:
      description: "Who to greet"
      required: true
      default: "World"

runs:
    uses: "docker"
    image: "Dockerfile"

branding:
    icon: "mic"
    color: "purple"
```

Notice the ```inputs``` section. Here, you're getting the value of a variable called MY_NAME. This variable will be set in the workflow that runs this action.

In the ```runs``` section, notice you specify *docker* in the ```uses``` attribute. When you do this, you'll need to provide the path to the docker image file. Here, it's called *Dockerfile*. We won't get into the specifics of Docker here, but if you would like more information, check out the [Introduction to Docker Containers](/learn/modules/intro-to-docker-containers/?azure-portal=true) module.

The last section, *branding*, personalizes your action in the GitHub Marketplace if you decide to publish it there.

You can find a complete list of action metadata at [Metadata syntax for GitHub Actions](https://help.github.com/en/actions/building-actions/metadata-syntax-for-github-actions?azure-portal=true).

## What is a GitHub Actions workflow?

A *GitHub Actions workflow* is a process that you set up in your repository to automate software-development lifecycle tasks, including GitHub Actions. With a workflow, you can build, test, package, release, and deploy any project on GitHub.

To create a workflow, you add actions to a .yml file in the ```.github/workflows``` directory in your GitHub repository.

In the exercise coming up, your workflow file, *main.yml*, will look like this.

```yml
name: A workflow for my Hello World file
on: push
jobs:
  build:
    name: Hello world action
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - uses: ./action-a
      with:
        MY_NAME: "Mona"
```

Notice the ```on:``` attribute. This is a *trigger* to specify when this workflow will run. Here, it triggers a run when there's a push event to your repository. You can specify single events like ```on: push```, an array of events like ```on: [push, pull_request]```, or an event-configuration map that schedules a workflow or restricts the execution of a workflow to specific files, tags, or branch changes. The map might look something like this:

```yml
on:
  # Trigger the workflow on push or pull request,
  # but only for the main branch
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  # Also trigger on page_build, as well as release created events
  page_build:
  release:
    types: # This configuration does not affect the page_build event above
      - created
```

An event will trigger on all activity types for the event unless you specify the type or types. For a comprehensive list of events and their activity types, see: [Events that trigger workflows](https://help.github.com/actions/reference/events-that-trigger-workflows?azure-portal=true) in the GitHub documentation.

A workflow must have at least one *job*. A job is a section of the workflow that will be associated with a *runner*. A runner can be GitHub-hosted or self-hosted, and the job can run on a machine or in a container. You'll specify the runner with the ```runs-on:``` attribute. Here, you're telling the workflow to run this job on ```ubuntu-latest```.

Each job will have steps to complete. In our example, the step uses the action *actions/checkout@v1* to check out the repository. What's interesting is the ```uses: ./action-a``` value, which is the path to the container action that you build in an *action.yml* file. We looked at the contents of an *action.yml* file in the **What is GitHub Actions?** section.

The last part of this workflow file sets the MY_NAME variable value for this workflow. Recall the container action took an input called MY_NAME.

For more information on workflow syntax, see [Workflow syntax for GitHub Actions](https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions?azure-portal=true)

## GitHub-hosted versus self-hosted runners

We briefly mentioned runners as being associated with a job. A runner is simply a server that has the GitHub Actions runner application installed. In the previous workflow example, there was a `runs-on: ubuntu-latest` attribute within the jobs block, which told the workflow that the job will run using the GitHub-hosted runner that is running in the environment ubuntu-latest.

When it comes to runners, there are two options to choose from: GitHub-hosted runners or self-hosted runners. If you use a GitHub-hosted runner, each job runs in a fresh instance of a virtual environment that is specified by the GitHub-hosted runner type you define, `runs-on: {operating system-version}`. With self-hosted runners, you need to apply the self-hosted label, its operating system, and the system architecture. For example, a self-hosted runner with a Linux operating system and ARM32 architecture would look like the following, `runs-on: [self-hosted, linux, ARM32]`.

Each type of runner has its benefits, but GitHub-hosted runners offer a quicker, simpler way to run your workflows, albeit with limited options. Self-hosted runners are a highly configurable way to run workflows in your own custom local environment. Self-hosted runners can be run on-premises or in the cloud. You can also use self-hosted runners to create a custom hardware configuration with more processing power or memory to run larger jobs, install software available on your local network, and choose an operating system not offered by GitHub-hosted runners.

You can now specify shell scripts that run before the runner starts running a job from a workflow, and after a job completes, when you are managing. self-hosted runners for GitHub Actions. Doing so allows you to perform a task on your self-hosted runner before a job starts and after a job ends. Allowing you to set up your execution environment and clean up after workflow runs to ensure a consistent state on the runner itself, without requiring users to add that to their workflows.

### GitHub Actions may have usage limits

GitHub Actions has some usage limits, depending on whether your runner is GitHub-hosted or self-hosted and your GitHub plan. For more information on usage limits, check out [Usage limits, billing, and administration](https://docs.github.com/en/actions/reference/usage-limits-billing-and-administration) in the GitHub documentation.
