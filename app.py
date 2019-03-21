from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')

# configuration of database
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@192.168.2.12/dvss"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

# api routers, apis package need to use db object
from apis.user import User

api.add_resource(User, '/user/<int:user_id>', endpoint='user_get')
api.add_resource(User, '/user', endpoint='user_post')


# index page
@app.route('/')
def index():
    return app.send_static_file('register.html')


if __name__ == '__main__':
    app.run()
