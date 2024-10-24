import asyncio
import unittest
from unittest import mock
from unittest.mock import patch, Mock
from nats_client_dev import NATSClient
from data_capture_module import DataCapture
from database import DatabaseManager
from main import main
from cli import parse_args
import warnings

# Ignore coroutine warnings (Only raised when closing NATS connection due to strange error)
warnings.filterwarnings("ignore", category=RuntimeWarning, message="coroutine .* was never awaited")
warnings.filterwarnings("ignore", message="Enable tracemalloc to get the object allocation traceback")

class TestDataCapture(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_generate_data(self,mock_connect):
        # Replace with a real database manager instance
        db = DatabaseManager('database.db') 
        # Replace with the desired reading frequency and sensor type
        data_capture = DataCapture(db, 1, 'mockup', 0, 100)  
        data = data_capture.read_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)

    def test_read_data_mockup(self):
        data_capture = DataCapture(None, 1, 'mockup', 0, 100)
        data = data_capture.read_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)
        for value in data:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)

    def test_read_data_mockup_min_value(self):
        data_capture = DataCapture(None, 1, 'mockup', 10, 100)
        data = data_capture.read_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)
        for value in data:
            self.assertGreaterEqual(value, 10)
            self.assertLessEqual(value, 100)

    def test_read_data_mockup_max_value(self):
        data_capture = DataCapture(None, 1, 'mockup', 0, 50)
        data = data_capture.read_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)
        for value in data:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 50)

    def test_read_data_mockup_invalid_min_value(self):
        data_capture = DataCapture(None, 1, 'mockup', 100, 50)
        with self.assertRaises(ValueError):
            data_capture.read_data()

class TestCLI(unittest.TestCase):
    @patch('argparse.ArgumentParser')
    def test_parse_args(self, mock_parser):
        # Create a mock ArgumentParser object
        mock_parser.return_value = Mock()
        mock_parser.return_value.parse_args.return_value = Mock(sensor_type='mockup')

        # Call the parse_args function
        args = parse_args(['--sensor-type', 'mockup'])

        # Verify that the sensor_type attribute is set correctly
        self.assertEqual(args.sensor_type, 'mockup')

class TestDatabaseManager(unittest.TestCase):
    @patch('sqlite3.connect')
    def test_connect(self, mock_connect):
        db_manager = DatabaseManager('database.db')
        db_manager.connect()
        mock_connect.assert_called_once_with('database.db')

    @patch('sqlite3.connect')
    def test_insert_data(self, mock_connect):
        db_manager = DatabaseManager('database.db')
        db_manager.connect()
        query = "INSERT INTO infrared_data (id, reading_time, data) VALUES (?, ?, ?)"
        data = (1, 1.0, b'Hello')
        db_manager.execute(query, data)
        mock_connect.assert_called_once_with('database.db')
        mock_cursor = mock_connect.return_value.cursor.return_value
        self.assertTrue(mock_cursor.execute.called)

if __name__ == '__main__':
    unittest.main()