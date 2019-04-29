from flask_restful import Resource, reqparse
from utils import msg, validator
from app import db
import models as md


class Vul(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('hid')     # host id
        self.parser.add_argument('severity')
        self.parser.add_argument('pluginname')
        self.parser.add_argument('pluginset')
        self.parser.add_argument('count')

    @validator.check_token
    @validator.check_login
    def post(self):
        args = self.parser.parse_args()
        plg_name_simple = args['pluginname'][:90]   # too long to display in front ui

        new_vul = md.Vul(hid=args['hid'], severity=args['severity'], pluginname=plg_name_simple, pluginset=args['pluginset'], count=args['count'])
        db.session.add(new_vul)
        db.session.commit()

        return msg.success_msg


class Vuls(Resource):
    def __init__(self):
        self.severity_dict = {4: "Critical", 3: "High", 2: "Medium", 1: "Low", 0: "Info"}

    @validator.check_token
    @validator.check_login
    def get(self, host_id):
        r = {'status': True, 'data': []}
        vul_list = md.Vul.query.filter(md.Vul.hid == host_id).order_by(md.Vul.severity.desc()).all()
        for vul in vul_list:
            r['data'].append({
                'severity': self.severity_dict[vul.severity],
                'pluginname': vul.pluginname,
                'pluginset': vul.pluginset,
                'count': vul.count
            })

        return r
