from flask_restful import Resource, reqparse
from app import db
from utils import msg, validator
import models as md


class ScannerStatus(Resource):
    @staticmethod
    def valid_status(status):
        return status.isdigit() and (0 <= int(status) < 3)

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('status')

    @validator.check_token
    @validator.check_admin
    def put(self, scanner_id):
        args = self.parser.parse_args()
        status = args['status']

        if ScannerStatus.valid_status(status):
            scanner = md.Scanner.query.filter_by(id=scanner_id).first()
            scanner.status = int(status)   # change status
            db.session.commit()
            r = msg.success_msg
        else:
            r = msg.invalid_data_msg
        return r
