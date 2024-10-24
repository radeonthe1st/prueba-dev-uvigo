import asyncio
import time
import struct #type: ignore
import random #type: ignore

class DataCapture:
    def __init__(self, db, reading_frequency, sensor_type, min_value=None, max_value=None):
        """
        Initialize DataCapture object.

        Args:
            db (DatabaseManager): The object to handle database operations.
            reading_frequency (int): The frequency in seconds to capture sensor data.
            sensor_type (str): Type of sensor to use, either 'mockup' or 'real'.
            min_value (int, optional): Minimum value of generated data if sensor_type is 'mockup'. Defaults to None.
            max_value (int, optional): Maximum value of generated data if sensor_type is 'mockup'. Defaults to None.
        """
        self.db = db
        self.reading_frequency = reading_frequency
        self.sensor_type = sensor_type
        self.min_value = min_value
        self.max_value = max_value
        self.capture_task = None
    
    def read_data(self):
        """
        Generate mockup sensor data.
        Returns a list of 64 random integers between specified min and max values.
        """
        if self.sensor_type == 'mockup':
            return [random.randint(self.min_value, self.max_value) for _ in range(64)]
        else:
            # TO DO: implement real sensor reading logic here
            print('Non-mockup sensors not yet supported')
            pass


    async def capture_loop(self):
        """
        Asynchronous loop to continuously capture sensor data at specified intervals
        and store the captured data in the SQLite database.
        """
        global capture_running
        capture_running = True
        print(f"Starting capture with sensor type: {self.sensor_type}")
        
        # Loop until capture_running is set to False
        while capture_running:
            # Read data from the sensor (mockup or real)
            data = self.read_data()
            
            # Pack the data as a binary BLOB for storage
            packed_data = struct.pack('64H', *data)
            
            # Insert the packed data along with the current timestamp into the database
            self.db.execute(
                "INSERT INTO infrared_data (reading_time, data) VALUES (?, ?)",
                (time.time(), packed_data)
            )
            
            # Wait for the specified reading frequency before capturing the next data
            await asyncio.sleep(self.reading_frequency)


    async def start_capture(self):
        """
        Start the data capture process by creating an asynchronous capture loop task.
        """
        self.capture_task = asyncio.create_task(self.capture_loop())


    async def stop_capture(self):
        """
        Stop the data capture process by canceling the capture loop task.

        This function sets the ``capture_running`` flag to ``False`` and
        cancels the capture loop task. If the capture loop task is already
        running, it will be cancelled and the task will be set to ``None``.
        """
        if self.capture_task:
            try:
                # Cancel the capture loop task
                self.capture_task.cancel()
                # Wait for the task to be cancelled
                await self.capture_task
            except asyncio.CancelledError:
                print("Capture task cancelled")
        else:
            print("No capture task running")
        # Set the capture task to None
        self.capture_task = None
        # Set the capture_running flag to False
        capture_running = False
        # Print a message to indicate that the capture has stopped
        print("Stopping capture")
