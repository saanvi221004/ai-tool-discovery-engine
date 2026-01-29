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
        """
        Calculate recommendation score with transparent, deterministic logic.
        
        SCORING WEIGHTS:
        - Workflow Match: 40% (primary factor - most important for daily use)
        - Challenge Match: 40% (addresses specific pain points)
        - Skill Level Compatibility: 20% (ensures tool is appropriate)
        
        RETURNS: Detailed scoring breakdown for transparency
        """
        scoring_breakdown = {
            'workflow_match': {'points': 0, 'max': 40, 'achieved': False},
            'challenge_match': {'points': 0, 'max': 40, 'matched_challenges': 0, 'total_challenges': 0},
            'skill_compatibility': {'points': 0, 'max': 20, 'compatible': False},
            'total_score': 0
        }
        
        # WORKFLOW MATCH (40% weight) - Most important factor
        user_workflow = user_response['workflow'].lower()
        tool_use_cases = [use_case.lower() for use_case in json.loads(tool.use_cases)]
        
        # Exact workflow match gets full points
        if any(user_workflow == use_case for use_case in tool_use_cases):
            scoring_breakdown['workflow_match']['points'] = 40
            scoring_breakdown['workflow_match']['achieved'] = True
        # Partial/related match gets partial points
        elif any(user_workflow in use_case or use_case in user_workflow for use_case in tool_use_cases):
            scoring_breakdown['workflow_match']['points'] = 25  # Partial match
            scoring_breakdown['workflow_match']['achieved'] = True
        
        # CHALLENGE MATCH (40% weight) - Addresses pain points
        user_pain_points = [point.lower() for point in user_response['pain_points']]
        tool_pain_points = [point.lower() for point in json.loads(tool.pain_points)]
        matched_challenges = set(user_pain_points) & set(tool_pain_points)
        
        scoring_breakdown['challenge_match']['matched_challenges'] = len(matched_challenges)
        scoring_breakdown['challenge_match']['total_challenges'] = len(user_pain_points)
        
        if user_pain_points:
            # Proportional scoring based on challenge match percentage
            challenge_percentage = len(matched_challenges) / len(user_pain_points)
            scoring_breakdown['challenge_match']['points'] = round(challenge_percentage * 40)
        
        # SKILL LEVEL COMPATIBILITY (20% weight) - Ensures appropriateness
        user_skill = user_response['skill_level']
        tool_skill = tool.skill_level
        
        # Exact match gets full points
        if tool_skill == user_skill or tool_skill == 'all':
            scoring_breakdown['skill_compatibility']['points'] = 20
            scoring_breakdown['skill_compatibility']['compatible'] = True
        # One level difference gets partial points (tool easier than user)
        elif (tool_skill == 'beginner' and user_skill == 'intermediate') or \
             (tool_skill == 'intermediate' and user_skill == 'advanced'):
            scoring_breakdown['skill_compatibility']['points'] = 15
            scoring_breakdown['skill_compatibility']['compatible'] = True
        # Tool harder than user gets minimal points (challenging but possible)
        elif (tool_skill == 'intermediate' and user_skill == 'beginner') or \
             (tool_skill == 'advanced' and user_skill == 'intermediate'):
            scoring_breakdown['skill_compatibility']['points'] = 10
            scoring_breakdown['skill_compatibility']['compatible'] = False
        
        # Calculate total score
        scoring_breakdown['total_score'] = (
            scoring_breakdown['workflow_match']['points'] +
            scoring_breakdown['challenge_match']['points'] +
            scoring_breakdown['skill_compatibility']['points']
        )
        
        return scoring_breakdown
    
    @staticmethod
    def get_recommendations(user_response, limit=10):
        """
        Get recommendations using the improved scoring algorithm.
        
        Only includes tools with meaningful relevance (>20% score).
        Returns tools sorted by total score (highest first).
        """
        tools = AITool.query.all()
        recommendations = []
        
        for tool in tools:
            scoring_breakdown = RecommendationEngine.calculate_score(tool, user_response)
            total_score = scoring_breakdown['total_score']
            
            # Only include tools with meaningful relevance (>20% score)
            if total_score > 20:
                recommendations.append({
                    'tool': tool,
                    'score': total_score,
                    'scoring_breakdown': scoring_breakdown,
                    'explanation': RecommendationEngine.generate_transparent_explanation(tool, user_response, scoring_breakdown)
                })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    @staticmethod
    def generate_transparent_explanation(tool, user_response, scoring_breakdown):
        """
        Generate concrete, user-friendly explanation of why a tool was recommended.
        
        Format: "This tool matches your [workflow] workflow,
                 solves [X] of your [Y] selected challenges,
                 and is suitable for [skill level] skill level."
        """
        workflow_score = scoring_breakdown['workflow_match']['points']
        challenge_score = scoring_breakdown['challenge_match']
        skill_score = scoring_breakdown['skill_compatibility']
        
        # Workflow description
        workflow_desc = user_response['workflow'].lower()
        if workflow_score > 0:
            workflow_text = f"matches your {workflow_desc} workflow"
        else:
            workflow_text = f"doesn't match your {workflow_desc} workflow"
        
        # Challenge description
        matched_challenges = challenge_score['matched_challenges']
        total_challenges = challenge_score['total_challenges']
        challenges_text = f"solves {matched_challenges} of your {total_challenges} selected challenges"
        
        # Skill level description
        user_skill = user_response['skill_level']
        if skill_score['points'] > 0:
            if skill_score['compatible']:
                skill_text = f"is suitable for {user_skill} skill level"
            else:
                skill_text = f"is challenging but possible for {user_skill} skill level"
        else:
            skill_text = f"is not suitable for {user_skill} skill level"
        
        return f"This tool {workflow_text}, {challenges_text}, and {skill_text}."

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
        'scoring_breakdown': rec['scoring_breakdown'],
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
