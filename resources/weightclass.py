from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.weightclassmodel import WeightClassModel

#Very nice setup: allows to creates requests on the fly instead off having to build the request yourself
class Weightclass(Resource):
    @jwt_required()
    def post(self, weight):
        weightclass = WeightClassModel(weight)
        if weightclass.find_by_weight(weight):
            return {"Message":'Weightclass {} already exists'.format(weightclass.weight)}, 400
        weightclass.save_weightclass()
        return weightclass.json(),201

    @jwt_required()
    def delete(self, weight):
        weightclass = WeightClassModel.find_by_weight(weight)
        if weightclass:
            weightclass.delete_weightclass()
            return {"Message":"weightclass deleted"}, 204
        return {"Message":"weightclass not found"},404


class Weightclasses(Resource):
    @jwt_required()
    def get(self):
        return {'weightclasses': [weightclass.json() for weightclass in WeightClassModel.query.all()]}