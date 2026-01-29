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
            <p><strong>Skill Level:</strong> {userInput.skill_level.charAt(0).toUpperCase() + userInput.skill_level.slice(1)}</p>
            <p><strong>Challenges:</strong> {userInput.pain_points?.join(', ')}</p>
          </div>
        </div>

        {recommendations.length === 0 ? (
          <div className="no-results">
            <div className="no-results-icon">🔍</div>
            <h2>We couldn't find a perfect match</h2>
            <p>But here are some popular AI tools you might find helpful for your journey.</p>
            <div className="popular-tools">
              <div className="popular-tool">
                <h4>ChatGPT</h4>
                <p>Versatile AI assistant for writing, coding, and problem-solving</p>
              </div>
              <div className="popular-tool">
                <h4>Notion AI</h4>
                <p>AI-powered workspace for organization and productivity</p>
              </div>
              <div className="popular-tool">
                <h4>Canva Magic Design</h4>
                <p>AI design tool for creating professional graphics easily</p>
              </div>
            </div>
            <button onClick={handleStartOver} className="btn btn-primary">
              Try Different Criteria
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
                      <span className="skill-badge">{tool.skill_level.charAt(0).toUpperCase() + tool.skill_level.slice(1)}</span>
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
                    <strong>Why this tool for you:</strong>
                    <div className="explanation-details">
                      {tool.explanation}
                    </div>
                  </div>

                  <div className="match-breakdown">
                    <h4>Match Breakdown</h4>
                    <div className="breakdown-item">
                      <span className="breakdown-label">Workflow match:</span>
                      <span className={`breakdown-value ${tool.scoring_breakdown.workflow_match.points > 0 ? 'yes' : 'no'}`}>
                        {tool.scoring_breakdown.workflow_match.points > 0 ? 'Yes' : 'No'}
                      </span>
                    </div>
                    <div className="breakdown-item">
                      <span className="breakdown-label">Challenges matched:</span>
                      <span className="breakdown-value">
                        {tool.scoring_breakdown.challenge_match.matched_challenges} / {tool.scoring_breakdown.challenge_match.total_challenges}
                      </span>
                    </div>
                    <div className="breakdown-item">
                      <span className="breakdown-label">Skill level compatibility:</span>
                      <span className={`breakdown-value ${tool.scoring_breakdown.skill_compatibility.points > 0 ? 'yes' : 'no'}`}>
                        {tool.scoring_breakdown.skill_compatibility.points > 0 ? 'Yes' : 'No'}
                      </span>
                    </div>
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
