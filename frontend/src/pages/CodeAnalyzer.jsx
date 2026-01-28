import React, { useState, useEffect } from 'react';
import api from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import './CodeAnalyzer.css';

const CodeAnalyzer = () => {
  const [formData, setFormData] = useState({
    code: '',
    language: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await api.get('/analyzer/history');
      setHistory(response.data.submissions);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    } finally {
      setLoadingHistory(false);
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

    if (!formData.code.trim() || !formData.language) {
      setError('Please provide both code and language');
      return;
    }

    setLoading(true);

    try {
      const response = await api.post('/analyzer/analyze', formData);
      setAnalysis(response.data);
      fetchHistory(); // Refresh history
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to analyze code');
    } finally {
      setLoading(false);
    }
  };

  const loadSubmission = (submission) => {
    setFormData({
      code: submission.code,
      language: submission.language
    });
    setAnalysis({ analysis: submission.analysis });
  };

  const renderAnalysis = (analysisData) => {
    return (
      <div className="analysis-result">
        <div className="analysis-header">
          <h2>Analysis Results</h2>
          <div className="quality-badge">
            Quality Score: {analysisData.overall_quality}/10
          </div>
        </div>

        <div className="analysis-summary">
          <h3>Summary</h3>
          <p>{analysisData.summary}</p>
        </div>

        {analysisData.strengths && analysisData.strengths.length > 0 && (
          <div className="analysis-section strengths">
            <h3>✅ Strengths</h3>
            <ul>
              {analysisData.strengths.map((strength, index) => (
                <li key={index}>{strength}</li>
              ))}
            </ul>
          </div>
        )}

        {analysisData.issues && analysisData.issues.length > 0 && (
          <div className="analysis-section issues">
            <h3>⚠️ Issues Found</h3>
            {analysisData.issues.map((issue, index) => (
              <div key={index} className={`issue-card ${issue.severity}`}>
                <div className="issue-header">
                  <span className="issue-severity">{issue.severity}</span>
                  <span className="issue-type">{issue.type}</span>
                </div>
                <p className="issue-description">{issue.description}</p>
                {issue.line !== 'N/A' && (
                  <p className="issue-line">Line: {issue.line}</p>
                )}
                <p className="issue-suggestion">
                  <strong>Suggestion:</strong> {issue.suggestion}
                </p>
              </div>
            ))}
          </div>
        )}

        {analysisData.improvements && analysisData.improvements.length > 0 && (
          <div className="analysis-section improvements">
            <h3>💡 Improvements</h3>
            {analysisData.improvements.map((improvement, index) => (
              <div key={index} className="improvement-card">
                <h4>{improvement.category}</h4>
                <p>{improvement.suggestion}</p>
                {improvement.example && (
                  <pre className="code-example">{improvement.example}</pre>
                )}
              </div>
            ))}
          </div>
        )}

        {analysisData.best_practices && analysisData.best_practices.length > 0 && (
          <div className="analysis-section best-practices">
            <h3>📚 Best Practices</h3>
            <ul>
              {analysisData.best_practices.map((practice, index) => (
                <li key={index}>{practice}</li>
              ))}
            </ul>
          </div>
        )}

        {analysisData.learning_resources && analysisData.learning_resources.length > 0 && (
          <div className="analysis-section resources">
            <h3>📖 Learning Resources</h3>
            {analysisData.learning_resources.map((resource, index) => (
              <div key={index} className="resource-item">
                <strong>{resource.topic}:</strong> {resource.resource}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="page-container">
      <div className="analyzer-page">
        <h1>Code Analyzer</h1>
        <p className="page-subtitle">
          Get instant AI-powered feedback on your code
        </p>

        <div className="analyzer-container">
          {/* Input Section */}
          <div className="analyzer-input">
            <h2>Submit Your Code</h2>
            
            {error && <div className="error-message">{error}</div>}

            <form onSubmit={handleSubmit} className="analyzer-form">
              <div className="form-group">
                <label htmlFor="language">Programming Language</label>
                <select
                  id="language"
                  name="language"
                  value={formData.language}
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
                  <option value="SQL">SQL</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="code">Your Code</label>
                <textarea
                  id="code"
                  name="code"
                  value={formData.code}
                  onChange={handleChange}
                  placeholder="Paste your code here..."
                  rows="15"
                  disabled={loading}
                  required
                />
              </div>

              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Analyzing...' : 'Analyze Code'}
              </button>
            </form>

            {loading && (
              <div className="loading-section">
                <LoadingSpinner message="Analyzing your code..." />
              </div>
            )}
          </div>

          {/* Results Section */}
          {analysis && (
            <div className="analyzer-results">
              {renderAnalysis(analysis.analysis)}
            </div>
          )}
        </div>

        {/* History Section */}
        <div className="history-section">
          <h2>Analysis History</h2>
          {loadingHistory ? (
            <LoadingSpinner message="Loading history..." />
          ) : history.length === 0 ? (
            <p className="no-data">No previous analyses. Submit your first code above!</p>
          ) : (
            <div className="history-list">
              {history.map((submission) => (
                <div key={submission.id} className="history-card">
                  <div className="history-header">
                    <h3>{submission.language}</h3>
                    <span className="history-date">
                      {new Date(submission.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <pre className="history-code-preview">
                    {submission.code.substring(0, 100)}
                    {submission.code.length > 100 ? '...' : ''}
                  </pre>
                  <button 
                    className="btn btn-secondary btn-small"
                    onClick={() => loadSubmission(submission)}
                  >
                    View Analysis
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

export default CodeAnalyzer;
