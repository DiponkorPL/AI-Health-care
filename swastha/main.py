# main.py
# Entry point for Swastha - AI Smart Healthcare System

import sys
import os

# Ensure project root path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox

from db.db_setup import setup_database
from auth.login import LoginPage


def main():
    # ── Database Setup ─────────────────────────
    ok = setup_database()

    if not ok:
        root = tk.Tk()
        root.withdraw()

        messagebox.showerror("Database Error", "Database connection failed!")

        root.destroy()
        return

    # ── Main App Window ────────────────────────
    root = tk.Tk()

    # Optional: global app title
    root.title("Swastha - AI Healthcare System")

    # Launch Login Page
    app = LoginPage(root)

    # Run app
    root.mainloop()


if __name__ == "__main__":
    main()

