import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Onboarding.css';

const Onboarding = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    role: '',
    workflow: '',
    skill_level: '',
    pain_points: []
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [availableRoles, setAvailableRoles] = useState([]);

  const roles = [
    'Developer',
    'Designer', 
    'Marketer',
    'Writer',
    'Project Manager',
    'Student',
    'Researcher',
    'Business Analyst',
    'Content Creator',
    'Software Engineer',
    'Full Stack Developer',
    'Copywriter',
    'SEO Specialist',
    'Social Media Manager',
    'Small Business Owner',
    'Video Creator',
    'Filmmaker',
    'Journalist',
    'Analyst',
    'Professional'
  ];

  const workflows = [
    'Software Development',
    'Content Creation',
    'Marketing',
    'Design',
    'Research',
    'Project Management',
    'Data Analysis',
    'Writing',
    'Video Production',
    'Business Operations',
    'Learning',
    'Customer Support'
  ];

  const painPointOptions = [
    'Writer\'s block',
    'Slow coding',
    'Design complexity',
    'Time consumption',
    'Creative blocks',
    'Research time',
    'Information overload',
    'Grammar errors',
    'Setup complexity',
    'Learning curve',
    'Debugging time',
    'Content ideas',
    'Brand consistency',
    'Professional look',
    'SEO optimization',
    'High production costs',
    'Technical skills',
    'Environment issues',
    'Source reliability',
    'Fact verification'
  ];

  useEffect(() => {
    // Fetch available roles from API
    const fetchRoles = async () => {
      try {
        const response = await axios.get('http://localhost:5001/api/roles');
        setAvailableRoles(response.data);
      } catch (err) {
        console.error('Error fetching roles:', err);
        // Use fallback roles if API fails
        setAvailableRoles(roles);
      }
    };
    fetchRoles();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePainPointChange = (painPoint) => {
    setFormData(prev => ({
      ...prev,
      pain_points: prev.pain_points.includes(painPoint)
        ? prev.pain_points.filter(p => p !== painPoint)
        : [...prev.pain_points, painPoint]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation
    if (!formData.role || !formData.workflow || !formData.skill_level || formData.pain_points.length === 0) {
      setError('Please fill in all fields and select at least one pain point.');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('http://localhost:5001/api/recommend', formData);
      
      // Store results in sessionStorage for the results page
      sessionStorage.setItem('recommendations', JSON.stringify(response.data));
      sessionStorage.setItem('userInput', JSON.stringify(formData));
      
      navigate('/results');
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboarding">
      <div className="container">
        <div className="onboarding-card">
          <div className="onboarding-header">
            <h1>Find Your AI Tools</h1>
            <p>Tell us about yourself so we can recommend the perfect AI tools for your needs.</p>
          </div>

          {error && <div className="error">{error}</div>}

          <form onSubmit={handleSubmit} className="onboarding-form">
            <div className="form-group">
              <label className="form-label">What is your role? *</label>
              <select
                name="role"
                value={formData.role}
                onChange={handleInputChange}
                className="form-control"
                required
              >
                <option value="">Select your role</option>
                {(availableRoles.length > 0 ? availableRoles : roles).map(role => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">What is your primary workflow? *</label>
              <select
                name="workflow"
                value={formData.workflow}
                onChange={handleInputChange}
                className="form-control"
                required
              >
                <option value="">Select your workflow</option>
                {workflows.map(workflow => (
                  <option key={workflow} value={workflow}>{workflow}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">What is your skill level with AI tools? *</label>
              <select
                name="skill_level"
                value={formData.skill_level}
                onChange={handleInputChange}
                className="form-control"
                required
              >
                <option value="">Select your skill level</option>
                <option value="beginner">Beginner - Just starting with AI tools</option>
                <option value="intermediate">Intermediate - Comfortable with basic AI tools</option>
                <option value="advanced">Advanced - Experienced with AI tools</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">What challenges are you facing? * (Select all that apply)</label>
              <div className="checkbox-group">
                {painPointOptions.map(painPoint => (
                  <label key={painPoint} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={formData.pain_points.includes(painPoint)}
                      onChange={() => handlePainPointChange(painPoint)}
                    />
                    {painPoint}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Getting Recommendations...' : 'Get My Recommendations'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Onboarding;
