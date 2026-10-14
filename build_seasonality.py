import pandas as pd
import json
from datetime import datetime

# Read historical data
df = pd.read_csv('Download_Gatun_Lake_Water_Level_History.csv')
df['DATE_LOG'] = pd.to_datetime(df['DATE_LOG'], errors='coerce')
df['LEVEL'] = pd.to_numeric(df['GATUN_LAKE_LEVEL(FEET)'], errors='coerce')

# Clean data (Remove nulls and 0s)
df = df.dropna(subset=['DATE_LOG', 'LEVEL'])
df = df[df['LEVEL'] > 0]

# Extract features
df['Year'] = df['DATE_LOG'].dt.year
df['MMDD'] = df['DATE_LOG'].dt.strftime('%m-%d')
df = df[df['MMDD'] != '02-29'] # Remove leap days for uniform 365 calendar

# Get current year
current_year_val = datetime.now().year

# 5-Year stats (excluding current year to prevent distortion)
last_5_years = df[(df['Year'] >= current_year_val - 5) & (df['Year'] < current_year_val)]
agg_5yr = last_5_years.groupby('MMDD')['LEVEL'].agg(['min', 'max', 'mean']).reset_index()

current_year_data = df[df['Year'] == current_year_val].set_index('MMDD')['LEVEL'].to_dict()
crisis_year_data = df[df['Year'] == 2023].set_index('MMDD')['LEVEL'].to_dict() # 2023 El Nino Benchmark

days = pd.date_range('2023-01-01', '2023-12-31').strftime('%m-%d').tolist()

output = {
    'labels': [], 'min_5yr': [], 'max_5yr': [], 'avg_5yr': [], 
    'crisis_2023': [], 'current_year': [], 'current_year_label': str(current_year_val)
}

for d in days:
    month_name = datetime.strptime(d, '%m-%d').strftime('%b %d')
    output['labels'].append(month_name)
    
    row = agg_5yr[agg_5yr['MMDD'] == d]
    if not row.empty:
        output['min_5yr'].append(round(row['min'].values[0], 2))
        output['max_5yr'].append(round(row['max'].values[0], 2))
        output['avg_5yr'].append(round(row['mean'].values[0], 2))
    else:
        output['min_5yr'].append(None)
        output['max_5yr'].append(None)
        output['avg_5yr'].append(None)
        
    output['crisis_2023'].append(crisis_year_data.get(d, None))
    output['current_year'].append(current_year_data.get(d, None))

with open('seasonality.json', 'w') as f:
    json.dump(output, f)

print("seasonality.json successfully built.")
