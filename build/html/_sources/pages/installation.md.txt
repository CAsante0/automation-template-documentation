---
layout: default
title: Installation
---


---
[← Back to Home](./workflow.md)

# Installation

## Environment Set Up for Local Runs

To run the Automation Template on your local machine, you must configure an environment capable of supporting the dependent libraries and software. For deployment inside a containerized setup.

### Requirements

- An installation of **Conda / Miniconda** OR a **Python Virtual Environment (`virtualenv`)**
  > **Note:** If you choose `virtualenv`, you must be prepared to download any system dependencies required for running the application.
- A cloned version of the **Automation Template** repository
- **Python 3.13.3**
- An **IDE** with a Python interpreter configured (e.g., Visual Studio Code, PyCharm, etc.)


---
### Option 1: Conda Environment

1. Open your terminal or Conda prompt.
2. Navigate to the root directory of your cloned Automation Template repository (which contains the `environment.yaml` file):
   ```bash
   cd path/to/your/project

```

3. Inspect the `environment.yaml` file to check the name of the environment and the Python version specified.
4. Create the Conda environment using the file. Conda will read the dependencies and spin up the environment:
```bash
conda env create -f environment.yaml

```


5. Activate the new environment after creation is complete:
```bash
conda activate automation-template-env

```


6. Verify the Python version within the active environment to confirm it is running Python 3.13:
```bash
python --version

```



---

### Option 2: Python virtualenv

1. Open your Terminal or Command Prompt.
2. Navigate to the root directory of the cloned Automation Template using the `cd` command:
```bash
cd path/to/your/project

```


3. Create the Virtual Environment using the Python built-in `venv` module. Replace `my_env` with your desired environment name (common conventions use `venv` or `.venv`):
```bash
python3 -m venv my_env

```


*Note: Depending on your system configuration, you might need to use `python` instead of `python3`.*

#### Activation Steps (Required before installing packages)

The command to activate the environment differs based on your operating system and shell environment:

* **macOS and Linux (Bash/Zsh):**
```bash
source my_env/bin/activate

```


* **Windows (Command Prompt):**
```cmd
my_env\Scripts\activate.bat

```



#### Installing Dependencies (After Activation)

With the environment activated, you can install the required packages using `pip`. They will only be installed within this isolated environment:

```bash
pip install -r requirements.txt

```

#### Deactivating the Environment

When you are finished working, simply run:

```bash
deactivate

```

---

### Installing Dependencies from a `requirements.txt` (Using Pip)

Once your Conda environment is active or you have initialized your Python virtual environment, you can use `pip` to install any additional packages listed in the `requirements.txt` file located in the root directory.

1. Ensure the `requirements.txt` file is in your current working directory.
2. Run the `pip install` command to read the file and update your active environment:
```bash
pip install -r requirements.txt

```



---

[← Back to Home](./index.md) | [Proceed to Writing a Workflow](./config_guide.md)

```

```