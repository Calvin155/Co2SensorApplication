import serial
import time

class CO2Sensor:
    def __init__(self, serial_port='/dev/serial0', baudrate=9600, timeout=5):
        try:
            self.ser = serial.Serial(serial_port, baudrate, timeout=timeout)
            time.sleep(2)  # Allow sensor to initialize
            self.request_data = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
            print(f"CO₂ sensor initialized on {serial_port} at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error initializing serial port: {e}")
            self.ser = None

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def read_co2(self):
        if not self.is_connected():
            print("CO₂ sensor is not connected.")
            return None

        try:
            self.ser.write(self.request_data)
            time.sleep(0.1)

            if self.ser.in_waiting >= 9:
                response = self.ser.read(9)
                if len(response) == 9 and response[0] == 0xFF and response[1] == 0x86:
                    co2 = response[2] * 256 + response[3]
                    return co2
                else:
                    print(f"Invalid or corrupt response: {response}")
                    return None
            else:
                print("No data received from CO₂ sensor.")
                return None

        except serial.SerialException as e:
            print(f"Serial error: {e}")
            return None

    def close(self):
        if self.is_connected():
            self.ser.close()
            print("CO₂ sensor connection closed.")

