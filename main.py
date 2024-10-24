import asyncio
import nats_client_dev
import database
import data_capture_module
import cli
import sys
import os

# Enable debug mode
DEBUG = True

async def main():
    """
    Main function to initialize database connection, NATS client, subscribe to NATS
    messages and start the event loop.
    """
    if DEBUG:
        print('Running in debug mode')
        print('=====================')
        print('Housekeeping tasks:')

        print("Removing old database...")
        try:
            path_to_database = os.getcwd() + "/infrared.db"
            if os.path.exists(path_to_database):
                os.remove(path_to_database)
                print("Removed old database")
            else:
                print("No old database found")
        except Exception as e:
            print(f"Error removing old database: {e}")

        print("Housekeeping tasks complete")
        print()

    # Parse and print command-line arguments
    args = cli.parse_args(sys.argv[1:])
    
    args_dict = {key: value for key, value in vars(args).items()}
    print('==== Arguments ====')
    for key, value in args_dict.items():
        print(f"{key:<20} {value}")
    print('===================')
    print()

    # Initialize database connection
    db = database.DatabaseManager(args.db_uri)
    db.connect()

    # Initialize NATS client
    exit_event = asyncio.Event()

    nats_client = nats_client_dev.NATSClient("nats://localhost:4222", db, args, exit_event)

    try:
        # Connect to NATS server
        await nats_client.connect()
    except Exception as e:
        # Handle any errors connecting to the NATS server
        print(f"Error connecting to NATS server: {e}")
        # Close the database connection and exit the program
        await nats_client.close()
        return

    # Subscribe to NATS messages for starting and stopping capture
    await nats_client.subscribe("test.*", cb=nats_client.message_handler)

    # Keep the program running to listen for NATS messages
    while not exit_event.is_set():
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
