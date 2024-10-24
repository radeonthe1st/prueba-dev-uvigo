import asyncio
import nats
import data_capture_module

class NATSClient:
    def __init__(self, server, db, args):
        """
        Initialize NATSClient object.

        Args:
            server (str): The NATS server URL.
            db (DatabaseManager): The database manager instance for handling database operations.
            args (argparse.Namespace): Parsed command-line arguments containing configurations.
        """
        self.server = server
        self.nc = None
        self.data_capture = None
        self.db = db
        self.args = args

    async def connect(self):
        """
        Establish a connection to the NATS server.

        This method connects to the specified NATS server using the provided server URI.
        Upon successful connection, a message is printed to indicate the connection status.
        """
        self.nc = await nats.connect(self.server)
        print("NATS client connected successfully")

    async def subscribe(self, subject, cb=None):
        """
        Subscribe to a NATS subject with an optional callback function.

        Args:
            subject (str): The subject to subscribe to.
            cb (callable, optional): An optional callback function to process messages.
        """
        await self.nc.subscribe(subject, cb=cb)

    async def message_handler(self, msg):
        """
        Handle incoming NATS messages and perform actions based on the message subject.

        Args:
            msg (nats.aio.msg.Msg): The received NATS message object.
        
        Handles the following message subjects:
            - "test.start_capture": Starts data capture if not already running.
            - "test.stop_capture": Stops data capture if it is currently running.
        """
        if msg.subject == "test.start_capture":
            if not self.data_capture:
                # Initialize DataCapture object with command-line arguments
                self.data_capture = data_capture_module.DataCapture(
                    self.db,
                    self.args.reading_frequency,
                    self.args.sensor_type,
                    self.args.min_value,
                    self.args.max_value
                )
            # Start data capture
            await self.data_capture.start_capture()
        elif msg.subject == "test.stop_capture":
            if self.data_capture:
                # Stop data capture
                await self.data_capture.stop_capture()

    async def close(self):
        """
        Close the NATS connection.

        This method terminates the connection to the NATS server, ensuring that
        any resources are properly released.
        """
        await self.nc.close()

