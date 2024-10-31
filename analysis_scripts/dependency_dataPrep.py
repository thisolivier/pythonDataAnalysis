import pandas as pd

# -----------------
# Shared Data Preparation
# -----------------

def data_preparation(df, start_date, end_date, event_types):
    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filter the data by date range, if provided
    if start_date and end_date:
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    elif start_date:
        df = df[df['timestamp'] >= start_date]
    elif end_date:
        df = df[df['timestamp'] <= end_date]

    # Filter the data by event types, if provided
    if event_types:
        df = df[df['event_name'].isin(event_types)]
    return df