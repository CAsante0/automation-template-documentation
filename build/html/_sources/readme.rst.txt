READ ME
==========



Data Import Workflow Installation and Running Locally
-----------------------------------------------------

This library automates data retrieval using a user-supplied configuration file, making it easier to pull predefined datasets without manual work. The configuration file specifies which platform to pull data from (ERDDAP, OPeNDAP, or GlobusAPI), what parameters to use, and where to store the results.


Running the Application:
~~~~~~~~~~~~~~~~~~~~~~~~

:bold: Requirements
~~~~~~~~~~~~~~~~~~~~~~


Install all required python packages using the below command in the main application directory:

:code: pip install -r requirements.txt 

Creating a Config File
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration file defines the target resource parameters and the source server. Expansion into other data platforms (OpenDAP, Globus, etc) are in progress.

In order to create your own configuration file by copying either of the provided config yaml files (ex: erddap-griddap-config.yaml) and editing with the necessary values to create your own configuration file. Use the path of your create config file as the first argument in running the application. The required data types for each field are defined within the variable.yaml fil.

:bold: The `variable.yaml` file should only be updated if a new version of the configuration file is released. 

Running the Application
~~~~~~~~~~~~~~~~~~~~~~~~

To run the application, ensure you are in the main application directory (same directory as app.py) and run the below command with your config file and the validation file. 

:code: ./app.py {config file path} variable.yaml

To obtain data pulled, uncomment the write(file) statement within the app.py.


Running tests:
~~~~~~~~~~~~~~~~~~~~~~

To run tests, install pytest using the following command:

:code: pip install pytest

From there, cd into either the data_retrieval or parser_testing directories. Run a test on either using the command:

:code: pytest test_parse_config.py or test_data_retrieval.py





Disclosure
===========
This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.


