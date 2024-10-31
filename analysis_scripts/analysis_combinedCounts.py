import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

from dependency_args import parse_arguments
from dependency_dataRead import read_database
from dependency_dataPrep import data_preparation

# -----------------
# Common Dependencies
# -----------------

# Parse arguments
start_date, end_date, event_types, _ = parse_arguments()
# Read database
df = read_database()
# Convert timestamp and apply filtering
df = data_preparation(df= df, start_date= start_date, end_date= end_date, event_types= event_types)

# -----------------
# Data Preparation for Grouped Time Series Plot
# -----------------

# Used to check the total failures over time to check for patterns.

# Define the events to combine
events_to_combine = event_types

# Filter the DataFrame to include only the specified events
df_filtered = df[df['event_name'].isin(events_to_combine)]

# Ensure timestamp is in datetime format and set as the index for resampling
df_filtered['timestamp'] = pd.to_datetime(df_filtered['timestamp'])
df_filtered.set_index('timestamp', inplace=True)

# Resample the data by hour and sum the counts
df_hourly = df_filtered.groupby('timestamp')['sum'].sum().reset_index()

# -----------------
# Plotting the Aggregated Counts Over Time
# -----------------

plt.figure(figsize=(12, 6))

# Plot the combined counts over time
plt.plot(df_hourly['timestamp'], df_hourly['sum'], marker='o', linestyle='-', color='b', label='Combined Event Counts')

# Add labels and title
plt.title('Combined Event Counts Over Time (Hourly Buckets)', fontsize=16)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Total Event Count', fontsize=14)

# Format the X-axis for dates and rotate labels for readability
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.xticks(rotation=45)

# Add legend and tighten layout
plt.legend()
plt.tight_layout()
plt.show()

