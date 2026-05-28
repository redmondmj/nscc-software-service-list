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
    
    # Define mappings from form question titles (lowercase substrings) to our inventory keys
    field_mappings = {
        "software name": "Software Name",
        "name of software": "Software Name",
        
        "version": "Version",
        
        "vendor": "Vendor/Provider",
        "provider": "Vendor/Provider",
        
        "your name": "Your Name",
        "name": "Your Name",
        
        "program": "What Program(s) does this software serve?",
        
        "course": "What is the specific course/module/project you are using this software for?",
        "module": "What is the specific course/module/project you are using this software for?",
        "project": "What is the specific course/module/project you are using this software for?",
        
        "license type": "License Type (Perpetual, Subscription, Client/Server,Free, Open Source, etc.)",
        "licensing": "License Type (Perpetual, Subscription, Client/Server,Free, Open Source, etc.)",
        
        "number of licenses": "Number of Licenses/Users (Only if known)",
        "users": "Number of Licenses/Users (Only if known)",
        "licenses": "Number of Licenses/Users (Only if known)",
        
        "scope": "Scope  (lab, faculty, student, cloud, all)",
        
        "classroom": "Specific Classrooms you intend to use software in. (If on-prem software)",
        "lab": "Specific Classrooms you intend to use software in. (If on-prem software)",
        
        "already being used": "Is this a software or service that is already being used?",
        "already used": "Is this a software or service that is already being used?",
        "existing": "Is this a software or service that is already being used?",
        
        "cost": "Cost (only if known)",
        
        "notes": "Notes/Comments/Special Requirements",
        "comments": "Notes/Comments/Special Requirements",
        "special requirements": "Notes/Comments/Special Requirements"
    }
    
    matched_key = None
    for kw, inventory_key in field_mappings.items():
        if kw in clean_title:
            matched_key = inventory_key
            break
            
    if not matched_key:
        print(f"  [Warning] Could not match question: '{title}'")
        return False
        
    value = item_data.get(matched_key, "")
    if str(value).strip() == "":
        print(f"  Matching: '{title}' -> Key: '{matched_key}' -> Leaving blank")
        # Clear the field if it was pre-filled (some textboxes might have placeholders or default values)
        text_input = container.locator('input[type="text"]')
        textarea = container.locator('textarea')
        if text_input.count() > 0:
            text_input.fill("")
        elif textarea.count() > 0:
            textarea.fill("")
        return True
        
    print(f"  Matching: '{title}' -> Key: '{matched_key}' -> Filling: '{value}'")
    
    # Determine the input type in the container
    text_input = container.locator('input[type="text"]')
    textarea = container.locator('textarea')
    radios = container.locator('input[type="radio"]')
    checkboxes = container.locator('input[type="checkbox"]')
    
    if text_input.count() > 0:
        text_input.fill(str(value))
        return True
    elif textarea.count() > 0:
        textarea.fill(str(value))
        return True
    elif radios.count() > 0:
        # It's a radio question. Find the option matching the value
        options_count = radios.count()
        # Find labels inside the container
        labels = container.locator('label').all()
        for label in labels:
            label_text = label.inner_text().strip().lower()
            if str(value).lower() in label_text or label_text in str(value).lower():
                label.click()
                return True
        # If no direct match, click the first one as default or leave blank
        if labels:
            print(f"  [Info] No direct match for '{value}' in options, clicking first option: '{labels[0].inner_text().strip()}'")
            labels[0].click()
        return True
    elif checkboxes.count() > 0:
        # Checkboxes question
        labels = container.locator('label').all()
        for label in labels:
            label_text = label.inner_text().strip().lower()
            if str(value).lower() in label_text:
                # Check it
                input_el = label.locator('input[type="checkbox"]')
                if not input_el.is_checked():
                    label.click()
        return True
        
    return False

import re

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
    
    # Prepare logs
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("Timestamp,Software Name,Status,Details\n")
            
    with sync_playwright() as p:
        print(f"Launching browser (headless={not headful})...")
        browser = p.chromium.launch(headless=not headful)
        context = browser.new_context(storage_state=AUTH_FILE)
        page = context.new_page()
        
        # If dry run, we only test the first item
        items_to_submit = [inventory[0]] if dry_run else inventory
        
        for idx, item in enumerate(items_to_submit):
            name = item["Software Name"]
            print(f"\n--- [{idx+1}/{len(items_to_submit)}] {'[DRY RUN]' if dry_run else 'Submitting'}: {name} ---")
            
            page.goto(FORM_URL)
            
            # Wait for form or check if we are redirected to login
            page.wait_for_timeout(2000) # Basic wait for redirect
            if "login" in page.url.lower() or "signin" in page.url.lower():
                print("Error: Session expired or invalid. Please re-authenticate using --login.")
                break
                
            # Wait for questions to load
            try:
                page.wait_for_selector('div[data-automation-id="question-container"]', timeout=15000)
            except Exception as e:
                print("Error: Question container not found. The form failed to render or session is invalid.")
                # Save screenshot
                page.screenshot(path="error_page.png")
                print("Saved error screenshot to error_page.png")
                break
                
            # Find all question containers
            containers = page.locator('div[data-automation-id="question-container"]').all()
            print(f"Found {len(containers)} questions on the form.")
            
            # Fill out each question
            for container in containers:
                title_el = container.locator('[data-automation-id="question-title"]')
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
