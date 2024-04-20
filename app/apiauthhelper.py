from flask import request
from .models import User

def token_auth_required(func):

    def decorated(*args, **kwargs):

        if "Authorization" in request.headers:
            val = request.headers['Authorization']
            type, token = val.split()

            if type == 'Bearer':
                token = token
            else:
                return {
                    'status': 'not ok',
                    'message': 'Issue in inner code block'
                }, 401
        
            user = User.query.filter_by(token=token).first()

            if user:
                return func(user=user, *args, **kwargs)
            
        else:
            return {
                'status': 'not ok',
                'message': 'Issue in outer code block'
            }, 401
    decorated.__name__ = func.__name__
    return decorated

