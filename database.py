import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('school_fee.db')
    c = conn.cursor()
    
    # Students table
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  class TEXT NOT NULL,
                  section TEXT,
                  roll_no INTEGER,
                  father_name TEXT,
                  contact TEXT,
                  address TEXT,
                  admission_date TEXT)''')
    
    # Fee structure table
    c.execute('''CREATE TABLE IF NOT EXISTS fee_structure
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class TEXT NOT NULL,
                  fee_type TEXT NOT NULL,
                  amount REAL NOT NULL,
                  due_date TEXT)''')
    
    # Payments table
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER NOT NULL,
                  amount REAL NOT NULL,
                  payment_date TEXT NOT NULL,
                  fee_type TEXT NOT NULL,
                  receipt_no TEXT UNIQUE,
                  FOREIGN KEY(student_id) REFERENCES students(id))''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('school_fee.db')

if __name__ == "__main__":
    create_database()
    # database.py
import sqlite3
from datetime import datetime
import hashlib

def create_database():
    conn = sqlite3.connect('school_fee.db')
    c = conn.cursor()
    
    # Students table
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  class TEXT NOT NULL,
                  section TEXT,
                  roll_no INTEGER,
                  father_name TEXT,
                  contact TEXT,
                  address TEXT,
                  admission_date TEXT)''')
    
    # Fee structure table
    c.execute('''CREATE TABLE IF NOT EXISTS fee_structure
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class TEXT NOT NULL,
                  fee_type TEXT NOT NULL,
                  amount REAL NOT NULL,
                  due_date TEXT,
                  reminder_days INTEGER DEFAULT 7)''')  # Added reminder days field
    
    # Payments table
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER NOT NULL,
                  amount REAL NOT NULL,
                  payment_date TEXT NOT NULL,
                  fee_type TEXT NOT NULL,
                  receipt_no TEXT UNIQUE,
                  FOREIGN KEY(student_id) REFERENCES students(id))''')
    
    # Users table for authentication
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  role TEXT NOT NULL DEFAULT 'admin')''')
    
    # Check if admin user exists
    c.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
    if c.fetchone()[0] == 0:
        # Create default admin user
        hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  ("admin", hashed_password))
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('school_fee.db')

if __name__ == "__main__":
    create_database()
    print("Database initialized successfully with default admin user (username: admin, password: admin123)")
    