# Walkthrough - IT Software & Service Registry Project

We have successfully built and deployed the Software and Service Registry tool, compiled the data, generated the spreadsheet and report, and pushed the repository to GitHub.

## What Was Achieved

1. **Boilerplate & Version Control**:
   - Initialized Git and made the repository **public** on GitHub: [nscc-software-service-list](https://github.com/redmondmj/nscc-software-service-list).
   - Created a `.gitignore` to prevent any sensitive session tokens (`auth_state.json`) or local environment variables from being checked in.
   - Added a detailed `README.md` and `requirements.txt`.

2. **Data Compilation (`compile_inventory.py`)**:
   - Consolidated 43 software and service items.
   - Scanned all 130 downloaded Notion Course Content pages, curriculum mappings, and RTF documents to link each software item to the specific courses (e.g. `OSYS3030`, `NETW2710`) that use it.
   - Handled unknown fields (like cost and license numbers) by leaving them blank (`""`) per your instructions.

3. **Output Generation (`generate_outputs.py`)**:
   - **Spreadsheet**: Created a styled Excel spreadsheet `software_service_list.xlsx` with a custom Navy header, border grids, and auto-adjusted column widths.
   - **Program Report**: Created a detailed report `software_service_report.md` grouping software by domain (Virtualization, DevOps, Cloud, OS) with inferred tools and future recommendations (ELK Stack, GitHub Actions, Vault).

4. **Playwright Form Automation (`automate_forms.py`)**:
   - Created and successfully executed a script with support for:
     - `--login`: Opens a headful browser for a one-time sign-in to save authenticated cookies into `auth_state.json`.
     - `--dry-run`: Runs headless, populates the form for the first item, leaves empty fields blank, and saves a full-page verification screenshot (`dry_run_filled_*.png`) without submitting.
     - `--submit`: Batch submits all 43 software items.
   - **Submission Execution**: Successfully batch-submitted all **43** items to the MS Form on 2026-05-28, logging each successful response in `submission_log.csv`.

---

## File Locations

- Local Project Folder: [nscc-software-service-list](file:///c:/Users/redmo/OneDrive/Documents/GitRepos/nscc-software-service-list)
- Excel Spreadsheet: [software_service_list.xlsx](file:///c:/Users/redmo/OneDrive/Documents/GitRepos/nscc-software-service-list/software_service_list.xlsx)
- Markdown Program Report: [software_service_report.md](file:///c:/Users/redmo/OneDrive/Documents/GitRepos/nscc-software-service-list/software_service_report.md)
- Public GitHub Repository: [redmondmj/nscc-software-service-list](https://github.com/redmondmj/nscc-software-service-list)

---

## How to Test the Form Automator

When you are ready to test the form automation, run these commands in the project folder:

```bash
# 1. Capture your NSCC authenticated session
python automate_forms.py --login

# 2. Perform a dry-run test (populates the first item, saves a screenshot, and exits without submitting)
python automate_forms.py --dry-run
```
You can inspect the generated `dry_run_filled_*.png` screenshot to verify that all fields align perfectly.
