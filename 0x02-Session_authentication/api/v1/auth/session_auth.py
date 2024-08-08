#!/usr/bin/env python3
"""
session auth module
"""


from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class
    """
    user_id_by_session_id = {}

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
        session_id = self.create_session(request)
        if session_id is None:
            return None
        user_id = self.user_id_by_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
