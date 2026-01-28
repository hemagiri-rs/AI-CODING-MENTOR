import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Master Programming with <span className="highlight">AI-Powered</span> Mentorship
          </h1>
          <p className="hero-subtitle">
            Get personalized learning roadmaps, instant coding help, and expert code analysis 
            powered by advanced AI technology.
          </p>
          <div className="hero-buttons">
            {isAuthenticated ? (
              <Link to="/dashboard" className="btn btn-primary">
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link to="/signup" className="btn btn-primary">
                  Start Learning Free
                </Link>
                <Link to="/login" className="btn btn-secondary">
                  Login
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2 className="section-title">Everything You Need to Excel</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🗺️</div>
            <h3>Personalized Roadmaps</h3>
            <p>
              Get custom learning paths tailored to your skill level and career goals. 
              Our AI creates structured plans with resources and projects.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <h3>AI Coding Assistant</h3>
            <p>
              Chat with an intelligent bot that understands your questions and provides 
              clear explanations, code examples, and debugging help.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Code Analysis</h3>
            <p>
              Submit your code for instant AI-powered review. Get detailed feedback on 
              bugs, performance, security, and best practices.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Progress Tracking</h3>
            <p>
              Monitor your learning journey with comprehensive statistics and insights 
              into your coding activity and improvements.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Career-Focused</h3>
            <p>
              Whether you're aiming for full-stack, data science, or mobile development, 
              get guidance aligned with your career aspirations.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Instant Feedback</h3>
            <p>
              No waiting for human mentors. Get immediate, detailed responses to your 
              coding questions and code submissions 24/7.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works">
        <h2 className="section-title">How It Works</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Sign Up</h3>
            <p>Create your free account and tell us about your coding background</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Get Your Roadmap</h3>
            <p>Receive a personalized learning path based on your goals</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Learn & Practice</h3>
            <p>Code, ask questions, and analyze your work with AI assistance</p>
          </div>
          <div className="step">
            <div className="step-number">4</div>
            <h3>Track Progress</h3>
            <p>Monitor your growth and adjust your learning path as needed</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <h2>Ready to Accelerate Your Coding Journey?</h2>
        <p>Join thousands of developers learning smarter with AI</p>
        {!isAuthenticated && (
          <Link to="/signup" className="btn btn-primary btn-large">
            Get Started Now - It's Free
          </Link>
        )}
      </section>
    </div>
  );
};

export default Home;
