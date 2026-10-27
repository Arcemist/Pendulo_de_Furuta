import serial
import struct
import csv

# Configure your serial port settings
SERIAL_PORT = "/dev/ttyUSB0"  # Change to '/dev/ttyUSB0' or '/dev/ttyACM0' on Linux
BAUD_RATE = 115200  # Match the transmitter's baud rate
TOTAL_BYTES = 64  # 32 elements * 2 bytes each
CSV_FILENAME = "datos.csv"

try:
    # Open the serial port with a 2-second timeout to prevent infinite blocking
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        timeout=0.005
    )

    ser.reset_input_buffer()

    # Abrir el archivo
    with open( CSV_FILENAME, mode="w", newline="", encoding="utf-8" ) as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(["Medicion"])

        # Inicializar el Buffer
        buffer_acumulado = bytearray()

        print("Recibiendo Datos...")

        while True:

            if ser.in_waiting > 0:
                buffer_acumulado.extend(ser.read(ser.in_waiting))

            while len(buffer_acumulado) >= TOTAL_BYTES:

                # Extraer 64 bytes
                paquete = buffer_acumulado[:TOTAL_BYTES]
                del buffer_acumulado[:TOTAL_BYTES]

                # Convertir datos crudos a int16
                int16_values = struct.unpack("<32h", paquete)

                for valor in int16_values:
                    csv_writer.writerow([valor])

                pass

except serial.SerialException as e:
    print(f"Serial Error: {e}")
except KeyboardInterrupt:
    print("\nProgram stopped by user.")
finally:
    if "ser" in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")

