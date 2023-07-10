# What is a Codespace?

GitHub Codespaces is an instant, cloud-based development environment that uses a container to provide you with common languages, tools, and utilities for development. GitHub Codespaces is a configurable, allowing you to create a customized development environment for your project. By configuring a custom development environment for your project, you can have a repeatable codespace configuration for all users of your project.

A Codespace’s lifecycle begins when you create a Codespace and ends when you delete it. You can disconnect and reconnect to an active Codespace without affecting its running processes. You can stop and restart a Codespace without losing the changes that you have made to your project.

:::image type="content" source="../media/codespaces-lifecycle.png" alt-text="Image of a circular lifecyle of a codespace that starts with creating and ends with deleting.":::

## Creating a Codespace
You can create a Codespace on GitHub.com, in Visual Studio Code, or by GitHub CLI. There are four ways to create a Codespace:

- From a GitHub template or any template repository on GitHub.com to start a new project
- From a branch in your repository for new feature work
- From an open pull request to explore work-in-progress
- From a commit in a repository's history to investigate a bug at a specific point in time

Codespaces can be temporary in order to test code or you can return to the same Codespace to work on long-running feature work.

**NOTE: You can create more than one Codespace per repository or even per branch. However, there are limits to the number of Codespaces you can create and run at the same time. If you reach the maximum number of Codespaces and try to create another, a message displays that an existing Codespace needs to be removed/deleted before a new Codespace can be created.**

You can create a new Codespace each time you develop in GitHub Codespaces or keep a long-running Codespace for a feature. If starting a new project, create a Codespace from a template and publish it to a repository on GitHub later.

When creating a new Codespace each time you work on a project, you should regularly push your changes to ensure that any new commits are on GitHub. When using a long-running Codespace for a new project, pull from the repository's default branch each time you start working in Codespace, This will enable the environment to have the latest commits. The workflow is very similar to working with a project on a local machine.

Repository administrators can enable GitHub Codespaces prebuilds for a repository to speed up Codespace creation.

## Codespace creation process

:::image type="content" source="../media/codespaces-diagram.png" alt-text="Diagram of a github codespace and how it connects from your code editor and into a docker container.":::

When creating a GitHub Codespace, four processes must occur:
1. VM and storage are assigned to your Codespace
2. A container is created
3. Connecting to the Codespace
4. Post-creation setup

### VM and storage are assigned to your Codespace
When creating a Codespace, a shallow clone is made of either the current repository or of the template repository if you're creating a Codespace from a template. A shadow clone is a repository created by limiting the depth of the history that duplicates from an original repository. The shallow clone enables you to have full root container access.

The cloned repository saves to a Linux virtual machine (VM) that you can have as both dedicated and private. Having a dedicated VM ensures you have the entire set of computing resources from that machine. 

### Creating a container
Creating a GitHub Codespace uses a development container as the environment based on configurations defined in a devcontainer.json file or a Dockerfile. When using a blank template, or from a repository with no devcontainer.json file, Codespace employs a default image, with the appropriate languages and runtimes available.

**NOTE: If you want to use Git hooks in your Codespace and apply anything in the git template directory to your Codespace, then you must set up hooks after the container is created.**

Since your repository is cloned onto the host VM before the container is created, anything in the git template directory will not apply in your Codespace unless you set up hooks in your devcontainer.json configuration file using the postCreateCommand

### Connecting to a Codespace
After container creation and any other initialization has run, you can connect to Codespace one of the following four methods.
- Web browser
- Visual studio code
- JetBrains IDE
- GitHub CLI

### Post-creation setup
Once the Codespace connection is complete, the automated setup process may continue to build based on the configuration specified in the devcontainer.json file. You may see postCreateCommand and postAttachCommand run after connection completion.

Once you have the Codespace complete, you may want to use Git hooks in your Codespace or set up hooks using the devcontainer.json lifecycle scripts, such as postCreateCommand.
 
You can enable a public dotfile repository using Codespaces. When implemented, your dotfiles will be cloned to the container and will invoke the install script. 

When creating a Codespace from a repository, the repository’s entire history is copied down with a full clone. If creating a Codespace from a template, the full history of the template repository is not preserved, unless you are using the blank template. You will start with an initial commit for the contents of the template repository.

**NOTE: During post-creation setup, you'll still be able to use the integrated terminal and make edits to your files, but take care to avoid any race conditions between your work and the commands that are running.**

## Saving changes in a Codespace
When you connect to a Codespace through the web, auto-save is automatically enabled to save changes after a specific amount of time has passed. When you connect to a Codespace through Visual Studio Code running on your desktop, you must enable auto-save. 

Your work will save to a virtual machine in the cloud. You can close and stop a Codespace and return to the saved work at a later time. If you have unsaved changes, you’ll receive a prompt to save them before exiting. However, if your Codespace is deleted, then your work will be lost. To save your work, you must commit your changes and push them to your remote repository or publish your work to a new one if you created your Codespace from a template.

## Opening an existing Codespace

You can reopen any of your active or stopped codespaces on GitHub.com, in a JetBrains IDE, in Visual Studio Code, or by using GitHub CLI.

To resume an existing Codespace you can either go to the respository where the Codespace exists and press "," key on your keyboard and **select Resume this codespace** or open https://github.com/codespaces in the browser, select the repository, and then select the existing Codespace. 

## Timeouts for a Codespace
If Codespace is inactive, or if you exit your Codespace without explicitly stopping, the application times out after a period of inactivity and stops running. The default timeout is after 30 minutes of inactivity. You cannot customize the duration of the timeout period for new Codespaces.

When a Codespace times out, your data is kept from the last time your changes were saved. 

## Losing internet connection while using GitHub Codespaces
A Codespace requires an internet connection. If the connection to the internet is lost while working in a Codespace, you will not be able to access your Codespace. However, any uncommitted changes will be saved. When you reestablish the internet connection, you can access the Codespace in the same state that it was left in when the connection was lost.

**NOTE: If you have an unstable internet connection, you should frequently commit and push your changes.**

## Closing or stopping a Codespace
If you exit the Codespace without running the stop command (for example, by closing the browser tab) or leave the Codespace running without interaction, the Codespace and its running processes continue for the duration of the inactivity timeout period. The default inactivity timeout period is 30 minutes. You can define your personal timeout setting for Codespaces you create, but this may be overruled by an organization timeout policy. 

Only running Codespaces incur CPU charges. A stopped Codespace incurs only storage costs.

You can stop and restart a Codespace to apply changes. For example, if you change the machine type used for your Codespace, you will need to stop and restart it for the change to take effect. When you close or stop your Codespace, all uncommitted changes are preserved until you connect to the Codespace again.

**NOTE: You can also stop Codespace and choose to restart or delete it if you encounter an error or something unexpected.**

## Rebuilding a Codespace
You can rebuild your Codespace to implement changes to your dev container configuration. For most uses, you can create a new Codespace as an alternative to rebuilding a Codespace. When you rebuild your Codespace, images from the cache speed up the rebuild process. You could also perform a full rebuild to clear the cache and rebuilds the container with fresh images.

**NOTE: When you rebuild the container in a Codespace, changes you made outside the /workspaces directory are cleared. Changes you made inside the /workspaces directory, including the clone of the repository or template you created the Codespace from, are preserved over a rebuild.**

## Deleting a Codespace
You can create a Codespace for a particular task. After you push your changes to a remote branch, then you can safely delete that Codespace.

If you try to delete a Codespace with unpushed git commits, the editor will notify you that you have changes that have not been pushed to a remote branch. You can push any desired changes and then delete your Codespace. You can also continue to delete your Codespace and any uncommitted changes or export the code to a new branch without creating a new Codespace. 

Stopped Codespaces that remain inactive for a specified amount of time will be deleted automatically. Inactive Codespaces delete after 30 days, but you can customize your Codespace retention intervals. 
