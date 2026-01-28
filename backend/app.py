from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import extensions
from extensions import db, bcrypt, jwt

# Import configuration
from config import Config

def create_app(config_class=Config):
    """Application factory pattern."""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Import models (required before db.create_all())
    from models import User, Roadmap, ChatMessage, CodeSubmission
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.roadmap import roadmap_bp
    from routes.chatbot import chatbot_bp
    from routes.code_analyzer import analyzer_bp
    from routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(roadmap_bp, url_prefix='/api/roadmap')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(analyzer_bp, url_prefix='/api/analyzer')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
    
    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'AI Coding Mentor API is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting AI Coding Mentor API...")
    print(f"📍 API running on http://localhost:5000")
    print(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True, host='0.0.0.0', port=5000)
