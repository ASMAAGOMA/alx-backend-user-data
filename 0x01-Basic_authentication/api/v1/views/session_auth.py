#!/usr/bin/env python3
"""
session auth module
"""


from api.v1.auth.auth import Auth
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    login 
    """
    from api.v1.app import auth
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({'error': 'password missing'}), 400
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({'error': 'no user found for this email'}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401
    session_id = auth.create_session(user.id)
    session_name = auth.session_cookie_name()
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)
    return response
