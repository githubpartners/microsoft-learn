GitHub Packages is a package-management service that makes it easy to publish public or private packages next to your source code.

> [!NOTE]
> If you are not already familiar with GitHub, check out the [Introduction to GitHub](/learn/modules/introduction-to-github/) Learn module.

## GitHub Packages is a package registry

GitHub Packages allow you to share your project dependencies within your organization or publicly.

When you work on a project that has package dependencies, it’s important for you to trust them, understand their code, and connect with the community who built them. Within organizations, you also need to be able to quickly find what’s been approved for your use.

GitHub Packages make it easy to use the same familiar GitHub interface to find public packages anywhere on GitHub, or private packages within your organization or repositories.

## A standard package manager

GitHub Packages is compatible with common package-management clients, so you can publish packages with your choice of tools. If your repository is more complex, you may need to publish multiple packages of different types. You can also use webhooks or GitHub Actions to fully customize your publishing and post-publishing workflows.

Are you publishing an open-source package? Most open-source projects store their code on GitHub, so you can publish prerelease versions of your packages for testing within your community, then easily promote specific versions to the public registry of your choice.

:::image type="content" source="../media/2-github-packages-npm-package.png" alt-text="GitHub n p m package page, with description, and instructions about how to install it." border="false":::

At the time of writing, GitHub Packages is compatible with the following package managers: 

- npm, a NodeJS package manager
- NuGet, the .NET package manager
- RubyGems
- Maven and Gradle, two package managers for Java

## GitHub Packages is also a container registry

From complete applications to CLI utilities, containers are another form of distributing code. GitHub Packages allow you to publish and distribute container images. Once published (in public or in private) you can use these images from anywhere, including: 

- In your local development environment
- As a base image from your [GitHub Codespaces](https://github.com/features/codespaces) development environment
- As a step to execute into your Continuous Integration (CI) / Continuous Deployment (CD) workflow with [GitHub Actions](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions/finding-and-customizing-actions#referencing-a-container-on-docker-hub)
- On a server or a cloud service

:::image type="content" source="../media/2-github-packages-docker-image.png" alt-text="GitHub container image page, with image versions listing, statistics and instructions about how to install it." border="false":::

## Safeguard your containers with new container signing

GitHub has integrated sigstore support for container image signing into the GitHub Actions starter workflow. This means that you can sign your container images by default. Leveraging this workflow gives your users confidence that the container images they got from their container registry was the trusted code that you built and published.

Cosign starts our journey with the sigstore tool for signing container images. It supports several types of signing keys and also supports adding key-value annotations to the signature. Keeping our example simple, let’s say you have a key you generated with `$ cosign generate-key-pair` that you’ve saved in your GitHub Actions repository secrets called `SIGNING_SECRET`. Then, in your Actions workflow, after you’ve built the container image, you’d sign it by doing something like:

```
...

jobs:
  build:
    steps:
      # ... build steps here

      - uses: sigstore/cosign-installer@main

      - name: Write signing key to disk (only needed for `cosign sign --key`)
        run: echo "${{ secrets.SIGNING_SECRET }}" > cosign.key

      - name: Sign container image
        run: |
          cosign sign --key cosign.key \
            ghcr.io/your-org/your-repo:some-tag
        env:
          COSIGN_PASSWORD: ""
```

That’s it! That’s all you have to do to sign your container image in GitHub Actions and store it in GitHub Packages (or any of the other container registries cosign supports as well). You can then verify the signature when you pull the image, before a deploy:

```
$ cosign verify --key cosign.pub ghcr.io/your-org/your-repo:some-tag

Verification for ghcr.io/your-org/your-repo:some-tag --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - The signatures were verified against the specified public key
  - Any certificates were verified against the Fulcio roots.

[{"critical":{"identity":{"docker-reference":"ghcr.io/your-org/your-repo"},"image":{"docker-manifest-digest":"sha256:..."},"type":"cosign container image signature"},"optional":{}}]
```

There are many other context variables you could pull in, depending on what properties you want to validate before deploying. It’s important to note another part of sigstore is fulcio, a root CA that issues signing certificates from OIDC tokens, as well as Rekor, a transparency log for certificates issued by fulcio. This means you can sign your container images with the GitHub-provided OIDC token in Actions, without provisioning or managing your own private key. This is what makes signing so easy. We can turn it on by default, because there’s no additional setup beyond adding a specific GitHub Actions workflow. This keyless signing includes Rekor, a public transparency log, meaning your username, organization name, repository name, and workflow name will be published to the public transparency log.

## Compare GitHub Packages to GitHub Releases

GitHub Packages are used to publish releases of your libraries to a standard package feed or a container registry. They are meant to leverage the ways the specific package-management client works with that feed, like linking back to the repository in which the package was created as well as the version of the code that was used.  

[GitHub Releases](https://docs.github.com/en/github/administering-a-repository/releasing-projects-on-github) are used to release a bundle of packaged software, along with release notes and links to binary files. You can download those releases directly from their unique URL and track them back to the specific commit they were created from. You can only download releases as tarballs or ZIP files.

## Unified identity and permissions

Let's say you're working on a project using GitHub for hosting source code: JavaScript for the front end, with npm and Java for the back end. You now maintain at least three different sets of user credentials and permissions: for Git, npm, and Maven repositories.

With GitHub Packages, you can use a single set of credentials across your source-code repository, your private npm registry, and your Maven or Gradle private registry. Packages published through GitHub inherit the visibility and permissions assigned at the repository level. A new team member needs read access to a package and its code? Give them read access to the repository and it's done!

## Build and publish packages from GitHub

[GitHub Actions](https://github.com/features/actions) is another GitHub feature that allows you to automate your software workflows. You can build, test, and deploy your code right from GitHub.

> [!TIP]
> If you want to learn more about GitHub Actions, checkout *[Build continuous integration (CI) workflows by using GitHub Actions](/learn/modules/github-actions-ci/)* Learn module.

By combining GitHub Actions and GitHub Packages, you can build a workflow that will build and test your code, and then publish it to GitHub Packages by simply pushing code to your repository.

In the next unit, we'll learn how to use our workflow to publish to GitHub Packages and GitHub Container Registry.
