from flask import request
from utils import msg, token
import models as md


def check_token(func):
    def inner(*args, **kwargs):
        tk = request.headers.get('Authorization')
        if not tk:
            return msg.auth_fail_msg
        else:
            return func(*args, **kwargs)    # call original api-function, return its response

    return inner


def check_login(func):
    def inner(*args, **kwargs):
        tk = request.headers.get('Authorization')   # this decorator should be called after [check_token]
        uid = token.check_token(tk)
        if not uid:
            return msg.token_invalid_msg
        else:
            return func(*args, **kwargs)

    return inner


def check_admin(func):
    def inner(*args, **kwargs):
        tk = request.headers.get('Authorization')  # this decorator should be called after [check_token]
        uid = token.check_token(tk)
        if not uid:
            return msg.token_invalid_msg    # login check as well
        else:
            user = md.User.query.filter_by(id=uid).first()
            return func(*args, **kwargs) if user.is_admin else msg.deny_msg

    return inner
