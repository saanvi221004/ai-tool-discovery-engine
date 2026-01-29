import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Results.css';

const Results = () => {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState([]);
  const [userInput, setUserInput] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedRecommendations = sessionStorage.getItem('recommendations');
    const storedUserInput = sessionStorage.getItem('userInput');

    if (!storedRecommendations) {
      navigate('/onboarding');
      return;
    }

    try {
      setRecommendations(JSON.parse(storedRecommendations));
      setUserInput(JSON.parse(storedUserInput));
    } catch (error) {
      console.error('Error parsing stored data:', error);
      navigate('/onboarding');
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  const handleStartOver = () => {
    sessionStorage.removeItem('recommendations');
    sessionStorage.removeItem('userInput');
    navigate('/onboarding');
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745';
    if (score >= 60) return '#ffc107';
    return '#dc3545';
  };

  const handleToolClick = (url) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  if (loading) {
    return (
      <div className="results loading">
        <div className="container">
          <div className="spinner"></div>
          <h2>Loading your recommendations...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="results">
      <div className="container">
        <div className="results-header">
          <h1>Your AI Tool Recommendations</h1>
          <div className="user-summary">
            <p><strong>Role:</strong> {userInput.role}</p>
            <p><strong>Workflow:</strong> {userInput.workflow}</p>
            <p><strong>Skill Level:</strong> {userInput.skill_level}</p>
            <p><strong>Challenges:</strong> {userInput.pain_points?.join(', ')}</p>
          </div>
        </div>

        {recommendations.length === 0 ? (
          <div className="no-results">
            <h2>No recommendations found</h2>
            <p>We couldn't find tools that match your specific criteria. Try adjusting your responses.</p>
            <button onClick={handleStartOver} className="btn btn-primary">
              Start Over
            </button>
          </div>
        ) : (
          <>
            <div className="results-summary">
              <p>We found <strong>{recommendations.length}</strong> AI tools that match your needs!</p>
            </div>

            <div className="recommendations-list">
              {recommendations.map((tool, index) => (
                <div key={tool.id} className="tool-card">
                  <div className="tool-header">
                    <div>
                      <h2 className="tool-name">{tool.name}</h2>
                      <span className="tool-category">{tool.category}</span>
                    </div>
                    <div className="tool-score" style={{ backgroundColor: getScoreColor(tool.score) }}>
                      {Math.round(tool.score)}% Match
                    </div>
                  </div>

                  <p className="tool-description">{tool.description}</p>

                  <div className="tool-details">
                    <div className="detail-section">
                      <h4>Best For:</h4>
                      <div className="tag-list">
                        {tool.target_roles.slice(0, 3).map((role, i) => (
                          <span key={i} className="tag">{role}</span>
                        ))}
                      </div>
                    </div>

                    <div className="detail-section">
                      <h4>Skill Level:</h4>
                      <span className="skill-badge">{tool.skill_level}</span>
                    </div>

                    <div className="detail-section">
                      <h4>Pricing:</h4>
                      <span className="pricing-badge">{tool.pricing_model}</span>
                    </div>

                    <div className="detail-section">
                      <h4>Key Features:</h4>
                      <div className="feature-list">
                        {tool.features.slice(0, 4).map((feature, i) => (
                          <span key={i} className="feature-tag">{feature}</span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="explanation">
                    <strong>Why we recommend this:</strong> {tool.explanation}
                  </div>

                  <div className="tool-actions">
                    <button 
                      onClick={() => handleToolClick(tool.official_url)}
                      className="btn btn-primary"
                    >
                      Visit Official Website
                    </button>
                    <div className="tool-meta">
                      <span className="rating">⭐ {tool.rating}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="results-actions">
              <button onClick={handleStartOver} className="btn btn-secondary">
                Start New Search
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Results;
