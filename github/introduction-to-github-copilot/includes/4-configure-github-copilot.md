GitHub Copilot generates new code in a probabilistic way. The models do not contain a database of code, and do not look up snippets. Programming Languages and Technology available in the Public code base all are supported, allowing you to enable, configure, or disable GitHub Copilot in a supported IDE.

## Configuring GitHub Copilot settings on GitHub.com

You can configure settings for GitHub Copilot on GitHub.com in addition to the configuration for the GitHub Copilot plugin in your supported IDE. The settings apply wherever you use GitHub Copilot. GitHub Copilot includes a filter, which detects code suggestions matching public code on GitHub that you can enable and disable.

### Enabling or disabling duplication detection

GitHub Copilot includes a duplication detection filter, which detects code suggestions matching public code on GitHub. When you enable the filter, GitHub Copilot checks code suggestions with their surrounding code of about 150 characters against public code on GitHub. The suggestion will not be shown to you if there is a match or near match. Meaning that you can block suggestions of 150+ characters matching public code (ignoring whitespace). While useful in some instances, blocking matching suggestions does not address all use cases.

Therefore, for any code fragment suggested by Copilot developers will get:

- An inventory of similar code found in GitHub public repositories.
- The ability to sort that inventory by repository license, commit date, etc.

Using this information, you can find inspiration from other codebases, discover documentation, and almost certainly gain confidence that this fragment is appropriate to use in your project.

Here are the steps to enable or disable the filter:

- In the upper-right corner of any page, click your profile photo, then click **Settings**.
- In the left sidebar, click **GitHub Copilot**.
- Under **Suggestions** matching public code, select the dropdown menu, then click **Allow** to allow suggestions matching public code, or **Block** to block suggestions matching public code.
- To confirm your new settings, click **Save**.

## Enabling or disabling telemetry

Enabling or disabling telemetry allows you to choose whether your code snippets are collected and retained by GitHub. Additionally, you can choose if your code snipper is further processed and shared with Microsoft and OpenAI by adjusting your user settings.

<!-- Use the, Allow GitHub to use my code, image... https://docs.github.com/en/copilot/configuring-github-copilot/configuring-github-copilot-in-visual-studio-code#enabling-or-disabling-telemetry -->

You can use the left sidebar and the GitHub Copilot option on GitHub.com to enable or disable telemetry data. Changing the option, allows GitHub to use my code snippets for product improvements, or not.

## Configuring GitHub Copilot in Visual Studio Code

GitHub Copilot can autocomplete code as you type when you use Visual Studio Code. After installation, you can enable or disable GitHub Copilot, and you can configure advanced settings within Visual Studio Code.  You need to install the GitHub Copilot plugin for use with Visual Studio Code.

When using GitHub Copilot, you can use the default keyboard shortcuts in Visual Studio Code. Alternatively, you can rebind the shortcuts in the Keyboard Shortcuts editor using your preferred keyboard shortcuts for each specific command. You can search for each keyboard shortcut by command name in the Keyboard Shortcuts editor.

In Visual Studio Code, the GitHub Copilot status icon in the bottom panel of the window indicates whether GitHub Copilot is enabled or disabled. When enabled, the background color of the icon matches the color of the status bar. When disabled, the background color of the icon contrasts with the color of the status bar.

<!-- Add image from here, https://docs.github.com/en/copilot/configuring-github-copilot/configuring-github-copilot-in-visual-studio-code#enabling-or-disabling-github-copilot -->

Additionally, you can choose to enable or disable inline suggestions and specify which languages you want to enable or disable GitHub Copilot for.

## Configuring GitHub Copilot in Visual Studio

After Visual Studio installation, you can enable or disable GitHub Copilot after installing the GitHub Copilot plugin, Then you can configure advanced settings within Visual Studio and GitHub.com.

In the bottom panel of the Visual Studio window, the GitHub Copilot status icon indicates whether GitHub Copilot is enabled or disabled. When enabled, the background color of the icon will match the color of the status bar. When disabled, the icon will have a diagonal line through it.

<!-- add image, https://docs.github.com/en/copilot/configuring-github-copilot/configuring-github-copilot-in-visual-studio#enabling-or-disabling-github-copilot -->

### Configuring ReSharper for GitHub Copilot

GitHub Copilot may work best when you configure ReSharper to use GitHub Copilot's native IntelliSense. ReSharper assists Visual Studio in terms of code analysis, set of refactorings and code transformations, and depth of navigation support. Additionally, ReSharper helps with software development and maintenance tasks such as: finding unused code, complying with naming guidelines, detecting possible runtime exceptions, and adopting software design patterns. In the Visual Studio toolbar, use tools, options, environment, IntelliSense, and general.

## Configuring GitHub Copilot in a JetBrains IDE

Using a JetBrains IDE, GitHub Copilot can autocomplete code as you type. After installation, you can enable or disable GitHub Copilot and you can configure advanced settings within your IDE or on GitHub.com. GitHub describes how to configure GitHub Copilot in the IntelliJ IDE on GitHub Docs. The user interfaces of other JetBrains IDEs may differ.

## Configuring GitHub Copilot in Neovim

You can find the GitHub Copilot documentation in Neovim by running the following command.

`:help copilot`

In the next unit, you’ll learn about troubleshooting GitHub Copilot.

<!-- Do not add a unit summary or references/links -->
