from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()  # Carga el archivo .env

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key')

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
