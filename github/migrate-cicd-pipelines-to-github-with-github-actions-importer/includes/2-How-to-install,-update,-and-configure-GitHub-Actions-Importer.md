In this unit we’ll be reviewing:
- [How to install GitHub Actions Importer CLI extension](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/2-How-to-install%2C-update%2C-and-configure-GitHub-Actions-Importer.md#how-to-install-github-actions-importer-cli-extension)
- [Updating the GitHub Actions Importer CLI](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/2-How-to-install%2C-update%2C-and-configure-GitHub-Actions-Importer.md#updating-the-github-actions-importer-cli
)

## How to install GitHub Actions Importer CLI extension

In the upcoming labs exercise before you install GitHub Actions Importer, you will want to make sure you have:
- Created your own private repository using the [actions/importer-labs](https://github.com/actions/importer-labs) as a template
- And have configured your ```codespace```

Now you're ready to follow the steps below! 

1. To install the GitHub Actions Importer CLI extension, insert the below content:
```
 $ gh extension install github/gh-actions-importer 
 ```

2. Next, to verify that the extension is installed, utilize the below content:
```
 $ gh actions-importer -h
```
3. If the extension was installed properly, you will see the following:
```
Options:
  -?, -h, --help  Show help and usage information
  
  Commands:
  update     Update to the latest version of the GitHub Actions Importer.
  version    Display the version of the GitHub Actions Importer.
  configure  Start an interactive prompt to configure credentials used to authenticate with your CI server(s).
  audit      Plan your CI/CD migration by analyzing your current CI/CD footprint.
  forecast   Forecast GitHub Actions usage from historical pipeline utilization.
  dry-run    Convert a pipeline to a GitHub Actions workflow and output its yaml file.
  migrate    Convert a pipeline to a GitHub Actions workflow and open a pull request with the changes.
  ```
Next up, let's ensure GitHub Actions Importer is up to date. 

## Updating the GitHub Actions Importer CLI

To ensure you're running the latest version of GitHub Actions Importer, you should regularly run the ‘update’ command:
```
$ gh actions-importer update
```

You must be authenticated with the Container registry for this command to be successful. Alternatively, you can provide credentials using the ```--username``` and ```--password-stdin``` parameters:

```
$ gh actions-importer migrate -h
Description:
  Convert a pipeline to a GitHub Actions workflow and open a pull request with the changes.
```
If GitHub Actions Importer has updated successfully, you should see something similar to the text below.

```
$ gh actions-importer update
Login Succeeded
latest: Pulling from actions-importer/cli
Digest: sha256:613627879a3b5cff9c23a43fd81d94d26d0597eac8a840f09d6dc496abbe2e5b
Status: Downloaded newer image for ghcr.io/actions-importer/cli:latest
ghcr.io/actions-importer/cli:latest
```

Next, we’ll tackle GitHub Actions Importer's commands and review what is not migrated. 
