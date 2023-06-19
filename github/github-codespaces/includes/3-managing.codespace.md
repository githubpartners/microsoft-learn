## Codespace directory structure
After creating a Codespace, the clone is placed into the /workspaces directory. This is a persistent directory placed into the container. Any changes you make inside this directory, including editing, adding, deleting files, and rebuilding the container are preserved when you stop and restart the Codespace.

Outside the /workspaces directory, your Codespace contains a Linux directory structure that varies depending on the image used to build your Codespace. You can add files or make changes to files outside the /workspaces directory. For example, you can install new programs, or set up your shell configuration in a file such as ~/.bashrc. As a non-root user, you may not automatically have write access to certain directories. Most images allow root access to these directories with the sudo command.

Outside /workspaces, except the /tmp directory, Codespace directories are linked to the container’s lifecycle. Any changes are preserved when you stop and start your Codespace but are not preserved when you rebuild the container. 

Clearing the directories outside /workspaces ensures the rebuilt container is in the same state as it would be in a newly created Codespace. If rebuilding a container to apply configuration changes to the Codespace you're working in, any changes you have made will work the same for users creating new Codespaces with the same configuration.

If you want to make Codespaces more robust over rebuilds and across different Codespaces, you have several options.

- Install programs and tools in all Codespaces created from a repository. In your dev container configuration, you can use lifecycle command properties such as postCreateCommand to run custom installation commands, or you can choose from pre-written installation commands called features.
- Install tools or customize your setup in every Codespace you create, such as configuring your bash profile, you can link GitHub Codespaces with a dotfiles repository. The dotfiles repository is also cloned into the persistent /workspaces directory.
- Preserve specific files over a rebuild, use a devcontainer.json file to create a symlink between the files and a persistent directory within /workspaces. A symlink points to another file or folder on your computer or a connected file system. A symlink is similar to a Windows shortcut.

## Running your application
Port forwarding provides access to TCP ports running within the Codespace. For example, if running a web application on port 4000 within your Codespace, you can automatically forward that port to make the application accessible from your browser.

Port forwarding determines which ports are made accessible to you from the remote machine. Even if you do not forward a port, that port is still accessible to other processes running inside the Codespace.

When an application running inside a GitHub Codespace outputs a port to the console, GitHub Codespace detects the localhost URL pattern and automatically forwards the port. You can click on the URL in the terminal, or the link in the "toast" notification message that pops up at the bottom right corner of VS Code, to open the port in a browser. By default, GitHub Codespace forwards the port using HTTP. 

While ports can be forwarded automatically, they are not publicly accessible to the internet. By default, all ports are private, but you can manually make a port available to your organization or public, and then share access through a URL.

Running your application when you first land in your Codespace can make for fast inner development. As you edit, your changes are automatically saved and available on your forwarded port. To view changes, go back to the running application tab in your browser and refresh it.

## Losing the connection while using GitHub Codespaces
A Codespace requires an internet connection. If the connection to the internet is lost while working in a Codespace, you will not be able to access your Codespace. However, any uncommitted changes will be saved. When you reestablish the internet connection, you can access the Codespace in the same state that it was left in when the connection was lost.

**NOTE: If you have an unstable internet connection, you should frequently commit and push your changes.**

If you know that you will often be working offline, you can use your devcontainer.json file with the "Dev Containers" extension for VS code to build and attach to a local development container for your repository.

## Committing and pushing your changes
If you're working with an existing repository, you can:
- create a Codespace from any branch, commit, or pull request in the repository
- switch to a new or existing branch from within your active Codespace.

GitHub Codespace is designed to be a short-lived clone of the UAT (user acceptance testing) or production environment. Use Codespace to create an isolated environment to:
- experiment
- check a teammate's pull request
- fix merge conflicts

If you only have read access to a repository, you can create a Codespace for the repository as long as you can fork it. When you make a commit from the Codespace or push a new branch, GitHub Codespaces either automatically create a fork of the repository for you or link the Codespace to an existing fork if you already have one for the upstream repository.

If you're working in a Codespace created from a template, Git is installed by default. You will need to publish your Codespace to a remote repository to save your work before sharing. If you start from GitHub's blank template, you first need to initialize your workspace as a Git repository (for example by entering git init) to start using source control within the Codespace.

**NOTE: Commits from your Codespace will be attributed to the name and public email configured at https://github.com/settings/profile. A token scoped to the repository, including in the environment as GITHUB_TOKEN, and your GitHub credentials will be used to authenticate.**

## Personalizing your Codespace with extensions or plugins
You can add plugins and extensions within a Codespace to personalize your experience in JetBrains and VS Code.
### VS Code extensions
If you work on your Codespaces in the VS Code desktop application or the web client, you can add any extensions you need from the Visual Studio Code Marketplace. For information on how extensions run in GitHub Codespaces, see Supporting Remote Development and GitHub Codespaces in the VS Code documentation.

If you already use VS Code, you can use Settings Sync to automatically sync extensions, settings, themes, and keyboard shortcuts between your local instance and any Codespaces you create.
## JetBrains plugins
If you work on your codespaces in a JetBrains IDE, you can add plugins from the JetBrains Marketplace.
