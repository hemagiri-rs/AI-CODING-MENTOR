from datetime import datetime
from extensions import db

class User(db.Model):
    """User model for authentication and profile data."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    skill_level = db.Column(db.String(50), nullable=False)  # beginner, intermediate, advanced
    primary_language = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    roadmaps = db.relationship('Roadmap', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True, cascade='all, delete-orphan')
    code_submissions = db.relationship('CodeSubmission', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'skill_level': self.skill_level,
            'primary_language': self.primary_language,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class Roadmap(db.Model):
    """Roadmap model for storing personalized learning paths."""
    
    __tablename__ = 'roadmaps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    language = db.Column(db.String(50), nullable=False)
    skill_level = db.Column(db.String(50), nullable=False)
    career_goal = db.Column(db.String(200), nullable=False)
    roadmap_data = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert roadmap object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'language': self.language,
            'skill_level': self.skill_level,
            'career_goal': self.career_goal,
            'roadmap_data': self.roadmap_data,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Roadmap {self.id} - {self.language}>'


class ChatMessage(db.Model):
    """ChatMessage model for storing chatbot conversation history."""
    
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'bot'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert chat message object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'sender': self.sender,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ChatMessage {self.id} - {self.sender}>'


class CodeSubmission(db.Model):
    """CodeSubmission model for storing code analysis history."""
    
    __tablename__ = 'code_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    language = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Text, nullable=False)
    analysis_result = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert code submission object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'language': self.language,
            'code': self.code,
            'analysis_result': self.analysis_result,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<CodeSubmission {self.id} - {self.language}>'
