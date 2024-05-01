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

The environment variables used in this repo all begin with
**AZURE_**, for example:

```
AZURE_COSMOSDB_NOSQL_ACCT
AZURE_COSMOSDB_NOSQL_URI
AZURE_COSMOSDB_NOSQL_CONN_STRING1
AZURE_COSMOSDB_NOSQL_RO_KEY1
AZURE_COSMOSDB_NOSQL_RW_KEY1

AZURE_COSMOSDB_MONGO_VCORE_CONN_STR
AZURE_COSMOSDB_MONGO_VCORE_PASS
AZURE_COSMOSDB_MONGO_VCORE_USER
```

Note: These environment variable names are my personal conventions;
they are **not** required by Azure or Cosmos DB or the Microsoft SDKs.

---

## Tools - IDEs, etc

Use the tools you prefer.  I like using the following:

- [Visual Studio Code (VSC)](https://code.visualstudio.com/)
  - This is my default editor; it's excellent for Python and TypeScript.
- [JetBrains IntelliJ Java IDE](https://www.jetbrains.com/idea/)
- [JetBrains PyCharm Python IDE](https://www.jetbrains.com/pycharm/)
- [GitHub CoPilot](https://github.com/features/copilot)
  - Add AI superpowers to your IDE, such as Visual Studio Code
- [Git Source Control System](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Azure Data Studio](https://azure.microsoft.com/en-us/products/data-studio)
  - Desktop explorer for Azure SQL, Azure PostgreSQL, and Cosmos DB vCore 

---

## DotNet

See https://dotnet.microsoft.com/en-us/download

I currently use this version of DotNet:

```
PS ...\env> dotnet -version

Welcome to .NET 8.0!
---------------------
SDK Version: 8.0.204
```

---

## Java

See https://learn.microsoft.com/en-us/java/openjdk/download

I currently use this version of Java:

```
PS ...\env> java -version
openjdk version "17.0.10" 2024-01-16 LTS
OpenJDK Runtime Environment Microsoft-8902769 (build 17.0.10+7-LTS)
OpenJDK 64-Bit Server VM Microsoft-8902769 (build 17.0.10+7-LTS, mixed mode, sharing)
```

This repo uses [Gradle](https://gradle.org/) rather than
[Apache Maven](https://maven.apache.org/) as the java project-management tool
as I feel that it's much simpler and less verbose.

See the **Gradle installation instructions** here:
https://gradle.org/install/

---

## Python

See https://www.python.org/downloads/

I currently use this version of Python:

```
(venv) PS ...\app_common> python --version
Python 3.12.3
```

The Python projects in this repo assume that **standard python**
is used rather than Python distributions such as **Anaconda/Conda**.

Please see the section below called **Learning Python** if you're
not yet fluent in Python.

---

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

**TypeScript is a strongly typed programming language that "transpiles" into JavaScript**.
It looks similar to Java or C#.
The strong-typing leads to better IDE support, and better software quality.

The strong-typing is removed during the transpilation process, so that your code
runs as regular JavaScript in the **Node.js** or other runtime environment.

---

## Learning Python

I recommend learning Python to both my customers and peers for these reasons:
- It's one of the top three programming languages at this time (2024)
- It's applicable to a very wide range of workloads, such as:
  - Ad-hoc scripting
  - DevOps and Infrastructure
  - Application Development
  - Data Science
  - Apache Spark "big data" processing with the PySpark syntax
- It's an easy to learn language
- It's Object-Oriented
- It's cross-platform; same code runs on Windows/Linux/Mac

This is a good tutorial:
https://docs.python.org/3/tutorial/index.html

O'Reilly Media books on Python are generally excellent, IMO.

Be sure to focus on Python 3, not the older Python 2.

### How is Python formatted?

**Correct indentation matters!** - otherwise the program will throw an error when executed.

I use the **black** library to automatically reformat my code:

```
> black .\main.py
reformatted main.py

All done! ✨ 🍰 ✨
1 file reformatted.
```

### Where are Python Packages Hosted and Downloaded From?

[PyPi - the Python Package Index](https://pypi.org/)

### Python Virtual Environments

A **Python Virtual Environment** (i.e. - a venv) is a combination of
a set of python libraries and a version of python.  Venvs are used
so that you can have multiple Python projects on your system
and they won't conflict with each other.

Python has a **venv** functionality as part of its' **standard library**;
see https://docs.python.org/3/library/venv.html

A **requirements file** is used to specify the list of libraries
for a given Python virtual environment.  This is an example:

```
Jinja2
azure-cosmos
azure-identity
azure-storage-blob
black
docopt
levenshtein
matplotlib
openai
pandas
plotly
psutil
pylint
pytest==7.3.2
pytest-cov
python-dotenv
pytz
redis
requests
scikit-learn
scipy
tiktoken>=0.4.0
```

In this repo, I consistently use these three filenames:

- **requirements.in** - a simple text file specififying the required libraries
- **venv.ps1** - Windows PowerShell script to create the venv
- **venv.sh** - Mac OS or Linux bash script to create the venv
 
The **venv.ps1/sh** scripts first "compile" the requirements.in file,
resolve any version discrepancies, and create the **requirements.txt** file.

The virtual environment is then created, within the script, with this command:

```
pip install -q -r .\requirements.txt
```

**pip** is another tool in the Python ecosystem.  It installs libraries.
See https://docs.python.org/3/installing/index.html

Creation of the venv is a "one time" activity.  You don't need to re-install
it unless your requirements file has changed.

However, each time you navigate into the directory where the venv exists
you must **activate** it.  These are the commands to do that in Windows
and Mac/Linux, respectively:

```
>.\venv\Scripts\Activate.ps1    <--- In Windows PowerShell terminal

> venv/bin/activate             <--- In bash terminal on Mac OS and Linux
```

This Python venv concept is very similar to other programming
ecosystems.  Each has their own way to specify dependencies/requirements,
has an Internet-hosted library repository, and has tools to install them.
