# retrogallery

## Setup

1. Clone the repository and navigate to the project directory in your terminal.
2. Create a new Python virtual environment by running the following command:

  ```
  python -m venv env
  ```

This will create a new directory called `env` in your project directory, which will contain the virtual environment files.

3. Activate the virtual environment by running the following command:

- On Windows:

  ```
  env\Scripts\activate.bat
  ```
  
- On Linux or macOS:

  ```
  source env/bin/activate
  ```
  
You should see the name of your virtual environment appear in your terminal prompt, indicating that the virtual environment is now active.

Note: If you want to deactivate the virtual environment, you can simply run the `deactivate` command in your terminal.

4. Install the required dependencies by running the following command:

  ```
  pip install -r requirements.txt
  ```


This will install all the packages listed in the `requirements.txt` file into your virtual environment.

Note: If you need to add or remove dependencies in the future, you can update the `requirements.txt` file and run this command again to update your virtual environment.

## Usage

1. Ensure that your virtual environment is activated by running the appropriate command from step 3 above.
2. Run the project using your preferred method, such as running a Python script or using a development server.
3. When you are finished working on the project, deactivate the virtual environment by running the `deactivate` command in your terminal.

## Testing

1. Ensure that your virtual environment is activated by running the appropriate command from step 3 in Setup above.
2. Run the tests using `nose2`:

  ```
  nose2
  ```

3. You should see the test results in your terminal. A coverage report will also be generated in the `htmlcov` directory. Use a browser to open the `index.html` file in that directory to view the report.
4. When you are finished testing the project, deactivate the virtual environment by running the `deactivate` command in your terminal. 

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information about contributing to this project.