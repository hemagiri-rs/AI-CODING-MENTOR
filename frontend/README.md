# AI Coding Mentor - Frontend

React-based frontend for the AI Coding Mentor application.

## Features

- 🔐 JWT Authentication (Login/Signup)
- 🗺️ AI-Powered Roadmap Generation
- 💬 Intelligent Chatbot Assistant
- 🔍 Code Analysis Tool
- 📊 Personal Dashboard with Statistics
- 📱 Responsive Design

## Tech Stack

- **React** 18.2.0
- **React Router** 6.21.0
- **Axios** for API calls
- **Context API** for state management
- **CSS3** for styling

## Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

## Project Structure

```
src/
├── components/
│   ├── Navbar.jsx           - Navigation bar
│   ├── ProtectedRoute.jsx   - Route authentication wrapper
│   └── LoadingSpinner.jsx   - Loading indicator
├── pages/
│   ├── Home.jsx             - Landing page
│   ├── Login.jsx            - Login form
│   ├── Signup.jsx           - Registration form
│   ├── Dashboard.jsx        - User statistics
│   ├── Roadmap.jsx          - Learning roadmap generator
│   ├── Chatbot.jsx          - AI chat interface
│   └── CodeAnalyzer.jsx     - Code analysis tool
├── services/
│   ├── api.js               - Axios configuration
│   └── auth.js              - Authentication service
├── context/
│   └── AuthContext.jsx      - Global auth state
├── App.js                   - Main app component
├── App.css                  - Global styles
└── index.js                 - Entry point
```

## Available Scripts

### `npm start`
Runs the app in development mode at [http://localhost:3000](http://localhost:3000)

### `npm build`
Builds the app for production to the `build` folder

### `npm test`
Launches the test runner

## API Configuration

The frontend connects to the Flask backend API at:
- **Base URL**: `http://localhost:5000/api`

Configure in `src/services/api.js` if needed.

## Authentication Flow

1. User logs in or signs up
2. JWT token stored in localStorage
3. Token automatically added to all API requests
4. Protected routes check for valid token
5. Logout clears token and redirects to home

## Features Overview

### 🏠 Home Page
- Hero section with call-to-action
- Features showcase
- How it works explanation

### 🔐 Authentication
- Login with email/password
- Signup with profile information
- Persistent session with JWT

### 📊 Dashboard
- User profile information
- Statistics (roadmaps, chats, analyses)
- Recent activity tracking
- Learning streak counter
- Quick action buttons

### 🗺️ Roadmap Generator
- Select language, skill level, career goal
- AI generates personalized learning path
- View phases, topics, resources, projects
- Save and access previous roadmaps

### 💬 AI Chatbot
- Real-time chat interface
- Context-aware responses
- Code explanations and debugging help
- Message history
- Clear conversation option

### 🔍 Code Analyzer
- Submit code with language selection
- AI-powered analysis
- Issues detection (critical, major, minor)
- Improvement suggestions
- Best practices recommendations
- Learning resources
- Analysis history

## Styling

- Clean, modern design
- Purple gradient theme (#667eea to #764ba2)
- Fully responsive (mobile-friendly)
- Smooth transitions and hover effects
- Card-based layouts

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Environment Variables

No environment variables needed for development. Backend URL is configured in `src/services/api.js`.

## Production Build

```bash
npm run build
```

Creates optimized production build in `build/` folder.

## Troubleshooting

### CORS Issues
Ensure Flask backend has CORS configured for `http://localhost:3000`

### API Connection
Verify Flask backend is running on `http://localhost:5000`

### Token Expiration
JWT tokens expire after 7 days. Re-login if expired.

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License
