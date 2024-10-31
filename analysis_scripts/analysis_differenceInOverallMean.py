import pandas as pd
from datetime import datetime
from scipy import stats
from dependency_dataRead import read_database

start_date = datetime.strptime("00:00 01/10/2024", '%H:%M %d/%m/%Y')
df = read_database()
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df[df['timestamp'] >= start_date]

# Filter data for each event type
event1_data = df[df['event_name'] == 'LocationDisplayed']['sum']
event2_data = df[df['event_name'] == 'AnalyticsEvent']['sum']

# Calculate means
mean_event1 = event1_data.mean()
mean_event2 = event2_data.mean()
mean_difference = mean_event1 - mean_event2

# Perform an independent t-test
t_stat, p_value = stats.ttest_ind(event1_data, event2_data, equal_var=False)

# Output the results
print(f"Mean of LocationDisplayed: {mean_event1}")
print(f"Mean of AnalyticsEvent: {mean_event2}")
print(f"Difference in Means: {mean_difference}")
print(f"T-Statistic: {t_stat}")
print(f"P-Value: {p_value}")

# Interpret the p-value
alpha = 0.05
if p_value < alpha:
    print("The difference in means is statistically significant.")
else:
    print("The difference in means is not statistically significant.")