import urllib.request
import json
import sys
import csv
import os
from .util import write_to_csv

def fetch_bea_nipa_data(api_key, table, year, frequency):
    """
    Fetch NIPA data from the BEA API.

    :param api_key: The API key for accessing the BEA API.
    :param table: The table name to fetch data from.
    :param year: The year for which to fetch data.
    :param frequency: The frequency of the data (e.g., 'A' for annual).
    :return: A list of data records retrieved from the API.
    :raises ValueError: If the API response format is invalid or contains an error.
    :raises urllib.error.HTTPError: If there is an HTTP error during the request.
    :raises json.JSONDecodeError: If the response cannot be parsed as JSON.
    """
    base_url = "https://apps.bea.gov/api/data"
    
    params = {
        "UserID": api_key,
        "method": "GETDATA",
        "datasetname": 'NIPA',
        "TableName": table,
        "Year": year,
        "Frequency": frequency,
        "ResultFormat": "JSON"
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{base_url}?{query_string}"
    
    # Print URL for testing (with API key partially masked)
    masked_url = url.replace(api_key, api_key[:4] + "..." + api_key[-4:])
    print(f"Debug - API URL (masked): {masked_url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        if 'BEAAPI' not in data:
            raise ValueError("Invalid API response format")
            
        if 'error' in data['BEAAPI']:
            raise ValueError(f"BEA API Error: {data['BEAAPI']['error']}")

        results = data['BEAAPI']['Results']
        return results['Data']
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print(f"Attempted URL: {url}")
        raise
    except json.JSONDecodeError:
        print("Failed to parse API response as JSON")
        raise

def fetch_bea_nipa_data_to_csv(api_key, table, year, frequency, output_file, overwrite=True):
    """
    Fetch NIPA data from the BEA API and write it to a CSV file.

    :param api_key: The API key for accessing the BEA API.
    :param table: The table name to fetch data from.
    :param year: The year for which to fetch data.
    :param frequency: The frequency of the data (e.g., 'A' for annual).
    :param output_file: The path to the output CSV file.
    :param overwrite: Whether to overwrite the file if it exists (default is True).
    :raises Exception: If an error occurs during data fetching or writing to CSV.
    """
    try:
        result = fetch_bea_nipa_data(api_key, table, year, frequency)
        print(f"Received {len(result) if result else 0} records from API")
        
        # Include headers in the CSV
        if result:
            headers = result[0].keys()  # Get the keys from the first record
            file_mode = 'w' if overwrite else 'a'  # Set file mode based on overwrite flag
            
            # Check if the file exists and if we are not overwriting
            if not overwrite and os.path.exists(output_file):
                # If appending, do not write headers
                file_mode = 'a'
            else:
                # If overwriting, write headers
                with open(output_file, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()  # Write the header row
            
            # Write the data rows
            with open(output_file, file_mode, newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writerows(result)  # Write the data rows
        else:
            print("No data to write to CSV.")
        
        print(f"Data successfully written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)