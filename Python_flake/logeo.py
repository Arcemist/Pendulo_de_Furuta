import csv
from datetime import datetime
import time
import serial

PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
OUTPUT_FILE = "arduino_data.csv"

try:
  # 1. Connect and wait for connection to stabilize
  ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
  time.sleep(2)

  # 2. Clear any partial data currently in the buffer
  ser.reset_input_buffer()
  print("Buffer cleared. Sending sync signal to Arduino...")

  # 3. Send the 'S' handshake signal to tell Arduino to start transmitting
  ser.write(b"S")
  print("Sync successful! Recording data... Press Ctrl+C to stop.")

  with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Add field name line if opening an empty csv file
    if file.tell() == 0:
      writer.writerow(["Timestamp", "Sensor_Value", "example"])

    while True:
      if ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").strip()
        info = line.split(",")

        if line:
          timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          writer.writerow([timestamp, info[0], info[1]])
          file.flush()
          print(f"[{timestamp}] {info[0]} {info[1]}")

except serial.SerialException as e:
  print(f"Serial Error: {e}")
except KeyboardInterrupt:
  print("\nRecording stopped by user.")
finally:
  if "ser" in locals() and ser.is_open:
    ser.close()
    print("Serial port closed.")
