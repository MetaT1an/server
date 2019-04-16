from flask_restful import Resource, reqparse
from flask import request
from app import db
import models as md
from utils import msg, validator, tester
from rpc.operation import operation_list


class Scanner(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.put_parser = reqparse.RequestParser()

        self.post_parser.add_argument('ip')
        self.post_parser.add_argument('username')
        self.post_parser.add_argument('password')

        self.put_parser.add_argument('op_code')

    @staticmethod
    def valid_op_code(op_code):
        return op_code.isdigit() and (0 <= int(op_code) <= 3)

    @validator.check_token
    @validator.check_admin
    def post(self):
        args = self.post_parser.parse_args()
        if md.Scanner.query.filter_by(ip=args['ip']).count():
            r = msg.error_msg("Scanner exists")
        else:
            # Test whether the target host can connect through ssh
            if tester.test_conn(args['ip'], args['username'], args['password']):
                new_scanner = md.Scanner(ip=args['ip'], username=args['username'], password=args['password'], status=0)
                db.session.add(new_scanner)
                db.session.commit()
                r = msg.success_msg
            else:
                r = msg.error_msg("can't establish connection")
        return r

    @validator.check_token
    @validator.check_admin
    def put(self, scanner_id):
        args, tk = self.put_parser.parse_args(), request.headers.get('Authorization')
        op_code = args['op_code']

        if Scanner.valid_op_code(op_code):
            op_code = int(op_code)
            s = md.Scanner.query.filter_by(id=scanner_id).first()   # get the scanner
            res = operation_list[op_code](tk, scanner_id, s.ip, s.username, s.password)     # remote process call
            r = msg.success_msg if res else msg.error_msg("internal error")
        else:
            r = msg.invalid_data_msg
        return r

    @validator.check_token
    @validator.check_admin
    def delete(self, scanner_id):
        s = md.Scanner.query.filter_by(id=scanner_id).first()
        if s:
            db.session.delete(s)
            db.session.commit()
            r = msg.success_msg
        else:
            r = msg.no_resource_msg
        return r


class Scanners(Resource):

    @validator.check_token
    @validator.check_login
    def get(self):
        r = {'status': True, 'data': []}
        scanner_list = md.Scanner.query.all()
        for scanner in scanner_list:
            r['data'].append({'sid': scanner.id, 'ip': scanner.ip, 'status': scanner.status})
        return r

