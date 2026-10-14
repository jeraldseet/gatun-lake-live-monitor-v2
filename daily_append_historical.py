import pandas as pd
from datetime import datetime

# Define file paths
live_feed_path = 'live_feed.csv'
historical_path = 'Download_Gatun_Lake_Water_Level_History.csv'

try:
    # 1. Read the live feed and extract the absolute latest reading
    live_df = pd.read_csv(live_feed_path)
    
    if live_df.empty:
        print("Live feed is empty. Exiting.")
        exit()

    # Get the last row
    latest_row = live_df.iloc[-1]
    raw_timestamp = latest_row['Timestamp']
    latest_value = latest_row['Value']

    # 2. Extract just the date component (YYYY-MM-DD) from the timestamp
    # Assuming timestamp format is "YYYY-MM-DD HH:MM:SS"
    date_only = raw_timestamp.split(' ')[0]

    # 3. Read the historical data to ensure we don't append duplicate dates
    hist_df = pd.read_csv(historical_path)
    
    if date_only in hist_df['DATE_LOG'].values:
        print(f"Data for {date_only} already exists in historical file. Skipping append.")
    else:
        # 4. Append the new row using a DataFrame to ensure proper formatting
        new_row = pd.DataFrame([{'DATE_LOG': date_only, 'GATUN_LAKE_LEVEL(FEET)': latest_value}])
        hist_df = pd.concat([hist_df, new_row], ignore_index=True)
        
        # 5. Save the updated historical file
        hist_df.to_csv(historical_path, index=False)
        print(f"Successfully appended {latest_value} ft for {date_only} to historical data.")

except Exception as e:
    print(f"An error occurred: {e}")
