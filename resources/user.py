import sqlite3
from flask_restful import Resource, reqparse
from flask import request
from models.usermodel import UserModel


class UserRegister(Resource):
    parser =reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = "This field cannot be left blank."
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field cannot be left blank."
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        print (data)
        search_user = UserModel.find_by_username(data['username'])
        print (search_user)
        if UserModel.find_by_username(data['username']):
            return {'message':'username not unique'},400
        user = UserModel(data['username'],data['password'])
        print (user)
        user.save_to_db()
        return {'message':'User created'},201