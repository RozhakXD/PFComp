from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # Maximum 50 Mb

    from .routes import main
    app.register_blueprint(main)

    return app
