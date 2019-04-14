from flask_restful import Resource, reqparse
from app import db
import models as md
from utils import token


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email')
        self.parser.add_argument('password')
        self.parser.add_argument('username')
        # self.parser.add_argument('ips', action='append')

    def get(self, user_id):
        user = md.User.query.filter_by(id=user_id).first()
        if user:
            r = {'status': True, 'username': user.username, 'email': user.email}
        else:
            r = {'status': False, 'msg': "no such user"}

        return r

    def post(self):
        args, r = self.parser.parse_args(), {}

        # 1. query if such name exists
        if md.User.query.filter_by(username=args['username']).count():
            r = {'status': False, 'msg': "username has been used"}
        elif md.User.query.filter_by(email=args['email']).count():
            r = {'status': False, 'msg': "email has been registered"}
        else:
            # if not exists in database, create new record
            new_user = md.User(username=args['username'], email=args['email'], admin=False)
            new_user.set_password(args['password'])

            db.session.add(new_user)
            db.session.commit()

            r = {
                'status': True,
                'data': {
                    'username': new_user.username,
                    'token': token.gen_token(new_user.id)
                }
            }
        return r
