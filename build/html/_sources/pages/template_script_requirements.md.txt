

# End-User Script Templating and Deployment Instructions

To ensure your script integrates successfully with the application workflow, follow this mandatory preparation and testing protocol.

## 1. Script Benchmarking and Initialization

Before templating, the script must pass a "solo" benchmark. It must execute from start to finish in a clean environment without manual intervention or IDE-specific features.

* **Remove Hardcoded Paths:** Replace all local absolute paths with dynamic variables.
* **Dependency Management:** Do not include `install.packages()` or `pip install` calls within the script.
* **R:** Dependencies must be managed via the premade `renv` environment mounted to the application container.
* **Python:** Dependencies must exist within the container's pre-configured Python environment.


* **Terminal Execution:** The script must be fully executable via the terminal (e.g., `Rscript my_script.R` or `python my_script.py`).

## 2. Mandatory Mount Points

The application communicates with your script using three standardized variables. You must configure your script to accept these as command-line arguments:

* **`mnt1` (Inputs):** Directory containing raw data or files that trigger the workflow.
* **`mnt2` (Supplementary):** Directory for static resources (e.g., lookup tables, species codes, coefficients).
* **`mnt3` (Outputs):** Directory where all produced files (e.g., CSVs, plots, logs) must be saved.

### Python Implementation Example

```python
import sys
import os

# Usage: python script.py /path/to/mount1 /path/to/mount2 /path/to/mount3
if len(sys.argv) < 4:
    print("Error: Missing required mount arguments.")
    sys.exit(1)

mount1, mount2, mount3 = sys.argv[1:4]
input_file = os.path.join(mount1, "data.csv")

```

### R Implementation Example

> **Note:** The `args` named list is automatically injected by the system.

```r
# Example structure of the provided system list: 
# args <- list(mnt1 = "/path/to/mount1", mnt2 = "/path/to/mount2", mnt3 = "/path/to/mount3") 

# Extract paths from the provided list using the system's named keys 
mount1_path <- args[["mnt1"]] 
mount2_path <- args[["mnt2"]] 
mount3_path <- args[["mnt3"]] 

# Alternatively, you can access them directly using the `$` operator:
# input_file <- file.path(args$mnt1, "data.csv") 
input_file <- file.path(mount1_path, "data.csv")

```

## 3. Error Handling and Annotation

* **Fail-Fast Logic:** Implement validation checks to ensure input files exist before processing.
* **Try-Except / TryCatch Blocks:** Wrap volatile operations in error-handling blocks to provide meaningful logs.
* **Annotation:** Include a header block defining the script's purpose, inputs, and outputs. Document the "why" behind complex logic.
* **Rollout Considerations:**
* Ingest and log errors for now to observe runtime behavior and identify common failure modes.
* Define the scope for user-facing error notifications.
* Implement versioning for data pulls to handle commercial data import failures gracefully.



### Warnings vs. Failures

Scripts should log clear status updates to distinguish between non-critical anomalies and critical failures:

* **Warnings (Skippable Steps):** An analysis step that can be skipped should log a warning rather than crash. *Example:* A script creating weekly plots only has 6 datasets available because an upstream data source does not update on Sundays. The scheduled run will safely prompt the script again the following week.
* **Failures (Critical Crashes):** Immediate termination is required for unrecoverable issues such as corrupt data sources, exceeding memory/storage limits, or a complete failure to generate outputs.

## 4. Container Environment Validation

Your script must be tested within the dedicated R or Python container environment referenced by the application to ensure library compatibility.

> 📋 **Status Note:** The dedicated R testing environment is currently in development with IT. Updates will be provided once this environment is live for user testing.

* **Environment Parity:** Until the testing environment is finalized, coordinate directly with Christina to manually verify package versions within the `renv` mount.

## 5. Self-Code Audit

Prior to deployment, perform a final self-audit:

* **Hardcode Check:** Verify that no local absolute paths or personal credentials remain in the code.
* **Library Hygiene:** Ensure all imports are grouped at the top of the script and correspond strictly to the container environment.
* **Output Verification:** Confirm the script writes files **exclusively** to `mount3`.
* **Exit Codes:** Use `sys.exit(1)` (Python) or `stop()` (R) to ensure the script explicitly returns a non-zero exit status upon failure.

## 6. Deployment and Configuration

* **GitHub:** Push the finalized script to your designated repository.
* **Branching Strategy:** You may use specific branches (e.g., `dev` or `workflow-template`) in your configuration file. This allows you to update the template without conflicting with your `main` branch.
* **Configuration File:** Complete the associated workflow configuration file. Ensure the repository URL and branch name point precisely to the location of your audited code.

