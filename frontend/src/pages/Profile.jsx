import React from 'react';
import { useAuth } from '../context/AuthContext';
import './Profile.css';

const Profile = () => {
  const { user } = useAuth();

  return (
    <div className="page-container">
      <div className="profile-page">
        <header className="profile-header">
          <h1>Profile Information</h1>
          <p className="profile-subtitle">Manage and view your account details</p>
        </header>

        <div className="profile-card">
          <div className="profile-grid">
            <div className="profile-item">
              <span className="profile-label">Full Name:</span>
              <span className="profile-value">{user?.full_name || '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Email:</span>
              <span className="profile-value">{user?.email || '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Skill Level:</span>
              <span className="profile-value">{user?.skill_level || '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Primary Language:</span>
              <span className="profile-value">{user?.primary_language || '-'}</span>
            </div>
            <div className="profile-item">
              <span className="profile-label">Member Since:</span>
              <span className="profile-value">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : '-'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
