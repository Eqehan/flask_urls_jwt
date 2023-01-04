from db import db 

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long= db.Column("long", db.String())
    short= db.Column("short", db.String(3))

    def __init__(self, long,short):
        self.long=long
        self.short=short 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)