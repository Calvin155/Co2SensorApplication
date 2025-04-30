from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import logging
import os

# Database connections
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
ORG="AQI"
BUCKET="AQIMetrics"


class InfluxDB:
    def __init__(self):
        self.url = INFLUXDB_URL
        self.token = INFLUXDB_TOKEN
        self.org = ORG
        self.bucket = BUCKET
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def connect(self):
        try:
            if self.client:
                self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
                logging.info("Successfully Connected to Influx Database")
            else:
                logging.info("Already connected to Influx")

        except Exception as e:
            logging.exception("Error Connecting to Database: ", str(e))

    def connected(self):
        try:
            if self.client.ping() == 200:
                logging.info("Connected & Pinging")
                return True
            else:
                logging.info("No Joy")
                return False
        except Exception as e:
            logging.exception(e)

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
            logging.info("CO2 data written to database")
        except Exception as e:
            logging.exception("Error writing data to Database:", str(e))

    def close(self):
        if self.client:
            self.client.close()
            logging.info("Connection to Database Closed")
