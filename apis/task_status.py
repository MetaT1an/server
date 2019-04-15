from flask_restful import Resource, reqparse
from app import db
from utils import msg, validator
import models as md


class TaskStatus(Resource):

    @staticmethod
    def valid_status(status):
        return status.isdigit() and (0 < int(status) < 3)

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('status')

    @validator.check_token
    @validator.check_login
    def put(self, task_id):
        args = self.parser.parse_args()
        status = args['status']

        if TaskStatus.valid_status(status):
            task = md.Task.query.filter_by(id=task_id).first()
            task.status = int(status)  # change status
            db.session.commit()
            r = msg.success_msg
        else:
            r = msg.invalid_data_msg
        return r

    @validator.check_token
    @validator.check_login
    def get(self, task_id):
        task = md.Task.query.filter_by(id=task_id).first()
        return {'status': True, 'data': task.status}

