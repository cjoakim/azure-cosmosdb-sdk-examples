# Workstation Setup

Windows 11 is assumed, but these instructions should be easily adaptable
to Mac OS and Linux.

## Environment Variables

All of the sample code in this repo reads environment variables
to obtain their configuration values (URLs, keys, etc.).

You should become familiar with setting environment variables
on your computer.  This is one way to do it on Windows 11,
in a PowerShell terminal:

```
[Environment]::SetEnvironmentVariable("AZURE_COSMOSDB_EMULATOR_ACCT", "localhost:8081", "User")

[Environment]::SetEnvironmentVariable("AZURE_COSMOSDB_EMULATOR_KEY", "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==", "User")
```

TODO - list my standard env vars here



## Tools - IDEs, etc

Use the tools you prefer.  I like using the following:

- [Visual Studio Code (VSC)](https://code.visualstudio.com/)
  - This is my default editor; it's excellend for Python and TypeScript.
- [JetBrains IntelliJ Java IDE](https://www.jetbrains.com/idea/)
- [JetBrains PyCharm Python IDE](https://www.jetbrains.com/pycharm/)
- [GitHub CoPilot](https://github.com/features/copilot)
  - Add AI superpowers to your IDE, such as Visual Studio Code
- [Git Source Control System](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Azure Data Studio](https://azure.microsoft.com/en-us/products/data-studio)
  - Desktop explorer for Azure SQL, Azure PostgreSQL, and Cosmos DB vCore 

## DotNet

See https://dotnet.microsoft.com/en-us/download

I currently use this version of DotNet:

```
PS ...\env> dotnet -version

Welcome to .NET 8.0!
---------------------
SDK Version: 8.0.204
```

## Java

See https://learn.microsoft.com/en-us/java/openjdk/download

I currently use this version of Java:

```
PS ...\env> java -version
openjdk version "17.0.10" 2024-01-16 LTS
OpenJDK Runtime Environment Microsoft-8902769 (build 17.0.10+7-LTS)
OpenJDK 64-Bit Server VM Microsoft-8902769 (build 17.0.10+7-LTS, mixed mode, sharing)
```

## Python

See https://www.python.org/downloads/

I currently use this version of Python:

```
(venv) PS ...\app_common> python --version
Python 3.12.3
```

## TypeScript and Node.js

See https://nodejs.org/en and https://www.typescriptlang.org/.

I currently use these versions of Node.js and TypeScript:

```
PS ...\env> node -v
v20.11.1

PS ...\env> npm list -g
C:\Users\chjoakim\AppData\Roaming\npm
+-- nodemon@3.1.0
`-- typescript@5.4.3
```
