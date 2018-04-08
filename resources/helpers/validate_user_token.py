import functools
import jwt
from flask_restful import request
from os import environ


def validate_user_token(func):

    @functools.wraps(func)
    def verify_token(*args, **kwargs):
        token = request.headers.get('token')
        key = environ.get('SECRET')
        try:
            jwt.decode(token, key=key, algorithms=['HS256'], options={
                        'verify_signature': True,
                        'verify_exp': True
                    })
        except jwt.ExpiredSignatureError:
            return {'status': 'fail', 'message': 'Token has expired'}, 401
        except jwt.InvalidAlgorithmError as error:
            if str(error):
                return {'status': 'fail', 'message': 'User Authorization failed. Enter a valid token.'}, 401
        except jwt.DecodeError as error:
            if str(error) == 'Signature verification failed':
                return {'status': 'fail', 'message': 'Token Signature verification failed.'}, 401
            else:
                return  {'status': 'fail', 'message': 'Authorization failed due to an Invalid token.'}, 401
        return func(*args, **kwargs)
    return verify_token
