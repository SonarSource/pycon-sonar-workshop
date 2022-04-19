# Overview

This is a simple demo project to highlight the analysis of Python on SonarCloud.

## Running the webapp

Python 3 and flask need to be installed in the environment. You can run the following command to install the required dependencies:

```pip install -r requirements.txt```

- Initialize the database with `python init_db.py` (optional: a `database.db` file is already committed in the repository)
- `cd pokedex` and then simply run the webapp with `flask run`

# Sonar Workshop

We're going to set up a SonarCloud analysis on this project. We'll visualise issues on the main branch and on pull requests and see how PRs get decorated automatically.

We'll then set up a CI-based analysis and import code coverage information into the SonarCloud UI.

Useful link: https://docs.sonarcloud.io/

## Getting started

- Fork this repository.
- A basic workflow which will act as our CI already exists in `.github/workflows/python-app.yml`. It is disabled by default. Go to `Actions` and enable GitHub Actions to activate it.
- Go to `Pull requests->New pull request` and open a pull request from the `add-feature` branch to the `main` branch of your fork. Be careful that, by default, the PR targets the upstream repository.
- The GitHub Action should run and succeed.


## First analysis on SonarCloud

We'll see how to enable SonarCloud analysis without making any changes to our CI pipeline.

- Go to https://sonarcloud.io/sessions/new and sign up using your GitHub account.
- Create a new organization under your name and give SonarCloud permission to see the forked repository. 
- Go to `Analyze new project` and select the forked repository.

The first analysis should execute on the main branch first, then on the pull request. 
The pull request should be decorated with the analysis result.

## Adding code coverage to the analysis result

By default, source code is analyzed automatically by SonarCloud. 
As it is a static analysis tool, it does not execute tests and is not able to compute code coverage by itself.
You'll need to generate code coverage information and run the analysis in your CI to be able to import it.

**Note:** for simplicity, the branch `enable-ci-analysis` is already created in this repository with the required changes. You only need to replace placeholders in the `sonar-project.properties` file with your project information.

### Generate coverage information
To generate coverage information, the `.github/workflow/python-app.yml` file should be updated. We'll also need to make sure file paths are set to be relative to avoid any issue when importing the report.

- Clone the repository and open it in your favorite IDE.
- At the root of the repository, create a `.coveragerc` file containing the following:
```
[run]
source = pokedex
branch = True
relative_files = True
```
- In the `.github/workflow/python-app.yml`, replace the `pytest` command with:
 
```pytest --cov --cov-report xml:cov.xml --cov-config=.coveragerc```


### Enable CI-based analysis
We'll then enable CI-based analysis using the [SonarCloud GitHub Action](https://github.com/marketplace/actions/sonarcloud-scan):

- Go to the overview of your project in SonarCloud.
- Under `Administration->Analysis Method`, turn Automatic Analysis off. 
- Under `GitHub Actions`, click `Follow the tutorial`.
- Create a `SONAR_TOKEN` in your GitHub repository settings then click `Continue`.
- To the question "What option best describes your build?", select `Other`.
- Update the `.github/workflow/python-app.yml` file to include the SonarCloud scan. For simplicity, the final file should look like this:

```
# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with pytest
      run: |
        pytest --cov --cov-report xml:cov.xml --cov-config=.coveragerc
    - name: SonarCloud Scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Needed to get PR information, if any
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

We still need to create the analysis configuration file:

- Create a `sonar-project.properties` file the root of the repository. You can copy and paste the following (replace the placeholders with your project and organization keys)

```
sonar.projectKey={{YOUR_PROJECT_KEY}}
sonar.organization={{YOUR_ORGANIZATION_KEY}}

sonar.sources=pokedex
sonar.tests=tests
sonar.python.coverage.reportPaths=cov.xml
```

Let's commit this on the main branch and push it by running:
`git add .` then `git commit -m "Add CI analysis and coverage"` and `git push`.

Let's also rebase our PR immediately by running: 
`git checkout add-feature`, `git rebase main` and `git push --force`.

A new analysis should have been triggered for the main branch as well as the pull request. When it's done, we should see the overall coverage for our project as well as the one for our PR.

## (Extra: import Flak8 reports into SonarCloud)

You're already using tools like Flake8 in your CI and want to visualize its report in the SonarCloud UI?

This is possible by redirecting flake8 output to a file: `flake8 --output-file=flake8report.txt` and then adding the property
`sonar.python.flake8.reportPaths=flake8report.txt` to your `sonar-project.properties` file. Note that the report will be displayed as-is and it will not be possible to silence issues from SonarCloud UI.


# SonarLint: Fix issues before they exist

In your IDE, you can install the SonarLint plugin to detect issues before even committing them.


## Synchronize issues between SonarCloud and SonarLint

By default, SonarLint analyses the currently opened file with its default configuration.
It means that if you are using a different quality profile on SonarCloud, decided to silence some issues, or have an older version of the analyzer than what is available on SonarCloud there may be discrepancies between the two tools.

To remedy to that, you can use SonarLint connected mode, which will retrieve your quality profile as well as the silenced issues from SonarCloud to offer you a consistent experience.

# Final words

Thank you for following this workshop!

If you'd like to know more, feel free to visit [our website](https://sonarsource.com/) or our [community forum](https://community.sonarsource.com/). 
