# 📁 Project File Structure

Complete file tree of the AI Coding Mentor application.

```
coding-mentor/
│
├── 📄 README.md                          # Main project documentation
├── 📄 QUICKSTART.md                      # Quick start guide
├── 🔧 setup-backend.bat                  # Automated backend setup
├── 🔧 setup-frontend.bat                 # Automated frontend setup
├── 🔧 start-backend.bat                  # Start backend script
├── 🔧 start-frontend.bat                 # Start frontend script
│
├── 📂 backend/                           # Flask Backend
│   │
│   ├── 📄 app.py                         # Application factory & entry point
│   ├── 📄 config.py                      # Configuration class
│   ├── 📄 extensions.py                  # Extension instances (db, bcrypt, jwt)
│   ├── 📄 models.py                      # Database models (User, Roadmap, etc.)
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 .env.example                   # Environment variables template
│   ├── 📄 .gitignore                     # Git ignore rules
│   ├── 📄 README.md                      # Backend documentation
│   │
│   ├── 📂 routes/                        # API route blueprints
│   │   ├── 📄 __init__.py                # Package initializer
│   │   ├── 📄 auth.py                    # Authentication (signup, login, me)
│   │   ├── 📄 roadmap.py                 # Roadmap generation & retrieval
│   │   ├── 📄 chatbot.py                 # Chatbot (send, history, clear)
│   │   ├── 📄 code_analyzer.py           # Code analysis & history
│   │   └── 📄 dashboard.py               # User statistics & dashboard
│   │
│   ├── 📂 venv/                          # Virtual environment (created on setup)
│   │   └── ...
│   │
│   └── 🗄️ coding_mentor.db               # SQLite database (created on first run)
│
└── 📂 frontend/                          # React Frontend
    │
    ├── 📄 package.json                   # Node.js dependencies & scripts
    ├── 📄 .gitignore                     # Git ignore rules
    ├── 📄 README.md                      # Frontend documentation
    │
    ├── 📂 public/                        # Static public files
    │   └── 📄 index.html                 # HTML template
    │
    ├── 📂 src/                           # Source code
    │   │
    │   ├── 📄 index.js                   # Application entry point
    │   ├── 📄 index.css                  # Global base styles
    │   ├── 📄 App.js                     # Main app component with routing
    │   ├── 📄 App.css                    # Global application styles
    │   │
    │   ├── 📂 components/                # Reusable components
    │   │   ├── 📄 Navbar.jsx             # Navigation bar
    │   │   ├── 📄 Navbar.css
    │   │   ├── 📄 ProtectedRoute.jsx     # Authentication wrapper
    │   │   ├── 📄 LoadingSpinner.jsx     # Loading indicator
    │   │   └── 📄 LoadingSpinner.css
    │   │
    │   ├── 📂 pages/                     # Page components
    │   │   ├── 📄 Home.jsx               # Landing page
    │   │   ├── 📄 Home.css
    │   │   ├── 📄 Login.jsx              # Login form
    │   │   ├── 📄 Signup.jsx             # Registration form
    │   │   ├── 📄 Auth.css               # Auth pages styles
    │   │   ├── 📄 Dashboard.jsx          # User dashboard
    │   │   ├── 📄 Dashboard.css
    │   │   ├── 📄 Roadmap.jsx            # Roadmap generator
    │   │   ├── 📄 Roadmap.css
    │   │   ├── 📄 Chatbot.jsx            # Chat interface
    │   │   ├── 📄 Chatbot.css
    │   │   ├── 📄 CodeAnalyzer.jsx       # Code analysis tool
    │   │   └── 📄 CodeAnalyzer.css
    │   │
    │   ├── 📂 services/                  # API service layer
    │   │   ├── 📄 api.js                 # Axios configuration & interceptors
    │   │   └── 📄 auth.js                # Authentication service functions
    │   │
    │   └── 📂 context/                   # React context providers
    │       └── 📄 AuthContext.jsx        # Global authentication state
    │
    └── 📂 node_modules/                  # Node dependencies (created on npm install)
        └── ...
```

## 📊 File Count Summary

### Backend (Python/Flask)
- **Total Files**: 12 core files
- **Routes**: 5 blueprint files
- **Models**: 4 database models
- **Dependencies**: 9 packages

### Frontend (React)
- **Total Files**: 25 core files
- **Components**: 3 reusable components
- **Pages**: 7 page components
- **Services**: 2 API services
- **Context**: 1 global state provider

## 🎯 Key Files Explained

### Backend Critical Files

| File | Purpose |
|------|---------|
| `app.py` | Flask application factory, initializes app and database |
| `extensions.py` | Single source of truth for db, bcrypt, jwt instances |
| `models.py` | SQLAlchemy models: User, Roadmap, ChatMessage, CodeSubmission |
| `config.py` | Configuration from environment variables |
| `routes/auth.py` | JWT authentication with signup, login, get user |
| `routes/roadmap.py` | AI roadmap generation using Groq API |
| `routes/chatbot.py` | Context-aware chatbot with message history |
| `routes/code_analyzer.py` | AI code analysis with detailed feedback |
| `routes/dashboard.py` | User statistics and activity tracking |

### Frontend Critical Files

| File | Purpose |
|------|---------|
| `App.js` | Main component with routing setup |
| `index.js` | React DOM render entry point |
| `AuthContext.jsx` | Global user state management |
| `api.js` | Axios instance with JWT interceptors |
| `auth.js` | Authentication service functions |
| `ProtectedRoute.jsx` | Route wrapper requiring authentication |
| `Home.jsx` | Landing page with features |
| `Dashboard.jsx` | User statistics and overview |
| `Roadmap.jsx` | AI roadmap generator interface |
| `Chatbot.jsx` | Real-time chat interface |
| `CodeAnalyzer.jsx` | Code submission and analysis |

## 📦 Generated/Runtime Files

These files are created during setup or runtime:

```
backend/
├── venv/                    # Created by: python -m venv venv
├── .env                     # Created by: copy .env.example .env
├── coding_mentor.db         # Created by: first run of app.py
└── __pycache__/             # Created by: Python automatically

frontend/
├── node_modules/            # Created by: npm install
├── build/                   # Created by: npm run build
└── .env.local               # Optional: for local overrides
```

## 🔐 Sensitive Files (.gitignore)

Files that should NOT be committed:

```
backend/
├── venv/
├── .env
├── *.db
├── *.sqlite
└── __pycache__/

frontend/
├── node_modules/
├── build/
└── .env.local
```

## 📝 Documentation Files

| File | Contains |
|------|----------|
| `README.md` | Complete project overview & setup |
| `QUICKSTART.md` | Step-by-step quick start guide |
| `backend/README.md` | Backend-specific documentation |
| `frontend/README.md` | Frontend-specific documentation |
| `FILE_STRUCTURE.md` | This file - project structure |

## 🚀 Execution Flow

### Backend Startup
```
app.py
  ↓
create_app()
  ↓
Initialize extensions (db, bcrypt, jwt)
  ↓
Register blueprints (auth, roadmap, chatbot, analyzer, dashboard)
  ↓
Create database tables
  ↓
Run Flask server on port 5000
```

### Frontend Startup
```
index.js
  ↓
Render App component
  ↓
AuthProvider wraps app
  ↓
BrowserRouter sets up routing
  ↓
Navbar always visible
  ↓
Routes render based on URL
  ↓
Protected routes check authentication
```

## 🔄 Data Flow

### API Request Flow
```
Frontend Component
  ↓
API Service (api.js)
  ↓
Axios Request + JWT Token
  ↓
Backend Route
  ↓
Database Operation
  ↓
Groq AI (if needed)
  ↓
Response JSON
  ↓
Frontend Component State
  ↓
UI Update
```

## 📏 Code Statistics

### Backend
- **Lines of Code**: ~1,500
- **API Endpoints**: 15+
- **Database Models**: 4
- **AI Integrations**: 3 (roadmap, chat, analyzer)

### Frontend
- **Lines of Code**: ~2,500
- **Components**: 10
- **Routes**: 7
- **API Calls**: 15+

## 🎨 Styling Organization

### CSS Files by Category

**Global Styles:**
- `index.css` - Base/reset styles
- `App.css` - App-wide components & utilities

**Component Styles:**
- `Navbar.css` - Navigation bar
- `LoadingSpinner.css` - Loading indicator

**Page Styles:**
- `Home.css` - Landing page
- `Auth.css` - Login & Signup
- `Dashboard.css` - Dashboard
- `Roadmap.css` - Roadmap page
- `Chatbot.css` - Chat interface
- `CodeAnalyzer.css` - Code analyzer

## 🛠️ Configuration Files

### Backend Config
- `.env` - Environment variables (secrets, API keys)
- `config.py` - Configuration class loading from .env
- `requirements.txt` - Python package dependencies

### Frontend Config
- `package.json` - Node.js config, dependencies, scripts
- `public/index.html` - HTML template with meta tags

## ✅ Complete File Checklist

Use this to verify all files are present:

### Backend (12 files)
- [ ] app.py
- [ ] config.py
- [ ] extensions.py
- [ ] models.py
- [ ] requirements.txt
- [ ] .env.example
- [ ] .gitignore
- [ ] README.md
- [ ] routes/__init__.py
- [ ] routes/auth.py
- [ ] routes/roadmap.py
- [ ] routes/chatbot.py
- [ ] routes/code_analyzer.py
- [ ] routes/dashboard.py

### Frontend (25 files)
- [ ] package.json
- [ ] .gitignore
- [ ] README.md
- [ ] public/index.html
- [ ] src/index.js
- [ ] src/index.css
- [ ] src/App.js
- [ ] src/App.css
- [ ] src/components/Navbar.jsx
- [ ] src/components/Navbar.css
- [ ] src/components/ProtectedRoute.jsx
- [ ] src/components/LoadingSpinner.jsx
- [ ] src/components/LoadingSpinner.css
- [ ] src/pages/Home.jsx
- [ ] src/pages/Home.css
- [ ] src/pages/Login.jsx
- [ ] src/pages/Signup.jsx
- [ ] src/pages/Auth.css
- [ ] src/pages/Dashboard.jsx
- [ ] src/pages/Dashboard.css
- [ ] src/pages/Roadmap.jsx
- [ ] src/pages/Roadmap.css
- [ ] src/pages/Chatbot.jsx
- [ ] src/pages/Chatbot.css
- [ ] src/pages/CodeAnalyzer.jsx
- [ ] src/pages/CodeAnalyzer.css
- [ ] src/services/api.js
- [ ] src/services/auth.js
- [ ] src/context/AuthContext.jsx

### Root (5 files)
- [ ] README.md
- [ ] QUICKSTART.md
- [ ] setup-backend.bat
- [ ] setup-frontend.bat
- [ ] start-backend.bat
- [ ] start-frontend.bat
- [ ] FILE_STRUCTURE.md

**Total: 42 files** (excluding generated/runtime files)
