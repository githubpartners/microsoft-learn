In this unit we'll be going over the following:

- Signing up for GitHub Copilot
- How to Configure GitHub Copilot with Visual Studio Code

Now let's dive into how to get started with Signing up for GitHub Copilot.

## Signing up for GitHub Copilot

You need to set up a free trial or subscription for your personal account before you can start using GitHub Copilot. 

You can do so by clicking on your profile photo and then found in **Settings**. 

After you sign up, you will need to install an extension for your preferred environment. GitHub Copilot supports GitHub.com, Visual Studio Code, Visual Studio, JetBrains IDEs, and Neovim as an unobtrusive extension. 

But for this specific module we will just be reviewing extensions and configurations for Visual Studio Code since the exercise we complete in this module will use Visual Studio Code.

If you are using a different environment, we will provide links to GitHub Docs under the Relevant links section at the end of this module that will review installing extensions and configuration. 


## Configuring GitHub Copilot in Visual Studio Code

### Adding the Visual Studio Code extension

Here is how you can add the Visual Studio Code extension.

- In the Visual Studio Code Marketplace, go to the GitHub Copilot extension page and click **Install**
- A popup will appear, asking to open Visual Studio Code, and then click **Open Visual Studio Code**
- In the Extension: GitHub Copilot tab in Visual Studio Code, click **Install**
- If you have not previously authorized Visual Studio Code in your GitHub account, you will be prompted to sign in to GitHub in Visual Studio Code

GitHub Copilot can autocomplete code as you type when you use Visual Studio Code. After installation, you can enable or disable GitHub Copilot, and you can configure advanced settings within Visual Studio Code. 

### Enabling or disabling GitHub Copilot in Visual Studio Code

1. To enable or disable GitHub Copilot, click the status icon in the bottom panel of the Visual Studio Code window

:::image type="content" source="../media/status-icon-visual-studio-code.png" alt-text="Status icon for GitHub Copilot in the bottom panel of the Visual Studio Code Window. Background color matches the color of the status bar when enabled." border="false":::

2. When disabling GitHub Copilot, you will be asked whether you want to disable suggestions globally, or for the language of the file you are currently editing
   -  To disable suggestions from GitHub Copilot globally, click **Disable Globally**
   -  To disable suggestions from GitHub Copilot for a specified language, click **Disable for LANGUAGE**

### Enabling or disabling inline suggestions in Visual Studio Code

1. In the File menu, navigate to Preferences and click **Settings**

:::image type="content" source="../media/vsc-settings.png" alt-text="File menu in Visual Studio Code. Preferences drop down sub-menu is open with Settings selected." border="false":::

2. In the left-side panel of the settings tab, click **Extensions** and then select **Copilot**
3. Under, Inline Suggest:Enable, select or deselect the checkbox to enable or disable inline suggestions

Additionally, you can choose to enable or disable inline suggestions and specify which languages you want to enable or disable GitHub Copilot for.

In the next unit, you’ll learn about troubleshooting GitHub Copilot.

<!-- Do not add a unit summary or references/links -->
