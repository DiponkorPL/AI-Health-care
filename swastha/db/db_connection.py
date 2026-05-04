# db/db_connection.py
# Handles MySQL connection using Singleton Pattern

import mysql.connector
from mysql.connector import Error
import sys
import os

# Enable imports from project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from config import DB_CONFIG


class DatabaseConnection:
    """
    Singleton class responsible for managing a single MySQL connection instance.
    """

    _instance = None  # Stores the active connection

    @classmethod
    def get_connection(cls):
        """
        Returns an active MySQL connection.
        Creates a new one if no connection exists or if it's disconnected.
        """
        if cls._instance is None or not cls._instance.is_connected():
            try:
                cls._instance = mysql.connector.connect(**DB_CONFIG)
            except Error as e:
                print(f"[DB ERROR] Could not connect to MySQL: {e}")
                return None

        return cls._instance

    @classmethod
    def close(cls):
        """
        Closes the current database connection if it exists.
        """
        if cls._instance and cls._instance.is_connected():
            cls._instance.close()
            cls._instance = None


def get_db():
    """
    Helper function to get the active database connection.
    """
    return DatabaseConnection.get_connection()