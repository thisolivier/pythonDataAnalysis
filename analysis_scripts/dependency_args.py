import argparse
from datetime import datetime

# -----------------
# Argument read
# -----------------

def parse_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process debug logs and visualize event data.')

    # Add arguments for start date, end date, and event types
    parser.add_argument('--start_date', type=str, required=False, help='Start date for filtering (format: HH:mm dd/MM/yyyy)')
    parser.add_argument('--end_date', type=str, required=False, help='End date for filtering (format: HH:mm dd/MM/yyyy)')
    parser.add_argument('--event_types', type=str, nargs='+', required=False, help='List of event types to filter')
    parser.add_argument('--event_types_secondary', type=str, nargs='+', required=False, help='List of event types for second group')

    # Parse the arguments
    args = parser.parse_args()

    # Define the expected datetime format: '12:45 22/01/2024'
    datetime_format = '%H:%M %d/%m/%Y'

    # Convert start_date and end_date to datetime objects using the custom format
    start_date = datetime.strptime(args.start_date, datetime_format) if args.start_date else datetime.strptime("00:00 01/10/2024", datetime_format)
    end_date = datetime.strptime(args.end_date, datetime_format) if args.end_date else None

    # Extract event types (if provided)
    event_types = args.event_types if args.event_types else None
    event_types_secondary = args.event_types_secondary if args.event_types else None
    return start_date, end_date, event_types, event_types_secondary