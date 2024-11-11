from functools import wraps
from flask import request, jsonify, make_response, Response
from .rate_limiting import apply_rate_limiting

# Sample bearer token for demonstration
VALID_TOKEN = "Bearer mysecrettoken"

# Decorator for endpoints which require authentication and are rate limited
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != VALID_TOKEN:
            return {"error": "Invalid token, check your Authorization header"}, 401

        # Apply rate limiting
        rate_limited_response = apply_rate_limiting(auth_header)
        if rate_limited_response:
            return rate_limited_response

        response = f(*args, **kwargs)

        if not isinstance(response, Response):
            response = make_response(response)

        return response

    return decorated

