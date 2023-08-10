from Web import db,login_manager
from flask_login import UserMixin
from flask import session

@login_manager.user_loader
def load_user(id):
      return User.query.get(int(id))
    
class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(length=30),nullable=False)
    email=db.Column(db.String(length=30),nullable=False,unique=True)
    password=db.Column(db.String(length=20),nullable=False)
    job=db.Column(db.String(length=1),nullable=False)

class Orders(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    item_name=db.Column(db.Integer,nullable=False)
    bill=db.Column(db.Integer(),nullable=False)
    status=db.Column(db.String(length=15),nullable=False)

class Items(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=True)
    price=db.Column(db.Integer(),nullable=False)
    
