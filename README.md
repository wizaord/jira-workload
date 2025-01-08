# JIRA-WORKLOAD

Project to extract from JIRA the workload assigned to a component. Extract the workload to an excel file.

# Requirements

## Step 1 - Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 2 - Create a `.env` file

Copy the `configuration_template.ini` file to `configuration.ini` file and fill in the necessary information.

## Step 3 - Run the application

```bash
python3 src/main/workload_extract.py
```
