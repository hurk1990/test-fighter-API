import os
import re

from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.fighter import Fighter, Fighters
from resources.weightclass import Weightclass,Weightclasses

#when imports are failing but you're sure the module is installed, go to cmd+shft+p, select interpreter and paste folder of venv

app = Flask(__name__)

app.config['DEBUG'] = True

uri  = os.environ.get('DATABASE_URL','sqlite:///data.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Don't put the key in the code normally!
app.secret_key = 'test'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth, send username and password

#Also nice: it handles that the endpoints is created in the this call. Very nice.
api.add_resource(Fighter, '/fighter/<string:name>') #http://127.0.0.1:5000/fighter/Khabib+Nurmagomedov
api.add_resource(Fighters, '/fighters') #http://127.0.0.1:5000/fights
api.add_resource(Weightclass, '/weightclass/<int:weight>') #http://127.0.0.1:5000/weightclass/155
api.add_resource(Weightclasses, '/weightclasses') #http://127.0.0.1:5000/weightclasses
api.add_resource(UserRegister, '/UserRegister') #http://127.0.0.1:5000/UserRegister

if  __name__ == '__main__':
    from db import db
    db.init_app(app)
    
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    app.run(port = 5000)