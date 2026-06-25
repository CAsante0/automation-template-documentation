---
layout: default
title: Creating Data Source Modules
---

[← Back to Home](./workflow.md)

---

# Creating Custom Data Source Modules

If your workflow requires data from a platform that isn't natively supported (like Copernicus Marine, THREDDS, or OPENDAP), you can create a custom **Data Source Module**.

To save time and avoid writing new code from scratch, you can often copy and adapt existing modules. For example, the OPENDAP and ERDDAP modules both pull data via standard web links (URLs), while the GLORYS module uses a specialized Python code library. If your new data provider uses similar methods, you can simply tweak those existing templates.

---

## How the System Works: The Two-Part Architecture

The Automation Template splits data management into two separate, organized roles:

* **The Toolkit (The Director):** This acts as the backend controller. It handles the "administrative" work—aligning dates, scheduling regular download intervals, tracking what has already been downloaded, and keeping an activity log.
* **Data Source Modules (The Connectors):** These are specialized plugins built for specific external websites or databases. While platforms like Copernicus Marine are built-in, you can build a custom "Connector" to bridge a new data provider to the main Toolkit.

---

## The Core Lifecycle Stages

When the system downloads data, it automatically runs through four distinct stages:

```
[1. Setup] ──> [2. Check Missing Data] ──> [3. Download Loop] ──> [4. Cleanup]

```

1. **Pre-Import Setup:** Handles background prep work, like logging in or checking your internet connection.
2. **Resolution:** Checks the logs to figure out exactly what data is missing since the last successful run so it doesn't download duplicates.
3. **Time-Window Loop:** Downloads the missing data in neat, organized time chunks (e.g., day-by-day).
4. **Post-Import Cleanup:** Performs finishing tasks like clearing temporary files or sending completion alerts.

---

## Steps to Build a Custom Module

To create your own connector, you will build a Python "child class" that hooks into our main framework using three straightforward steps.

### Step 1: Create the Module Base

Create a new file and link it to our base importer system. You will give your module a unique name and define what datasets and variables it should expect.

```python
class MyCustomDataset(BaseDatasetImporter):
    def __init__(self):
        # Links this custom code to the master system
        super().__init__() 

```

### Step 2: Set Up the Setup and Cleanup Actions

Tell the system exactly what to do right before the download starts and right after it finishes.

```python
    def custom_custom_pre_import_hook(self):
        # Runs BEFORE the download starts (e.g., Logging into the website)
        self.logger.info("User Custom Pre Import Function")

    def custom_post_import_hook(self):
        # Runs AFTER the download finishes (e.g., Saving records)
        self.logger.info("Syncing local metadata to cloud...")
        self.sync_metadata()

```


### Step 3: Define How to Grab the Data (`fetch_dataset`)

This is the core engine of your module. It tells the system exactly how to fetch a single block of data for a specific time range and variable list.

```python
    def fetch_dataset(self, win_start, win_end, variables, **kwargs):
        """
        Retrieves a single time chunk of data from the external provider.
        """
        raw_data = self.get_records(
            start=win_start, 
            end=win_end, 
            fields=variables
        )
        return raw_data

```

---

## Next Steps & Interactive Guides

For a step-by-step interactive walkthrough on building these modules, open the **Jupyter Notebook tutorial** located in the `Tutorials/` section of the Automation Template repository.



[← Back to Home](./workflow.md) | [Proceed to Installation](./installation.md)