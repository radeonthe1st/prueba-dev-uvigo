import sqlite3

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
        # Execute database query
        if params is not None:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        """
        Close database connection.
        """
        self.conn.close()
