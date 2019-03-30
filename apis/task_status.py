from flask_restful import Resource, reqparse
from app import db
from utils import Token
import models as md


class TaskStatus(Resource):

    @staticmethod
    def valid_status(status):
        return status.isdigit() and (0 < int(status) < 3)

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('status')

    def put(self, token, task_id):
        args = self.parser.parse_args()
        uid = Token.check_token(token)
        status = args['status']
        if uid and TaskStatus.valid_status(status):
            task = md.Task.query.filter_by(id=task_id).first()
            task.status = int(status)    # change status
            db.session.commit()
            r = {'status': True, 'data': ""}
        else:
            r = {'status': False, 'msg': "invalid token or status"}
        return r

    def get(self, token, task_id):
        uid = Token.check_token(token)
        if uid:
            task = md.Task.query.filter_by(id=task_id).first()
            r = {'status': True, 'data': task.status}
        else:
            r = {'status': False, 'msg': "invalid token"}
        return r
