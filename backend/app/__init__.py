from flask import Flask, jsonify
from .config import Config
from .database import db
from .routes.auth_routes import auth_bp, init_oauth
from .routes.chatbot_routes import chatbot_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

    # Initialize OAuth
    init_oauth(app)

    # Initialize health func
    @app.route('/api/health')
    def health():
        return jsonify({'status':'ok'})

    return app