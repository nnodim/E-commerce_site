from app import db, app
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String(180), nullable=False)
    profile = db.Column(db.String, unique=False, nullable=False, default='default.jpg')
    
    def __repr__(self):
        return '<User %r>' % self.username
    

with app.app_context():
    db.create_all()
