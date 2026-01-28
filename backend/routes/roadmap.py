from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from groq import Groq
import os
import json
from extensions import db
from models import Roadmap, User

roadmap_bp = Blueprint('roadmap', __name__)

def get_groq_client():
    """Lazy initialize Groq client."""
    return Groq(api_key=os.getenv('GROQ_API_KEY'))

def generate_roadmap_with_ai(programming_language, skill_level, career_goal):
    """Generate a personalized learning roadmap using Groq AI."""
    
    prompt = f"""You are an expert programming mentor. Create a detailed, personalized learning roadmap for a student with the following profile:

Programming Language: {programming_language}
Current Skill Level: {skill_level}
Career Goal: {career_goal}

Generate a comprehensive learning roadmap in JSON format with the following structure:
{{
    "title": "Learning Roadmap Title",
    "description": "Brief overview of the learning path",
    "estimated_duration": "Estimated time to complete (e.g., '3-6 months')",
    "phases": [
        {{
            "phase_number": 1,
            "phase_name": "Phase Name",
            "duration": "Estimated duration",
            "topics": [
                {{
                    "topic": "Topic Name",
                    "description": "What you'll learn",
                    "resources": ["Resource 1", "Resource 2"],
                    "projects": ["Project idea 1", "Project idea 2"]
                }}
            ]
        }}
    ],
    "milestones": [
        {{
            "milestone": "Milestone name",
            "description": "What you should achieve"
        }}
    ],
    "recommended_resources": [
        {{
            "type": "Documentation/Course/Book/Tutorial",
            "name": "Resource name",
            "url": "URL or description"
        }}
    ],
    "career_tips": [
        "Career advice 1",
        "Career advice 2"
    ]
}}

Make it specific to the {skill_level} level and tailored for someone aspiring to become a {career_goal}. Include at least 3-5 phases with practical projects and real-world applications. Return ONLY valid JSON, no additional text."""

    try:
        groq_client = get_groq_client()
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert programming educator who creates structured, actionable learning roadmaps. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        roadmap_content = response.choices[0].message.content.strip()
        
        # Try to extract JSON if there's extra text
        if roadmap_content.startswith('```json'):
            roadmap_content = roadmap_content.split('```json')[1].split('```')[0].strip()
        elif roadmap_content.startswith('```'):
            roadmap_content = roadmap_content.split('```')[1].split('```')[0].strip()
        
        # Validate JSON
        roadmap_json = json.loads(roadmap_content)
        
        return roadmap_json
        
    except json.JSONDecodeError as e:
        # Return a basic structured roadmap if JSON parsing fails
        return {
            "title": f"{programming_language} Learning Roadmap for {career_goal}",
            "description": f"A personalized learning path for {skill_level} level developers",
            "estimated_duration": "3-6 months",
            "phases": [
                {
                    "phase_number": 1,
                    "phase_name": "Foundations",
                    "duration": "4-6 weeks",
                    "topics": [
                        {
                            "topic": f"{programming_language} Basics",
                            "description": "Master the fundamentals",
                            "resources": ["Official documentation", "Online tutorials"],
                            "projects": ["Build a simple application"]
                        }
                    ]
                }
            ],
            "milestones": [
                {"milestone": "Complete beginner tutorials", "description": "Understand core concepts"}
            ],
            "recommended_resources": [],
            "career_tips": ["Practice consistently", "Build projects", "Contribute to open source"]
        }
    except Exception as e:
        raise Exception(f"Failed to generate roadmap: {str(e)}")


@roadmap_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_roadmap():
    """Generate a personalized learning roadmap for the user."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['programming_language', 'skill_level', 'career_goal']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        programming_language = data['programming_language']
        skill_level = data['skill_level']
        career_goal = data['career_goal']
        
        # Validate skill level
        valid_skill_levels = ['beginner', 'intermediate', 'advanced']
        if skill_level.lower() not in valid_skill_levels:
            return jsonify({
                'success': False,
                'message': f'Invalid skill level. Must be one of: {", ".join(valid_skill_levels)}'
            }), 400
        
        # Generate roadmap using AI
        roadmap_data = generate_roadmap_with_ai(
            programming_language,
            skill_level,
            career_goal
        )
        
        # Save roadmap to database
        new_roadmap = Roadmap(
            user_id=user_id,
            language=programming_language,
            skill_level=skill_level.lower(),
            career_goal=career_goal,
            roadmap_data=json.dumps(roadmap_data)
        )
        
        db.session.add(new_roadmap)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Roadmap generated successfully',
            'roadmap': {
                'id': new_roadmap.id,
                'language': new_roadmap.language,
                'skill_level': new_roadmap.skill_level,
                'career_goal': new_roadmap.career_goal,
                'data': roadmap_data,
                'created_at': new_roadmap.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to generate roadmap: {str(e)}'
        }), 500


@roadmap_bp.route('/my-roadmaps', methods=['GET'])
@jwt_required()
def get_my_roadmaps():
    """Get all roadmaps for the current user."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Query user's roadmaps, ordered by creation date (newest first)
        roadmaps = Roadmap.query.filter_by(user_id=user_id).order_by(Roadmap.created_at.desc()).all()
        
        roadmaps_list = []
        for roadmap in roadmaps:
            roadmaps_list.append({
                'id': roadmap.id,
                'language': roadmap.language,
                'skill_level': roadmap.skill_level,
                'career_goal': roadmap.career_goal,
                'data': json.loads(roadmap.roadmap_data),
                'created_at': roadmap.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'roadmaps': roadmaps_list,
            'count': len(roadmaps_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch roadmaps: {str(e)}'
        }), 500


@roadmap_bp.route('/<int:roadmap_id>', methods=['GET'])
@jwt_required()
def get_roadmap_by_id(roadmap_id):
    """Get a specific roadmap by ID."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Query roadmap
        roadmap = Roadmap.query.filter_by(id=roadmap_id, user_id=user_id).first()
        
        if not roadmap:
            return jsonify({
                'success': False,
                'message': 'Roadmap not found'
            }), 404
        
        return jsonify({
            'success': True,
            'roadmap': {
                'id': roadmap.id,
                'language': roadmap.language,
                'skill_level': roadmap.skill_level,
                'career_goal': roadmap.career_goal,
                'data': json.loads(roadmap.roadmap_data),
                'created_at': roadmap.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch roadmap: {str(e)}'
        }), 500


@roadmap_bp.route('/<int:roadmap_id>', methods=['DELETE'])
@jwt_required()
def delete_roadmap(roadmap_id):
    """Delete a roadmap."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Query roadmap
        roadmap = Roadmap.query.filter_by(id=roadmap_id, user_id=user_id).first()
        
        if not roadmap:
            return jsonify({
                'success': False,
                'message': 'Roadmap not found'
            }), 404
        
        db.session.delete(roadmap)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Roadmap deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to delete roadmap: {str(e)}'
        }), 500
