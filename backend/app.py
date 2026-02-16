import sqlite3
import os
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from livereload import Server

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your-secret-key-change-in-production'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('portfolio.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['logged_in'] = True
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, '../templates')
    static_dir = os.path.join(base_dir, '../static')
    
    # Watch for file changes
    server.watch(os.path.join(templates_dir, '*.html'))
    server.watch(os.path.join(static_dir, 'css', '*.css'))
    server.watch(os.path.join(static_dir, 'js', '*.js'))
    server.watch('*.py')
    
    server.serve(debug=True, host='127.0.0.1', port=5000, restart_delay=1)