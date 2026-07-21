import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture, folder='products', output_size=(800, 800)):
    """Save uploaded picture and return filename."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'uploads', folder, picture_fn)

    # Ensure directory exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    # Resize and save
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return os.path.join('uploads', folder, picture_fn)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def generate_order_number():
    """Generate a unique order number."""
    import secrets
    import string
    timestamp = __import__('datetime').datetime.utcnow().strftime('%Y%m%d')
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f"ORD-{timestamp}-{random_part}"

