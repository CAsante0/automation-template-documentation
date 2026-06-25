---
layout: default
title: Logs and Auditing Mechanics
---


[← Back to Home](./workflow.md)

---

# Understanding Pipeline Artifacts & Logs

Every time a workflow executes, the Automation Template generates three core artifacts to track execution progress, historical data status, and system health. This page outlines these three components—**Registry Actions**, **Persistent Log Streams**, and **Dataset File Trackers**—and provides real-world troubleshooting scenarios.

---

## 1. Registry Actions (Execution Tracking)

The system maintains a master runtime database (`run_tracker.csv`) that logs the lifecycle and health metrics of every single pipeline run. Each workflow configuration entry acts as a project container that triggers these tracked executions.

* **Behavior:** Appends a new line entry for every active run initialization, status transition (`initialized`, `running`, `completed`, `failed`), and error traceback.
* **Key Fields Logged:**
* `project_id` & `run_id`: Unique tracking hashes for the execution.
* `workflow_name`: Name matching your configuration file.
* `status`: Real-time state of the execution pipeline (`initialized`, `running`, `completed`, `failed`).
* `steps`: A JSON array mapping internal step completions (e.g., `[{"name": "validate_data_source", "status": "completed"}]`).



---

## 2. Persistent Log Streams (System Messages)

Each unique workflow manages its own continuous terminal printout stream (e.g., `WORKFLOW_NAME.log`). Unlike individual runtime registries, this stream acts as a single, endless record that appends data across multiple distinct scheduled runs (daily, weekly, etc.).

* **Log Rotation Safety:** To prevent text files from growing large enough to crash host environments, an automated log rotation is hard-coded into the pipeline. When a specific workflow log hits **50,000 KB**, the system automatically archives it and rotates to a fresh file.
* **Common Severity Levels:**
* `INFO`: Standard execution landmarks (e.g., `Attempt 1/5: Fetching tabledap...`).
* `WARNING`: Minor pipeline friction or expected data edge cases (e.g., `Fetch attempt failed, retrying...`).
* `ERROR`: Critical failures or query exceptions returned directly by remote data providers (e.g., `ERDDAP Error 404: Query outside of variable actual_range`).



---

## 3. Dataset File Trackers (Data Inventory)

For import-based workflows, the framework acts as an intelligent cache system. Successful data downloads trigger the creation of a local File Tracker inventory (e.g., `dataset_id_date.csv`).

* **Behavior:** Whenever a data slice is successfully processed, its structural metadata is extracted and saved to this file.
* **Format Flexibility:** If the underlying target dataset is a binary spatial format (like **NetCDF**), the tracker automatically extracts and flattens its header values into clear table parameters. For tabular files (like **CSV**), relevant row and bounding fields are tracked.
* **Preventing Duplicate Work:** The "Registry/Config Resolution" phase reads this exact file. By checking your data inventory, the pipeline dynamically determines the gap "Delta" (missing dates), meaning it only downloads files you don't already have.

### Anatomy of a Data Registry File

To trace a file directly back to the pipeline run that generated it, the data registry preserves a comprehensive list of dataset structural properties alongside execution metadata:

* `checksum_id`: Unique cryptographic file signature to check for file corruption.
* `dataset_id`: The product ID target specified in your configuration.
* `dataset_date`: The targeted data window slice (e.g., `['1993-01-01T00:00:00+00:00', '1993-01-01T23:59:59+00:00']`).
* `data_start_date` / `data_end_date`: Exact baseline timestamps inside the raw payload.
* `date_retrieved`: Exactly when the system downloaded the slice.
* `dataset_type` / `dataset_source`: File extensions (`nc`, `csv`) and backend type (`GLORYS`, `ERDDAP`).
* `metadata`: The raw data header dictionary (containing licensing, provider institutions, history logs, and global attributes).
* `number_of_records`: Integer count verifying payload size.
* `variables`: Arrays tracking exactly what metrics were preserved (e.g., `['sea_water_potential_temperature_at_sea_floor']`).
* `workflow_name` & `run_id`: **The Core Audit Link.** This explicitly stores the exact string name and unique tracking ID matching your configuration and `run_tracker.csv`.

---

## Troubleshooting Scenarios (Case-by-Case Examples)

### Case 1: You are notified of an issue with a data pull (Remote Provider Failures)

* **What to Check:** The individual **Log Stream** file for that workflow (e.g., `FISHBOT_DISSOLVED-O2.log`).
* **Why:** When remote servers experience downtime, structural changes, or bad requests, the raw error responses are written straight to the text log.
* **Example Application:** You check the log stream and find an explicit `ERROR` statement:
```text
2026-06-23 22:30:22,415;ERROR;ERDDAP Error 404: Error { message="Not Found: Your query produced no matching results. (time<=1993-02-07T23:59:59Z is outside of the variable's actual_range)" }
2026-06-23 22:30:22,415;WARNING;Fetch attempt 4 failed for fishbot_realtime...

```


*Verdict:* The log stream immediately reveals that the script's connection logic is working fine, but the data provider doesn't actually have records dating back to your requested 1993 timeframe.

### Case 2: You want to verify if a file for a specific date was successfully processed

* **What to Check:** The **Dataset File Tracker** inventory (e.g., `cmems_mod_glo_phy_my_0.083deg_P1D-m_2026-06-22.csv`).
* **Why:** You want to avoid scouring massive raw files or looking through thousands of text logs. You need a simple data index proving that a target timestamp exists on disk.
* **Example Application:** A researcher asks if May 14, 1993, was safely cataloged. You open your tracker file and search the `dataset_date` and `status` columns:
```csv
"5b84376dfce6e3e7d6...", "cmems_mod_glo_phy_my...", "['1993-05-14T00:00:00...', '1993-05-14T23:59:59...']", "2026-06-23 18:30:14", "nc", "GLORYS", "5d60dd6b-dc65-4326-86d4-7ff92d5fb29e"

```


*Verdict:* The record confirms that a NetCDF file (`nc`) for May 14, 1993, was successfully pulled down and indexed.

### Case 3: You want to isolate an internal step failure within a multi-stage pipeline

* **What to Check:** The **Registry / Run Tracker** database (`run_tracker.csv`).
* **Why:** If you have an all-in-one workflow configured to run both an **Import Step** and a **Templated Analysis Step**, a failure at the analysis level might mask a successful import. You need to verify if the file was downloaded successfully despite the downstream crash.
* **Example Application:** Your tracking platform alerts you that a master run finished with a `failed` status. You look inside `run_tracker.csv` to map out the individual internal operations:
```json
[
  {"name": "validate_data_source", "status": "completed"},
  {"name": "import_dataset", "status": "completed"},
  {"name": "templated_analysis", "status": "failed"}
]

```


By grabbing the `run_id` (`5d60dd6b-dc65-4326-86d4-7ff92d5fb29e`) from this row, you switch over to your Dataset Tracker file from **Case 2** and find that exact ID stamped inside the line.
*Verdict:* The tracker proves the import pipeline executed perfectly and securely committed the downloaded file to your local database registry before the downstream Python analysis script hit an exception and crashed. You do *not* need to waste time redownloading the source files.


---
[← Back to Home](./workflow.md)