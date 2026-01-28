# AI Coding Mentor - Backend

A Flask-based REST API for an AI-powered coding education platform using Groq's Llama 3.3 70B model.

## Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 🗺️ **AI Roadmap Generation** - Personalized learning paths using Groq AI
- 💬 **Intelligent Chatbot** - Context-aware coding assistance
- 🔍 **Code Analysis** - AI-powered code review and suggestions
- 📊 **Dashboard Analytics** - Track learning progress and activity

## Tech Stack

- **Framework**: Flask 3.1
- **Database**: SQLite with Flask-SQLAlchemy
- **Authentication**: Flask-JWT-Extended
- **AI Provider**: Groq API (Llama 3.3 70B)
- **Password Hashing**: Flask-Bcrypt
- **CORS**: Flask-CORS

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=gsk_your_api_key_here
```

Get your Groq API key from: https://console.groq.com/keys

### 4. Run the Application

```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### Authentication (`/api/auth`)

- `POST /signup` - Register new user
- `POST /login` - User login
- `GET /me` - Get current user (protected)

### Roadmap (`/api/roadmap`)

- `POST /generate` - Generate learning roadmap (protected)
- `GET /my-roadmaps` - Get user's roadmaps (protected)
- `GET /<id>` - Get specific roadmap (protected)
- `DELETE /<id>` - Delete roadmap (protected)

### Chatbot (`/api/chatbot`)

- `POST /send` - Send message to chatbot (protected)
- `GET /history` - Get chat history (protected)
- `DELETE /clear` - Clear chat history (protected)
- `DELETE /message/<id>` - Delete specific message (protected)

### Code Analyzer (`/api/analyzer`)

- `POST /analyze` - Analyze code (protected)
- `GET /history` - Get analysis history (protected)
- `GET /<id>` - Get specific submission (protected)
- `DELETE /<id>` - Delete submission (protected)
- `DELETE /clear` - Clear analysis history (protected)

### Dashboard (`/api/dashboard`)

- `GET /stats` - Get comprehensive user statistics (protected)
- `GET /summary` - Get quick summary (protected)

## Project Structure

```
backend/
├── app.py                 # Application factory
├── config.py             # Configuration
├── extensions.py         # Extension instances
├── models.py            # Database models
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore file
└── routes/
    ├── auth.py          # Authentication routes
    ├── roadmap.py       # Roadmap generation routes
    ├── chatbot.py       # Chatbot routes
    ├── code_analyzer.py # Code analysis routes
    └── dashboard.py     # Dashboard routes
```

## Key Implementation Details

### JWT Authentication Fix

The application uses **string-based JWT identities** to avoid the "Subject must be a string" error:

```python
# Creating token
token = create_access_token(identity=str(user.id))

# Reading token in protected routes
user_id = int(get_jwt_identity())
```

### SQLAlchemy Initialization

Proper initialization to avoid circular imports:

```python
# extensions.py
db = SQLAlchemy()

# app.py
db.init_app(app)
```

### CORS Configuration

Configured to allow requests from React frontend:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## Database Models

- **User** - User accounts with authentication
- **Roadmap** - AI-generated learning paths
- **ChatMessage** - Chatbot conversation history
- **CodeSubmission** - Code analysis history

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_APP` | Flask application entry point | `app.py` |
| `FLASK_ENV` | Environment mode | `development` |
| `SECRET_KEY` | Flask secret key | Required |
| `JWT_SECRET_KEY` | JWT secret key | Required |
| `SQLALCHEMY_DATABASE_URI` | Database connection string | `sqlite:///coding_mentor.db` |
| `GROQ_API_KEY` | Groq API key | Required |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

## Security Notes

⚠️ **Important for Production:**

1. Change `SECRET_KEY` and `JWT_SECRET_KEY` to strong random values
2. Use PostgreSQL or MySQL instead of SQLite
3. Set `FLASK_ENV=production`
4. Use HTTPS for all communications
5. Implement rate limiting
6. Add input validation and sanitization
7. Configure proper CORS origins

## Testing the API

### Health Check

```bash
curl http://localhost:5000/api/health
```

### Register User

```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "skill_level": "beginner",
    "primary_language": "Python"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Generate Roadmap (Protected)

```bash
curl -X POST http://localhost:5000/api/roadmap/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "programming_language": "Python",
    "skill_level": "beginner",
    "career_goal": "Full Stack Developer"
  }'
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "message": "Error description"
}
```

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.
