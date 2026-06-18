---
layout: default
title: Logs and Auditing Mechanics
---

[← Back to Home](/)

# Logs and Auditing Mechanics

This page explains how to parse diagnostic log outputs and handle errors when a workflow halts unexpectedly.

### Common Errors Cheat Sheet

If your process stops, cross-reference the last line of your terminal output against this table:

| Error Message | What It Means | How to Fix It |
| :--- | :--- | :--- |
| `FileNotFoundError` | The tool cannot locate your file. | Check your file name spelling in the custom config settings layer. |
| `PermissionError` | The target Excel/CSV file is open. | Close the data spreadsheet in Excel and re-run the script. |
| `ModuleNotFoundError` | A required tool library is missing. | Re-run the environment installation setup step. |

### System Audits

The application tracks run cycles inside automated transaction histories. Logs are written continuously to the `/logs/app.log` pipeline registry.

---
[← Back to Home](/)