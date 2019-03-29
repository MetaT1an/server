from flask_restful import Resource, reqparse
from utils import Token
from app import db
import models as md


class Vul(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token')   # permission check
        self.parser.add_argument('hid')     # host id
        self.parser.add_argument('severity')
        self.parser.add_argument('pluginname')
        self.parser.add_argument('pluginset')
        self.parser.add_argument('count')

    def post(self):
        args = self.parser.parse_args()
        uid = Token.check_token(args['token'])
        if uid:
            new_vul = md.Vul(hid=args['hid'], severity=args['severity'], pluginname=args['pluginname'], pluginset=args['pluginset'], count=args['count'])
            db.session.add(new_vul)
            db.session.commit()
            r = {'status': True, 'data': ""}
        else:
            r = {'status': False, 'msg': "invalid token"}
        return r


class Vuls(Resource):
    def __init__(self):
        self.severity_dict = {4: "Critical", 3: "High", 2: "Medium", 1: "Low", 0: "Info"}

    def get(self, token, host_id):
        uid = Token.check_token(token)
        if uid:
            r = {'status': True, 'data': []}
            vul_list = md.Vul.query.filter(md.Vul.hid == host_id).order_by(md.Task.id.desc()).all()
            for vul in vul_list:
                r['data'].append({
                    'severity': self.severity_dict[vul.severity],
                    'pluginname': vul.pluginname,
                    'pluginset': vul.pluginset,
                    'count': vul.count
                })
        else:
            r = {'status': False, 'msg': "invalid token"}
        return r
