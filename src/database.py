import sqlite3

class Database:
    def __init__(self, db_file="fitness_tracker.db"):
        self.db_file = db_file
        self.initialize_database()

    def initialize_database(self):
        """Create the database and tables if they don't exist."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # Create users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            # Create exercises table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    exercise TEXT NOT NULL,
                    duration INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """
            )
            # Create calories table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS calories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    calories INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """
            )
            conn.commit()

    def get_connection(self):
        """Return a connection to the database."""
        return sqlite3.connect(self.db_file)