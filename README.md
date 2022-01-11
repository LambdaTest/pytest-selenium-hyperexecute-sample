# How to run Selenium automation tests on Hypertest (using PyTest framework)

Download the concierge binary corresponding to the host operating system. It is recommended to download the binary in the project's Parent Directory.

* Mac: https://downloads.lambdatest.com/concierge/darwin/concierge
* Linux: https://downloads.lambdatest.com/concierge/linux/concierge
* Windows: https://downloads.lambdatest.com/concierge/windows/concierge.exe

[Note - The current project has concierge for macOS. Irrespective of the host OS, the concierge will auto-update whenever there is a new version on the server]

## Running tests in PyTest using the Matrix strategy

Matrix YAML file (pytest_hypertest_matrix_sample.yaml) in the repo contains the following configuration:

```yaml
globalTimeout: 90
testSuiteTimeout: 90
testSuiteStep: 90
```

Global timeout, testSuite timeout, and testSuite timeout are set to 90 minutes.
 
The target platform is set to Windows

```yaml
 os: [win]
```

Python files in the 'tests' folder contain the 'tests' that will be run in parallel on the Hypertest grid

```yaml
files: ["tests/lt_sample_todo.py", "tests/lt_selenium_playground.py"]
```

Environment variables *LT_USERNAME* and *LT_ACCESS_KEY* are added under *env* directive. The user_name and access_key to access the LambdaTest platform can be found in your [LambdaTest Profile](https://accounts.lambdatest.com/detail/profile) page. Any more environment variables can be added in this section.

```yaml
env:
  LT_USERNAME: LT_USERNAME
  LT_ACCESS_KEY: LT_ACCESS_KEY
```

### Matrix Execution: Pre, Post, and Dependency Caching for faster package download & installation

To leverage the advantage offered by *Dependency Caching* in HyperTest, we first check the integrity of *requirements.txt* using checksum functionality

```yaml
cacheKey: '{{ checksum "requirements.txt" }}'
```

By default, *pip* in Python saves the downloaded packages in the cache so that next time, the package download request can be serviced from the cache (rather than re-downloading it again). The caching advantage offered by *pip* can be leveraged in HyperTest whereby the downloaded packages can be stored (or cached) in a secure server for future executions. The packages available in the cache will only be used if the checksum stage results in a Pass.

The *cacheDirectories* directive is used for specifying the directory where the packages have to be cached. The mentioned directory will override the default directory where Python packages are normally cached, further information about Caching in pip is available [here](https://pip.pypa.io/en/stable/cli/pip_cache/). The packages downloaded using pip will be cached in the directory (or location) mentioned under the *cacheDirectories* directive.

In our case, the downloaded packages are cached in *CacheDir* folder in the project's root. The folder is automatically created when the packages mentioned in *requirements.txt* are downloaded.  

```yaml
cacheDirectories:
  - CacheDir
```

Content under the *pre* directive is the pre-condition that will be run before the tests are executed on Hypertest grid. The *--cache-dir* option in *pip3* is used for specifying the cache directory. It is important to note that downloaded packages that are cached are securely uploaded to a secure upload, before the execution environment is auto-purged after build completion. Please modify *requirements.txt* as per the project requirements.

```yaml
pip3 install -r requirements.txt  --cache-dir CacheDir
```

The *post* directive contains a list of commands that run as a part of post-test execution. Here, the contents of *yaml/pytest_hypertest_matrix_sample.yaml* are read using cat as a part of post step. 

```yaml
post:
  - cat yaml/pytest_hypertest_matrix_sample.yaml
```

The *upload* directive contains an array of entries for requesting HyperTest to perform certain actions (e.g.upload Artifacts - files, reports, etc.) after the test (or task) completion. The test artifacts from the respective VM are downloaded using the *--download-artifacts* option provided by Concierge CLI. In the provided sample, the *reports* folder that contains the test report is downloaded on the local machine.

```yaml
upload:
  - reports/
```

The *testSuites* object contains a list of commands (that can be presented in an array). In the current YAML file, commands for executing the tests are added in an array (with a '-' preceding each item). In the current YAML file, the pytest command to run tests in *.py* files mentioned as array to *files* key are executed on Hypertest grid

```yaml
testSuites:
  - pytest -s --verbose --html=reports/report.html $files
```

The [user_name and access_key of LambdaTest](https://accounts.lambdatest.com/detail/profile) is appended to the *concierge* command using the **--user** and **--key** command-line options. The CLI option **--config** is used for providing the custom Hypertest YAML file (e.g. pytest_hypertest_matrix_sample.yaml). Run the following command on the terminal to trigger the tests in Pytest files on the Hypertest grid.

```bash
./concierge --user LT_USERNAME --key LT_ACCESS_KEY --download-artifacts --config yaml/pytest_hypertest_matrix_sample.yaml --verbose
```

Visit [Hypertest Automation Dashboard](https://automation.lambdatest.com/hypertest) to check the status of execution

## Running tests using PyTest using the Auto-Split strategy

Auto-Split YAML file (pytest_hypertest_autosplit_sample.yaml) in the repo contains the following configuration:

```yaml
globalTimeout: 90
testSuiteTimeout: 90
testSuiteStep: 90
```

Global timeout, testSuite timeout, and testSuite timeout are set to 90 minutes.
 
The *runson* key determines the platform (or operating system) on which the tests would be executed. Here we have set the target OS as Windows.

```yaml
 runson: win
``` 

Auto-split is set to true in the YAML file.

```yaml
 autosplit: true
``` 

*retryOnFailure* is set to True which instructs HyperTest to retry failed command(s). The retry operation is carried out till the number of retries mentioned in *maxRetries* are exhausted or the command execution results in a pass. The concurrency (i.e. number of parallel sessions) is set to 2.

```yaml
  retryOnFailure: true
  maxRetries: 5
  concurrency: 2
```

Environment variables *LT_USERNAME* and *LT_ACCESS_KEY* are added under *env* directive. The user_name and access_key to access the LambdaTest platform can be found in your [LambdaTest Profile](https://accounts.lambdatest.com/detail/profile) page. Any more environment variables can be added in this section.

```yaml
env:
  LT_USERNAME: LT_USERNAME
  LT_ACCESS_KEY: LT_ACCESS_KEY
```

### Auto-Split Execution: Pre, Post, and Dependency Caching for faster package download & installation

To leverage the advantage offered by *Dependency Caching* in HyperTest, we first check the integrity of *requirements.txt* using checksum functionality

```yaml
cacheKey: '{{ checksum "requirements.txt" }}'
```

By default, *pip* in Python saves the downloaded packages in the cache so that next time, the package download request can be serviced from the cache (rather than re-downloading it again). The caching advantage offered by *pip* can be leveraged in HyperTest whereby the downloaded packages can be stored (or cached) in a secure server for future executions. The packages available in the cache will only be used if the checksum stage results in a Pass.

The *cacheDirectories* directive is used for specifying the directory where the packages have to be cached. The mentioned directory will override the default directory where Python packages are normally cached, further information about Caching in pip is available [here](https://pip.pypa.io/en/stable/cli/pip_cache/). The packages downloaded using pip will be cached in the directory (or location) mentioned under the *cacheDirectories* directive.

In our case, the downloaded packages are cached in *CacheDir* folder in the project's root. The folder is automatically created when the packages mentioned in *requirements.txt* are downloaded.  

```yaml
cacheDirectories:
  - CacheDir
```

Content under the *pre* directive is the pre-condition that will be run before the tests are executed on Hypertest grid. The *--cache-dir* option in *pip3* is used for specifying the cache directory. It is important to note that downloaded packages that are cached are securely uploaded to a secure upload, before the execution environment is auto-purged after build completion. Please modify *requirements.txt* as per the project requirements.

```yaml
pip3 install -r requirements.txt  --cache-dir CacheDir
```

The *post* directive contains a list of commands that run as a part of post-test execution. Here, the contents of *yaml/pytest_hypertest_matrix_sample.yaml* are read using cat as a part of post step. 

```yaml
post:
  - cat yaml/pytest_hypertest_matrix_sample.yaml
```

The *upload* directive contains an array of entries for requesting HyperTest to perform certain actions (e.g.upload Artifacts - files, reports, etc.) after the test (or task) completion. The test artifacts from the respective VM are downloaded using the *--download-artifacts* option provided by Concierge CLI. In the provided sample, the *reports* folder that contains the test report is downloaded on the local machine.

```yaml
upload:
  - reports/
```

The *testDiscoverer* directive contains the command that gives details of the tests that are a part of the project. Here, we are fetching the list of Python files that would be further executed using the *value* passed in the *testRunnerCommand*

```bash
grep -nri 'class' tests -ir --include=\*.py | sed 's/:.*//'
```

Running the above command on the terminal will give a list of Python files that are located in the Project folder:

```bash
tests/lt_selenium_playground.py
tests/lt_sample_todo.py
```

The *testRunnerCommand* contains the command that is used for triggering the test. The output fetched from the *testDiscoverer* command acts as an input to the *testRunner* command.

```yaml
testRunnerCommand: pytest -s  --verbose --html=reports/report.html $test
```

Run the following command on the terminal to trigger the tests in Python files on the Hypertest grid.

```bash
./concierge --user LT_USERNAME --key LT_ACCESS_KEY --config yaml/pytest_hypertest_autosplit_sample.yaml --verbose
```

Visit [Hypertest Automation Dashboard](https://automation.lambdatest.com/hypertest) to check the status of execution
