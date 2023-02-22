Troubleshooting GitHub Copilot is done in each environment. Here is some information about troubleshooting GitHub Copilot for:

- Visual Studio Code
- Visual Studio
- JetBrains IDE
- Neovim
- Certificate errors for GitHub Copilot

## Troubleshooting GitHub Copilot in Visual Studio Code

In Visual Studio Code, the log files are useful for diagnosing connection issues. The GitHub Copilot extension stores the log files in the standard log location for Visual Studio Code extensions. The log files are found through the developer option and open extension logs folder within Visual Studio Code.

In rare cases, errors might not be logged in the regular locations. If you encounter errors and there is nothing in the logs, you may try to see the logs from the process running VS Code and the extension. This allows you to view the Electron logs. These logs are found under developer and the toggle developer tools within Visual Studio Code.

Network restrictions, firewalls, or your proxy may occur when connecting to GitHub Copilot. If this occurs you can follow the steps below to open a new editor with the relevant information that you can inspect yourself or share with the support team.

Open the VS Code Command Palette
For Mac: use: **Shift+Command+P**
For Windows or Linux: **use: Ctrl+Shift+P**
Type **Diagnostics** and then select **GitHub Copilot: Collect Diagnostics** from the list

## Troubleshooting GitHub Copilot in Visual Studio

The log files contain a lot of the error information. The files are stored in the GitHub Copilot extension in the standard log location for Visual Studio extensions.

## Troubleshooting GitHub Copilot in a JetBrains IDE

To troubleshoot issues while using JetBrains IDE, you can view the log files. The location of the log files depends on the JetBrains IDE you are using. Each of these JetBrains IDE have log files that will help troubleshoot GitHub Copilot.

IntelliJ IDEA
Android Studio
GoLand
PhpStorm
PyCharm
RubyMine
WebStorm

## Troubleshooting GitHub Copilot in Neovim

In case GitHub Copilot is not operational. You can run the following command in Neovim:

`:Copilot status`

## Troubleshooting certificate errors for GitHub Copilot

You may encounter errors like “certificate signature failure”, “self-signed certificate”, or “unable to verify the first certificate” depending on your proxy setup. These errors are usually caused by a corporate proxy setup that intercepts secure connections, terminates the secure connection to GitHub, and instead uses a self-signed certificate to act like a TLS middleman. Support for this type of proxy is not available for all GitHub Copilot licenses. 

However, here are possible ways to resolve this issue. While using a corporate proxy please contact your IT department to see if they can configure the proxy to not intercept secure connections. Check the install of the proxy certificates on your machine in the OS trust chain. You can try to configure a different proxy that does not intercept secure connections. Or, try to configure GitHub Copilot to ignore certificate errors.

Next up, an exercise and knowledge check questions.
