import logging
from logging.handlers import RotatingFileHandler
import asyncio
import nats_client_dev
import database
import data_capture_module
import cli
import sys
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger.addHandler(file_handler)
logger.addHandler(console_handler)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Enable debug mode
DEBUG = True

async def main():
    """
    Main function to initialize database connection, NATS client, subscribe to NATS
    messages and start the event loop.
    """
    logger.debug("Running main function")
    logger.debug("DEBUG mode is enabled")

    # Parse and print command-line arguments
    args = cli.parse_args(sys.argv[1:])
    
    args_dict = {key: value for key, value in vars(args).items()}
    logger.debug('==== Arguments ====')
    for key, value in args_dict.items():
        logger.debug(f"{key:<20} {value}")
    logger.debug('===================')

    if DEBUG:
        logger.info('Running in debug mode')
        logger.info('=====================')
        logger.info('Housekeeping tasks:')

        logger.debug("Removing old database...")
        try:
            path_to_database = args.db_uri
            if os.path.exists(path_to_database):
                os.remove(path_to_database)
                logger.info("Removed old database")
            else:
                logger.info("No old database found")
        except Exception as e:
            logger.error(f"Error removing old database: {e}")

        logger.debug("Housekeeping tasks complete")


    # Initialize database connection
    db = database.DatabaseManager(args.db_uri)
    logger.debug("Initializing database connection")
    db.connect()

    # Initialize NATS client
    exit_event = asyncio.Event()

    nats_client = nats_client_dev.NATSClient("nats://localhost:4222", db, args, exit_event)

    try:
        # Connect to NATS server
        logger.debug("Connecting to NATS server")
        await nats_client.connect()
    except Exception as e:
        # Log  any errors connecting to the NATS server
        logger.error(f"Error connecting to NATS server: {e}")
        # Close the database connection and exit the program
        logger.debug("Closing database connection")
        await nats_client.close()
        return

    # Subscribe to NATS messages for starting and stopping capture
    logger.debug("Subscribing to NATS messages")
    await nats_client.subscribe("test.*", cb=nats_client.message_handler)

    # Keep the program running to listen for NATS messages
    logger.debug("Starting event loop")
    while not exit_event.is_set():
        logger.debug("Waiting for NATS messages")
        await asyncio.sleep(1)

if __name__ == "__main__":
    logger.debug("Starting main function")
    asyncio.run(main())
