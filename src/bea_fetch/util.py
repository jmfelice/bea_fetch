import csv
import os

def write_to_csv(data, file_path, overwrite='yes'):
    """
    Write data to a CSV file.

    Parameters:
    data (list): A list of dictionaries containing the data to write.
    file_path (str): The path to the output CSV file.
    overwrite (str): 'yes' to overwrite the file, 'no' to append to it.

    Returns:
    None
    """
    if not data:
        print("Warning: No data received from BEA API")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Determine the file mode based on the overwrite parameter
    mode = 'w' if overwrite.lower() == 'yes' else 'a'
        
    with open(file_path, mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        
        # Write header only if overwriting
        if mode == 'w':
            writer.writeheader()
        
        writer.writerows(data)

        