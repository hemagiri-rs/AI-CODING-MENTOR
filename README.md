# 🚀 AI Coding Mentor - Complete Full Stack Application

An AI-powered platform that helps students learn programming through personalized roadmaps, chatbot assistance, and code analysis using Groq's Llama 3.3 70B model.

## 📋 Project Overview

This is a complete full-stack web application with:
- **Backend**: Flask (Python) REST API
- **Frontend**: React SPA
- **AI Provider**: Groq API (Llama 3.3 70B)
- **Database**: SQLite with SQLAlchemy
- **Authentication**: JWT tokens

## ✨ Features

### 🎯 Core Features
- **User Authentication** - Secure signup/login with JWT
- **AI Roadmap Generator** - Personalized learning paths based on skill level and goals
- **Intelligent Chatbot** - Context-aware coding assistance and explanations
- **Code Analyzer** - AI-powered code review with suggestions
- **Dashboard** - Track learning progress and statistics

### 🔐 Security
- Password hashing with bcrypt
- JWT token authentication
- Protected API routes
- CORS configuration

## 🏗️ Project Structure

```
coding mentor/
├── backend/
│   ├── app.py                    # Flask application factory
│   ├── config.py                 # Configuration
│   ├── extensions.py             # Extension instances
│   ├── models.py                 # Database models
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment variables template
│   └── routes/
│       ├── auth.py               # Authentication endpoints
│       ├── roadmap.py            # Roadmap generation
│       ├── chatbot.py            # Chat endpoints
│       ├── code_analyzer.py      # Code analysis
│       └── dashboard.py          # Statistics
│
└── frontend/
    ├── public/
    │   └── index.html            # HTML template
    ├── src/
    │   ├── components/           # Reusable components
    │   │   ├── Navbar.jsx
    │   │   ├── ProtectedRoute.jsx
    │   │   └── LoadingSpinner.jsx
    │   ├── pages/                # Page components
    │   │   ├── Home.jsx
    │   │   ├── Login.jsx
    │   │   ├── Signup.jsx
    │   │   ├── Dashboard.jsx
    │   │   ├── Roadmap.jsx
    │   │   ├── Chatbot.jsx
    │   │   └── CodeAnalyzer.jsx
    │   ├── services/             # API services
    │   │   ├── api.js
    │   │   └── auth.js
    │   ├── context/              # State management
    │   │   └── AuthContext.jsx
    │   ├── App.js                # Main app component
    │   ├── App.css               # Global styles
    │   └── index.js              # Entry point
    ├── package.json              # Node dependencies
    └── README.md                 # Frontend documentation
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **Groq API Key** (get from https://console.groq.com/keys)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example env file
   copy .env.example .env
   
   # Edit .env and add your Groq API key
   GROQ_API_KEY=gsk_your_api_key_here
   ```

5. **Run the backend**
   ```bash
   python app.py
   ```

   Backend will run on **http://localhost:5000**

### Frontend Setup

1. **Open new terminal and navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

   Frontend will open at **http://localhost:3000**

## 🔑 Getting Your Groq API Key

1. Visit https://console.groq.com/
2. Sign up or log in
3. Go to API Keys section
4. Create new API key
5. Copy the key (starts with `gsk_`)
6. Add to backend `.env` file

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user (protected)

### Roadmap
- `POST /api/roadmap/generate` - Generate learning roadmap (protected)
- `GET /api/roadmap/my-roadmaps` - Get user's roadmaps (protected)

### Chatbot
- `POST /api/chatbot/send` - Send message (protected)
- `GET /api/chatbot/history` - Get chat history (protected)
- `DELETE /api/chatbot/clear` - Clear history (protected)

### Code Analyzer
- `POST /api/analyzer/analyze` - Analyze code (protected)
- `GET /api/analyzer/history` - Get analysis history (protected)

### Dashboard
- `GET /api/dashboard/stats` - Get user statistics (protected)

## 🎨 Features Walkthrough

### 1. Sign Up & Login
- Create account with email, password, skill level, and primary language
- JWT token stored securely
- Automatic redirection to dashboard

### 2. Dashboard
- View profile information
- Track total roadmaps, chats, and code analyses
- See recent activity
- Learning streak counter
- Quick access to all features

### 3. Roadmap Generator
- Select programming language
- Choose skill level (Beginner/Intermediate/Advanced)
- Enter career goal
- AI generates structured learning path with:
  - Multiple learning phases
  - Topics with descriptions
  - Resources and projects
  - Milestones and career tips

### 4. AI Chatbot
- Ask coding questions
- Get explanations and code examples
- Debugging assistance
- Context-aware responses
- Message history saved

### 5. Code Analyzer
- Paste your code
- Select programming language
- Get instant AI analysis with:
  - Quality score (1-10)
  - Strengths identified
  - Issues found (critical/major/minor)
  - Improvement suggestions
  - Best practices
  - Learning resources

## 🎯 Usage Example

### Testing the Application

1. **Sign Up**
   - Navigate to http://localhost:3000/signup
   - Fill in details:
     - Full Name: "John Doe"
     - Email: "john@example.com"
     - Password: "password123"
     - Skill Level: "Beginner"
     - Primary Language: "Python"

2. **Generate Roadmap**
   - Go to Roadmap page
   - Select: Python, Beginner, "Web Developer"
   - Click "Generate Roadmap"
   - View personalized learning path

3. **Chat with AI**
   - Go to Chat page
   - Ask: "How do I create a Python function?"
   - Get detailed explanation

4. **Analyze Code**
   - Go to Analyzer page
   - Paste Python code
   - Get comprehensive feedback

## 🛠️ Tech Stack Details

### Backend
- **Flask 3.1.0** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-Bcrypt** - Password hashing
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - CORS handling
- **Groq 0.9.0** - AI API client
- **SQLite** - Database

### Frontend
- **React 18.2.0** - UI library
- **React Router 6.21.0** - Routing
- **Axios** - HTTP client
- **Context API** - State management
- **CSS3** - Styling

## 🔧 Configuration

### Backend Environment Variables
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
SQLALCHEMY_DATABASE_URI=sqlite:///coding_mentor.db
GROQ_API_KEY=gsk_your_groq_api_key
CORS_ORIGINS=http://localhost:3000
```

### Frontend API Configuration
Located in `frontend/src/services/api.js`:
```javascript
baseURL: 'http://localhost:5000/api'
```

## 🐛 Troubleshooting

### Backend Issues

**ModuleNotFoundError: No module named 'groq'**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Database not created**
- Ensure you run `python app.py` from backend directory
- Database file will be created at `backend/coding_mentor.db`

**CORS errors**
- Verify CORS_ORIGINS in .env includes frontend URL
- Check Flask-CORS is installed

### Frontend Issues

**Cannot connect to backend**
- Ensure backend is running on http://localhost:5000
- Check API baseURL in `src/services/api.js`

**npm install fails**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Blank page on load**
- Check browser console for errors
- Ensure all dependencies installed

## 📝 Development Notes

### Key Implementation Details

1. **JWT Authentication**
   - Tokens use string identity: `str(user.id)`
   - Protected routes convert back: `int(get_jwt_identity())`

2. **Groq Client**
   - Lazy initialization to avoid import errors
   - Model: `llama-3.3-70b-versatile`
   - Temperature: 0.7 for balanced creativity

3. **Database**
   - SQLAlchemy with application factory pattern
   - Automatic table creation on first run
   - Cascading deletes for user relationships

4. **Frontend State**
   - AuthContext for global user state
   - Protected routes check authentication
   - Auto-refresh user data on mount

## 🚀 Production Deployment

### Backend
1. Set `FLASK_ENV=production`
2. Use strong SECRET_KEY and JWT_SECRET_KEY
3. Switch to PostgreSQL/MySQL
4. Use production WSGI server (Gunicorn)
5. Enable HTTPS

### Frontend
1. Build production bundle: `npm run build`
2. Serve with Nginx or similar
3. Update API baseURL to production backend
4. Configure proper CORS origins

## 📄 License

MIT License - Feel free to use for learning and projects

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 💡 Future Enhancements

- [ ] Password reset functionality
- [ ] Email verification
- [ ] Social authentication (Google, GitHub)
- [ ] Code syntax highlighting
- [ ] Export roadmaps as PDF
- [ ] User progress tracking
- [ ] Community features
- [ ] Mobile app version

## 📞 Support

For issues and questions:
- Check troubleshooting section
- Review backend and frontend READMEs
- Open GitHub issue

## 🎉 Acknowledgments

- Groq for providing the AI API
- Flask and React communities
- Open source contributors

---

**Happy Coding! 🚀**
