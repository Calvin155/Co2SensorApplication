import serial
import time

# Function to initialize the serial connection and set up the sensor
def initialize_sensor():
    # Open serial port
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=5)
    time.sleep(2)  # Allow time for the sensor to initialize

    # MH-Z19B command to request CO2 data (request data)
    request_data = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    return ser, request_data

# Main function to read CO2 data
def read_co2_data(ser, request_data):
    while True:
        ser.write(request_data)
        if ser.in_waiting > 0:
            response = ser.read(9)
            if len(response) == 9 and response[0] == 0xFF and response[1] == 0x86:
                co2 = response[2] * 256 + response[3]
                print(f"CO₂ Concentration: {co2} ppm")
                time.sleep(15)
            else:
                print(f"Invalid or corrupt response: {response}")
                print(f"Re-Initialize Sensor")
                initialize_sensor()
                time.sleep(15)
        else:
            print("No data received.")
        time.sleep(2)  # Increase or decrease based on your testing needs

if __name__ == "__main__":
    ser, request_data = initialize_sensor()

    try:
        read_co2_data(ser, request_data)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()
