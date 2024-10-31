
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from dependency_args import parse_arguments
from dependency_dataRead import read_database
from dependency_dataPrep import data_preparation

# -----------------
# Parse Arguments
# -----------------

start_date, end_date, event_types, event_types_secondary = parse_arguments()

# Ensure both groups are provided
if not event_types or not event_types_secondary:
    raise ValueError("Both --event_types and --event_types_secondary must be specified.")

# -----------------
# Read and Prepare Data
# -----------------

df = read_database()
df = data_preparation(df=df, start_date=start_date, end_date=end_date, event_types=None)

# -----------------
# Filter and Resample Data for Each Group
# -----------------

# Filter for the first event group and resample by hour
df_group1 = df[df['event_name'].isin(event_types)]
df_group1_hourly = df_group1.groupby('timestamp')['sum'].sum().reset_index(name='group1_count')

# Filter for the second event group and resample by hour
df_group2 = df[df['event_name'].isin(event_types_secondary)]
df_group2_hourly = df_group2.groupby('timestamp')['sum'].sum().reset_index(name='group2_count')

# Merge the two groups on the timestamp to calculate the ratio
df_ratio = pd.merge(df_group1_hourly, df_group2_hourly, on='timestamp', how='outer').fillna(0)
df_ratio['ratio'] = df_ratio['group1_count'] / df_ratio['group2_count']
df_ratio.replace([float('inf'), -float('inf')], 0, inplace=True)  # Replace infinite ratios with zero

# -----------------
# Plotting the Ratio Over Time
# -----------------

# Create custom legend labels showing event types in each group
group1_label = f"Group 1 ({', '.join(event_types)})"
group2_label = f"Group 2 ({', '.join(event_types_secondary)})"
ratio_label = f"Ratio of {group1_label} to {group2_label}"

plt.figure(figsize=(12, 6))
plt.plot(df_ratio['timestamp'], df_ratio['ratio'], marker='o', linestyle='-', color='purple', label=ratio_label)

# Add a little guide at 0
plt.axhline(y=1, color='orange', linestyle='--', linewidth=1)

# Customize the plot
plt.title('Ratio of Event Counts for Group 1 vs Group 2 (Hourly Buckets)', fontsize=16)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Ratio of Group 1 to Group 2', fontsize=14)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.xticks(rotation=45)

# Add legend and tighten layout
plt.legend()
plt.tight_layout()
plt.show()