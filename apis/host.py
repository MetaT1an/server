from flask_restful import Resource, reqparse
from flask import request
from app import db
from utils import token, msg
import models as md


class Host(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.add_args()

    def add_args(self):
        self.parser.add_argument('status')
        self.parser.add_argument('start')
        self.parser.add_argument('end')
        self.parser.add_argument('elapse')
        self.parser.add_argument('critical')
        self.parser.add_argument('high')
        self.parser.add_argument('medium')
        self.parser.add_argument('low')
        self.parser.add_argument('info')

    def get(self, host_id):
        tk = request.headers.get('Authorization')
        if not tk:      # check token
            r = msg.auth_fail_msg
        else:
            uid = token.check_token(tk)
            if not uid:
                r = msg.token_invalid_msg
            else:
                host = md.Host.query.filter_by(id=host_id).first()
                if not host:
                    r = msg.no_resource_msg
                else:
                    r = {
                        'status': True,
                        'data': {
                            'hname': host.hname,
                            'status': host.status,
                            'policy': host.policy,
                            'target': host.target,
                            'start': host.start,
                            'end': host.end,
                            'elapse': host.elapse,
                            'critical': host.critical,
                            'high': host.high,
                            'medium': host.medium,
                            'low': host.low,
                            'info': host.info
                        }
                    }
        return r

    def put(self, host_id):
        tk, args = request.headers.get('Authorization'), self.parser.parse_args()
        if not tk:
            r = msg.auth_fail_msg
        else:
            uid = token.check_token(tk)
            if not uid:
                r = msg.token_invalid_msg
            else:
                host = md.Host.query.filter_by(id=host_id).first()
                if host:
                    host.status = args['status']
                    host.start = args['start']
                    host.end = args['end']
                    host.elapse = args['elapse']
                    host.critical = args['critical']
                    host.high = args['high']
                    host.medium = args['medium']
                    host.low = args['low']
                    host.info = args['info']

                    db.session.commit()
                    r = msg.success_msg
                else:
                    r = msg.no_resource_msg
        return r


class Hosts(Resource):
    def get(self, task_id):
        tk = request.headers.get('Authorization')
        if not tk:
            r = msg.auth_fail_msg
        else:
            uid = token.check_token(tk)
            if not uid:
                r = msg.token_invalid_msg
            else:
                r = {'status': True, 'data': []}
                host_list = md.Host.query.filter_by(tid=task_id).all()
                for host in host_list:
                    r['data'].append({'hid': host.id, 'target': host.target, 'policy': host.policy})
        return r
