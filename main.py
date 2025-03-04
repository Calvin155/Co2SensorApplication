from Sensors.co2 import CO2Sensor
from Database.influxdb import InfluxDB
import time
import logging

time.sleep(20)
while True:
    try:
        co2_sensor = CO2Sensor()
        influx_db = InfluxDB()
        if co2_sensor.is_connected:
            co2_sensor.read_co2()
            time.sleep(15)
        else:
            co2_sensor = CO2Sensor()
            influx_db = InfluxDB()
    except Exception as e:
        print(f"Exception in main loop: {e}")