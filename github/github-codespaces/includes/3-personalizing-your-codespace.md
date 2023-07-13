GitHub Codespaces is a dedicated environment for you. You can configure your repositories with a dev container to define their default GitHub Codespaces environment, and personalize your development experience across all of your codespaces with dotfiles and Settings Sync.

## What you can customize

There are a multitude of ways for you to customize your Codespace. Let's review each one.

- **Settings Sync:** You can synchronize your Visual Studio Code settings between the desktop application and the VS Code web client.
- **Dotfiles:** You can use a dotfiles repository to specify scripts, shell preferences, and other configurations.
- **Rename a codespace:** When you create a codespace it's assigned an auto-generated display name. If you have multiple codespaces, the display name helps you to differentiate between codespaces.You can change the display name for your codespace.
- **Change your shell:** You can change your shell in a codespace to keep the setup you're used to. When you're working in a codespace, you can open a new terminal window with a shell of your choice, change your default shell for new terminal windows, or install a new shell. You can also use dotfiles to configure your shell.
- **Change the machine type:** You can change the type of machine that's running your codespace, so that you're using resources appropriate for the work you're doing.
- **Set the default editor:** You can set your default editor for Codespaces in your personal settings page. On the settings page, you can set your editor preference so that when you create a codespace, or open an existing codespace, it is opened in your choice of:
  - Visual Studio Code (desktop application)
  - Visual Studio Code (web client application)
  - JetBrains Gateway - for opening codespaces in a JetBrains IDE
  - JupyterLab - the web interface for Project Jupyter
- **Set the default region:** You can set your default region in the GitHub Codespaces profile settings page to personalize where your data is held.
- **Set the timeout:** A codespace will stop running after a period of inactivity. By default this period is 30 minutes, but you can specify a longer or shorter default timeout period in your personal settings on GitHub. The updated setting will apply to any new codespaces you create, or to existing codespaces the next time you start them.
- **Configuring automatic deletion:** Inactive codespaces are automatically deleted. You can choose how long your stopped codespaces are retained, up to a maximum of 30 days.

For more on how on customization and step by step instructions on how to do everything we reviewed above, check out article titled, "Personalize your codespace" in the Resources section at the end of this module.

## Add to your Codespace with extensions or plugins

You can add plugins and extensions within a Codespace to personalize your experience in JetBrains and VS Code.

### VS Code extensions

If you work on your Codespaces in the VS Code desktop application or the web client, you can add any extensions you need from the Visual Studio Code Marketplace. For information on how extensions run in GitHub Codespaces, see Supporting Remote Development and GitHub Codespaces in the VS Code documentation.

If you already use VS Code, you can use Settings Sync to automatically sync extensions, settings, themes, and keyboard shortcuts between your local instance and any Codespaces you create.

### JetBrains plugins

If you work on your codespaces in a JetBrains IDE, you can add plugins from the JetBrains Marketplace.
