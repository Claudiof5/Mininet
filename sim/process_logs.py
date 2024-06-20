import csv
import os
import re
from collections import defaultdict

def process_logs(log_file):
    data = defaultdict(list)
    moteid_limit = 54
    out_directory = "datasets-test"
    with open(log_file, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            parts = re.split(r'\s+', line.strip())
            if len(parts) < 8:
                parts += [None] * (8 - len(parts))
                
            # Extract values from the log line
            moteid = int(parts[3]) if parts[3] is not None else None
            if moteid is None or moteid > moteid_limit: 
                continue
            date_time = parts[0] + ' ' + parts[1]
            epoch = int(parts[2]) if parts[2] is not None else None
            temperature = float(parts[4]) if parts[4] is not None else None
            humidity = float(parts[5]) if parts[5] is not None else None
            light = float(parts[6]) if parts[6] is not None else None
            voltage = float(parts[7]) if parts[7] is not None else None
            
            data[moteid].append([date_time, epoch, moteid, temperature, humidity, light, voltage])
    
    headers = ["date_time", "epoch", "moteid", "temperature", "humidity", "light", "voltage"]
    
    # Create a CSV file for each moteid
    for moteid, rows in data.items():
        file_name = ""
        if(moteid < 10):
            file_name = f"sc0{moteid}.csv"
        else:
            file_name = f"sc{moteid}.csv"

        csv_file = os.path.join(out_directory, file_name)
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)

        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)


if __name__ == "__main__":
    log_file_path = os.path.join('datasets-test', 'data.txt')

    process_logs(log_file_path)
