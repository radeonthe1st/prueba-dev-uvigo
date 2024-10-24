import argparse #type: ignore

def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Infrared Sensor Reader')
    parser.add_argument('--sensor-type', type=str, choices=['mockup', 'real'], required=True, help='Type of sensor to use')
    parser.add_argument('--reading-frequency', type=int, required=True, help='Frequency of sensor readings')
    parser.add_argument('--min-value', type=int, help='Minimum value of generated data (only used with --sensor-type mockup)')
    parser.add_argument('--max-value', type=int, help='Maximum value of generated data (only used with --sensor-type mockup)')
    parser.add_argument('--db-uri', type=str, required=True, help='URI of the SQL database')

    # Add a check to ensure that --min-value and --max-value are provided when --sensor-type is mockup
    def check_mockup_args(args):
        if args.sensor_type == 'mockup':
            if not args.min_value or not args.max_value:
                parser.error('--min-value and --max-value are required when --sensor-type is mockup')
        return args

    return parser.parse_args(args)