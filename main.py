import nats
import sqlite3
import time
import argparse
import asyncio

parser = argparse.ArgumentParser(description='Infrared Sensor Reader')

parser.add_argument('--sensor-type', type=str, choices=['mockup', 'real'], required=True,
                    help='Sensor type: "mockup" or "real"')
parser.add_argument('--reading-frequency', type=int, required=True,
                    help='Reading frequency in seconds')
parser.add_argument('--min-value', type=int, help='Minimum value generated by the sensor (for "mockup" type)')
parser.add_argument('--max-value', type=int, help='Maximum value generated by the sensor (for "mockup" type)')
parser.add_argument('--db-uri', type=str, required=True,
                    help='URI to the SQL database')

args = parser.parse_args()
args_dict = {key: value for key, value in vars(args).items()}
print('==== Arguments ====')
for key, value in args_dict.items():
    print(f"{key:<20} {value}")
print('===================')
# Initialize sensor reader
if args.sensor_type == 'mockup':
    def read_data():
        """
        Simulate reading data from a mockup sensor.
        
        Returns:
            list: A list of 64 random integer values between min_value and max_value.
        """
        # Generate a list of 64 random integers between the specified min and max values
        return [random.randint(args.min_value, args.max_value) for _ in range(64)]
else:
    def read_data():
        """
        Simulate reading data from a real sensor.
        
        Returns:
            list: A list of 64 integer values read from the real sensor.
        """
        # Replace with real sensor reader implementation
        pass
