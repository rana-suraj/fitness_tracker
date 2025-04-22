import sqlite3
from threading import Lock

class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the database connection with thread-safe settings"""
        self.conn = sqlite3.connect(
            "fitness_tracker.db",
            check_same_thread=False,  # Allow multiple threads
            timeout=30.0,  # Wait longer for locks
            isolation_level=None  # Enable autocommit
        )
        self.conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        self.initialize_database()

    def initialize_database(self):
        """Create tables with thread-safe execution"""
        with self._lock:
            try:
                cursor = self.conn.cursor()
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Create exercises table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS exercises (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        exercise TEXT NOT NULL,
                        duration INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                # Create calories table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS calories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        calories INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Database initialization error: {e}")

    def get_connection(self):
        """Get a thread-safe database connection"""
        return self.conn

    def close(self):
        """Properly close the database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()