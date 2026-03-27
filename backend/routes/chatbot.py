from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from groq import Groq
import os
from extensions import db
from models import ChatMessage, User

chatbot_bp = Blueprint('chatbot', __name__)

def get_groq_client():
    """Lazy initialize Groq client."""
    return Groq(api_key=os.getenv('GROQ_API_KEY'))

def get_ai_response(user_message, chat_history=None):
    """Get AI response from Groq using chat history for context."""
    
    # Build conversation context
    messages = [
        {
            "role": "system",
            "content": """You are an expert programming mentor and coding assistant. Your role is to:
1. Help students learn programming concepts clearly and patiently
2. Explain code and debug errors with detailed explanations
3. Provide step-by-step guidance for solving coding problems
4. Recommend best practices and design patterns
5. Answer questions about algorithms, data structures, and software development
6. Encourage learning by asking guiding questions when appropriate

Be friendly, supportive, and educational. Provide code examples when helpful. 
If you see code with errors, point them out and explain how to fix them.
Always format code blocks properly with language-specific syntax highlighting."""
        }
    ]
    
    # Add chat history for context (last 10 messages)
    if chat_history:
        for msg in chat_history[-10:]:
            messages.append({
                "role": "assistant" if msg.sender == "bot" else "user",
                "content": msg.message
            })
    
    # Add current user message
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        groq_client = get_groq_client()
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"Failed to get AI response: {str(e)}")


@chatbot_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send a message to the chatbot and get a response."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        data = request.get_json()
        
        # Validate message
        if not data.get('message'):
            return jsonify({
                'success': False,
                'message': 'Message is required'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'message': 'Message cannot be empty'
            }), 400
        
        # Get recent chat history for context
        chat_history = ChatMessage.query.filter_by(user_id=user_id)\
            .order_by(ChatMessage.created_at.desc())\
            .limit(10)\
            .all()
        chat_history.reverse()  # Order from oldest to newest
        
        # Save user message
        user_chat_message = ChatMessage(
            user_id=user_id,
            message=user_message,
            sender='user'
        )
        db.session.add(user_chat_message)
        db.session.commit()
        
        # Get AI response
        bot_response = get_ai_response(user_message, chat_history)
        
        # Save bot response
        bot_chat_message = ChatMessage(
            user_id=user_id,
            message=bot_response,
            sender='bot'
        )
        db.session.add(bot_chat_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'message_id': bot_chat_message.id,
            'user_message': {
                'id': user_chat_message.id,
                'message': user_message,
                'sender': 'user',
                'created_at': user_chat_message.created_at.isoformat()
            },
            'bot_message': {
                'id': bot_chat_message.id,
                'message': bot_response,
                'sender': 'bot',
                'created_at': bot_chat_message.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to send message: {str(e)}'
        }), 500


@chatbot_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Get chat history for the current user."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Limit per_page to prevent excessive queries
        per_page = min(per_page, 100)
        
        # Query chat messages with pagination
        pagination = ChatMessage.query.filter_by(user_id=user_id)\
            .order_by(ChatMessage.created_at.asc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        messages = []
        for msg in pagination.items:
            messages.append({
                'id': msg.id,
                'message': msg.message,
                'sender': msg.sender,
                'created_at': msg.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'messages': messages,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'total_messages': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch chat history: {str(e)}'
        }), 500


@chatbot_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_chat_history():
    """Clear all chat history for the current user."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Delete all chat messages for this user
        deleted_count = ChatMessage.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Chat history cleared successfully',
            'deleted_count': deleted_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to clear chat history: {str(e)}'
        }), 500


@chatbot_bp.route('/message/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    """Delete a specific message."""
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        
        # Query message
        message = ChatMessage.query.filter_by(id=message_id, user_id=user_id).first()
        
        if not message:
            return jsonify({
                'success': False,
                'message': 'Message not found'
            }), 404
        
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Message deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to delete message: {str(e)}'
        }), 500
