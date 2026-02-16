"""
Database management for Portfolio Website
"""

import sqlite3
from werkzeug.security import generate_password_hash


def init_db():
    """Initialize database and create default admin user if not exists"""
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    
    # Check if admin user exists
    c.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    if not c.fetchone():
        # Create default admin user
        username = 'admin'
        password = 'admin123'
        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hashed_password))
        conn.commit()
        print("✅ Database initialized!")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
    
    conn.close()


def get_user(username):
    """Get user by username"""
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user
