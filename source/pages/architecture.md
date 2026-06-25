System Architecture
===================

.. Data Ingestion Pipeline
-----------------------
The Automation Template Workflow is a python based ETL pipeline framework for automation and auditing of data processing and import. Workflows are defined within description (configuration file) and an optional analysis script which runs the pipeline on a scheduled interval and audits the files and metadata generated. This allows for raw data to be prepared for downstream analyses or report generation such as in the example case outline in the tutorial for [Dissolved Oxygen Heatmap Workflow](./example_workflow)




<picture of automation template puzzle pieces>



Each workflow is broken down into one atomic action: an import (powered by one of the predefined data source modules) or a templated script (a user defined script or application that runs analysis and produces result) defined in the [configuration file](./config_guide.md) with all information pertaining to that step (data source, dataset details, schedule, storage locations) are defined within the configuration file. This configuration file now acts as a ledger and a establishes provenance for any data import or processing steps (dev) done using the Automation Template. 

Workflow step behaviour is defined within the data_transfer (Toolkit) class. For information on how to expand functionality via custom hooked see [expanding Automation Template Guide](./running_custom.md)




