import os

# --- VERCEL CONFIGURATION ---
# Vercel is a read-only serverless environment except for the /tmp directory.
# We must store uploads and the SQLite database in /tmp when running on Vercel.
IS_VERCEL = os.environ.get('VERCEL') == '1'

if IS_VERCEL:
    # On Vercel, everything must go to /tmp
    UPLOAD_FOLDER = '/tmp/uploads'
    DB_PATH = 'sqlite:////tmp/gallery.db'
else:
    # On local machine, use the standard project folders
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'images', 'gallery_uploads')
    DB_PATH = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'gallery.db')

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
