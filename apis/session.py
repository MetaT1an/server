from flask_restful import Resource, reqparse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
import models as md


class Session(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username')
        self.parser.add_argument('password')

    @staticmethod
    def check_token(token):
        s = Serializer("secrete")
        try:
            data = s.loads(token)    # decrypt from token str
        except (SignatureExpired, BadSignature):
            return None

        return data['id']   # get user id

    @staticmethod
    def gen_token(user):
        s = Serializer("secrete", expires_in=3600)
        return s.dumps({'id': user.id}).decode("ascii")     # decode to plain str

    def post(self):
        args, r = self.parser.parse_args(), {}
        user = md.User.query.filter_by(username=args['username']).first()
        if user and user.check_password(args['password']):
            r = {
                'status': True,
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'token': Session.gen_token(user)
                }
            }
        else:
            r = {
                'status': False,
                'msg': "username or password error"
            }
        return r
