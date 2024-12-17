from flask import Flask
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    register_routes(app)  # Asegúrate de que las rutas están registradas
    return app
