from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import shutil
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.secret_key = 'rk_welding_secret_key' # In a real app, use a secure random key

# Database and Upload Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB max upload size
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin Credentials
ADMIN_USER = 'admin'
ADMIN_PASS = 'welding123'

# --- MODELS ---
class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

# In-memory storage for messages for demonstration purposes
messages = []

# --- PUBLIC ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/gallery')
def gallery():
    images = GalleryImage.query.order_by(GalleryImage.uploaded_at.desc()).all()
    return render_template('gallery.html', images=images)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        if name and phone and message:
            messages.append({'name': name, 'phone': phone, 'message': message})
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill out all fields.', 'error')
            
    return render_template('contact.html')

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- ADMIN ROUTES ---
@app.route('/admin')
def admin_redirect():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials.', 'error')
            
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part in the form.', 'error')
            return redirect(request.url)
            
        file = request.files['image']
        title = request.form.get('title', 'Untitled')
        
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            new_image = GalleryImage(filename=unique_filename, title=title)
            db.session.add(new_image)
            db.session.commit()
            
            flash('Image uploaded successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid file type. Allowed: png, jpg, jpeg, gif, webp', 'error')
            
    images = GalleryImage.query.order_by(GalleryImage.uploaded_at.desc()).all()
    return render_template('admin_dashboard.html', images=images)

@app.route('/admin/delete/<int:id>', methods=['POST'])
def admin_delete_image(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    image = GalleryImage.query.get_or_404(id)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error removing file: {e}")
            
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

# --- SETUP SCRIPT ---
if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    with app.app_context():
        db.create_all()
        # Seed initial gallery images if empty
        if GalleryImage.query.count() == 0:
            initial_images = [
                {'filename': 'gallery_heavy_welding_1772957216709.png', 'title': 'Heavy Duty Welding'},
                {'filename': 'gallery_iron_gate_1772957236931.png', 'title': 'Custom Gate Design'},
                {'filename': 'hero_welding_bg_1772957181063.png', 'title': 'Industrial Structures'},
                {'filename': 'gallery_window_grill_1772957273883.png', 'title': 'Window Grills'},
                {'filename': 'gallery_metal_furniture_1772957354593.png', 'title': 'Precision Fabrication'},
                {'filename': 'about_welding_1772957199790.png', 'title': 'On-site Repair'}
            ]
            
            static_images_dir = os.path.join('static', 'images')
            for img in initial_images:
                src = os.path.join(static_images_dir, img['filename'])
                dst = os.path.join(app.config['UPLOAD_FOLDER'], img['filename'])
                if os.path.exists(src):
                    if not os.path.exists(dst):
                        shutil.copy(src, dst)
                    new_img = GalleryImage(filename=img['filename'], title=img['title'])
                    db.session.add(new_img)
            db.session.commit()
            
    app.run(debug=True, port=5000)
