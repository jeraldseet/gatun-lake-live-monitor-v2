import pandas as pd
from playwright.sync_api import sync_playwright, expect
import os
from datetime import datetime
import csv

# Target file
LIVE_FILE = 'live_feed.csv'
MAX_ROWS = 432 # 3 days * 24 hours * 6 runs/hour (Requested by analyst team)

def get_water_level():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 1. Navigate to the URL>wait for background API requests to settle
        # CHANGED: 'networkidle' replaced with 'domcontentloaded' to prevent timeouts
        page.goto("https://panama.aquaticinformatics.net/Data/Dashboard/1", timeout=60000, wait_until="domcontentloaded")
        
        try:
             # 1. Lock onto the first gauge chart in the DOM (Gatun) regardless of its text
             gatun_locator = page.locator(".gaugechart .text-center").nth(0)
             
             # 2. Force Playwright to watch ONLY this specific Gatun gauge and wait for it to load
             expect(gatun_locator).to_contain_text("ft", timeout=15000)
             
             # 3. Extract the text safely
             raw_level = gatun_locator.inner_text().strip()
             
             # Failsafe
             if not raw_level:
                 raise ValueError("Element loaded, but no text was found inside.")
             
             # Clean up the string to only keep the number
             level = raw_level.replace(' ft', '')
             
        except Exception as e:
             print(f"Error finding element: {e}")
             level = None
             
        browser.close()
        return level

def update_data():
    level = get_water_level()
    if level is None:
        print("Failed to retrieve water level. Exiting.")
        return

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if file exists, if not create with headers
    if not os.path.exists(LIVE_FILE):
        with open(LIVE_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Value'])

    # Read existing data
    try:
        df = pd.read_csv(LIVE_FILE)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=['Timestamp', 'Value'])

    # Append new data
    new_row = pd.DataFrame([{'Timestamp': now, 'Value': level}])
    df = pd.concat([df, new_row], ignore_index=True)

    # Keep only the last 3 days of data (432 rows)
    if len(df) > MAX_ROWS:
        df = df.tail(MAX_ROWS)

    # Save back to CSV
    df.to_csv(LIVE_FILE, index=False)
    print(f"Added {level} at {now}. File length: {len(df)}")

if __name__ == "__main__":
    update_data()
