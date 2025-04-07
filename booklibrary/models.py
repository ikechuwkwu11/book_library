from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(30), nullable = False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(50),nullable = False)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.String(4))
    available = db.Column(db.Boolean, default = True)
    user_id = db.Columndb(db.Integer,db.ForeignKey('user.id'), nullable = False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'author': self.author,
            'year': self.year
        }

