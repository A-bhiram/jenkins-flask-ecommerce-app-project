from flask import Flask
from app.routes import main

def create_app():
    app = Flask(_name_)
    app.register_blueprint(main)
    return app
