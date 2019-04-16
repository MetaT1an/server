from flask_restful import Resource, reqparse
import models as md
from utils import token, msg


class AdminSession(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username')
        self.parser.add_argument('password')

    def post(self):
        args = self.parser.parse_args()
        user = md.User.query.filter_by(username=args['username']).first()
        if user and user.check_password(args['password']) and user.is_admin():
            r = {
                'status': True,
                'data': {
                    'username': user.username,
                    'token': token.gen_token(user.id)
                }
            }
        else:
            r = msg.deny_msg
        return r
