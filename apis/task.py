import json
import time
import multiprocessing

from flask_restful import Resource, reqparse
from flask import request
from app import db
import models as md
from utils import dns, token, msg, validator
from manager import celery_task


class Task(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.add_args()

    def add_args(self):
        self.parser.add_argument('tname')
        self.parser.add_argument('hosts')

    @validator.check_token
    @validator.check_login
    def delete(self, task_id):
        tk = request.headers.get('Authorization')
        uid = token.check_token(tk)

        task = md.Task.query.filter_by(id=task_id, uid=uid).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            r = msg.success_msg
        else:
            r = msg.no_resource_msg
        return r

    """
    when task is submitted ,this method will be called
    1. update the status of the task
    2. create a new process to launch a new celery-based distributed task for scanning
    """

    @validator.check_token
    @validator.check_login
    def put(self, task_id):
        tk = request.headers.get('Authorization')
        uid = token.check_token(tk)

        task = md.Task.query.filter_by(id=task_id, uid=uid).first()
        user = md.User.query.filter_by(id=uid).first()
        if task:
            # to create a new process to start distributed task, making this request immediately return
            scan_process = multiprocessing.Process(target=celery_task.launch, args=(task.id, tk, user.email))
            scan_process.start()

            r = msg.success_msg
        else:
            r = msg.no_resource_msg
        return r

    @validator.check_token
    @validator.check_login
    def post(self):
        args, tk = self.parser.parse_args(), request.headers.get('Authorization')
        uid = token.check_token(tk)

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

        return msg.success_msg


class Tasks(Resource):

    @validator.check_token
    @validator.check_login
    def get(self):
        tk = request.headers.get('Authorization')
        uid = token.check_token(tk)

        r = {'status': True, 'data': []}
        task_list = md.Task.query.filter(md.Task.uid == uid).order_by(md.Task.id.desc()).all()
        for task in task_list:
            r['data'].append({'tid': task.id, 'tname': task.tname, 'date': task.date, 'status': task.status})
        return r
