from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import logging
import os

# Database connections
URL = "http://18.201.230.235:8086"
TOKEN="_NaX4deSsnKPA6cbcwVqx-G16p_M5ed3tJR-4JYZMBUnJq2pNQWQ7Pz_Mtjq-82oI79pvPiqDMeJ-jPtsfQlmg=="
ORG="AQI"
BUCKET="AQIMetrics"


class InfluxDB:
    def __init__(self):
        self.url = URL
        self.token = TOKEN
        self.org = ORG
        self.bucket = BUCKET
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def connect(self):
        try:
            if self.client:
                self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
                print("Successfully Connected to Influx Database")
                print("Successfully connected to Influx")
            else:
                print("Already connected to Influx Database")
                print("Already connected to Influx")

        except Exception as e:
            print("Error Connecting to Database: ", str(e))

    def connected(self):
        try:
            if self.client.ping() == 200:
                print("Connected & Pinging")
                return True
            else:
                print("No Joy")
                return False
        except Exception as e:
            print(e)

    def write_co2_data(self, co2_ppm, co2_percentage):
        try:
            co2_ppm = float(co2_ppm)
            co2_percentage = float(co2_percentage)

            timestamp = datetime.utcnow().isoformat()
            point = {
                "measurement": "air_quality",
                "tags": {"location": "local"},
                "fields": {
                    "Co2 - Parts Per-Million": co2_ppm,
                    "Co2 Percentage": co2_percentage,
                },
                "time": timestamp
            }

            self.write_api.write(bucket=self.bucket, record=point)
        except Exception as e:
            print("Error writing data to Database:", str(e))

    def close(self):
        if self.client:
            self.client.close()
            print("Connection to Database Closed")
