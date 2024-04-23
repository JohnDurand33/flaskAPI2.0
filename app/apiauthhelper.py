from flask import request, jsonify   #RESEARCH TOKEN AUTH IN FLASK AND REACT
from functools import wraps
from .models import User
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


def token_auth_required(func):
    # @wraps(func)
    def decorated(*args, **kwargs):
            if "Authorization" not in request.headers:
                return jsonify({'status': 'not ok', 'message': 'Authentication required'}), 401

            val = request.headers['Authorization']
            parts = val.split()

            if len(parts) == 2 and parts[0] == 'Bearer':
                token=parts[1]
                try:
                    user = User.query.filter_by(token=token).first()
                    if user:
                        return func(*args, **kwargs, user=user)
                    else:
                        raise ValueError("User not found")

                except Exception as e:
                    return jsonify({'status': 'not ok', 'message': 'Authentication failed', 'details': str(e)}), 401

            else:
                return jsonify({'status': 'not ok', 'message': 'Incorrect authorization format'}), 401

        decorated.__name__ = func.__name__
        return decorated

def token_auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):

    #     if "Authorization" not in request.headers:
    #         return jsonify({'status': 'not ok', 'message': 'Authentication required'}), 401

    #     val = request.headers['Authorization']
    #     parts = val.split()

    #     if len(parts) == 2 and parts[0] == 'Bearer':
    #         token=parts[1]
    #         try:
    #             user = User.query.filter_by(token=token).first()
    #             if user:
    #                 return func(*args, **kwargs, user=user)
    #             else:
    #                 raise ValueError("User not found")
                
    #         except Exception as e:
    #             return jsonify({'status': 'not ok', 'message': 'Authentication failed', 'details': str(e)}), 401

    #     else:
    #         return jsonify({'status': 'not ok', 'message': 'Incorrect authorization format'}), 401

    # decorated.__name__ = func.__name__
    # return decorated