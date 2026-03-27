import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/dashboard/stats');
      setStats(response.data.stats);
    } catch (err) {
      setError('Failed to load dashboard statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <LoadingSpinner message="Loading dashboard..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="dashboard">
        <header className="dashboard-header">
          <h1>Welcome back, {user?.full_name}! 👋</h1>
          <p className="dashboard-subtitle">Here's your learning progress</p>
        </header>

        {/* Statistics Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">🗺️</div>
            <div className="stat-content">
              <h3>{stats?.totals?.roadmaps || 0}</h3>
              <p>Learning Roadmaps</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">💬</div>
            <div className="stat-content">
              <h3>{stats?.totals?.chats || 0}</h3>
              <p>Chat Messages</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🔍</div>
            <div className="stat-content">
              <h3>{stats?.totals?.analyses || 0}</h3>
              <p>Code Analyses</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🔥</div>
            <div className="stat-content">
              <h3>{stats?.learning_streak || 0}</h3>
              <p>Day Streak</p>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        {stats?.recent_activity && (
          <div className="recent-activity">
            <h2>Recent Activity (Last 7 Days)</h2>
            <div className="activity-grid">
              <div className="activity-item">
                <span className="activity-label">Roadmaps Generated:</span>
                <span className="activity-value">
                  {stats.recent_activity.last_7_days.roadmaps}
                </span>
              </div>
              <div className="activity-item">
                <span className="activity-label">Chat Sessions:</span>
                <span className="activity-value">
                  {stats.recent_activity.last_7_days.chats}
                </span>
              </div>
              <div className="activity-item">
                <span className="activity-label">Code Analyses:</span>
                <span className="activity-value">
                  {stats.recent_activity.last_7_days.analyses}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="quick-actions">
          <h2>Quick Actions</h2>
          <div className="actions-grid">
            <Link to="/roadmap" className="action-card">
              <div className="action-icon">🗺️</div>
              <h3>Generate Roadmap</h3>
              <p>Create a personalized learning path</p>
            </Link>

            <Link to="/chat" className="action-card">
              <div className="action-icon">💬</div>
              <h3>Ask AI Assistant</h3>
              <p>Get instant coding help</p>
            </Link>

            <Link to="/analyzer" className="action-card">
              <div className="action-icon">🔍</div>
              <h3>Analyze Code</h3>
              <p>Get feedback on your code</p>
            </Link>
          </div>
        </div>

        {/* Latest Items */}
        {stats?.latest_items && (
          <div className="latest-items">
            {stats.latest_items.roadmap && (
              <div className="latest-card">
                <h3>Latest Roadmap</h3>
                <p className="latest-title">
                  {stats.latest_items.roadmap.language} - {stats.latest_items.roadmap.career_goal}
                </p>
                <p className="latest-date">
                  {new Date(stats.latest_items.roadmap.created_at).toLocaleDateString()}
                </p>
              </div>
            )}

            {stats.latest_items.code_submission && (
              <div className="latest-card">
                <h3>Latest Code Analysis</h3>
                <p className="latest-title">
                  {stats.latest_items.code_submission.language}
                </p>
                <p className="latest-date">
                  {new Date(stats.latest_items.code_submission.created_at).toLocaleDateString()}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
