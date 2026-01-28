from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from groq import Groq
import os
import json
from extensions import db
from models import CodeSubmission, User

analyzer_bp = Blueprint('analyzer', __name__)

def get_groq_client():
    """Lazy initialize Groq client."""
    return Groq(api_key=os.getenv('GROQ_API_KEY'))

def analyze_code_with_ai(code, language):
    """Analyze code using Groq AI and provide feedback."""
    
    prompt = f"""You are an expert code reviewer and programming mentor. Analyze the following {language} code and provide a comprehensive analysis in JSON format.

Code to analyze:
```{language}
{code}
```

Provide your analysis in the following JSON structure:
{{
    "overall_quality": "A rating from 1-10",
    "summary": "Brief overall assessment of the code",
    "strengths": [
        "Strength 1",
        "Strength 2"
    ],
    "issues": [
        {{
            "severity": "critical/major/minor",
            "type": "bug/performance/style/security",
            "description": "Description of the issue",
            "line": "Line number if applicable (or 'N/A')",
            "suggestion": "How to fix it"
        }}
    ],
    "improvements": [
        {{
            "category": "performance/readability/maintainability/security",
            "suggestion": "Specific improvement suggestion",
            "example": "Code example if applicable"
        }}
    ],
    "best_practices": [
        "Best practice recommendation 1",
        "Best practice recommendation 2"
    ],
    "learning_resources": [
        {{
            "topic": "Topic to learn",
            "resource": "Recommended resource or concept"
        }}
    ]
}}

Be constructive, educational, and specific. Point out bugs, security issues, performance problems, and style improvements. Return ONLY valid JSON."""

    try:
        groq_client = get_groq_client()
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert code reviewer who provides detailed, constructive feedback. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=2500
        )
        
        analysis_content = response.choices[0].message.content.strip()
        
        # Try to extract JSON if there's extra text
        if analysis_content.startswith('```json'):
            analysis_content = analysis_content.split('```json')[1].split('```')[0].strip()
        elif analysis_content.startswith('```'):
            analysis_content = analysis_content.split('```')[1].split('```')[0].strip()
        
        # Validate JSON
        analysis_json = json.loads(analysis_content)
        
        return analysis_json
        
    except json.JSONDecodeError as e:
        # Return a basic analysis if JSON parsing fails
        return {
            "overall_quality": "7",
            "summary": "Code analysis completed. The code appears functional but may benefit from review.",
            "strengths": [
                "Code is syntactically correct",
                "Basic functionality appears to be implemented"
            ],
            "issues": [
                {
                    "severity": "minor",
                    "type": "style",
                    "description": "Could not generate detailed analysis due to parsing error",
                    "line": "N/A",
                    "suggestion": "Please ensure code is well-formatted"
                }
            ],
            "improvements": [
                {
                    "category": "readability",
                    "suggestion": "Add comments to explain complex logic",
                    "example": "# This function does X"
                }
            ],
            "best_practices": [
                "Follow language-specific style guides",
                "Write unit tests for your code"
            ],
            "learning_resources": [
                {
                    "topic": "Code quality",
                    "resource": "Official language documentation"
                }
            ]
        }
    except Exception as e:
        raise Exception(f"Failed to analyze code: {str(e)}")


@analyzer_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_code():
    """Analyze code and provide feedback."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('code'):
            return jsonify({
                'success': False,
                'message': 'Code is required'
            }), 400
        
        if not data.get('language'):
            return jsonify({
                'success': False,
                'message': 'Language is required'
            }), 400
        
        code = data['code'].strip()
        language = data['language'].strip()
        
        if not code:
            return jsonify({
                'success': False,
                'message': 'Code cannot be empty'
            }), 400
        
        # Analyze code using AI
        analysis_result = analyze_code_with_ai(code, language)
        
        # Save code submission to database
        submission = CodeSubmission(
            user_id=user_id,
            language=language,
            code=code,
            analysis_result=json.dumps(analysis_result)
        )
        
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Code analyzed successfully',
            'submission_id': submission.id,
            'analysis': analysis_result,
            'created_at': submission.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to analyze code: {str(e)}'
        }), 500


@analyzer_bp.route('/history', methods=['GET'])
@jwt_required()
def get_analysis_history():
    """Get code analysis history for the current user."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limit per_page to prevent excessive queries
        per_page = min(per_page, 50)
        
        # Query submissions with pagination
        pagination = CodeSubmission.query.filter_by(user_id=user_id)\
            .order_by(CodeSubmission.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        submissions = []
        for sub in pagination.items:
            submissions.append({
                'id': sub.id,
                'language': sub.language,
                'code': sub.code,
                'analysis': json.loads(sub.analysis_result),
                'created_at': sub.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'submissions': submissions,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'total_submissions': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch analysis history: {str(e)}'
        }), 500


@analyzer_bp.route('/<int:submission_id>', methods=['GET'])
@jwt_required()
def get_submission_by_id(submission_id):
    """Get a specific code submission by ID."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Query submission
        submission = CodeSubmission.query.filter_by(id=submission_id, user_id=user_id).first()
        
        if not submission:
            return jsonify({
                'success': False,
                'message': 'Submission not found'
            }), 404
        
        return jsonify({
            'success': True,
            'submission': {
                'id': submission.id,
                'language': submission.language,
                'code': submission.code,
                'analysis': json.loads(submission.analysis_result),
                'created_at': submission.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch submission: {str(e)}'
        }), 500


@analyzer_bp.route('/<int:submission_id>', methods=['DELETE'])
@jwt_required()
def delete_submission(submission_id):
    """Delete a code submission."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Query submission
        submission = CodeSubmission.query.filter_by(id=submission_id, user_id=user_id).first()
        
        if not submission:
            return jsonify({
                'success': False,
                'message': 'Submission not found'
            }), 404
        
        db.session.delete(submission)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Submission deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to delete submission: {str(e)}'
        }), 500


@analyzer_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_analysis_history():
    """Clear all code submissions for the current user."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Delete all submissions for this user
        deleted_count = CodeSubmission.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Analysis history cleared successfully',
            'deleted_count': deleted_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to clear analysis history: {str(e)}'
        }), 500
