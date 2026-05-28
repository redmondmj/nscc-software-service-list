import json
import os
import sys
import time
import argparse
from playwright.sync_api import sync_playwright

FORM_URL = "https://forms.office.com/Pages/ResponsePage.aspx?id=etmbxRtLq02JrKCrao5ENZS3ZWR4PuZOmfOuxrEnO1hUMUZGVlc4TDdTUERUT004RzhLSUVXWTIxVS4u&origin=Invitation&channel=0"
AUTH_FILE = "auth_state.json"
INVENTORY_FILE = "software_inventory.json"
LOG_FILE = "submission_log.csv"

def run_login():
    print("=== Launching Browser for Login ===")
    print("A browser window will open. Please sign in with your NSCC credentials.")
    print("Once you are fully signed in and see the form questions, return to this console.")
    
    with sync_playwright() as p:
        # Launch headful browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto(FORM_URL)
        
        # Wait for user to log in and press Enter in the console
        input("\n--> Press ENTER here in the console AFTER you have logged in and see the form questions... ")
        
        # Save storage state
        context.storage_state(path=AUTH_FILE)
        print(f"Success! Session state saved to {AUTH_FILE}")
        browser.close()

def match_field_and_fill(page, container, title, item_data):
    """
    Fills out the input element inside a question container based on the question title text.
    """
    # Clean the title text
    clean_title = re.sub(r'^\d+\.\s*', '', title).strip().lower()
    clean_title = re.sub(r'\*$', '', clean_title).strip() # Remove required asterisk
    
    # Let's inspect the inputs available in this container
    text_input = container.locator('input:not([type="radio"]):not([type="checkbox"])')
    textarea = container.locator('textarea')
    radios = container.locator('input[type="radio"]')
    checkboxes = container.locator('input[type="checkbox"]')
    
    # Question 1: Campus
    if "campus" in clean_title:
        # Default to "Truro"
        campus_val = "Truro"
        # Find option matching "Truro"
        labels = container.locator('label').all()
        for label in labels:
            if "truro" in label.inner_text().strip().lower():
                label.click()
                print("  Campus -> Selected 'Truro'")
                return True
        return False

    # Question 2: Software/Service name and Version
    if "software/service name and version" in clean_title or ("software/service name" in clean_title and "version" in clean_title):
        name = item_data.get("Software Name", "")
        version = item_data.get("Version", "")
        value = f"{name} {version}".strip() if version else name
        if text_input.count() > 0:
            text_input.fill(value)
            print(f"  Software Name & Version -> Filled: '{value}'")
            return True
        return False

    # Question 3: Vendor/Provider
    if "vendor/provider" in clean_title or ("vendor" in clean_title and "provider" in clean_title):
        value = item_data.get("Vendor/Provider", "")
        if text_input.count() > 0:
            text_input.fill(str(value))
            print(f"  Vendor/Provider -> Filled: '{value}'")
            return True
        return False

    # Question 4: License type
    if "license type" in clean_title or "licensing" in clean_title:
        inv_license = str(item_data.get("License Type (Perpetual, Subscription, Client/Server,Free, Open Source, etc.)", "")).lower()
        target_option = None
        if "subscription" in inv_license:
            target_option = "Annual Subscription"
        elif "open source" in inv_license or "gpl" in inv_license or "lgpl" in inv_license or "busl" in inv_license or "sspl" in inv_license:
            target_option = "Open Source"
        elif "free" in inv_license or "proprietary" in inv_license:
            target_option = "Free"
        elif "perpetual" in inv_license:
            target_option = "Perpetual"
        elif "client" in inv_license or "server" in inv_license:
            target_option = "Client/Server"
        
        # Click the matched radio button
        labels = container.locator('label').all()
        if target_option:
            for label in labels:
                if target_option.lower() in label.inner_text().strip().lower():
                    label.click()
                    print(f"  License Type -> Selected: '{target_option}' (Mapped from '{inv_license}')")
                    return True
        # Fallback to "Free" or first option if not matched
        if labels:
            fallback = labels[2] if len(labels) > 2 else labels[0] # Try to choose Free or first
            fallback.click()
            print(f"  License Type -> Fallback Selected: '{fallback.inner_text().strip()}'")
            return True
        return False

    # Question 5: Program(s)
    if "program(s) does this software serve" in clean_title or ("program" in clean_title and "notes" not in clean_title):
        # Check "IT Systems Management and Security" if "systems management" or "itsm" is in the program
        inv_program = str(item_data.get("What Program(s) does this software serve?", "")).lower()
        labels = container.locator('label').all()
        for label in labels:
            lbl_text = label.inner_text().strip().lower()
            if "systems management" in lbl_text:
                if "systems management" in inv_program or "itsm" in inv_program:
                    input_el = label.locator('input[type="checkbox"]')
                    if not input_el.is_checked():
                        label.click()
                    print("  Program -> Checked 'IT Systems Management and Security'")
                    return True
        return False

    # Question 6: Course/module/project
    if "course/module/project" in clean_title or "course" in clean_title:
        value = item_data.get("What is the specific course/module/project you are using this software for?", "")
        if text_input.count() > 0:
            text_input.fill(str(value))
            print(f"  Courses -> Filled: '{value}'")
            return True
        return False

    # Question 7: Number of Licenses/Users
    if "number of licenses" in clean_title or "licenses/users" in clean_title:
        value = item_data.get("Number of Licenses/Users (Only if known)", "")
        if text_input.count() > 0:
            text_input.fill(str(value))
            print(f"  Number of Licenses -> Filled: '{value}'")
            return True
        return False

    # Question 8: Cost
    if "cost" in clean_title:
        value = item_data.get("Cost (only if known)", "")
        if text_input.count() > 0:
            text_input.fill(str(value))
            print(f"  Cost -> Filled: '{value}'")
            return True
        return False

    # Question 9: Specific Classrooms
    if "specific classrooms" in clean_title or "classrooms" in clean_title:
        value = item_data.get("Specific Classrooms you intend to use software in. (If on-prem software)", "")
        if text_input.count() > 0:
            text_input.fill(str(value))
            print(f"  Classrooms -> Filled: '{value}'")
            return True
        return False

    # Question 10: Scope of use
    if "scope of use" in clean_title or "scope" in clean_title:
        inv_scope = str(item_data.get("Scope  (lab, faculty, student, cloud, all)", "")).lower()
        labels = container.locator('label').all()
        matched_any = False
        for label in labels:
            lbl_text = label.inner_text().strip().lower()
            should_check = False
            if "all" in inv_scope:
                should_check = True
            elif "lab" in lbl_text and "lab" in inv_scope:
                should_check = True
            elif "faculty" in lbl_text and "faculty" in inv_scope:
                should_check = True
            elif "student" in lbl_text and "student" in inv_scope:
                should_check = True
            elif "cloud" in lbl_text and "cloud" in inv_scope:
                should_check = True
            
            if should_check:
                input_el = label.locator('input[type="checkbox"]')
                if not input_el.is_checked():
                    label.click()
                print(f"  Scope of use -> Checked '{label.inner_text().strip()}'")
                matched_any = True
        return matched_any

    # Question 11: Notes/Comments
    if "notes/comments" in clean_title or "notes" in clean_title or "comments" in clean_title:
        value = item_data.get("Notes/Comments/Special Requirements", "")
        if text_input.count() > 0:
            text_input.fill(str(value))
            print(f"  Notes -> Filled: '{value}'")
            return True
        return False

    # Question 12: Already being used
    if "already being used" in clean_title or "already used" in clean_title or "existing" in clean_title:
        value = str(item_data.get("Is this a software or service that is already being used?", "")).lower()
        labels = container.locator('label').all()
        for label in labels:
            lbl_text = label.inner_text().strip().lower()
            if value == "yes" and lbl_text == "yes":
                label.click()
                print("  Already used -> Selected 'Yes'")
                return True
            elif value == "no" and lbl_text == "no":
                label.click()
                print("  Already used -> Selected 'No'")
                return True
        return False
        
    return False

import re

def get_submitted_software():
    submitted = set()
    if os.path.exists(LOG_FILE):
        import csv
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                # Skip header
                next(reader, None)
                for row in reader:
                    if len(row) >= 3 and row[2] == "Success":
                        submitted.add(row[1])
        except Exception as e:
            print(f"Warning: Could not read submission log: {e}")
    return submitted

def run_submit(headful=False, confirm_each=False, dry_run=False):
    if not os.path.exists(AUTH_FILE):
        print(f"Error: Authentication file '{AUTH_FILE}' not found. Please run with --login first.")
        sys.exit(1)
        
    if not os.path.exists(INVENTORY_FILE):
        print(f"Error: Inventory file '{INVENTORY_FILE}' not found. Please run compile_inventory.py first.")
        sys.exit(1)
        
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        inventory = json.load(f)
        
    print(f"Loaded {len(inventory)} software items for submission.")
    
    # Check already submitted items to prevent duplicates
    submitted_items = get_submitted_software()
    if submitted_items:
        print(f"Detected {len(submitted_items)} successfully submitted items in log.")
    
    # Prepare logs
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("Timestamp,Software Name,Status,Details\n")
            
    with sync_playwright() as p:
        print(f"Launching browser (headless={not headful})...")
        browser = p.chromium.launch(headless=not headful)
        context = browser.new_context(storage_state=AUTH_FILE)
        page = context.new_page()
        
        # If dry run, we only test the first unsubmitted item
        if dry_run:
            unsubmitted = [item for item in inventory if item["Software Name"] not in submitted_items]
            items_to_submit = [unsubmitted[0]] if unsubmitted else [inventory[0]]
        else:
            items_to_submit = inventory
            
        for idx, item in enumerate(items_to_submit):
            name = item["Software Name"]
            
            if not dry_run and name in submitted_items:
                print(f"--- [{idx+1}/{len(items_to_submit)}] Skipping: {name} (already submitted) ---")
                continue
                
            print(f"\n--- [{idx+1}/{len(items_to_submit)}] {'[DRY RUN]' if dry_run else 'Submitting'}: {name} ---")
            
            page.goto(FORM_URL)
            
            # Wait for form or check if we are redirected to login
            page.wait_for_timeout(2000) # Basic wait for redirect
            if "login" in page.url.lower() or "signin" in page.url.lower():
                print("Error: Session expired or invalid. Please re-authenticate using --login.")
                break
                
            # Wait for questions to load
            try:
                page.wait_for_selector('div[data-automation-id="questionItem"]', timeout=15000)
            except Exception as e:
                print("Error: Question container not found. The form failed to render or session is invalid.")
                # Save screenshot
                page.screenshot(path="error_page.png")
                print("Saved error screenshot to error_page.png")
                break
                
            # Find all question containers
            containers = page.locator('div[data-automation-id="questionItem"]').all()
            print(f"Found {len(containers)} questions on the form.")
            
            # Fill out each question
            for container in containers:
                title_el = container.locator('[data-automation-id="questionTitle"]')
                if title_el.count() > 0:
                    title_text = title_el.inner_text()
                    match_field_and_fill(page, container, title_text, item)
                    
            if dry_run:
                # In dry run mode, we take a screenshot of the filled form and do not submit!
                screenshot_path = f"dry_run_filled_{name.replace(' ', '_').replace('/', '_')}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"  [Dry Run Success] Form fields populated successfully. Screenshot saved to: {screenshot_path}")
                break
                
            # Submit flow
            if confirm_each:
                input("\n--> Fields populated. Press ENTER in this console to submit this response... ")
                
            # Click Submit button
            submit_btn = page.locator('button:has-text("Submit"), [data-automation-id="submit-button"]').first
            submit_btn.click()
            
            # Wait for success screen
            page.wait_for_timeout(2000)
            success_selector = '.thank-you-page, div:has-text("submitted"), div:has-text("Thank you")'
            success = False
            try:
                page.wait_for_selector(success_selector, timeout=8000)
                print("  [Success] Submitted successfully!")
                success = True
                status_str = "Success"
                detail_str = ""
            except Exception as e:
                print("  [Warning] Did not detect default success page. Checking URL or content...")
                # Fallback check
                body_text = page.locator('body').inner_text()
                if "submitted" in body_text.lower() or "thank" in body_text.lower():
                    print("  [Success] Submission detected via page text!")
                    success = True
                    status_str = "Success"
                    detail_str = "Detected via text fallback"
                else:
                    print("  [Error] Submission verification failed.")
                    page.screenshot(path=f"fail_{name.replace(' ', '_')}.png")
                    status_str = "Failed"
                    detail_str = "Verification timed out"
                    
            # Log results
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f'"{timestamp}","{name}","{status_str}","{detail_str}"\n')
                
            # Small cooldown
            time.sleep(1)
            
        browser.close()
        print(f"\n=== Form {'dry-run' if dry_run else 'submissions'} process completed ===")

def main():
    parser = argparse.ArgumentParser(description="NSCC Software Registry Form Automator")
    parser.add_argument("--login", action="store_true", help="Launch browser to log in and save session")
    parser.add_argument("--submit", action="store_true", help="Submit all compiled software items using saved session")
    parser.add_argument("--dry-run", action="store_true", help="Populate fields for the first item and save a screenshot without submitting")
    parser.add_argument("--headful", action="store_true", help="Run browser in headful mode during submissions")
    parser.add_argument("--confirm", action="store_true", help="Pause for user confirmation before submitting each item")
    
    args = parser.parse_args()
    
    if args.login:
        run_login()
    elif args.submit:
        run_submit(headful=args.headful, confirm_each=args.confirm)
    elif args.dry_run:
        run_submit(headful=args.headful, confirm_each=False, dry_run=True)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
