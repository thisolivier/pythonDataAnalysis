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
# Data Preparation Distribution Plot
# -----------------

# Shows us basic distribution of counts for the time range per min

# Get unique event types
event_types = df['event_name'].unique()
num_events = len(event_types)

# Create subplots: calculate grid size (rows x cols)
cols = 2
rows = math.ceil(num_events / cols)
fig, axes = plt.subplots(rows, cols, figsize=(12, 8))
fig.suptitle('Distributions of Event Count/Hour')

# Flatten axes for easier iteration
axes = axes.flatten()

# Loop through each event type and create a histogram in its own subplot
for i, event in enumerate(event_types):
    subset = df[df['event_name'] == event]
    mean_count = subset['sum'].mean()

    # Plot histogram for this event type
    n, bins, patches = axes[i].hist(subset['sum'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    axes[i].axvline(mean_count, color='red', linestyle='dashed', linewidth=2)

    # Add title and labels to each subplot
    axes[i].set_title(f'{event} (Mean: {mean_count:.2f})')
    axes[i].set_xlabel('Event Count')
    axes[i].set_ylabel('Frequency')

    # Set Y-axis limit based on max frequency count
    max_count = max(n)
    axes[i].set_ylim(0, max_count + max_count * 0.1)  # Add a little padding above the max

# Hide any unused subplots (if number of events is odd)
for j in range(i + 1, rows * cols):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()

# -----------------
# Data Visualization: Bar Plot for Total Event Counts
# -----------------

# Shows the total events across the time period for each event

# Create a grouped DataFrame for total event counts by event type (for bar/donut chart)
df_grouping = df.groupby('event_name')['sum'].sum().reset_index(name='total_count')

plt.figure(figsize=(10, 6))
plt.bar(df_grouping['event_name'], df_grouping['total_count'], color='blue')
plt.title('Total Event Count by Event Type')
plt.xlabel('Event Type')
plt.ylabel('Total Event Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------
# Data Preparation for Time Trend Plot
# -----------------

# Shows the event count totals over time

# Grouping and resampling the data to show time-based resolutions
def plot_with_time_resolution(resolution, time_format):
    """
    This function plots the line graph for a given time resolution
    - resolution can be 'H' for hours, 'D' for days
    """
    # Resample the data by the specified resolution and sum the counts for each event
    resampled_df = df.groupby([pd.Grouper(key='timestamp', freq=resolution), 'event_name'])['sum'].sum().unstack().fillna(0)

    # Plotting
    plt.figure(figsize=(12, 6))
    for event in resampled_df.columns:
        plt.plot(resampled_df.index, resampled_df[event], marker='o', label=event)

    # Customizing the plot
    plt.title(f'Event Count Over Time (Resolution: {resolution})', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Event Count', fontsize=14)
    
    # Format the X-axis to show full date and time
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(time_format))
    plt.xticks(rotation=45, ha='right', fontsize=10)
    
    # Add a legend and tighten layout
    plt.legend(title='Event Type', fontsize=10)
    plt.tight_layout()
    plt.show()


# -----------------
# Visualization with Different Time Resolutions
# -----------------

# For full date formatting, adjust time_format to:
# '%Y-%m-%d' for day-level
# '%Y-%m-%d %H:%M' for hour-level
# '%Y-%m-%d %H:%M:%S' for minute-level

plot_with_time_resolution('h', '%Y-%m-%d %H:%M')  # Change resolution and time format as needed
# Not sure the resolution works
