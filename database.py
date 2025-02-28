import sqlite3

class Database:
    def __init__(self, db_file="fitness_tracker.db"):
        self.db_file = db_file
        self.initialize_database()

    def initialize_database(self):
        """Create the database and tables if they don't exist."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # Create exercises table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    exercise TEXT NOT NULL,
                    duration INTEGER NOT NULL
                )
            """
            )
            # Create calories table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS calories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    calories INTEGER NOT NULL
                )
            """
            )
            conn.commit()

    def get_connection(self):
        """Return a connection to the database."""
        return sqlite3.connect(self.db_file)