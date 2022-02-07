# How to run Selenium automation tests on HyperTest (using PyTest framework)

* [Pre-requisites](#pre-requisites)
   - [Download Concierge](#download-concierge)
   - [Configure Environment Variables](#configure-environment-variables)
   
* [Matrix Execution with PyTest](#matrix-execution-with-pytest)
   - [Core](#core)
   - [Pre Steps and Dependency Caching](#pre-steps-and-dependency-caching)
   - [Post Steps](#post-steps)
   - [Artefacts Management](#artefacts-management)
   - [Test Execution](#test-execution)

* [Auto-Split Execution with PyTest](#auto-split-execution-with-pytest)
   - [Core](#core-1)
   - [Pre Steps and Dependency Caching](#pre-steps-and-dependency-caching-1)
   - [Post Steps](#post-steps-1)
   - [Artefacts Management](#artefacts-management-1)
   - [Test Execution](#test-execution-1)

* [Secrets Management](#secrets-management)
* [Navigation in Automation Dashboard](#navigation-in-automation-dashboard)

# Pre-requisites

Before using HyperTest, you have to download Concierge CLI corresponding to the host OS. Along with it, you also need to export the environment variables *LT_USERNAME* and *LT_ACCESS_KEY* that are available in the [LambdaTest Profile](https://accounts.lambdatest.com/detail/profile) page.

## Download Concierge

Concierge is a CLI for interacting and running the tests on the HyperTest Grid. Concierge provides a host of other useful features that accelerate test execution. In order to trigger tests using Concierge, you need to download the Concierge binary corresponding to the platform (or OS) from where the tests are triggered:

Also, it is recommended to download the binary in the project's parent directory. Shown below is the location from where you can download the Concierge binary: 

* Mac: https://downloads.lambdatest.com/concierge/darwin/concierge
* Linux: https://downloads.lambdatest.com/concierge/linux/concierge
* Windows: https://downloads.lambdatest.com/concierge/windows/concierge.exe

## Configure Environment Variables

Before the tests are run, please set the environment variables LT_USERNAME & LT_ACCESS_KEY from the terminal. The account details are available on your [LambdaTest Profile](https://accounts.lambdatest.com/detail/profile) page.

For macOS:

```bash
export LT_USERNAME=LT_USERNAME
export LT_ACCESS_KEY=LT_ACCESS_KEY
```

For Linux:

```bash
export LT_USERNAME=LT_USERNAME
export LT_ACCESS_KEY=LT_ACCESS_KEY
```

For Windows:

```bash
set LT_USERNAME=LT_USERNAME
set LT_ACCESS_KEY=LT_ACCESS_KEY
```

# Matrix Execution with PyTest

Matrix-based test execution is used for running the same tests across different test (or input) combinations. The Matrix directive in HyperTest YAML file is a *key:value* pair where value is an array of strings.

Also, the *key:value* pairs are opaque strings for HyperTest. For more information about matrix multiplexing, check out the [Matrix Getting Started Guide](https://www.lambdatest.com/support/docs/getting-started-with-hypertest/#matrix-based-build-multiplexing)

### Core

In the current example, matrix YAML file (*yaml/pytest_hypertest_matrix_sample.yaml*) in the repo contains the following configuration:

```yaml
globalTimeout: 90
testSuiteTimeout: 90
testSuiteStep: 90
```

Global timeout, testSuite timeout, and testSuite timeout are set to 90 minutes.
 
The target platform is set to Windows. Please set the *[runson]* key to *[mac]* if the tests have to be executed on the macOS platform. 

```yaml
runson: win
```

Python files in the 'tests' folder contain the test suites run on the HyperTest grid. In the example, the tests in the files *tests/lt_sample_todo.py* and *tests/lt_selenium_playground.py* run in parallel using the specified input combinations.

```yaml
files: ["tests/lt_sample_todo.py", "tests/lt_selenium_playground.py"]
```

The *testSuites* object contains a list of commands (that can be presented in an array). In the current YAML file, commands for executing the tests are put in an array (with a '-' preceding each item). The Python command is used to run tests in *.py* files. The files are mentioned as an array to the *files* key that is a part of the matrix.

```yaml
testSuites:
  - pytest -s --verbose --html=reports/report.html $files
```

### Pre Steps and Dependency Caching

Dependency caching is enabled in the YAML file to ensure that the package dependencies are not downloaded in subsequent runs. The first step is to set the Key used to cache directories.

```yaml
cacheKey: '{{ checksum "requirements.txt" }}'
```

Set the array of files & directories to be cached. In the example, all the packages will be cached in the *CacheDir* directory.

```yaml
cacheDirectories:
  - CacheDir
```

Steps (or commands) that must run before the test execution are listed in the *pre* run step. In the example, the packages listed in *requirements.txt* are installed using the *pip3* command.

The *--cache-dir* option is used for specifying the location of the directory used for caching the packages (i.e. *CacheDir*). It is important to note that downloaded cached packages are securely uploaded to a secure cloud before the execution environment is auto-purged after build completion. Please modify *requirements.txt* as per the project requirements.

```yaml
pre:
  - pip3 install -r requirements.txt --cache-dir CacheDir
```

### Post Steps

Steps (or commands) that need to run after the test execution are listed in the *post* step. In the example, we *cat* the contents of *yaml/pytest_hypertest_matrix_sample.yaml*

```yaml
post:
  - cat yaml/pytest_hypertest_matrix_sample.yaml
```

### Artefacts Management

The *mergeArtifacts* directive (which is by default *false*) is set to *true* for merging the artefacts and combing artefacts generated under each task.

The *uploadArtefacts* directive informs HyperTest to upload artefacts [files, reports, etc.] generated after task completion. In the example, *path* consists of a regex for parsing the directory (i.e. *reports* that contains the test reports).

```yaml
mergeArtifacts: true

uploadArtefacts:
  [
    {
      "name": "reports",
      "path": ["reports/**"]
    }
  ]
```

HyperTest also facilitates the provision to download the artefacts on your local machine. To download the artefacts, click on Artefacts button corresponding to the associated TestID.

<img width="1425" alt="pytest_matrix_artefacts_1" src="https://user-images.githubusercontent.com/1688653/152557067-5a7a6340-b4de-42c4-8805-de2ba403b851.png">

Now, you can download the artefacts by clicking on the Download button as shown below:

<img width="1425" alt="pytest_matrix_artefacts_2" src="https://user-images.githubusercontent.com/1688653/152557101-1216351b-5461-4729-8d26-a1ab2def068e.png">

## Test Execution

The CLI option *--config* is used for providing the custom HyperTest YAML file (i.e. *yaml/pytest_hypertest_matrix_sample.yaml*). Run the following command on the terminal to trigger the tests in Python files on the HyperTest grid. The *--download-artifacts* option is used to inform HyperTest to download the artefacts for the job.

```bash
./concierge --download-artifacts --config --verbose yaml/pytest_hypertest_matrix_sample.yaml
```

Visit [HyperTest Automation Dashboard](https://automation.lambdatest.com/hypertest) to check the status of execution:

<img width="1414" alt="pytest_matrix_execution" src="https://user-images.githubusercontent.com/1688653/152155422-bca002b1-4331-4b7e-82e2-7b3588391dc0.png">

Shown below is the execution screenshot when the YAML file is triggered from the terminal:

<img width="1413" alt="pytest_cli_execution" src="https://user-images.githubusercontent.com/1688653/152514085-8b56de2b-4b92-4b81-a94d-58757f9cb3f7.png">

<img width="1101" alt="pytest_cli2_execution" src="https://user-images.githubusercontent.com/1688653/152516090-b06d3d80-145f-477a-b1ed-25c1d0be3be5.png">

## Auto-Split Execution with PyTest

Auto-split execution mechanism lets you run tests at predefined concurrency and distribute the tests over the available infrastructure. Concurrency can be achieved at different levels - file, module, test suite, test, scenario, etc.

For more information about auto-split execution, check out the [Auto-Split Getting Started Guide](https://www.lambdatest.com/support/docs/getting-started-with-hypertest/#smart-auto-test-splitting)

### Core

Auto-split YAML file (*yaml/pytest_hypertest_autosplit_sample.yaml*) in the repo contains the following configuration:

```yaml
globalTimeout: 90
testSuiteTimeout: 90
testSuiteStep: 90
```

Global timeout, testSuite timeout, and testSuite timeout are set to 90 minutes.
 
The *runson* key determines the platform (or operating system) on which the tests are executed. Here we have set the target OS as Windows.

```yaml
runson: win
```

Auto-split is set to true in the YAML file.

```yaml
 autosplit: true
``` 

*retryOnFailure* is set to true, instructing HyperTest to retry failed command(s). The retry operation is carried out till the number of retries mentioned in *maxRetries* are exhausted or the command execution results in a *Pass*. In addition, the concurrency (i.e. number of parallel sessions) is set to 2.

```yaml
retryOnFailure: true
maxRetries: 5
concurrency: 2
```

## Pre Steps and Dependency Caching

To leverage the advantage offered by *Dependency Caching* in HyperTest, the integrity of *requirements.txt* is checked using the checksum functionality.

```yaml
cacheKey: '{{ checksum "requirements.txt" }}'
```

By default, *pip* in Python saves the downloaded packages in the cache so that next time, the package download request can be serviced from the cache (rather than re-downloading it again).

The caching advantage offered by *pip* can be leveraged in HyperTest, whereby the downloaded packages can be stored (or cached) in a secure server for future executions. The packages available in the cache will only be used if the checksum stage results in a Pass.

The *cacheDirectories* directive is used for specifying the directory where the packages have to be cached. The mentioned directory will override the default directory where Python packages are usually cached; further information about caching in pip is available [here](https://pip.pypa.io/en/stable/cli/pip_cache/). The packages downloaded using pip will be cached in the directory (or location) mentioned under the *cacheDirectories* directive.

In our case, the downloaded packages are cached in the *CacheDir* folder in the project's root directory. The folder is automatically created when the packages mentioned in *requirements.txt* are downloaded.  

```yaml
cacheDirectories:
  - CacheDir
```

Content under the *pre* directive is the precondition that will run before the tests are executed on the HyperTest grid. The *--cache-dir* option in *pip3* is used for specifying the cache directory. It is important to note that downloaded cached packages are securely uploaded to a secure cloud before the execution environment is auto-purged after build completion. Please modify *requirements.txt* as per the project requirements.

```yaml
pip3 install -r requirements.txt  --cache-dir CacheDir
```

## Post Steps

The *post* directive contains a list of commands that run as a part of post-test execution. Here, the contents of *yaml/pyunit_hypertest_autosplit_sample.yaml* are read using the *cat* command as a part of the post step. 

```yaml
post:
  - cat yaml/pytest_hypertest_autosplit_sample.yaml
```

The *testDiscovery* directive contains the command that gives details of the mode of execution, along with detailing the command that is used for test execution. Here, we are fetching the list of Python files that would be further executed using the *value* passed in the *testRunnerCommand*

```yaml
testDiscovery:
  type: raw
  mode: dynamic
  command: grep -nri 'class' tests -ir --include=\*.py | sed 's/:.*//'
  
testRunnerCommand: pytest -s  --verbose --html=reports/report.html $test
```

Running the above command on the terminal will give a list of Python files that are located in the Project folder:

* tests/lt_selenium_playground.py
* tests/lt_sample_todo.py

The *testRunnerCommand* contains the command that is used for triggering the test. The output fetched from the *testDiscoverer* command acts as an input to the *testRunner* command.

```yaml
testRunnerCommand: pytest -s  --verbose --html=reports/report.html $test
```

### Artefacts Management

The *mergeArtifacts* directive (which is by default *false*) is set to *true* for merging the artefacts and combing artefacts generated under each task.

The *uploadArtefacts* directive informs HyperTest to upload artefacts [files, reports, etc.] generated after task completion.  In the example, *path* consists of a regex for parsing the directory (i.e. *reports* that contains the test reports).

```yaml
mergeArtifacts: true

uploadArtefacts:
  [
    {
      "name": "reports",
      "path": ["reports/**"]
    }
  ]
```
HyperTest also facilitates the provision to download the artefacts on your local machine. To download the artefacts, click on *Artefacts* button corresponding to the associated TestID.

<img width="1235" alt="pytest_autosplit_artefacts_1" src="https://user-images.githubusercontent.com/1688653/152527265-27011c1c-95ee-4ff5-ae56-e570a0c4391a.png">

Now, you can download the artefacts by clicking on the *Download* button as shown below:

<img width="1420" alt="pytest_autosplit_artefacts_2" src="https://user-images.githubusercontent.com/1688653/152527278-57a071f2-7b17-4a2a-822a-7bf9759a7531.png">

### Test Execution

The CLI option *--config* is used for providing the custom HyperTest YAML file (i.e. *yaml/pyunit_hypertest_autosplit_sample.yaml*). Run the following command on the terminal to trigger the tests in Python files on the HyperTest grid. The *--download-artifacts* option is used to inform HyperTest to download the artefacts for the job.

```bash
./concierge --download-artifacts --verbose --config yaml/pytest_hypertest_autosplit_sample.yaml
```

Visit [HyperTest Automation Dashboard](https://automation.lambdatest.com/hypertest) to check the status of execution

<img width="1414" alt="pytest_autosplit_execution" src="https://user-images.githubusercontent.com/1688653/152155403-969161d7-3d0c-4238-b80a-a63c88ea1023.png">

Shown below is the execution screenshot when the YAML file is triggered from the terminal:

<img width="1412" alt="pytest_autosplit_cli1_execution" src="https://user-images.githubusercontent.com/1688653/152523181-7acbfa32-e53a-454e-b4a6-dd7834498482.png">

<img width="1408" alt="pytest_autosplit_cli2_execution" src="https://user-images.githubusercontent.com/1688653/152523202-7da45332-560c-4e9b-b77b-8e750faea20d.png">

## Secrets Management

In case you want to use any secret keys in the YAML file, the same can be set by clicking on the *Secrets* button the dashboard.

<img width="703" alt="pyunit_secrets_key_1" src="https://user-images.githubusercontent.com/1688653/152540968-90e4e8bc-3eb4-4259-856b-5e513cbd19b5.png">

Now create *secrets* that you can use in the HyperTest YAML file.

<img width="362" alt="pyunit_secrets_key_2" src="https://user-images.githubusercontent.com/1688653/152540977-436a8ba8-0ded-44db-8407-b3fb21b1f98d.png">

## Navigation in Automation Dashboard

HyperTest lets you navigate from/to *Test Logs* in Automation Dashboard from/to *HyperTest Logs*. You also get relevant get relevant Selenium test details like video, network log, commands, Exceptions & more in the Dashboard. Effortlessly navigate from the automation dashboard to HyperTest logs (and vice-versa) to get more details of the test execution.

Shown below is the HyperTest Automation dashboard which also lists the tests that were executed as a part of the test suite:

<img width="1238" alt="pytest_hypertest_automation_dashboard" src="https://user-images.githubusercontent.com/1688653/152553665-9411f98c-e8de-487a-97a7-04310f8ef43a.png">

Here is a screenshot that lists the automation test that was executed on the HyperTest grid:

<img width="1425" alt="pytest_testing_automation_dashboard" src="https://user-images.githubusercontent.com/1688653/152553689-817191b9-db5b-4fa9-a233-df1779929191.png">

## We are here to help you :)
* LambdaTest Support: [support@lambdatest.com](mailto:support@lambdatest.com)
* HyperTest HomePage: https://www.lambdatest.com/support/docs/getting-started-with-hypertest/
* Lambdatest HomePage: https://www.lambdatest.com
