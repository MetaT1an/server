from flask_restful import Resource, reqparse
from app import db
import models as md


class Policies(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('pname')
        self.parser.add_argument('description')

    def get(self):
        policy_list = md.Policy.query.all()
        policies = [{'id': policy.id, 'pname': policy.pname} for policy in policy_list]

        return {
            'status': True,
            'data': policies
        }


class Policy(Resource):
    def get(self, p_id):
        policy = md.Policy.query.filter_by(id=p_id).first()
        if policy:
            r = {'status': True, 'pname': policy.pname, 'description': policy.description}
        else:
            r = {'status': False, 'msg': "no such policy"}

        return r

    def post(self):
        args = self.parser.parse_args()

        if md.Policy.query.filter_by(pname=args['pname']).count():
            r = {'status': False, 'msg': "policy name has been used"}
        else:
            new_policy = md.Policy(pname=args['pname'], description=args['description'])
            db.session.add(new_policy)
            db.session.commit()
            r = {'status': True}

        return r
