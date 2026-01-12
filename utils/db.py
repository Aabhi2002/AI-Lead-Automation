import sqlite3
import os

# Get the project root directory (parent of utils)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "db", "database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)
