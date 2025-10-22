from flask import Flask, jsonify
from .config import Config
from .database import db
from .routes.auth_routes import auth_bp
from .routes.chatbot_routes import chatbot_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

    @app.route('/api/health')
    def health():
        return jsonify({'status':'ok'})

    return app