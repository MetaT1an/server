import json
import time
import multiprocessing

from flask_restful import Resource, reqparse
from app import db
import models as md
from utils import dns, celery_task, Token


class Task(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.add_args()

    def add_args(self):
        self.parser.add_argument('tname')
        self.parser.add_argument('token')
        self.parser.add_argument('hosts')

    def delete(self, token, task_id):
        uid = Token.check_token(token)
        if not uid:
            r = {'status': False, 'msg': "invalid token"}
        else:
            task = md.Task.query.filter_by(id=task_id, uid=uid).first()
            if task:
                db.session.delete(task)
                db.session.commit()
                r = {'status': True, 'data': ''}
            else:
                r = {'status': False, 'msg': "missing target"}
        return r

    def put(self, token, task_id):
        uid = Token.check_token(token)
        if not uid:
            r = {'status': False, 'msg': "invalid token"}
        else:
            task = md.Task.query.filter_by(id=task_id, uid=uid).first()
            if task:
                # to create a new process to start distributed task, making this request immediately return
                scan_process = multiprocessing.Process(target=celery_task.launch, args=(task.id, token))
                scan_process.start()

                task.status = 1
                db.session.commit()
                r = {'status': True, 'data': ""}
            else:
                r = {'status': False, 'msg': "missing target"}
        return r

    def post(self):
        args = self.parser.parse_args()
        uid = Token.check_token(args['token'])
        date = time.strftime("%Y-%m-%d %H:%M", time.localtime())

        new_task = md.Task(uid=uid, tname=args['tname'], date=date, status=0)
        db.session.add(new_task)
        db.session.commit()

        host_list = json.loads(args['hosts'])   # convert pure json to python list

        for host in host_list:
            if dns.valid_host(host['target']):
                new_host = md.Host(tid=new_task.id, hname=new_task.tname, target=host['target'], policy=host['policy'])
                db.session.add(new_host)

        db.session.commit()

        return {'status': True, 'data': ""}


class Tasks(Resource):

    def get(self, token):
        uid = Token.check_token(token)
        if not uid:
            r = {'status': False, 'msg': "invalid token"}
        else:
            r = {'status': True, 'data': []}
            task_list = md.Task.query.filter(md.Task.uid == uid).order_by(md.Task.id.desc()).all()
            for task in task_list:
                r['data'].append({'tid': task.id, 'tname': task.tname, 'date': task.date, 'status': task.status})
        return r
