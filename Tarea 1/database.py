from logging.handlers import RotatingFileHandler
import sqlite3
import logging

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

class DatabaseManager:
    """
    Class to manage database operations.
    """

    def __init__(self, db_uri):
        """
        Initialize DatabaseManager object.

        Args:
            db_uri (str): URI of the SQL database.
        """
        self.db_uri = db_uri

    def connect(self):
        """
        Connect to the database.

        Connects to the database at the URI specified by the constructor,
        and creates a cursor object for executing queries.
        """
        logger.info("Connecting to database at URI: %s", self.db_uri)
        self.conn = sqlite3.connect(self.db_uri)
        self.cursor = self.conn.cursor()

        # Create table to store infrared sensor data
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS infrared_data (
                id INTEGER PRIMARY KEY,
                reading_time REAL,
                data BLOB
            );
        """)

    def execute(self, query, params=None):
        """
        Execute database query.

        Args:
            query (str): SQL query to execute.
            params (tuple, optional): Parameters to pass to the query. Defaults to None.
        """
        logger.debug("Executing SQL query: %s", query)
        # Execute database query
        if params is not None:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        logger.debug("Query executed successfully")

    def close(self):
        """
        Close database connection.
        """
        logger.info("Closing database connection")
        self.conn.close()