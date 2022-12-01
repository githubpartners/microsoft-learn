Here are some troubleshooting ideas if you are having problems with code scanning.

## Troubleshooting the CodeQL workflow

You can enable step debug logging to produce more detailed logging output.

### Creating CodeQL debugging artifacts

You can get artifacts to help you debug CodeQL. The debug artifacts are uploaded to the workflow run as an artifact named debug-artifacts. The data contains the CodeQL logs, CodeQL database(s), and any SARIF file(s) produced by the workflow. 

### Creating CodeQL debugging artifacts using a workflow flag

You can create CodeQL debugging artifacts by using a flag in your workflow. You will need to modify the `init` step of your CodeQL analysis workflow file and set `debug: true`.

### Automatic build for a compiled language fails

Try the following troubleshooting steps if an automatic build of code for a compiled language within your project fails.

- Remove the `autobuild` step from your code scanning workflow and add specific build steps
- Edit the workflow and add a matrix specifying the languages you want to analyze
  - CodeQL implicitly detects the supported languages in your code base if your workflow does not explicitly specify the languages to analyze 
  - CodeQL only analyzes the language with the most source files, in this configuration, the compiled languages C/C++, C#, Go, and Java
- The default CodeQL analysis workflow uses such a matrix
  - The following code sample from a workflow show how you can use a matrix within the job strategy to specify languages and then reference each language within the "Initialize CodeQL" step:

```
jobs:
  analyze:
    permissions:
      security-events: write
      actions: read
    ...
    strategy:
      fail-fast: false
      matrix:
        language: ['csharp', 'cpp', 'javascript']

    steps:
    ...
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: ${{ matrix.language }}
 ```

### No code found during the build

Several reasons can explain if your workflow fails with an error `No source code was seen during the build` or `The process '/opt/hostedtoolcache/CodeQL/0.0.0-20200630/x64/codeql/codeql' failed with exit code 32`, this indicates that CodeQL was unable to monitor your code.

1. The repository may not contain source code that is written in languages supported by CodeQL
   - Fix: Check the list of supported languages and, if this is the case, remove the CodeQL workflow
2. Automatic language detection identified a supported language, but there is no analyzable code of that language in the repository
   - Fix: You can manually define the languages you want to analyze by updating the list of languages in the `language` matrix
3. Your code scanning workflow is analyzing a compiled language (C, C++, C#, Go, or Java), but the code was not compiled
   - Fix: The CodeQL analysis workflow autobuild step may not have succeeded in building your code
   - Fix: Compilation may also fail if you have removed the `autobuild` step and did not include build steps manually
4. Your workflow is analyzing a compiled language (C, C++, C#, Go, or Java), but portions of your build are cached to improve performance
   - Fix: CodeQL requires a complete build to take place in order to perform analysis
5. Your workflow is analyzing a compiled language (C, C++, C#, Go, or Java), but compilation does not occur between the `init` and `analyze` steps in the workflow
   - Fix: CodeQL requires that your build happens in between these two steps in order to observe the activity of the compiler and perform analysis
6. Your compiled code (in C, C++, C#, Go, or Java) was compiled successfully, but CodeQL was unable to detect the compiler invocations
   - Fix: You ran the build process in a separate container to CodeQL
   - Fix: You are using a distributed build system external to GitHub Actions, using a daemon process
   - Fix: CodeQL is not aware of the specific compiler you are using.

## Troubleshooting query performance

Here are some tips on to avoid problems that can affect the performance of your queries.

### Eliminate cartesian products

You may have used two variables without relating them in any way, or only relating them using a negation. This leads to computing the Cartesian product between the sets of possible values for each variable. This could potentially generate a huge table of results. Additionally, this can occur if you do not specify restrictions on your variables.

### Use specific types

“Types” provide an upper bound on the size of a relation. This helps the query optimizer be more effective. It’s generally good to use the most specific types possible. Here is an example:

```
predicate foo(LoggingCall e)
```

is preferred over:

```
predicate foo(Expr e)
```

### Determine the most specific types of a variable

You can use CodeQL to determine what types an entity has when you are unfamiliar with the library used in a query. The predicate `getAQlClass()` returns the most specific QL types of the entity that it is called on.

### Avoid complex recursion

“Recursion” is about self-referencing definitions. On the whole, you should try to make recursive predicates as simple as possible. Meaning, you should define a base case that allows the predicate to bottom out, along with a single recursive call. Here is an example:

```
int depth(Stmt s) {
  exists(Callable c | c.getBody() = s | result = 0) // base case
  or
  result = depth(s.getParent()) + 1 // recursive call
}
```

Next up, the module summary.
