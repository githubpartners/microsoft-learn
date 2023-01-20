Before we get into learning about the different commands you can run in GitHub Actions Importer, first we'll review installation, ensuring you have the most up-to-date version, and learn about the supported CI platforms.

In this unit we’ll be reviewing:
- [How to install GitHub Actions Importer CLI extension](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/2-How-to-install%2C-update%2C-and-configure-GitHub-Actions-Importer.md#how-to-install-github-actions-importer-cli-extension)
- [Updating the GitHub Actions Importer CLI](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/2-How-to-install%2C-update%2C-and-configure-GitHub-Actions-Importer.md#updating-the-github-actions-importer-cli
)
- [GitHub Actions Importer CI supported platforms](https://github.com/githubpartners/microsoft-learn/blob/cami-actions-importer/github/migrate-cicd-pipelines-to-github-with-github-actions-importer/includes/2-How-to-install%2C-update%2C-and-configure-GitHub-Actions-Importer.md#github-actions-importer-ci-supported-platforms)

Let’s start with how to install GitHub Actions Importer CLI extension.

## How to install GitHub Actions Importer CLI extension

Once you have installed [Docker](https://docs.docker.com/get-docker/) and [GitHub CLI](https://cli.github.com/) is installed, navigate to your Linuxed-based environment. 

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
Next up, let's ensure GitHub Actions Importer is up-to-date. 

## Updating the GitHub Actions Importer CLI

To ensure you're running the latest version of GitHub Actions Importer, you should regularly run the ‘update’  command:
```
$ gh actions-importer update
```

You must be authenticated with the Container registry for this command to be successful. Alternatively, you can provide credentials using the ```--username``` and ```--password-stdin``` parameters:

```
$ gh actions-importer migrate -h
Description:
  Convert a pipeline to a GitHub Actions workflow and open a pull request with the changes.
```

Once you are granted access to the preview, you will be able to access further reference documentation about running a migration.

## GitHub Actions Importer CI supported platforms

And finally, here are the platforms that you can use GitHub Action Importer to migrate from:

- Azure DevOps
- CircleCI
- GitLab
- Jenkins
- Travis CI

Next we’ll tackle how to run the different commands and how to interpret their results. 
