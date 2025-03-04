import serial
import time
# from Database.influxdb import InfluxDB

class CO2Sensor:
    def __init__(self, baudrate=9600):
        try:
            self.serial_port = '/dev/ttyAMA0'
            self.baudrate = baudrate
            self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=10)
            self.request_data = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
            print(f"Connected to {self.serial_port} at {self.baudrate} baudrate.")
        
        except serial.SerialException as e:
            print(e)


    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def read_co2(self):
        if not self.is_connected():
            print("CO₂ sensor is not connected - Check Connection.")
            return None

        try:
            self.ser.write(self.request_data)
            time.sleep(0.1)
            if self.ser.in_waiting >= 9:
                response = self.ser.read(9)
                # influx_db = InfluxDB()
                if len(response) == 9 and response[0] == 0xFF and response[1] == 0x86:
                    co2 = response[2] * 256 + response[3]
                    co2_perc = co2 / 1000
                    print(f"CO2 {co2} & Co2 percentage: {co2_perc}")
                    # influx_db.write_co2_data(co2, co2_perc)
                else:
                    print(f"Invalid or corrupt response: {response}")
            else:
                print("No data received from CO₂ sensor.")

        except Exception as e:
            print(f"Serial error: {e}")
            return None

    def close(self):
        if self.is_connected():
            self.ser.close()
            print("CO₂ sensor connection closed.")

