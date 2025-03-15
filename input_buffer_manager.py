import csv
from config import combined_log, combined_headers

def add_input_event(event_data):
    try:
        # Open the CSV file in append mode
        with open(combined_log, mode='a', newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)

            # Write the header if the file is empty
            if log_file.tell() == 0:
                writer.writerow(combined_headers)

            # Write the log event
            writer.writerow(event_data)
            print(f"Log Written to CSV: {event_data}")  # Debug statement
    except Exception as e:
        print(f"Error writing to log: {e}")