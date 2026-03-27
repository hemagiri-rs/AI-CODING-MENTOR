import React, { useState, useEffect } from 'react';
import api from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import './Roadmap.css';

const Roadmap = () => {
  const [formData, setFormData] = useState({
    programming_language: '',
    skill_level: '',
    career_goal: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [currentRoadmap, setCurrentRoadmap] = useState(null);
  const [myRoadmaps, setMyRoadmaps] = useState([]);
  const [loadingRoadmaps, setLoadingRoadmaps] = useState(true);

  useEffect(() => {
    fetchMyRoadmaps();
  }, []);

  const fetchMyRoadmaps = async () => {
    try {
      const response = await api.get('/roadmap/my-roadmaps');
      setMyRoadmaps(response.data.roadmaps);
    } catch (err) {
      console.error('Failed to fetch roadmaps:', err);
    } finally {
      setLoadingRoadmaps(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.programming_language || !formData.skill_level || !formData.career_goal) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);

    try {
      const response = await api.post('/roadmap/generate', formData);
      setCurrentRoadmap(response.data.roadmap);
      // Refresh the list
      fetchMyRoadmaps();
      // Reset form
      setFormData({
        programming_language: '',
        skill_level: '',
        career_goal: ''
      });
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to generate roadmap');
    } finally {
      setLoading(false);
    }
  };

  const renderRoadmapData = (roadmap) => {
    const data = typeof roadmap.data === 'string' ? JSON.parse(roadmap.data) : roadmap.data;

    return (
      <div className="roadmap-display">
        <h2>{data.title}</h2>
        <p className="roadmap-description">{data.description}</p>
        <p className="roadmap-duration">
          <strong>Estimated Duration:</strong> {data.estimated_duration}
        </p>

        {data.phases && data.phases.length > 0 && (
          <div className="phases-section">
            <h3>Learning Phases</h3>
            {data.phases.map((phase, index) => (
              <div key={index} className="phase-card">
                <h4>
                  Phase {phase.phase_number}: {phase.phase_name}
                </h4>
                <p className="phase-duration">Duration: {phase.duration}</p>
                
                {phase.topics && phase.topics.length > 0 && (
                  <div className="topics-list">
                    {phase.topics.map((topic, topicIndex) => (
                      <div key={topicIndex} className="topic-item">
                        <h5>{topic.topic}</h5>
                        <p>{topic.description}</p>
                        
                        {topic.resources && topic.resources.length > 0 && (
                          <div className="topic-resources">
                            <strong>Resources:</strong>
                            <ul>
                              {topic.resources.map((resource, rIndex) => (
                                <li key={rIndex}>{resource}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        
                        {topic.projects && topic.projects.length > 0 && (
                          <div className="topic-projects">
                            <strong>Projects:</strong>
                            <ul>
                              {topic.projects.map((project, pIndex) => (
                                <li key={pIndex}>{project}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {data.milestones && data.milestones.length > 0 && (
          <div className="milestones-section">
            <h3>Key Milestones</h3>
            <ul>
              {data.milestones.map((milestone, index) => (
                <li key={index}>
                  <strong>{milestone.milestone}:</strong> {milestone.description}
                </li>
              ))}
            </ul>
          </div>
        )}

        {data.career_tips && data.career_tips.length > 0 && (
          <div className="tips-section">
            <h3>Career Tips</h3>
            <ul>
              {data.career_tips.map((tip, index) => (
                <li key={index}>{tip}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="page-container">
      <div className="roadmap-page">
        <h1>Learning Roadmap Generator</h1>
        <p className="page-subtitle">
          Get a personalized learning path tailored to your goals
        </p>

        {/* Generate Form */}
        <div className="roadmap-form-card">
          <h2>Generate New Roadmap</h2>
          
          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit} className="roadmap-form">
            <div className="form-group">
              <label htmlFor="programming_language">Programming Language</label>
              <select
                id="programming_language"
                name="programming_language"
                value={formData.programming_language}
                onChange={handleChange}
                disabled={loading}
                required
              >
                <option value="">Select a language</option>
                <option value="Python">Python</option>
                <option value="JavaScript">JavaScript</option>
                <option value="Java">Java</option>
                <option value="C++">C++</option>
                <option value="C#">C#</option>
                <option value="Ruby">Ruby</option>
                <option value="Go">Go</option>
                <option value="PHP">PHP</option>
                <option value="Swift">Swift</option>
                <option value="Kotlin">Kotlin</option>
                <option value="TypeScript">TypeScript</option>
                <option value="Rust">Rust</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="skill_level">Skill Level</label>
              <select
                id="skill_level"
                name="skill_level"
                value={formData.skill_level}
                onChange={handleChange}
                disabled={loading}
                required
              >
                <option value="">Select your level</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="career_goal">Career Goal</label>
              <input
                type="text"
                id="career_goal"
                name="career_goal"
                value={formData.career_goal}
                onChange={handleChange}
                placeholder="e.g., Full Stack Developer, Data Scientist, Mobile Developer"
                disabled={loading}
                required
              />
            </div>

            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate Roadmap'}
            </button>
          </form>

          {loading && (
            <div className="loading-section">
              <LoadingSpinner message="Generating your personalized roadmap..." />
            </div>
          )}
        </div>

        {/* Current Roadmap Display */}
        {currentRoadmap && (
          <div className="current-roadmap">
            <h2>Your New Roadmap</h2>
            {renderRoadmapData(currentRoadmap)}
          </div>
        )}

        {/* My Roadmaps List */}
        <div className="my-roadmaps-section">
          <h2>My Roadmaps</h2>
          {loadingRoadmaps ? (
            <LoadingSpinner message="Loading roadmaps..." />
          ) : myRoadmaps.length === 0 ? (
            <p className="no-data">No roadmaps yet. Generate your first one above!</p>
          ) : (
            <div className="roadmaps-list">
              {myRoadmaps.map((roadmap) => (
                <div key={roadmap.id} className="roadmap-card">
                  <h3>{roadmap.language} - {roadmap.career_goal}</h3>
                  <p className="roadmap-meta">
                    <span>Skill Level: {roadmap.skill_level}</span>
                    <span>Created: {new Date(roadmap.created_at).toLocaleDateString()}</span>
                  </p>
                  <button 
                    className="btn btn-secondary"
                    onClick={() => setCurrentRoadmap(roadmap)}
                  >
                    View Details
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Roadmap;
