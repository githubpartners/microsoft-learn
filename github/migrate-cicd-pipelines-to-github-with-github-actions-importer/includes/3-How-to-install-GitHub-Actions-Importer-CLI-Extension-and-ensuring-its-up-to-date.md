Before we get into learning about the different commands you can run in GitHub Actions Importer, first we'll review installation, ensuring you have the most up-to-date version, and learn about the supported CI platforms.

In this unit we’ll be reviewing:
- How to install GitHub Actions Importer CLI extension
- Updating the GitHub Actions Importer CLI
- Authenticating at the command line
- GitHub Actions Importer CI supported platforms

Let’s start with how to install GitHub Actions Importer CLI extension.

## How to install GitHub Actions Importer CLI extension

1. Install the GitHub Actions Importer CLI extension:
```
 $ gh extension install github/gh-actions-importer 
 ```

2. Verify that the extension is installed:
```
 $ gh actions-importer -h
Options:
  -?, -h, --help  Show help and usage information
  ```

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

Next we’ll tackle how to run the command, Audit, and how to interpret the information GitHub Actions Importer provides you. 
