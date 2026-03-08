# RK Welding Workshop Website

A dynamic, professional website built for RK Welding Workshop using Flask, Vanilla CSS, and JavaScript.

## 🛠️ Technology Stack
- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3 (Custom Styling), JavaScript
- **Templates:** Jinja2
- **Icons:** FontAwesome
- **Fonts:** Google Fonts (Outfit, Roboto)

## 📁 Project Structure
```text
rk_welding/
│
├── app.py                  # Main Flask application
├── README.md               # Project documentation
│
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Custom styles
│   ├── js/
│   │   └── main.js         # Interactivity and animations
│   └── images/             # Uploaded/stored images
│
└── templates/              # HTML Templates
    ├── base.html           # Main layout block
    ├── index.html          # Home Page
    ├── about.html          # About Us Page
    ├── services.html       # Services Overview
    ├── gallery.html        # Project Gallery
    └── contact.html        # Contact Form & Map
```

## 🚀 How to Run Locally

### Prerequisites
1. Ensure you have **Python 3.7+** installed on your system.
2. (Optional but recommended) Set up a virtual environment.

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd path/to/rk_welding
   ```

2. **Install Flask:**
   If you don't have Flask installed, run:
   ```bash
   pip install flask
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

4. **View the Website:**
   Open your web browser and go to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🌟 Features Implemented
- **Industrial Design Theme:** Utilizing steel gray, extreme dark backgrounds, and an industrial orange accent to represent metal works, combining bold and modern typography.
- **Dynamic Contact Form:** Displays success messages using Flask's messaging system.
- **Scroll Animations:** JavaScript-powered intersection observer animations for elements scrolling into view.
- **Floating Action Button:** WhatsApp integration for easy contact.
- **Responsive Navigation:** A mobile-friendly hamburger menu.
- **Google Maps Ready:** Embedded physical address map on the contact page.
