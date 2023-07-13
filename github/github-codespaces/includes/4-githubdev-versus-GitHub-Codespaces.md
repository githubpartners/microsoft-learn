In understanding GitHub Codespaces, it is also important we review github.dev, a free, lightweight editing experiences that runs entirely in your browser.

It is important that you understand the differences between the two types of coding software before you choose which is the best fit for you or your organization.

The main difference between github.dev and GitHub Codespaces is that github.dev has no associated compute, so you won't be able to build and run your code or have terminal access. Meanwhile GitHub Codespaces you get the power of a persoanl Virtual Machine (VM) with terminal access, the same way you could use your local enviornment, just in the cloud. 

The github.dev editor provides many of the benefits of Visual Studio Code, such as search, syntax highlighting, and a source control view. You can also use Settings Sync to share your own VS Code settings with the editor.

The github.dev editor runs entirely in your browser’s sandbox. The editor doesn’t clone the repository, but instead uses the GitHub Repositories extension to carry out most of the functionality that you will use. Your work is saved in the browser’s local storage until you commit it. You should commit your changes regularly to ensure that they're always accessible.

You must be signed in to GitHub.com to use the github.dev editor.

### Codespace vs. github.dev

|  | github.dev | GitHub Codespace |
|--------|--------|--------|
| Cost | Free | Free monthly quota of usage for personal accounts |
| Availability |  Available to everyone on GitHub.com | Available to everyone on GitHub.com |
| Startup | Github.dev opens instantly with a key-press and you can start using it right away without having to wait for additional configuration or installation | When you create or resume a codespace, the codespace is assigned a VM and the container is configured based on the contents of a devcontainer.json file. This setup may take a few minutes to create the development environment. |
| Compute | There is no associated compute, so you won’t be able to build and run your code or use the integrated terminal. | With GitHub Codespaces, you get the power of a dedicated VM on which you can run and debug your application.|
| Terminal access | None | GitHub Codespaces provides a common set of tools by default, meaning that you can use the Terminal exactly as you would in your local environment.|
| Extensions | Only a subset of extensions that can run on the web will appear in the Extensions View and can be installed | With GitHub Codespaces, you can use most extensions from the Visual Studio Code Marketplace.|

### Continue working on Codespaces

You can start your workflow in github.dev and continue working on a codespace. If you try to access the Run and Debug View or the Terminal, you'll be notified that they are not available in github.dev.

To continue your work in a codespace, click Continue Working on… and select Create New Codespace to create a codespace on your current branch. Before you choose this option, you must commit any changes.
