import pandas as pd
import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from dependency_dataRead import read_database

# Setup argument
parser = argparse.ArgumentParser(description='Process debug logs and visualize a single event type data.')
parser.add_argument('--event_type', type=str, required=True, help='The event types to graph')
parser.add_argument('--bucketing', type=str, required=False, help='The event types to graph')

# Parse the arguments
args = parser.parse_args()
event_name = args.event_type
bucketing_resolution = args.bucketing if args.bucketing else 'D'

# Define start date
start_date = datetime.strptime("00:00 01/10/2024", '%H:%M %d/%m/%Y')

# Load and prepare data
df = read_database()
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df[(df['timestamp'] >= start_date) & (df['event_name'] == event_name)]

# Resample data and sum the counts for each day
df_daily = df.set_index('timestamp').resample(bucketing_resolution)['sum'].sum().reset_index()

# Plotting the daily event counts over time
plt.figure(figsize=(12, 6))
plt.plot(df_daily['timestamp'], df_daily['sum'], marker='o', linestyle='-', color='b', label=event_name)

# Customize the plot
plt.title(f'Count of "{event_name}" Over Time, bucketed by {bucketing_resolution}', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Total Event Count', fontsize=14)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Add legend and tighten layout
plt.legend()
plt.tight_layout()
plt.show()