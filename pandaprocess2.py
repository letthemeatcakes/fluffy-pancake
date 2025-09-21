import json
import glob
import os
from pathlib import Path
import pandas as pd
import datetime

# Debug printing function for testing purposes
def print_info():
    """Print information about the filtered DataFrame and processing flags"""
    print("Filtered DataFrame Structure:")
    print(filtered_df.info)
    print("wcsv" + (str(write_csv)))
    print("wrjson" + (str(write_raw_json)))
    print("and" + (str(and_logic)))

# Set path to JSON data directory (works universally across environments)
json_data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'json_data')
json_data_dir = os.path.normpath(json_data_dir)
files = glob.glob(os.path.join(json_data_dir, "*.json"))

# Set path to input command JSON file
default_input_path = os.path.join(os.path.dirname(__file__), '..', '..', 'input_commands', 'latest_command.json')
input_file_path = os.path.normpath(default_input_path)

# Error handling for reading input command file
try:
    with open(input_file_path, 'r', encoding='utf-8') as f:
        user_input = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {input_file_path}")
    user_input = {}
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in file {input_file_path}: {e}")
    user_input = {}
except Exception as e:
    print(f"Unexpected error: {e}")
    user_input = {}
    print("InputFileNotFound")

# Extract processing parameters from user input with default values
write_csv = user_input.get('write_csv', False)
write_raw_json = user_input.get('write_raw_json', False)
and_logic = user_input.get('and_logic', False)
filters = user_input.get('filters', [])

# Build query string from filters
query_string = ""
conditions = []
for filter in filters:
    condition = f"`{filter['column']}` {filter['operator']} {filter['value']}"
    conditions.append(condition)

# Apply AND or OR logic to combine conditions
if and_logic is True:
    query_string = " and ".join(conditions)
elif and_logic is False:
    query_string = " or ".join(conditions)

# Load and process all JSON files
all_data = []
for file in files:
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
        for record in data:
            normalized_df = pd.json_normalize(data)
            all_data.append(normalized_df)

# Combine all data into a single DataFrame and apply filters
df = pd.concat(all_data, ignore_index=True)
filtered_df = df.query(query_string)

# Output processing based on user preferences
if write_raw_json is True:
    # Save raw JSON data to archive
    archive_dir = os.path.join(json_data_dir, 'json_archive')
    os.makedirs(archive_dir, exist_ok=True)
    archive_path = os.path.join(archive_dir, f"tiktokmeta_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    df.to_json(archive_path, orient='records', indent=2)

if write_csv is True:
    # Save filtered results to CSV
    csvname = "tiktokmeta_" + datetime.datetime.now().strftime("%H%M_%m_%d_%y") + ".csv"
    csv_archive_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
    csv_archive_dir = os.path.normpath(csv_archive_dir)
    os.makedirs(csv_archive_dir, exist_ok=True)
    full_csv_path = os.path.join(csv_archive_dir, csvname)
    filtered_df.to_csv(full_csv_path, index=False)
    print_info()
else:
    print_info()