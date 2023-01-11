There are four commands that you can utilize with GitHub Actions Importer to assess, plan, test, and migrate your CI/CD environment into GitHub.

There commands are:

- **Audit**: Fetches all of the pipelines defined in a specified scope of the existing CI/CD environment, attempt a conversion of these pipelines to their equivalent workflow, and write a summary report with statistics gathered from the audit. 
- **Forcast**: Fetches jobs that have been completed over a specified time period and uses that data to calculate usage metrics.
- **Dry Run**: Provide existing pipelines with their equivalent GitHub Actions workflow and highlight ones that will need to potentially migrate manually. 
- **Migrate**: Convert an existing pipeline to its equivalent action and open a pull request with the converted workflows and associated files

In the upcoming sections we’ll be going through each one and how to utilize them, along with a section with what will not be automatically migrated. 

But before we dive into the commands, let’s start with reviewing how to install GitHub Actions CLI Extension. 
