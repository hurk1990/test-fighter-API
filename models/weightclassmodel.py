from db import db

class WeightClassModel(db.Model):
    __tablename__ = 'weightclasses'
    id = db.Column(db.Integer, primary_key = True)
    weight = db.Column(db.Integer(),unique = True)
    
    #the use of 'lazy = 'dynamic'' is really important. Otherwise you will create many items in memory which you may not need
    fighters = db.relationship('FighterModel',lazy='dynamic')

    def __init__(self, weight):
        self.weight = weight
    def json(self):
        return {
                 "weight":self.weight,
                 'fighters':[fighter.json() for fighter in self.fighters.all()]
            }
    @classmethod
    def find_by_weight(cls,weight):
        return cls.query.filter_by(weight=weight).first() # SELECT * FROM fighters WHERE NAME = NAME LIMIT 1
    
    def save_weightclass(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_weightclass(self):
        db.session.delete(self)
        db.session.commit()