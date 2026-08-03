import pandas as pd
from playwright.sync_api import sync_playwright
import os
from datetime import datetime
import csv

# Target file
LIVE_FILE = 'live_feed.csv'
MAX_ROWS = 432 # 3 days * 24 hours * 6 runs/hour

def get_water_level():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Navigate to the Gatun Water Level Indicators page
        page.goto("https://evtms-rpts.pancanal.com/eng/h2o/index.html", timeout=60000)
        
        # Scrape the data. 
        # Note: You will need to inspect the page and update this selector to the exact element 
        # containing the live water level.
        try:
             element = page.wait_for_selector(".water-level-class", timeout=10000) # UPDATE THIS SELECTOR
             level = element.inner_text().strip()
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
