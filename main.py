from Sensors.co2 import CO2Sensor
import time
import logging

time.sleep(20)
while True:
    try:
        co2_sensor = CO2Sensor()
        if co2_sensor.is_connected:
            co2_sensor.read_co2()
            time.sleep(15)
        else:
            # Restart connections to sensor if it fails to connect
            co2_sensor = CO2Sensor()
    except Exception as e:
        print(f"Exception in main loop: {e}")