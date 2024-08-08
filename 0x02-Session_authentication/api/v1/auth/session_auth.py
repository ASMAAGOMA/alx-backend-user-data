#!/usr/bin/env python3
"""
session auth module
"""


from api.v1.auth.auth import Auth
import uuid
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify
from os import getenv


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


class SessionAuth(Auth):
    """
    SessionAuth class
    """
    def __init__(self):
        """Initialize the session auth"""
        super().__init__()
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create session function
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        user_id_for_session_id function
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        current user function
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def session_cookie_name(self) -> str:
        """
        Return the session cookie name
        """
        return getenv('SESSION_NAME', '_my_session_id')
