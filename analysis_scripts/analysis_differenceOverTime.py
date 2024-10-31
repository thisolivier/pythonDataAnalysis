import pandas as pd
import argparse
from datetime import datetime
from dependency_dataRead import read_database
from scipy.stats import ttest_rel, wilcoxon

# Define start date
start_date = datetime.strptime("00:00 01/10/2024", '%H:%M %d/%m/%Y')

# Read data and filter by start date
df = read_database()
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df[df['timestamp'] >= start_date]

# Filter data for each event type, keeping timestamp for alignment
event1_data = df[df['event_name'] == 'LocationDisplayed'][['timestamp', 'sum']].rename(columns={'sum': 'group1_count'})
event2_data = df[df['event_name'] == 'AnalyticsEvent'][['timestamp', 'sum']].rename(columns={'sum': 'group2_count'})

# Merge data on timestamp to align both groups by time
df_merged = pd.merge(event1_data, event2_data, on='timestamp', how='inner').dropna()

# Calculate paired differences
differences = df_merged['group1_count'] - df_merged['group2_count']
print("Comparing LocationDisplayed to AnalyticsEvent hourly groupings")

# Perform a paired t-test
t_stat, p_value = ttest_rel(df_merged['group1_count'], df_merged['group2_count'])
print(f"Paired T-Test: t-statistic = {t_stat}, p-value = {p_value}")

# Perform Wilcoxon signed-rank test if data is non-parametric
wilcoxon_stat, wilcoxon_p = wilcoxon(differences)
print(f"Wilcoxon Test: statistic = {wilcoxon_stat}, p-value = {wilcoxon_p}")
