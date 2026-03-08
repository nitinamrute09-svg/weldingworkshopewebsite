from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'rk_welding_secret_key' # In a real app, use a secure random key

# In-memory storage for messages for demonstration purposes
messages = []

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
    return render_template('gallery.html')

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

if __name__ == '__main__':
    # Ensure templates and static directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    app.run(debug=True, port=5000)
