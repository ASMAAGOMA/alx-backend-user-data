#!/usr/bin/env python3
"""
auth module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require auth func
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for ipath in excluded_paths:
            if ipath is not None and path == ipath:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header func
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user func
        """
        return None
