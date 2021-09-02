from db import db

class FighterModel(db.Model):
    __tablename__ = 'fighters'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    weight = db.Column(db.Integer,db.ForeignKey('weightclasses.weight'))
    weightclass = db.relationship('WeightClassModel')

    def __init__(self, name, wins, losses, weight):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.weight = weight
    def json(self):
        return {
                 "name":self.name,
                 "wins":self.wins,
                 "losses":self.losses,
                 "weight":self.weight
            }
    @classmethod
    def find_by_fighter(cls,name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM fighters WHERE NAME = NAME LIMIT 1
    
    def save_fight(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_fighter(self):
        db.session.delete(self)
        db.session.commit()