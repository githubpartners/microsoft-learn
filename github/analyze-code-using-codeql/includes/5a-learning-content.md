You will learn the recommended specifications (RAM, CPU cores, and disk) for running CodeQL analysis on self-hosted machines, based on the size of your codebase.

## Recommended hardware resources for running CodeQL

As you have learned, you can set up CodeQL on GitHub Actions or on an external CI system. CodeQL is fully compatible with GitHub-hosted runners on GitHub Actions.

You're responsible for configuring your own hardware when you're using an external CI system or self-hosted runners on GitHub Actions for private repositories. The optimal hardware configuration for running CodeQL may vary based on the size and complexity of your codebase, the programming languages and build systems being used, and your CI workflow setup.

This table below provides recommended hardware specifications for running CodeQL analysis based on the size of your codebase. This is a starting point for determining your choice of hardware or virtual machine.

| Codebase size | Ram | CPU |
|--------|--------|--------|
| Small (<100 K lines of code)	| 8 GB or higher	| 2 cores |
| Medium (100 K to 1 M lines of code) | 16 GB or higher |4 or 8 cores |
| Large (>1 M lines of code) | 64 GB or higher | 8 cores |

Additional recommendations include using an SSD with 14 GB or more of disk space for all codebase sizes.

## Additional software requirements

To generate a CodeQL database for a compiled language, you need to ensure that the system can successfully build and compile your code. CodeQL extraction has the following requirements.

For extraction of compiled languages (C/C++, C#, Go, Java) and Ruby on Linux:

- `glibc` version 2.17 or greater must be installed
- `musl-c`-based Linux distributions, such as Alpine Linux, are not supported

For TypeScript extraction on all platforms:

- Node.js must be installed and available on the PATH as `node`

For Python extraction:

- On Linux and macOS, Python 3 must be installed and available on the `PATH` as `python3` or `python`
- For Python 2 extraction on Linux and macOS, we also recommend having Python 2 installed and available on the `PATH` as `python2`
- On Windows, the Python launcher must be installed and available on the `PATH` as `py.exe`

Next up are some knowledge check questions.
