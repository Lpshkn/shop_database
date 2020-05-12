from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(_id):
    return User.query.get(int(_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    server = db.Column(db.String(128), nullable=False)
    dbname = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

