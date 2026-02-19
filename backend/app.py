import os
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from livereload import Server
from database import *

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your-secret-key-change-in-production'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html',
                           header=get_header_content(),
                           home=get_home_content(),
                           about=get_about_content(),
                           skills=get_skills_content(),
                           tech_items=get_all_tech_items(),
                           awards=get_all_awards(),
                           certificates=get_all_certificates(),
                           projects=get_projects_content(),
                           contact=get_contact_content()
                    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not password:
            return render_template('login.html', error='Password is Required')
        
        user = verify_user(username, password)
        
        if user:
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user['id']
            return redirect('/admin')
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect('/login')
    
    username = session.get('username', 'User')
    return render_template('admin.html',
                           username = username,
                           header=get_header_content(),
                           home=get_home_content(),
                           about=get_about_content(),
                           skills=get_skills_content(),
                           tech_items=get_all_tech_items(),
                           awards=get_all_awards(),
                           certificates=get_all_certificates(),
                           projects=get_projects_content(),
                           contact=get_contact_content()
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/admin/update-header', methods=['POST'])
def update_header_route():
    data = {'logo_text': request.form.get('logo_text')}
    update_header_content(data)
    return redirect(url_for('admin'))

@app.route('/admin/update-home', methods=['POST'])
def update_home_route():
    data = {
        'greeting' : request.form.get('greeting'),
        'subtitle' : request.form.get('subtitle')
    }

    file = request.files.get('profile_image')
        
    if isinstance(file, FileStorage) and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        data['profile_image'] = '/static/uploads/' + filename

    update_home_content(data)
    return redirect(url_for('admin'))

@app.route('/admin/update-about', methods=['POST'])
def update_about_route():
    data = {
        'title' : request.form.get('title'),
        'description' : request.form.get('description'),
        'hobbies' : request.form.get('hobbies'),
        'skills' : request.form.get('skills')
    }
    update_about_content(data)
    return redirect(url_for('admin'))

@app.route('/admin/update-skills', methods=['POST'])
def update_skills_route():
    data = {
        'section_title' : request.form.get('section_title'),
        'description' : request.form.get('description')
    }
    update_skills_content(data)
    return redirect(url_for('admin'))

@app.route('/admin/add-tech-item', methods=['POST'])
def add_tech_item_route():
    data = {
        'name' : request.form.get('name'),
        'order_num' : request.form.get('order_num', 0)
    }
    file = request.files.get('icon')
        
    if isinstance(file, FileStorage) and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        data['icon'] = '/static/uploads/' + filename

    
    add_tech_item(data)
    return redirect(url_for('admin'))

@app.route('/admin/delete-tech-item/<int:item_id>', methods=['DELETE'])
def delete_tech_item_route(item_id):
    delete_tech_item(item_id)
    return jsonify({'success' : True}), 200

@app.route('/admin/add-award', methods=['POST'])
def add_award_route():
    data = {
        'title' : request.form.get('title'),
        'details' : request.form.get('details'),
        'order_num' : request.form.get('order_num', 0)
    }
    add_award(data)
    return redirect(url_for('admin'))

@app.route('/admin/delete-award/<int:award_id>', methods=['DELETE'])
def delete_award_route(award_id):
    delete_award(award_id)
    return jsonify({'success' : True}), 200

@app.route('/admin/add-certificate', methods=['POST'])
def add_certificate_route():
    data = {
        'alt_text' : request.form.get('alt_text'),
        'order_num' : request.form.get('order_num', 0)
    }
    
    
    file = request.files.get('cert_image')
        
    if isinstance(file, FileStorage) and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        data['image'] = '/static/uploads/' + filename

    add_certificate(data)
    return redirect(url_for('admin'))

@app.route('/admin/delete-certificate/<int:cert_id>', methods=['DELETE'])
def delete_certificate_route(cert_id):
    delete_certificate(cert_id)
    return jsonify({'success' : True}), 200

@app.route('/admin/update-projects', methods=['POST'])
def update_projects_route():
    data = {
        'section_title' : request.form.get('section_title'),
        'message' : request.form.get('message')
    }
    update_projects_content(data)
    return redirect(url_for('admin'))

@app.route('/admin/update-contact', methods=['POST'])
def update_contact_route():
    data = {
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'facebook': request.form.get('facebook'),
            'github': request.form.get('github'),
            'linkedin': request.form.get('linkedin'),
    }
    update_contact_content(data)
    return redirect(url_for('admin'))

if __name__ == "__main__":
    # Initialize database on startup
    init_db()
    
    server = Server(app.wsgi_app)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, '../templates')
    static_dir = os.path.join(base_dir, '../static')
    
    # Watch for file changes
    server.watch(os.path.join(templates_dir, '*.html'))
    server.watch(os.path.join(templates_dir, '.trigger'))
    server.watch(os.path.join(static_dir, 'css', '*.css'))
    server.watch(os.path.join(static_dir, 'js', '*.js'))
    server.watch('*.py')
    
    server.serve(debug=True, port=5000, restart_delay=1)
