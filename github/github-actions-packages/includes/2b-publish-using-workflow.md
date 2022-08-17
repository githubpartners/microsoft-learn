Here, you'll learn the basics of using a workflow to publish to GitHub Packages, and the necessary steps to build, authenticate, tag, and push a Docker image to the GitHub Container Registry. 


## Use a workflow to publish to GitHub Packages

GitHub Packages let you securely publish and consume packages, store your packages alongside your code, and share your packages privately with your team or publicly with the open-source community. You can also use GitHub Actions to automate your packages. That means that for any developer or team using GitHub Packages, they have all of their packages right in their repository. There’s no need to source them from different places. They build automation workflows to consume and manage them at scale.

Following is an example of a basic workflow that runs whenever a new release is created in a repository. If the tests pass, then the package is published to GitHub Packages.

```yml
name: Node.js Package

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v1
        with:
          node-version: 12
      - run: npm ci
      - run: npm test

  publish-gpr:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v1
        with:
          node-version: 12
          registry-url: https://npm.pkg.github.com/
      - run: npm ci
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

First, the workflow file must exist in the `.github/workflows` directory. It's common practice to name a workflow that publishes a new package whenever a new release is created something like `release-package.yml`, to make it easy for project collaborators to understand its purpose without navigating to the workflow file. 

The preceding workflow does a few things after a new release is created:

1. A job named `build` runs `npm ci` (named after Continuous Integration) to install dependencies directly from the `package-lock.json` file, as well as the tests for the project.
1. Once the `build` job succeeds, the job named `publish-gpr` publishes the package.
1. The workflow publishes the package to the `registry-url: https://npm.pkg.github.com/` using an access token for authentication.

Actions written in YAML can also reference other actions. This is in addition to using scripts. Being able to reference actions as well should help reduce duplication in your workflows. You can use setup-node action to cache dependencies for projects with monorepo and pnpm package manager. Additionally, you can now run Node.js projects faster on GitHub Actions by enabling dependency caching on the setup-node action. `setup-node` supports caching from both npm and yarn package managers.

## Use GitHub Container Registry to host and manage Docker container images

GitHub Packages support the use of containers, Kubernetes, and other cloud-native technologies to manage their entire application lifecycle including production operations, development, release, and deployment. GitHub Packages also offers a container registry designed to support the unique needs of container images. You can use GitHub Container Registry to seamlessly host and manage Docker container images in your GitHub organization or personal user account. GitHub Container Registry allows you to configure who can manage and access packages using fine-grained permissions. You can use images from public and private registries in job and service containers. 

In GitHub Actions, job and service containers allow you to containerize your continuous integration environment and make databases, caches, or other services available to your tests.

With the container registry, you can:

- Store container images within your organization and user account rather than a repository.
- Set fine-grained permissions for the container images.
- Access public container images anonymously.

After you've built the image and authenticated and signed in to the GitHub Container Registry service at `ghcr.io`, you can then tag and push the latest version of the image to the container registry using these commands:

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

docker tag IMAGE_ID ghcr.io/OWNER/IMAGE_NAME:latest

docker push ghcr.io/OWNER/IMAGE_NAME:latest
```

> [!Note]
> To authenticate using a GitHub Actions workflow, you can use a GITHUB_TOKEN:
>
>- For package registries at `PACKAGE-REGISTRY.pkg.github.com`.
>- For the container registry at `ghcr.io/OWNER/IMAGE-NAME`.

### Use GITHUB_TOKEN to secure how you manage packages and containers

GITHUB_TOKEN is a special access token available with GitHub Actions. Each token is automatically generated for every job that needs authentication or installation access. Once that job is complete, the token automatically expires to reduce any possible risk exposure. Put more simply. When you run a workflow, the token only exists until that workflow is completed and then it’s deleted. In other solutions, you might have a token that exists for a longer period of time and if you don’t rotate that token, it may expire and break things. The GitHub token in an action workflow can by default publish to GitHub Packages. The net benefit is you have a much more secure system when you use GITHUB_TOKEN and reduce your attack surface area.
