from flask_restful import Resource, reqparse
from flask import request
from app import db
from utils import token, msg
import models as md


class TaskStatus(Resource):

    @staticmethod
    def valid_status(status):
        return status.isdigit() and (0 < int(status) < 3)

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('status')

    def put(self, task_id):
        args, tk = self.parser.parse_args(), request.headers.get('Authorization')
        if not tk:
            r = msg.auth_fail_msg
        else:
            uid = token.check_token(tk)
            if not uid:
                r = msg.token_invalid_msg
            else:
                status = args['status']
                if TaskStatus.valid_status(status):
                    task = md.Task.query.filter_by(id=task_id).first()
                    task.status = int(status)  # change status
                    db.session.commit()
                    r = msg.success_msg
                else:
                    r = msg.invalid_data_msg
        return r

    def get(self, task_id):
        tk = request.headers.get('Authorization')
        if not tk:
            r = msg.auth_fail_msg
        else:
            uid = token.check_token(token)
            if uid:
                task = md.Task.query.filter_by(id=task_id).first()
                r = {'status': True, 'data': task.status}
            else:
                r = msg.token_invalid_msg
        return r
