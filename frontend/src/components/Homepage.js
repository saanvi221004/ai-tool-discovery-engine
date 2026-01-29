import React from 'react';
import { Link } from 'react-router-dom';

const Homepage = () => {
  return (
    <div className="homepage">
      <div className="container">
        <div className="hero">
          <h1 className="hero-title">Find Your Perfect AI Tools</h1>
          <p className="hero-subtitle">
            Get personalized AI tool recommendations based on your role, workflow, and specific needs. 
            No more guessing - just the right tools for your success.
          </p>
          <div className="hero-actions">
            <Link to="/onboarding" className="btn btn-primary btn-large">
              Discover AI Tools
            </Link>
          </div>
        </div>

        <div className="features">
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Personalized Recommendations</h3>
              <p>AI tools matched to your specific role, skill level, and pain points</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Fast & Free</h3>
              <p>Get instant recommendations without any cost or registration</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>Safe & Reliable</h3>
              <p>We only recommend tools and link to official websites</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Smart Matching</h3>
              <p>Our algorithm considers multiple factors for perfect tool matching</p>
            </div>
          </div>
        </div>

        <div className="how-it-works">
          <h2>How It Works</h2>
          <div className="steps">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Tell Us About Yourself</h3>
              <p>Share your role, workflow, skill level, and challenges</p>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>AI Analysis</h3>
              <p>Our smart algorithm analyzes your needs against our tool database</p>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Get Recommendations</h3>
              <p>Receive personalized tool suggestions with explanations</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Homepage;
