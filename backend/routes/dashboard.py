from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from extensions import db
from models import User, Roadmap, ChatMessage, CodeSubmission
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get comprehensive dashboard statistics for the current user."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Count total roadmaps
        total_roadmaps = Roadmap.query.filter_by(user_id=user_id).count()
        
        # Count total chat messages (user messages only, not bot responses)
        total_chats = ChatMessage.query.filter_by(user_id=user_id, sender='user').count()
        
        # Count total code analyses
        total_analyses = CodeSubmission.query.filter_by(user_id=user_id).count()
        
        # Get recent activity (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_roadmaps = Roadmap.query.filter(
            Roadmap.user_id == user_id,
            Roadmap.created_at >= seven_days_ago
        ).count()
        
        recent_chats = ChatMessage.query.filter(
            ChatMessage.user_id == user_id,
            ChatMessage.sender == 'user',
            ChatMessage.created_at >= seven_days_ago
        ).count()
        
        recent_analyses = CodeSubmission.query.filter(
            CodeSubmission.user_id == user_id,
            CodeSubmission.created_at >= seven_days_ago
        ).count()
        
        # Get most recent items
        latest_roadmap = Roadmap.query.filter_by(user_id=user_id)\
            .order_by(Roadmap.created_at.desc())\
            .first()
        
        latest_submission = CodeSubmission.query.filter_by(user_id=user_id)\
            .order_by(CodeSubmission.created_at.desc())\
            .first()
        
        # Get language distribution from roadmaps
        language_stats = db.session.query(
            Roadmap.language,
            func.count(Roadmap.id).label('count')
        ).filter_by(user_id=user_id)\
         .group_by(Roadmap.language)\
         .all()
        
        languages_distribution = [
            {'language': lang, 'count': count}
            for lang, count in language_stats
        ]
        
        # Get activity timeline (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # Group activity by date
        activity_timeline = []
        for i in range(30):
            day = datetime.utcnow() - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            roadmaps_count = Roadmap.query.filter(
                Roadmap.user_id == user_id,
                Roadmap.created_at >= day_start,
                Roadmap.created_at < day_end
            ).count()
            
            chats_count = ChatMessage.query.filter(
                ChatMessage.user_id == user_id,
                ChatMessage.sender == 'user',
                ChatMessage.created_at >= day_start,
                ChatMessage.created_at < day_end
            ).count()
            
            analyses_count = CodeSubmission.query.filter(
                CodeSubmission.user_id == user_id,
                CodeSubmission.created_at >= day_start,
                CodeSubmission.created_at < day_end
            ).count()
            
            if roadmaps_count > 0 or chats_count > 0 or analyses_count > 0:
                activity_timeline.append({
                    'date': day_start.strftime('%Y-%m-%d'),
                    'roadmaps': roadmaps_count,
                    'chats': chats_count,
                    'analyses': analyses_count
                })
        
        activity_timeline.reverse()  # Order from oldest to newest
        
        # Calculate learning streak (consecutive days with activity)
        learning_streak = 0
        current_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        while True:
            day_start = current_date - timedelta(days=learning_streak)
            day_end = day_start + timedelta(days=1)
            
            # Check if there was any activity on this day
            has_activity = (
                Roadmap.query.filter(
                    Roadmap.user_id == user_id,
                    Roadmap.created_at >= day_start,
                    Roadmap.created_at < day_end
                ).first() is not None or
                ChatMessage.query.filter(
                    ChatMessage.user_id == user_id,
                    ChatMessage.created_at >= day_start,
                    ChatMessage.created_at < day_end
                ).first() is not None or
                CodeSubmission.query.filter(
                    CodeSubmission.user_id == user_id,
                    CodeSubmission.created_at >= day_start,
                    CodeSubmission.created_at < day_end
                ).first() is not None
            )
            
            if has_activity:
                learning_streak += 1
            else:
                break
            
            # Limit to prevent infinite loop
            if learning_streak > 365:
                break
        
        # Prepare response
        stats = {
            'user_info': user.to_dict(),
            'totals': {
                'roadmaps': total_roadmaps,
                'chats': total_chats,
                'analyses': total_analyses
            },
            'recent_activity': {
                'last_7_days': {
                    'roadmaps': recent_roadmaps,
                    'chats': recent_chats,
                    'analyses': recent_analyses
                }
            },
            'learning_streak': learning_streak,
            'languages_distribution': languages_distribution,
            'activity_timeline': activity_timeline,
            'latest_items': {
                'roadmap': latest_roadmap.to_dict() if latest_roadmap else None,
                'code_submission': latest_submission.to_dict() if latest_submission else None
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch dashboard stats: {str(e)}'
        }), 500


@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """Get a quick summary of user statistics."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Get basic counts
        total_roadmaps = Roadmap.query.filter_by(user_id=user_id).count()
        total_chats = ChatMessage.query.filter_by(user_id=user_id, sender='user').count()
        total_analyses = CodeSubmission.query.filter_by(user_id=user_id).count()
        
        return jsonify({
            'success': True,
            'summary': {
                'total_roadmaps': total_roadmaps,
                'total_chats': total_chats,
                'total_analyses': total_analyses
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch summary: {str(e)}'
        }), 500
