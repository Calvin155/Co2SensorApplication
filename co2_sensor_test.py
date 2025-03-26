import unittest
from unittest.mock import patch, MagicMock
import serial
from Sensors.co2 import CO2Sensor

class TestCO2Sensor(unittest.TestCase):

    @patch("serial.Serial")
    def test_initialization(self, mock_serial):
        """Test if CO2Sensor initializes correctly."""
        mock_serial_instance = MagicMock()
        mock_serial.return_value = mock_serial_instance
        
        sensor = CO2Sensor()
        
        self.assertTrue(sensor.is_connected())
        mock_serial.assert_called_once_with('/dev/ttyAMA0', 9600, timeout=10)

    @patch("serial.Serial")
    def test_is_connected(self, mock_serial):
        """Test if the sensor correctly detects connection status."""
        mock_serial_instance = MagicMock()
        mock_serial.return_value = mock_serial_instance

        mock_serial_instance.is_open = True
        sensor = CO2Sensor()
        self.assertTrue(sensor.is_connected())

        mock_serial_instance.is_open = False
        self.assertFalse(sensor.is_connected())

    # @patch("serial.Serial")
    # @patch("Database.influxdb.InfluxDB")
    # def test_read_co2_valid_response(self, mock_influxdb, mock_serial):
    #     """Test if valid CO2 sensor data is read and stored correctly."""
    #     mock_serial_instance = MagicMock()
    #     mock_serial_instance.read.return_value = bytes([0xFF, 0x86, 0x03, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x79])
    #     mock_serial_instance.in_waiting = 9
    #     mock_serial.return_value = mock_serial_instance

    #     sensor = CO2Sensor()

    #     with patch("builtins.print") as mock_print:
    #         sensor.read_co2()
    #         mock_print.assert_any_call("CO2 1000 & Co2 percentage: 0.1")
        
    #     mock_influxdb.return_value.write_co2_data.assert_called_once_with(1000, 0.1)

    @patch("serial.Serial")
    def test_read_co2_no_data(self, mock_serial):
        """Test if the sensor handles cases where no data is received."""
        mock_serial_instance = MagicMock()
        mock_serial_instance.in_waiting = 0
        mock_serial.return_value = mock_serial_instance

        sensor = CO2Sensor()

        with patch("builtins.print") as mock_print:
            sensor.read_co2()
            mock_print.assert_any_call("No data received from CO₂ sensor.")

    # @patch("serial.Serial")
    # def test_read_co2_corrupt_response(self, mock_serial):
    #     """Test if the sensor correctly handles a corrupt response."""
    #     corrupt_data = bytes([0xFF, 0x01, 0x00, 0x00])
    #     mock_serial_instance = MagicMock()
    #     mock_serial_instance.read.return_value = corrupt_data
    #     mock_serial_instance.in_waiting = len(corrupt_data)
    #     mock_serial.return_value = mock_serial_instance

    #     sensor = CO2Sensor()

    #     with patch("builtins.print") as mock_print:
    #         sensor.read_co2()
    #         mock_print.assert_any_call(f"Invalid or corrupt response: {corrupt_data}")

    @patch("serial.Serial")
    def test_close(self, mock_serial):
        """Test if the CO2Sensor properly closes the serial connection."""
        mock_serial_instance = MagicMock()
        mock_serial_instance.is_open = True
        mock_serial.return_value = mock_serial_instance

        sensor = CO2Sensor()
        sensor.close()

        mock_serial_instance.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
