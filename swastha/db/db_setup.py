# db/db_setup.py
# Creates the database and required tables if they don't exist

import mysql.connector
from mysql.connector import Error
import sys
import os

# Enable imports from project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from config import DB_CONFIG


def setup_database():
    """
    1. Connects to MySQL without specifying a database.
    2. Creates the 'swastha' database if it doesn't exist.
    3. Creates all required tables.
    """
    try:
        # Connect without selecting a database
        conn_params = {k: v for k, v in DB_CONFIG.items() if k != "database"}
        conn = mysql.connector.connect(**conn_params)
        cursor = conn.cursor()

        # Create database and select it
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS swastha "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cursor.execute("USE swastha")

        # ── Users Table ───────────────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(150) UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ── Medicine Reminders Table ─────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicine_reminders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                medicine_name VARCHAR(150) NOT NULL,
                reminder_time VARCHAR(10) NOT NULL,
                frequency VARCHAR(50) DEFAULT 'Daily',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

        print("[DB SETUP] Database and tables created successfully.")
        return True

    except Error as e:
        print(f"[DB SETUP ERROR] {e}")
        return False


if __name__ == "__main__":
    setup_database()