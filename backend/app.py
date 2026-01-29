from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_tools.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class AITool(db.Model):
    __tablename__ = 'ai_tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    target_roles = db.Column(db.String(200), nullable=False)  # JSON array
    skill_level = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    use_cases = db.Column(db.Text, nullable=False)  # JSON array
    pain_points = db.Column(db.Text, nullable=False)  # JSON array
    pricing_model = db.Column(db.String(50), nullable=False)
    official_url = db.Column(db.String(200), nullable=False)
    features = db.Column(db.Text, nullable=False)  # JSON array
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    workflow = db.Column(db.String(100), nullable=False)
    skill_level = db.Column(db.String(20), nullable=False)
    pain_points = db.Column(db.Text, nullable=False)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Recommendation Engine
class RecommendationEngine:
    @staticmethod
    def calculate_score(tool, user_response):
        score = 0
        
        # Role matching (30% weight)
        user_roles = [user_response['role'].lower()]
        tool_roles = [role.lower() for role in json.loads(tool.target_roles)]
        role_match = any(role in user_roles for role in tool_roles)
        if role_match:
            score += 30
        
        # Skill level matching (20% weight)
        if tool.skill_level == user_response['skill_level'] or tool.skill_level == 'all':
            score += 20
        elif tool.skill_level == 'beginner' and user_response['skill_level'] == 'intermediate':
            score += 10
        elif tool.skill_level == 'intermediate' and user_response['skill_level'] == 'advanced':
            score += 10
        
        # Pain point matching (30% weight)
        user_pain_points = [point.lower() for point in user_response['pain_points']]
        tool_pain_points = [point.lower() for point in json.loads(tool.pain_points)]
        pain_point_matches = len(set(user_pain_points) & set(tool_pain_points))
        if user_pain_points:
            score += (pain_point_matches / len(user_pain_points)) * 30
        
        # Workflow matching (20% weight)
        user_workflow = user_response['workflow'].lower()
        tool_use_cases = [use_case.lower() for use_case in json.loads(tool.use_cases)]
        workflow_match = any(user_workflow in use_case or use_case in user_workflow for use_case in tool_use_cases)
        if workflow_match:
            score += 20
        
        return min(score, 100)  # Cap at 100
    
    @staticmethod
    def get_recommendations(user_response, limit=10):
        tools = AITool.query.all()
        recommendations = []
        
        for tool in tools:
            score = RecommendationEngine.calculate_score(tool, user_response)
            if score > 20:  # Only include tools with meaningful relevance
                recommendations.append({
                    'tool': tool,
                    'score': score,
                    'explanation': RecommendationEngine.generate_explanation(tool, user_response, score)
                })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    @staticmethod
    def generate_explanation(tool, user_response, score):
        explanations = []
        
        # Role-based explanation
        user_roles = [user_response['role'].lower()]
        tool_roles = [role.lower() for role in json.loads(tool.target_roles)]
        if any(role in user_roles for role in tool_roles):
            explanations.append(f"Specifically designed for {user_response['role']}s")
        
        # Skill level explanation
        if tool.skill_level == user_response['skill_level']:
            explanations.append(f"Matches your {user_response['skill_level']} skill level")
        
        # Pain point explanation
        user_pain_points = [point.lower() for point in user_response['pain_points']]
        tool_pain_points = [point.lower() for point in json.loads(tool.pain_points)]
        matched_pain_points = set(user_pain_points) & set(tool_pain_points)
        if matched_pain_points:
            explanations.append(f"Addresses your pain points: {', '.join(matched_pain_points)}")
        
        # Workflow explanation
        user_workflow = user_response['workflow'].lower()
        tool_use_cases = [use_case.lower() for use_case in json.loads(tool.use_cases)]
        if any(user_workflow in use_case or use_case in user_workflow for use_case in tool_use_cases):
            explanations.append(f"Fits your {user_response['workflow']} workflow")
        
        return "; ".join(explanations) if explanations else "Recommended based on your profile"

# Routes
@app.route('/api/tools', methods=['GET'])
def get_tools():
    tools = AITool.query.all()
    return jsonify([{
        'id': tool.id,
        'name': tool.name,
        'description': tool.description,
        'category': tool.category,
        'target_roles': json.loads(tool.target_roles),
        'skill_level': tool.skill_level,
        'use_cases': json.loads(tool.use_cases),
        'pain_points': json.loads(tool.pain_points),
        'pricing_model': tool.pricing_model,
        'official_url': tool.official_url,
        'features': json.loads(tool.features),
        'rating': tool.rating
    } for tool in tools])

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['role', 'workflow', 'skill_level', 'pain_points']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Save user response
    user_response = UserResponse(
        role=data['role'],
        workflow=data['workflow'],
        skill_level=data['skill_level'],
        pain_points=json.dumps(data['pain_points'])
    )
    db.session.add(user_response)
    db.session.commit()
    
    # Get recommendations
    recommendations = RecommendationEngine.get_recommendations(data)
    
    return jsonify([{
        'id': rec['tool'].id,
        'name': rec['tool'].name,
        'description': rec['tool'].description,
        'category': rec['tool'].category,
        'target_roles': json.loads(rec['tool'].target_roles),
        'skill_level': rec['tool'].skill_level,
        'use_cases': json.loads(rec['tool'].use_cases),
        'pain_points': json.loads(rec['tool'].pain_points),
        'pricing_model': rec['tool'].pricing_model,
        'official_url': rec['tool'].official_url,
        'features': json.loads(rec['tool'].features),
        'rating': rec['tool'].rating,
        'score': rec['score'],
        'explanation': rec['explanation']
    } for rec in recommendations])

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(AITool.category).distinct().all()
    return jsonify([cat[0] for cat in categories])

@app.route('/api/roles', methods=['GET'])
def get_roles():
    tools = AITool.query.all()
    all_roles = set()
    for tool in tools:
        roles = json.loads(tool.target_roles)
        all_roles.update(roles)
    return jsonify(sorted(list(all_roles)))

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
