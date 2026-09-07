import serial
import csv
import time

# Configure the serial port (Change 'COM3' to match your Arduino's port)
serial_port = 'COM3'
baud_rate = 9600
output_file = 'arduino_data.csv'

# Open serial connection and the output CSV file
with serial.Serial(serial_port, baud_rate, timeout=1) as ser, open(output_file, 'a', newline='') as f:
    writer = csv.writer(f)
    print(f"Logging data to {output_file}. Press Ctrl+C to stop.")
    
    while True:
        try:
            # Read a line of data from the Arduino
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                # Split the comma-separated values sent by Arduino
                data_points = line.split(',')
                
                # Add a computer timestamp to the data row
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                row = [current_time] + data_points
                
                # Write to the file
                writer.writerow(row)
                print(f"Logged: {row}")
                
        except KeyboardInterrupt:
            print("\nLogging stopped.")
            break
