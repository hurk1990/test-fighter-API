from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.fightermodel import FighterModel

#Very nice setup: allows to creates requests on the fly instead off having to build the request yourself
class Fighter(Resource):
    parser =reqparse.RequestParser()
    parser.add_argument('wins',
        type = int,
        required = True,
        help = "This field cannot be left blank."
    )
    parser.add_argument('losses',
        type = int,
        required = True,
        help = "This field cannot be left blank."
    )
    parser.add_argument('weight',
        type = int,
        required = True,
        help = "This field cannot be left blank."
    )
    @jwt_required()
    def get(self, name):
        fighter = FighterModel.find_by_fighter(name)
        if fighter:
            return fighter.json()
        return {"Message":"fighter not found"},404
       
    @jwt_required()
    def post(self, name):
        request_data = Fighter.parser.parse_args()
        fighter = FighterModel(name,request_data['wins'],request_data['losses'],request_data['weight'])
        if fighter.find_by_fighter(name):
            return {"Message":'fighter {} already exists'.format(fighter.name)}, 400
        fighter.save_fight()
        return fighter.json(),201

    @jwt_required()
    def put(self, name):
        request_data = Fighter.parser.parse_args()
        fighter = FighterModel.find_by_fighter(name)
        if fighter is None:
            fighter = FighterModel(name, request_data['wins'],request_data['losses'],request_data['weight'])
        else:
            fighter.wins = request_data['wins']
            fighter.losses = request_data['losses']
            fighter.weight = request_data['weight']
        fighter.save_fight()
        return fighter.json()
    
    @jwt_required()
    def delete(self,name):
        fighter = FighterModel.find_by_fighter(name)
        if fighter:
            fighter.delete_fighter()
            return {"Message":"fighter deleted"}, 204
        return {"Message":"fighter not found"},404


class Fighters(Resource):
    @jwt_required()
    def get(self):
        return {'fighters': [fighter.json() for fighter in FighterModel.query.all()]}