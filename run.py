from app import app
from db import db

db.init_app(app)

#Like magic... it creates the tables required when you call a function which tries to commit something to a table
@app.before_first_request
def create_tables():
    db.create_all()