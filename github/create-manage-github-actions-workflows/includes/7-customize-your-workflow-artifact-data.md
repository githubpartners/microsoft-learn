Here, you'll learn to Customize your workflow with artifact data and environment variables.

## Pass artifact data between jobs

Similar to the idea of caching dependencies within your workflow, you can pass data between jobs within the same workflow. You can do this by using the `upload-artifact` and `download-artifact` actions. Jobs that are dependent on a previous job's artifacts must wait for the dependent job to complete successfully before they can run. This is useful if you have a series of jobs that need to run sequentially based on artifacts uploaded from a previous job. For example, `job_2` requires `job_1` by using the `needs: job_1` syntax.

```yml
name: Share data between jobs
on: push
jobs:
  job_1:
    name: Upload File
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello World" > file.txt
      - uses: actions/upload-artifact@v2
        with:
          name: file
          path: file.txt

  job_2:
    name: Download File
    runs-on: ubuntu-latest
    needs: job_1
    steps:
      - uses: actions/download-artifact@v2
        with:
          name: file
      - run: cat file.txt
```

The preceding example has two jobs. `job_1` writes some text into the file `file.txt` and then uses the `actions/upload-artifact@v2` action to upload this artifact and store the data for future use within the workflow. `job_2` requires `job_1` to complete by using the `needs: job_1` syntax, then uses the `actions/download-artifact@v2` action to download that artifact and then print the contents of `file.txt`.

## Custom environment variables

Similar to using default environment variables, you can use custom environment variables in your workflow file. To create a custom variable, you need to define it in your workflow file using the `env` context. If you want to use the value of an environment variable inside a runner, you can use the runner operating system's normal method for reading environment variables.

```yml
name: CI
on: push
jobs:
  prod-check:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Nice work, $First_Name. Deploying to production server on branch $GITHUB_REF"
        env:
          First_Name: Mona
```
Next up is a quick knowledge check.
