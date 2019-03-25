from flask_restful import Resource, reqparse
import time

from apis.session import Session
from app import db
import models as md
import utils
import json


class Task(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('tname')
        self.parser.add_argument('token')
        self.parser.add_argument('hosts')

    def get(self, token, task_id):
        uid = Session.check_token(token)
        if not uid:
            return {'status': False, 'msg': "invalid token"}
        else:
            task = md.Task.query.filter_by(id=task_id, uid=uid).first()

    def get(self, token):
        pass

    def post(self):
        args = self.parser.parse_args()
        uid = Session.check_token(args['token'])
        date = time.strftime("%Y-%m-%d %H:%M", time.localtime())

        new_task = md.Task(uid=uid, tname=args['tname'], date=date, status=0)
        db.session.add(new_task)
        db.session.commit()

        host_list = json.loads(args['hosts'])   # convert pure json to python list

        for host in host_list:
            if utils.valid_host(host['target']):
                new_host = md.Host(tid=new_task.id, hname=new_task.tname, target=host['target'], policy=host['policy'])
                db.session.add(new_host)

        db.session.commit()

        return {'status': True, 'data': ""}
