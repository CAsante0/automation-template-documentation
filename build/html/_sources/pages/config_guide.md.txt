---
layout: default
title: Configuration File Guide
---

# Configuration File Specification

This guide describes the structure, blocks, and parameters used to write configuration files for the ETL pipeline. Configuration files are written in JSON and allow you to define various workflows, import strategies, data source properties, and coordinates for spatial or temporal subsetting.

---

## 0. Configuration File Naming Conventions

**Format & Structure:** Configuration files use JSON (JavaScript Notation), structured as an array of objects representing workflow profiles.

**Naming Convention:** Use the standard pattern:

```text
<data_source>_<variables/products>_<data_provider>.<version_number>.json

```

* `<data_provider>`: The data source provider or organization (e.g., `CMEMS`, `COASTWATCH`).
* `<data_source>`: The ingestion protocol or profile identifier (e.g., `GLORYS`, `ERDDAP`).
* `<variables/products>`: Descriptive tag for targeted data parameters (e.g., `PHYSICS`, `CHLOR-A`).
* `<version_number>`: Configuration schema version track (e.g., `v1`).

**Example:** `CMEMS_GLORYS_PHYSICS.v1.json`

---

## 1. File Structure Overview

The configuration file is a JSON array containing objects. Each object represents a data source group or a collection of workflow profiles (such as `"GLORYS"` or `"ERDDAP_WORKFLOW"`).

Within each profile, you define two primary configuration blocks:

* **`workflow`**: Specifies high-level orchestrations such as workflow name, execution steps, source types, scheduling parameters, and logging paths.
* **`import_dataset`**: Contains granular dataset specifications, target folder paths, variables, time ranges, bounding boxes, and source-specific access types.

---

## 2. Configuration Blocks & Fields Reference

### 2.1. The `workflow` Block

| Key | Required / Optional | Type | Allowed Values / Examples | Description |
| --- | --- | --- | --- | --- |
| `workflow_name` | Required | String | `"CMEMS_GLORYS_DAILY"`, `"COASTWATCH_CHLOR-A_DAILY"` | A unique identifying name for the orchestration pipeline. |
| `steps` | Required | Array of Strings | `["validate_data_source", "import_dataset"]` | Order of structural functions or execution stages to trigger. |
| `schedule` | Required | Array of Strings | `["daily"]`, `["weekly"]` | How often the orchestrator triggers or queries the data source. |
| `source_type` | Required | String | `"glorys"`, `"erddap"`, `"opendap"` | The source access mechanism or protocol type. |
| `log_folder_path` | Optional | String | `"./logger"` | Relative or absolute directory path where pipeline logs are generated. |

### 2.2. The `import_dataset` Block

| Key | Required / Optional | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `one_variable_per_file` | Optional | Boolean | `false` | If set to `true`, the pipeline separates multiple variables into individual target files. |
| `batch_import` | Optional | Boolean | `true` | When `true`, pulls all available data since the last recorded sync. When `false`, pulls a single or latest individual iteration. |
| `mnt1_import` | Required | String | *None* | Root folder structure directory where retrieved raw datasets are stored. |
| `project_name` | Optional | String | *None* | Name of the overarching research project or organizational category (e.g., `"GLORYS_PHYSICS_REANALYSIS_FORECAST"`). |
| `dataset_id` | Required | String | *None* | The unique institution-assigned identifier given to the dataset (e.g., `"cmems_mod_glo_phy_my_0.083deg_P1D-m"`). |
| `filename_prefix` | Optional | String | *None* | Custom prefix prepended to all output or downloaded filenames. |
| `schedule` | Required | Array of Strings | *None* | Temporal frequency for checking data source updates (separate from `dataset_temporal_scope`). |
| `dataset_temporal_scope` | Required | String | `"daily"`, `"monthly"` | Target chunk duration or temporal resolution for atomic output datasets. |
| `time_range` | Required | Array | *None* | Bounds mapping in ISO 8601 string format `[start, end]`. Use `"*"` for the earliest or latest available boundaries (e.g., `["1993-01-01", "*"]`). |
| `dataset_variables` | Optional | Array of Strings | *None* | List of specific parameters/fields targeted for import, matching the data source conventions (e.g., `["chlor_a", "sea_water_salinity"]`). |
| `latitude` | Optional | Array of Floats | *None* | Latitudinal bounding box coordinates formatted as `[min_latitude, max_latitude]`. Ranges: -90.0 to 90.0. |
| `longitude` | Optional | Array of Floats | *None* | Longitudinal bounding box coordinates formatted as `[min_longitude, max_longitude]`. Ranges: -180.0 to 180.0. |
| `base_url` | Optional (ERDDAP) | String | *None* | Root web link endpoint used to build API requests for ERDDAP servers. |
| `output_format` | Optional (ERDDAP) | String | `"nc"` | File download format (e.g., `"nc"` for NetCDF, `"csv"`, etc.). |
| `dap_type` | Optional (ERDDAP) | String | `"griddap"` | ERDDAP access protocol layer, commonly `"griddap"` or `"tabledap"`. |
| `dimensions` | Optional (ERDDAP) | Array of Strings | *None* | Coordinate dimensions required for multidimensional queries (e.g., `["time", "latitude", "longitude"]`). |

### 2.3. The `transform_dataset` Block

The `transform_dataset` block handles the execution parameters required for running downstream analysis, data cleaning, or custom modeling algorithms directly after data extraction. This block registers the processing framework, remote or local source code repositories, and the required execution arguments to establish absolute data provenance.

| Key | Required / Optional | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `mnt1_import` | Required | String | *None* | Source dataset directory containing the raw input files, relative to the mounted drive root directory. |
| `mnt3_processed` | Required | String | *None* | Output directory where transformed results, figures, or aggregated data are saved, relative to the mounted drive root directory. |
| `template_application_location_type` | Required | String | `"local"` | Specifies how or where the analysis code environment is executed. Allowed options include `"r-container"`, `"github"`, or `"local"`. |
| `template_app_entrypoint` | Required | String | *None* | The target handler script name used to execute the application (e.g., `"dissolved_oxygen.R"` or `"process_spatial_averages.py"`). |
| `template_application_repo` | Optional | String / Null | `null` | Reference identifier for localized version-controlled environments where applicable. |
| `github_repo_url` | Optional | String / Null | `null` | The remote GitHub repository URL holding the source code branch used for the transformation. |
| `template_app_arguments` | Optional | Object | *None* | Key-value pairs passed as parameters directly to the script at runtime (such as input overrides or targeted variable names). |

---

## 3. Configuration Examples

Below are standard compliant templates for configuring COPERNICUS MARINE (GLORYS) and NOAA CoastWatch (ERDDAP) workflow endpoints.

### Example 1: Copernicus Marine (GLORYS) Dataset

This example executes a daily workflow that checks for new daily data updates, subsets the global model to a specific latitudinal/longitudinal bounding box over the Northeast Shelf, and extracts four distinct physical oceanography variables into single-variable NetCDF files.

```json
[
  {
    "GLORYS": [
      {
        "workflow": {
          "workflow_name": "CMEMS_GLORYS_DAILY",
          "steps": [
            "validate_data_source",
            "import_dataset"
          ],
          "schedule": ["daily"],
          "source_type": "glorys"
        },
        "import_dataset": {
          "one_variable_per_file": true,
          "batch_import": true,
          "mnt1_import": "/GLORYS_DEMO/SOURCE/NES_PHY_001_024/",
          "project_name": "GLORYS_PHYSICS_REANALYSIS_FORECAST",
          "filename_prefix": "GLORYS_PHY_001",
          "schedule": ["daily"],
          "dataset_temporal_scope": "daily",
          "time_range": ["1993-01-01", "*"],
          "dataset_variables": [
            "sea_water_potential_temperature_at_sea_floor",
            "ocean_mixed_layer_thickness_defined_by_sigma_theta",
            "sea_water_salinity",
            "sea_water_potential_temperature"
          ],
          "latitude": [22.5, 48.4],
          "longitude": [-82.5, -51.5],
          "dataset_id": "cmems_mod_glo_phy_my_0.083deg_P1D-m"
        }
      }
    ]
  }
]

```

### Example 2: NOAA CoastWatch (ERDDAP) Dataset

This example executes a daily workflow constraint that targets a fixed historical time-slice via an external ERDDAP network, querying specific multidimensional coordinate dimensions to extract and download a single chlorophyll variable into a NetCDF format.

```json
[
  {
    "ERDDAP_WORKFLOW": [
      {
        "workflow": {
          "workflow_name": "COASTWATCH_CHLOR-A_DAILY",
          "steps": [
            "import_dataset"
          ],
          "schedule": ["daily"],
          "source_type": "erddap",
          "log_folder_path": "./logger"
        },
        "import_dataset": {
          "one_variable_per_file": true,
          "batch_import": false,
          "mnt1_import": "/COASTWATCH_DEMO/SOURCE/NES_4KM_CHLOR_A_DAILY/",
          "dataset_id": "noaacwNPPN20S3ASCIDINEOF2kmDaily",
          "filename_prefix": "ERDDAP",
          "base_url": "https://coastwatch.noaa.gov",
          "output_format": "nc",
          "dap_type": "griddap",
          "dataset_variables": [
            "chlor_a"
          ],
          "dimensions": [
            "time",
            "latitude",
            "longitude"
          ],
          "time_range": [
            "2025-01-09",
            "2025-02-11"
          ],
          "latitude": [22.5, 48.4],
          "longitude": [-82.5, -51.5]
        }
      }
    ]
  }
]

```
### Example 3: Automated R-Container Transformation (FISHBOT Dissolved Oxygen)

This profile executes a monthly workflow designed exclusively to run post-processing computations, pulling a custom analysis script directly from GitHub into a containerized R environment to calculate monthly averages from raw files stored in mount 1 and output the results to mount 3.

```json
[
  {
    "FISHBOT_TRANSFORM_WORKFLOW": [
      {
        "workflow": {
          "workflow_name": "FISHBOT_DISSOLVED-O2_MONTHLY",
          "steps": [
            "transform_dataset"
          ],
          "schedule": ["monthly"],
          "source_type": "erddap"
        },
        "transform_dataset": {
          "mnt1_import": "/FISHBOT/SOURCE/NRT/DISS02/",
          "mnt3_processed": "/FISHBOT/PRODUCT/NRT/monthly/",
          "template_application_location_type": "r-container",
          "template_app_entrypoint": "dissolved_oxygen.R",
          "template_application_repo": null,
          "github_repo_url": "https://github.com/GITHUB-USERNAME/dissolved-oxygen-avg",
          "template_app_arguments": {
            "param1_name": "argument_value",
            "param2_name": "mnt1_value"
          }
        }
      }
    ]
  }
]

```
---

## 4. Environment File Setup (`.env`)

To supplement your workflow configurations without exposing private data or hardcoding local storage structures, you must establish an environment configuration file.

Create a copy of the `.env-example` file located in the root directory of your cloned application repository, rename it to `.env`, and populate the variables using the formatting below.

### Key Environment Parameters

* **`MNT_ONE`**: Maps the default system mount directory used by workflows to resolve relative paths for `mnt1_import`.
* **`LOGGER_DIR`**: Defines where application-wide activity traces are stored if no localized path is passed to the workflow block.
* **`CM_USERNAME` / `CM_PASSWORD**`: Secures your access credentials for workflows that communicate with protected servers (such as Copernicus Marine API endpoints).

### Environment Template Formats

You can configure your environment variables using standard flat text format or JSON, depending on your system execution requirements. This .env file should be stored in the root directory of your cloned Automation Template:

#### Option A: Standard Key-Value Text Format (`.env`)

```text
EXAMPLE=foobar
MNT_ONE=./mnt1
LOGGER_DIR=./logger
CM_USERNAME=your_username
CM_PASSWORD=your_secure_password

```

#### Option B: JSON Context Format (`.env.json`)

```json
{
  "EXAMPLE": "foobar",
  "MNT_ONE": "./mnt1",
  "LOGGER_DIR": "./logger",
  "CM_USERNAME": "your_username",
  "CM_PASSWORD": "your_secure_password!"
}

```



