import csv
import os


def process_cenario(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        device_data = {}

        for row in csv_reader:
            device = row['device']
            
            if device not in device_data:
                device_data[device] = []
            
            device_data[device].append(row)

    for device, rows in device_data.items():
        output_file_path = os.path.join(output_dir, f'{device}.csv')
        
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as device_file:
            csv_writer = csv.DictWriter(device_file, fieldnames=rows[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(rows)


if __name__ == "__main__":

    output_dir = 'datasets-test'
    log_file_path = os.path.join('datasets-test', 'Cenario_argus1usuario.csv')

    process_cenario(log_file_path, output_dir)
