---
layout: default
title: Terminology & Glossary
---

[← Back to Home](./workflow.md)


## Core Components of a Configuration

Each configuration file represents its own **Project**. A Project is a container that holds one or more **Workflows**. Each workflow is a custom pipeline built by choosing specific building blocks (steps) and providing the technical details required to execute them.

> *Think of it like a modular assembly line: you pick the stations (steps) and then provide the technical manual (details) for each station.*

A standard configuration entry is divided into three primary functional areas:

1. **The Workflow Definition (`workflow`)** This is the "ID card" of your process. It specifies:
* What the process is called (`workflow_name`).
* Which actions to take (`steps`). If you list `["all"]`, the system executes every stage from data ingestion to final analysis.
* When to run (`schedule`).
* Where the code logic lives (`template_script_url`).


2. **Functional Details (`import`, `template`, `transfer`)** These blocks provide the execution details for the steps you selected. You only include the blocks that correspond to your active steps:
* `import_details`: Required if you are fetching data. It defines the coordinates, dates, and dataset IDs of the raw data.
* `template_details`: Required if you are running a script. This maps raw data to specific variables (`params`) and defines the target processing timeframe.
* `transfer_details`: Required if output data needs to be delivered to a external destination that the application has credentials to access.



 
[← Back to Home](./workflow.md) | [Proceed to Installation](./installation.md)