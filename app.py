from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')

# configuration of database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@192.168.2.12/dvss"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

# api routers. apis package need to use db object, import after db's init
from apis.user import User
from apis.session import Session
from apis.policy import Policies, Policy
from apis.task import Task, Tasks
from apis.host import Host, Hosts
from apis.vul import Vul, Vuls
from apis.task_status import TaskStatus

api.add_resource(User, '/user/<int:user_id>', endpoint='user_get')      # get user info by id
api.add_resource(User, '/user', endpoint='user_post')       # register
api.add_resource(Session, '/session', endpoint='session_post')      # login
api.add_resource(Policies, '/policies', endpoint='policies_get')
api.add_resource(Policy, '/policy/<policy_id>', endpoint='policy_get')      # get certain policy
api.add_resource(Policy, '/policy', endpoint='policy_post')     # create a policy
api.add_resource(Task, '/task', endpoint='task_post')   # create a task
api.add_resource(Task, '/<token>/task/<int:task_id>', endpoint='task_delete')     # delete certain task
api.add_resource(Task, '/<token>/task/<int:task_id>', endpoint='task_put')   # launch a task
api.add_resource(Tasks, '/<token>/tasks', endpoint='tasks_get')   # all tasks of user
api.add_resource(Host, '/<token>/host/<int:host_id>', endpoint='host_get')   # scan result query
api.add_resource(Host, '/<token>/host/<int:host_id>', endpoint='host_put')   # scan result store
api.add_resource(Hosts, '/<token>/task/<int:task_id>/hosts', endpoint='hosts_get')  # get hosts list
api.add_resource(Vul, '/vul', endpoint='vul_post')  # create new vul
api.add_resource(Vuls, '/<token>/host/<int:host_id>/vuls', endpoint='vuls_get')
api.add_resource(TaskStatus, '/<token>/task/<int:task_id>/status', endpoint='status_put')
api.add_resource(TaskStatus, '/<token>/task/<int:task_id>/status', endpoint='status_get')     # query task status


# index page
@app.route('/')
def index():
    return app.send_static_file('login.html')

