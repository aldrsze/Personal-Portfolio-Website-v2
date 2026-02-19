"""
Database management for Portfolio Website
"""

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'portfolio.db')
TRIGGER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates/.trigger')

def trigger_reload():
    """Touch a file to trigger livereload"""
    with open(TRIGGER_FILE, 'w') as f:
        f.write(str(datetime.now()))

def init_db():
    """Initialize database and create default admin user if not exists"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT)''')
    
    # Header content table
    c.execute('''CREATE TABLE IF NOT EXISTS header_content (
        id INTEGER PRIMARY KEY, logo_text TEXT)''')

    # home section table
    c.execute('''CREATE TABLE IF NOT EXISTS home_content (
        id INTEGER PRIMARY KEY, greeting TEXT, subtitle TEXT, profile_image TEXT)''')

    # about section table
    c.execute('''CREATE TABLE IF NOT EXISTS about_content(
        id INTEGER PRIMARY KEY, title TEXT, description TEXT, hobbies TEXT, skills TEXT)''')

    # skills section table
    c.execute('''CREATE TABLE IF NOT EXISTS skills_content(
        id INTEGER PRIMARY KEY, section_title TEXT, description TEXT)''')
    
    # tech stack items table
    c.execute('''CREATE TABLE IF NOT EXISTS tech_items (
        id INTEGER PRIMARY KEY, name TEXT, icon TEXT, order_num INTEGER DEFAULT 0)''')
    
    # awards table
    c.execute('''CREATE TABLE IF NOT EXISTS awards(
        id INTEGER PRIMARY KEY, title TEXT, details TEXT, order_num INTEGER DEFAULT 0)''')
    
    # certificated table
    c.execute('''CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY, image TEXT, alt_text TEXT, order_num INTEGER DEFAULT 0)''')
    
    # projects section table
    c.execute('''CREATE TABLE IF NOT EXISTS projects_content (
        id INTEGER PRIMARY KEY, section_title TEXT, message TEXT)''')
    
    # insert the default admin user
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                  ('admin', generate_password_hash('admin123')))
    conn.commit()
    conn.close()

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def verify_user(username, password):
    conn = db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None

# HEADER
def get_header_content():
    conn = db()
    r = conn.execute("SELECT * FROM header_content LIMIT 1").fetchone()
    
    conn.close()
    return dict(r) if r else {}

def update_header_content(data):
    conn = db()
    existing = conn.execute("SELECT id FROM header_content LIMIT 1").fetchone()
    if existing:
        conn.execute("UPDATE header_content SET logo_text=? WHERE id=?", 
                     (data['logo_text'], existing['id']))
    else:
        conn.execute("INSERT INTO header_content (logo_text) VALUES (?)",
                     (data['logo_text'],))
    conn.commit()
    conn.close()
    trigger_reload()

# home
def get_home_content():
    conn = db()
    r = conn.execute("SELECT * FROM home_content LIMIT 1").fetchone()
    conn.close()
    return dict(r) if r else {}

def update_home_content(data):
    conn = db()
    existing = conn.execute("SELECT id FROM home_content LIMIT 1").fetchone()
    if existing:
        if 'profile_image' in data and data['profile_image']:
            conn.execute("UPDATE home_content SET greeting =?, subtitle =?, profile_image =? WHERE id =? ",
                         (data['greeting'], data['subtitle'], data['profile_image'], existing['id']))
        else:
            conn.execute("UPDATE home_content SET greeting =?, subtitle =? WHERE id =?",
                         (data['greeting'], data['subtitle'], existing['id']))
    else:
        conn.execute("INSERT INTO home_content (greeting, subtitle, profile_image) VALUES (?, ?, ?)",
                     (data['greeting'], data['subtitle'], data.get('profile_image')))
    conn.commit()
    conn.close()
    trigger_reload()

# about
def get_about_content():
    conn = db()
    r = conn.execute("SELECT * FROM about_content LIMIT 1").fetchone()
    conn.close()
    return dict(r) if r else {}

def update_about_content(data):
    conn = db()
    existing = conn.execute("SELECT id FROM about_content LIMIT 1").fetchone()
    if existing:
        conn.execute("UPDATE about_content SET title=?, description=?, hobbies=?, skills=? WHERE id=?",
                     (data['title'], data['description'], data['hobbies'], data['skills'], existing['id']))
    else:
        conn.execute("INSERT INTO about_content (title, description, hobbies, skills) VALUES (?, ?, ?, ?)",
                     (data['title'], data['description'], data['hobbies'], data['skills']))
    conn.commit()
    conn.close()
    trigger_reload()


# skills

def get_skills_content():
    conn = db()
    r = conn.execute("SELECT * FROM skills_content LIMIT 1").fetchone()
    conn.close()
    return dict(r) if r else {}

def update_skills_content(data):
    conn = db()
    existing = conn.execute("SELECT id FROM skills_content LIMIT 1").fetchone()
    if existing:
        conn.execute("UPDATE skills_content SET section_title=?, description=? WHERE id=?", 
                     (data['section_title'], data['description'], existing['id']))
    else:
        conn.execute("INSERT INTO skills_content (section_title, description) VALUES (?, ?)",
                     (data['section_title'], data['description']))
    conn.commit()
    conn.close()
    trigger_reload()


# Tech Stacks
def get_all_tech_items():
    conn = db()
    rows = conn.execute("SELECT * FROM tech_items ORDER BY order_num").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_tech_item(data):
    conn = db()
    conn.execute("INSERT INTO tech_items (name, icon, order_num) VALUES (?, ?, ?)",
                 (data['name'], data.get('icon'), data.get('order_num', 0)))
    conn.commit()
    conn.close()
    trigger_reload()

def delete_tech_item(item_id):
    conn = db()
    conn.execute("DELETE FROM tech_items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    trigger_reload()

# awards
def get_all_awards():
    conn = db()
    rows = conn.execute("SELECT * FROM awards ORDER BY order_num").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_award(data):
    conn = db()
    conn.execute("INSERT INTO awards (title, details, order_num) VALUES (?, ?, ?)",
                 (data['title'], data['details'], data.get('order_num', 0)))
    conn.commit()
    conn.close()
    trigger_reload()

def delete_award(award_id):
    conn = db()
    conn.execute("DELETE FROM awards WHERE id=?", (award_id,))
    conn.commit()
    conn.close()
    trigger_reload()

# certificates
def get_all_certificates():
    conn = db()
    rows = conn.execute("SELECT * FROM certificates ORDER BY order_num").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_certificate(data):
    conn = db()
    conn.execute("INSERT INTO certificates (image, alt_text, order_num) VALUES (?, ?, ?)",
                 (data['image'], data['alt_text'], data.get('order_num', 0)))
    conn.commit()
    conn.close()
    trigger_reload()

def delete_certificate(cert_id):
    conn = db()
    conn.execute("DELETE FROM certificates WHERE id=?", (cert_id,))
    conn.commit()
    conn.close()
    trigger_reload()

# projects
def get_projects_content():
    conn = db()
    r = conn.execute("SELECT * FROM projects_content LIMIT 1").fetchone()
    conn.close()
    return dict(r) if r else {}

def update_projects_content(data):
    conn = db()
    existing = conn.execute("SELECT id FROM projects_content LIMIT 1").fetchone()
    if existing:
        conn.execute("UPDATE projects_content SET section_title=?, message=? WHERE id=?",
                     (data['section_title'], data['message'], existing['id']))
    else:
        conn.execute("INSERT INTO projects_content (section_title, message) VALUES (?, ?)",
                     (data['section_title'], data['message']))
    conn.commit()
    conn.close()
    trigger_reload()

































