import unittest
from unittest.mock import patch, MagicMock
import serial
from Sensors.co2 import CO2Sensor

class TestCO2Sensor(unittest.TestCase):

    @patch("serial.Serial")
    def test_connected(self, mock_serial):
        mock_serial_instance = MagicMock()
        mock_serial.return_value = mock_serial_instance
        sensor = CO2Sensor()
        mock_serial_instance.is_open = True
        self.assertTrue(sensor.is_connected())

    @patch("serial.Serial")
    def test_connection_failure(self, mock_serial):
        mock_serial.side_effect = serial.SerialException("Failed to open serial port")
        
        with self.assertRaises(serial.SerialException):
            CO2Sensor()

if __name__ == "__main__":
    unittest.main()
