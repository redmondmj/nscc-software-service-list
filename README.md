# NSCC IT Systems Management & Security - Software & Service Registry Tool

This project compiles a comprehensive list of all software and services required by students throughout the two-year **IT Systems Management and Security** diploma program at NSCC. It extracts data from program curriculum outcomes, local mapping spreadsheets, and a Notion course content database.

Additionally, it automates the tedious task of registering each software item on the institutional Microsoft 365 Software Registry Form.

## Features

- **Multi-Source Parsing**: Extracts software tools from Notion course database logs, curriculum outcome PDFs/RTFs, and military credit transfer (CAF) alignment spreadsheets.
- **Data Export**: Outputs a structured spreadsheet (`software_service_list.xlsx`) matching all required fields, alongside a clean Markdown summary report.
- **Form Automation**: Automates filling out the Microsoft Form for each software item using Playwright, reusing your authenticated Office 365 session state safely.

---

## Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- **pip** (Python Package Installer)

### 2. Install Dependencies
Clone the repository and install the required libraries:
```bash
pip install -r requirements.txt
```
*Note: A virtual environment is highly recommended.*

### 3. Initialize Playwright
Install the required browser engines for automation:
```bash
playwright install chromium
```

---

## Usage Instructions

### Step 1: Compile the Software Inventory
Run the parser to scan your course logs and curriculum data. This generates `software_inventory.json`:
```bash
python compile_inventory.py
```

### Step 2: Generate Spreadsheet and Report
Generate the Excel spreadsheet (`software_service_list.xlsx`) and the summary report (`software_service_report.md`):
```bash
python generate_outputs.py
```

### Step 3: Automate Microsoft Form Submissions
Because the MS Form requires NSCC authentication, the script uses a two-phase process:

1. **Log In and Save Session**:
   Run the login script. A browser window will open. Sign in with your NSCC credentials. Once logged in, close the browser. The script will save your session tokens to a secure local file `auth_state.json`:
   ```bash
   python automate_forms.py --login
   ```

2. **Run Batch Submissions**:
   Run the submission script. It will run in the background (headless mode) and submit the form for each compiled item, logging results to `submission_log.csv`:
   ```bash
   python automate_forms.py --submit
   ```

---

## Folder Structure

- `compile_inventory.py`: Parses the Notion data and RTF files to compile a consolidated software list.
- `generate_outputs.py`: Generates the final Excel file and Markdown report.
- `automate_forms.py`: Playwright script to log in and submit the form for each item.
- `implementation_plan.md`: The approved project plan.
- `.gitignore`: Configured to exclude sensitive session state (`auth_state.json`) and local configurations.
