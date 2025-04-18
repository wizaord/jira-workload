# JIRA-WORKLOAD

Project to extract from JIRA the workload assigned to a component. Extract the workload to an excel file.

# Requirements

## Step 1 - Create environment (linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 1 - Create environment (Windows)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 - Create a `.env` file

Copy the `configuration_template.ini` file to `configuration.ini` file and fill in the necessary information.

## Step 3 - Run the application (Linux)

```bash
python3 src/main/window.py
```
## Step 3 - Run the application (Windows)

```bash
python src/main/window.py
```

## Bonus : Créer un exécutable
### Windows

```bash
pyinstaller --onefile --windowed src/main/window.py
```

