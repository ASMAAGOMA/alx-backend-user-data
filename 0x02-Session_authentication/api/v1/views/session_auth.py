#!/usr/bin/env python3
"""
Session authentication module
"""

from api.v1.auth.auth import Auth
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify
from typing import Tuple
from os import getenv

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    login
    """
    email = request.form.get('email')
    if not email or len(email.strip()) == 0:
        return jsonify({'error': 'email missing'}), 400
    
    password = request.form.get('password')
    if not password or len(password.strip()) == 0:
        return jsonify({'error': 'password missing'}), 400
    
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({'error': 'no user found for this email'}), 404
    
    if not users:
        return jsonify({'error': 'no user found for this email'}), 404
    
    user = users[0]
    
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(getenv('SESSION_NAME'), session_id)
        return response
    
    return jsonify({'error': 'wrong password'}), 401
