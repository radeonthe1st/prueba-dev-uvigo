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
        """
        Test DataCapture.read_data() method with a mockup sensor type.
        
        The test creates a DataCapture instance with a mockup sensor type and
        asserts that the read_data() method returns a list of 64 random integers.
        """
        db = DatabaseManager('database.db') 
        # Replace with the desired reading frequency and sensor type
        data_capture = DataCapture(db, 1, 'mockup', 0, 100)  
        data = data_capture.read_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)

    def test_read_data_mockup(self):
        """
        Test DataCapture.read_data() method with a mockup sensor type.
        
        The test creates a DataCapture instance with a mockup sensor type and
        asserts that the read_data() method returns a list of 64 random integers
        between 0 and 100.
        """
        data_capture = DataCapture(None, 1, 'mockup', 0, 100)
        data = data_capture.read_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)
        for value in data:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)

    def test_read_data_mockup_min_value(self):
        """
        Test DataCapture.read_data() method with a mockup sensor type and a non-zero minimum value.
        
        The test creates a DataCapture instance with a mockup sensor type and a minimum value of 10.
        It then asserts that the read_data() method returns a list of 64 random integers between 10 and 100.
        """
        data_capture = DataCapture(None, 1, 'mockup', 10, 100)
        data = data_capture.read_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)
        for value in data:
            self.assertGreaterEqual(value, 10)
            self.assertLessEqual(value, 100)

    def test_read_data_mockup_max_value(self):
        """
        Test DataCapture.read_data() method with a mockup sensor type and a non-zero maximum value.
        
        The test creates a DataCapture instance with a mockup sensor type and a maximum value of 50.
        It then asserts that the read_data() method returns a list of 64 random integers between 0 and 50.
        """
        data_capture = DataCapture(None, 1, 'mockup', 0, 50)
        data = data_capture.read_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 64)
        for value in data:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 50)

    def test_read_data_mockup_invalid_min_value(self):
        """
        Tests that a ValueError is raised when the minimum value for the mockup
        sensor is greater than the maximum value.
        """
        data_capture = DataCapture(None, 1, 'mockup', 100, 50)
        with self.assertRaises(ValueError):
            data_capture.read_data()

class TestCLI(unittest.TestCase):
    @patch('argparse.ArgumentParser')
    def test_parse_args(self, mock_parser):
        # Create a mock ArgumentParser object
        """
        Tests that the parse_args function correctly parses the command-line
        arguments and sets the sensor_type attribute accordingly.

        The test creates a mock ArgumentParser object and sets the sensor_type
        attribute of the returned Mock object to 'mockup'. The parse_args
        function is then called with the argument list ['--sensor-type', 'mockup'].

        The test verifies that the sensor_type attribute of the returned
        Mock object is set correctly.
        """
        mock_parser.return_value = Mock()
        mock_parser.return_value.parse_args.return_value = Mock(sensor_type='mockup')

        # Call the parse_args function
        args = parse_args(['--sensor-type', 'mockup'])

        # Verify that the sensor_type attribute is set correctly
        self.assertEqual(args.sensor_type, 'mockup')

class TestDatabaseManager(unittest.TestCase):
    @patch('sqlite3.connect')
    def test_connect(self, mock_connect):
        """
        Tests that the DatabaseManager.connect() method correctly
        connects to the database and calls the underlying sqlite3.connect()
        function with the correct database URI.
        """
        db_manager = DatabaseManager('database.db')
        db_manager.connect()
        mock_connect.assert_called_once_with('database.db')

    @patch('sqlite3.connect')
    def test_insert_data(self, mock_connect):
        """
        Tests that the DatabaseManager.execute() method correctly
        executes the given query with the given parameters and
        calls the underlying sqlite3.connect() function with the
        correct database URI.

        The test creates a DatabaseManager object and calls the
        connect() method to connect to the database. It then calls
        the execute() method with a query and parameters, and verifies
        that the query was executed correctly by checking that the
        underlying sqlite3.connect() function was called with the
        correct database URI and that the execute() method of the
        mock cursor object was called.
        """
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