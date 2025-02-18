import sys
from bea_fetch.fetch_bea_parameters import fetch_bea_parameters_to_csv

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <api_key> <table> <year> <frequency> <output_file>")
        sys.exit(1)
    
    fetch_bea_parameters_to_csv(
        api_key=sys.argv[1],
        dataset_name=sys.argv[2],
        output_file=sys.argv[3]
    ) 
