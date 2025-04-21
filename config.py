import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    PRODUCT_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'products')
    # Add any other configuration variables (e.g., external conversion server URL)
    CONVERSION_SERVER_URL = "https://converter.example.com/api/convert"  # Replace with your conversion server URL
