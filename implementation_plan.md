# Implementation Plan - IT Software & Service List Project

This plan outlines the design and execution steps to generate a comprehensive list of software and services for the IT Systems Management and Security program, create the required spreadsheet, write a summary report, automate the Microsoft Form submission, and set up a GitHub repository.

## User Review Required

> [!NOTE]
> **Plan Location**: The plan is managed by the AI assistant inside its App Data brain directory. However, we will copy this plan and other documentation directly into your project folder `c:\Users\redmo\OneDrive\Documents\GitRepos\nscc-software-service-list` so you can view it directly in your editor.

> [!IMPORTANT]
> **Form Authentication via Playwright**:
> To automate the NSCC-authenticated Microsoft Form:
> 1. We will write a script that opens a browser in "headful" mode once.
> 2. You will sign in with your NSCC credentials.
> 3. The script will save your session tokens/cookies to a local `auth_state.json` file.
> 4. Subsequent submissions will run in "headless" mode automatically, reusing this session state to submit the form for each software item.
> *No password or credentials will ever be saved in the codebase.*

## Open Questions

> [!NOTE]
> 1. **GitHub Visibility**: Do you want the GitHub repository to be **private** (default recommendation for school-specific data) or **public**?
> 2. **Default Values**: For fields in the spreadsheet and form where details are unknown (e.g., cost, exact license count), should we leave them blank, write "Unknown", or write "N/A"?
> 3. **Submission Confirmations**: Do you want the form automation script to submit the form immediately, or run in a semi-automated mode where it fills out the form and waits for your confirmation before clicking "Submit"?

## Proposed Changes

We will build the project inside the workspace directory `c:\Users\redmo\OneDrive\Documents\GitRepos\nscc-software-service-list`.

---

### Git & GitHub Repository Component

We will set up version control and document usage instructions.

#### [NEW] [README.md](file:///c:/Users/redmo/OneDrive/Documents/GitRepos/nscc-software-service-list/README.md)
A detailed overview of the tool, installation steps, and instructions on how to run the data compilation and form submission automation.

#### [NEW] [.gitignore](file:///c:/Users/redmo/OneDrive/Documents/GitRepos/nscc-software-service-list/.gitignore)
Standard Python/Node gitignore that explicitly includes rules to ignore session tokens (`auth_state.json`), local settings (`.env`), and compiled spreadsheets, preventing any security leaks.

#### [NEW] [Local Git & GitHub Repo Init]
We will run `git init`, commit the initial repository structure, and use `gh repo create` to push it to your GitHub account.

---

### Data Analysis & Compilation Component

We will consolidate and clean the software inventory from:
- `curriculum_extracted.json` (Curriculum outcomes)
- `notion_pages_content.json` (Lab content)
- Sibling CAF mapping spreadsheets

#### [NEW] [compile_inventory.py](file:///c:/Users/redmo/OneDrive/Documents/GitRepos/nscc-software-service-list/compile_inventory.py)
A script that parses the raw sources, maps software items to their respective courses, determines license types, scopes, and classrooms (where applicable), and outputs a clean consolidated `software_inventory.json` file.

---

### Output Generation Component

We will create scripts to generate the Excel spreadsheet and the Markdown report.

#### [NEW] [generate_outputs.py](file:///c:/Users/redmo/OneDrive/Documents/GitRepos/nscc-software-service-list/generate_outputs.py)
A Python script using `pandas` or `openpyxl` that reads `software_inventory.json` and creates:
- `software_service_list.xlsx`: The spreadsheet with the requested fields.
- `software_service_report.md`: A detailed Markdown report summarizing the findings, inferences, and future needs.

---

### Form Automation Component

We will write a Node.js or Python Playwright script to automate MS Forms filling.

#### [NEW] [automate_forms.py](file:///c:/Users/redmo/OneDrive/Documents/GitRepos/nscc-software-service-list/automate_forms.py)
A Python script using `playwright` that:
1. Provides a `--login` mode to capture user session cookies.
2. Reads the `software_inventory.json` and submits the MS Form for each item.
3. Logs submission status (success/failure) to `submission_log.csv`.

---

## Verification Plan

### Automated Verification
- Verify `software_inventory.json` matches all required fields.
- Verify `software_service_list.xlsx` matches the requested columns exactly.
- Verify the Playwright script can load the form using `auth_state.json`.

### Manual Verification
- Review `software_service_report.md` for completeness.
- Review a single draft test submission on the MS Form before running the full batch.
- Check that the remote repository on GitHub is initialized correctly.
