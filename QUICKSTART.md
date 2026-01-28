# 🚀 Quick Start Guide - AI Coding Mentor

Get the full-stack AI Coding Mentor application running in minutes!

## Prerequisites Check ✓

Before starting, ensure you have:
- [ ] **Python 3.8+** installed (`python --version`)
- [ ] **Node.js 16+** and npm installed (`node --version`)
- [ ] **Groq API Key** from https://console.groq.com/keys

## 🎯 Installation Steps

### Option A: Automated Setup (Windows)

1. **Setup Backend**
   ```bash
   setup-backend.bat
   ```
   This will:
   - Create virtual environment
   - Install Python dependencies
   - Create .env file

2. **Add Your Groq API Key**
   - Open `backend/.env` in a text editor
   - Replace `gsk_your_groq_api_key_here` with your actual key
   - Save the file

3. **Setup Frontend**
   ```bash
   setup-frontend.bat
   ```
   This will:
   - Install Node.js dependencies

4. **Start the Application**
   
   Open TWO terminals:
   
   **Terminal 1 - Backend:**
   ```bash
   start-backend.bat
   ```
   
   **Terminal 2 - Frontend:**
   ```bash
   start-frontend.bat
   ```

### Option B: Manual Setup

#### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
copy .env.example .env

# 6. Edit .env and add your GROQ_API_KEY

# 7. Start backend
python app.py
```

#### Frontend Setup

```bash
# 1. Open NEW terminal and navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start frontend
npm start
```

## 🌐 Access the Application

Once both servers are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 🎮 First Steps

### 1. Create an Account
- Go to http://localhost:3000/signup
- Fill in:
  - Full Name
  - Email
  - Password (min 6 characters)
  - Skill Level (Beginner/Intermediate/Advanced)
  - Primary Language (Python/JavaScript/etc.)
- Click "Sign Up"

### 2. Explore the Dashboard
You'll be automatically redirected to your dashboard showing:
- Profile information
- Learning statistics
- Quick action buttons

### 3. Try Key Features

**Generate a Roadmap:**
1. Click "Roadmap" in navigation
2. Select: Python, Beginner, "Web Developer"
3. Click "Generate Roadmap"
4. View your personalized learning path!

**Chat with AI:**
1. Click "Chat" in navigation
2. Ask: "How do I create a function in Python?"
3. Get instant AI response!

**Analyze Code:**
1. Click "Analyzer" in navigation
2. Paste some Python code
3. Select "Python" as language
4. Click "Analyze Code"
5. Get detailed feedback!

## ✅ Verification

### Backend is Working:
```bash
# Visit in browser or use curl
http://localhost:5000/api/health

# Should return:
{
  "status": "healthy",
  "message": "AI Coding Mentor API is running"
}
```

### Frontend is Working:
- Open http://localhost:3000
- Should see the landing page with "Master Programming with AI-Powered Mentorship"

### Database Created:
- Check for `backend/coding_mentor.db` file
- Created automatically on first run

## 🐛 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'groq'"
**Solution:**
```bash
cd backend
venv\Scripts\activate
pip install groq==0.9.0
```

### Issue: "Cannot GET /api/health"
**Solution:**
- Ensure backend is running
- Check terminal for errors
- Verify you're in the backend directory when running `python app.py`

### Issue: Frontend shows blank page
**Solution:**
- Open browser console (F12) to see errors
- Ensure dependencies installed: `npm install`
- Try deleting node_modules and reinstalling

### Issue: CORS errors in browser console
**Solution:**
- Verify backend .env has `CORS_ORIGINS=http://localhost:3000`
- Restart backend after changing .env

### Issue: "JWT token errors"
**Solution:**
- Clear browser localStorage (F12 → Application → Local Storage → Clear)
- Try logging in again

## 📊 Test Data

Use these for quick testing:

**Test User:**
- Email: test@example.com
- Password: test123
- Skill Level: Beginner
- Language: Python

**Test Roadmap:**
- Language: Python
- Skill Level: Beginner
- Career Goal: Full Stack Developer

**Test Code (Python):**
```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)
```

## 🎯 What to Expect

### Roadmap Generation (15-30 seconds)
- AI creates structured learning path
- Includes phases, topics, resources, projects
- Saved to your account

### Chatbot Response (3-10 seconds)
- Context-aware answers
- Code examples when relevant
- Conversational and helpful

### Code Analysis (10-20 seconds)
- Quality score (1-10)
- Identifies issues
- Provides suggestions
- Best practices

## 🔄 Stopping the Application

### Stop Backend:
- Press `Ctrl + C` in backend terminal

### Stop Frontend:
- Press `Ctrl + C` in frontend terminal

## 🚀 Next Steps

1. **Explore all features** - Try every page
2. **Generate multiple roadmaps** - Different languages and goals
3. **Have conversations** - Ask coding questions in chat
4. **Analyze various code** - Test with different languages
5. **Check your dashboard** - Track your progress

## 📚 Documentation

- **Main README**: `/README.md`
- **Backend README**: `/backend/README.md`
- **Frontend README**: `/frontend/README.md`

## 💡 Tips

1. **Keep both servers running** while using the app
2. **Check browser console** (F12) if something doesn't work
3. **Check terminal output** for backend errors
4. **Clear localStorage** if you encounter auth issues
5. **Restart servers** after making configuration changes

## 🎉 You're Ready!

Your AI Coding Mentor application is now running. Start learning with personalized AI assistance!

### Quick Commands Reference

```bash
# Backend
cd backend
venv\Scripts\activate
python app.py

# Frontend (new terminal)
cd frontend
npm start
```

**Happy Learning! 🚀**
