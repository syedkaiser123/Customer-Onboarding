"""Authentication for Customer Onboarding App."""

from functools import wraps
import jwt
from flask import jsonify
from flask import request
from customer_onboarding.constants.default import JWT_SECRET_KEY
from customer_onboarding.constants.generals import (AUTHORIZATION, MESSAGE)
from customer_onboarding.constants.messages import (TOKEN_MISSING, TOKEN_INVALID, SECRET_KEY)


def user_auth(function):
    """Authenticatiion for Customer Onboarding API endpoints."""

    @wraps(function)
    def decorated(*args, **kwargs):
        try:
            if request.headers.get(AUTHORIZATION):
                token = request.headers.get(AUTHORIZATION).split()[-1]
            else:
                return jsonify({MESSAGE: TOKEN_MISSING}), 403

            if token:
                data = jwt.decode(token, key = "my_super_secret", algorithms = ["HS256",])
            else:
                return jsonify({MESSAGE: TOKEN_INVALID}), 403
        except:
            return jsonify({MESSAGE: TOKEN_INVALID}), 403
        return function(*args, **kwargs)
    return decorated