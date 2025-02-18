import urllib.request
import json
import sys
from .util import write_to_csv

def fetch_bea_parameters(api_key, dataset_name):
    """
    Fetches parameter information for a specified BEA dataset.
    
    Args:
        api_key (str): BEA API key
        dataset_name (str): Name of the dataset (e.g., 'NIPA')
    
    Returns:
        dict: Parameter information for the dataset
    """
    base_url = "https://apps.bea.gov/api/data"
    
    params = {
        "UserID": api_key,
        "method": "GetParameterList",
        "datasetname": dataset_name,
        "ResultFormat": "JSON"
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{base_url}?{query_string}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        if 'BEAAPI' not in data:
            raise ValueError("Invalid API response format")
            
        if 'error' in data['BEAAPI']:
            raise ValueError(f"BEA API Error: {data['BEAAPI']['error']}")
            
        parameters = data['BEAAPI']['Results']['Parameter']
        
        print(f"\nAvailable Parameters for {dataset_name} dataset:")
        for param in parameters:
            print(f"\n{param['ParameterName']}:")
            print(f"  Description: {param['ParameterDescription']}")
            print(f"  Required: {'Yes' if param['ParameterIsRequiredFlag'] == '1' else 'No'}")
            if 'ParameterDefaultValue' in param:
                print(f"  Default Value: {param['ParameterDefaultValue']}") 

        return parameters
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        raise
    except json.JSONDecodeError:
        print("Failed to parse API response as JSON")
        raise   

def fetch_bea_parameters_to_csv(api_key, dataset_name, output_file):
    try:
        parameters = fetch_bea_parameters(api_key, dataset_name)
        print(f"Received {len(parameters) if parameters else 0} records from API")
        write_to_csv(parameters, output_file)
        print(f"Data successfully written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)
