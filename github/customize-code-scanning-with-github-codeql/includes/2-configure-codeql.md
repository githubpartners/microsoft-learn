QL is a query language for CodeQL databases. 

## QL language specification

The query language is a dialect of Datalog, using stratified semantics, and it includes object-oriented classes. The data is relational named relations hold sets of tuples. QL language specification is a formal specification for the QL language. It provides a comprehensive reference for terminology, syntax, and other technical details about QL.

### Unicode characters

One unicode character description is to supply the character inline in the text, between double quote marks. The second is to write a capital U, followed by a plus sign, followed by a four-digit hexadecimal number representing the character’s code point. As an example of both, the first character in the name QL is “Q” (U+0051).

### Grammar

The syntactic forms of QL constructs are specified using a modified Backus-Naur Form (BNF). Syntactic forms including classes of tokens are named using bare identifiers. Quoted text denotes a token by its exact sequence of characters in the source code.

### Architecture

A QL program consists of a query module defined in a QL file and a number of library modules defined in QLL files that it imports. The module in the QL file includes one or more queries. Additionally, a module may include import directives, non-member predicates, class definitions, and module definitions.

### Library path

The library path is not strictly speaking a core part of the QL language. Different implementations of QL construct it in slightly different ways. Most QL tools allow you to explicitly specify the library path on the command line for a particular invocation. That is rarely done and only useful in very special situations.

Here is the the default construction of the library path. First, determine the query directory of the .ql file being compiled. Starting with the directory containing the .ql file each directory is checked for a file called qlpack.yml or codeql-pack.yml. The first directory where such a file is found is the query directory. If there is no such directory then the directory of the .ql file itself is the query directory.

## Configuring the CodeQL workflow for compiled languages

You can configure how GitHub uses the CodeQL analysis workflow to scan code written in compiled languages for vulnerabilities and errors. You can configure code scanning for that repository if you have write permissions to a repository. You can edit GitHub's CodeQL analysis workflow to specify the frequency of scans, the languages or directories to scan, and what CodeQL code scanning looks for in your code.

For the supported compiled languages, you can use the `autobuild` action in the CodeQL analysis workflow to build your code. If your workflow uses a language matrix, autobuild attempts to build each of the compiled languages listed in the matrix. Without a matrix autobuild attempts to build the supported compiled language that has the most source files in the repository. With the exception of Go, analysis of other compiled languages in your repository will fail unless you supply explicit build commands.

Next up, you'll learn about customizing your scanning workflow with CodeQL.

