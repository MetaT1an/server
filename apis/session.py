from flask_restful import Resource, reqparse
import models as md
from utils import token


class Session(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username')
        self.parser.add_argument('password')

    def post(self):
        args, r = self.parser.parse_args(), {}
        user = md.User.query.filter_by(username=args['username']).first()
        if user and user.check_password(args['password']):
            r = {
                'status': True,
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'token': token.gen_token(user.id)
                }
            }
        else:
            r = {
                'status': False,
                'msg': "username or password error"
            }
        return r
