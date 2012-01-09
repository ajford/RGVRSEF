from hashlib import sha256

from flaskext.sqlalchemy import SQLAlchemy

from RGVRSEF import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(70))
    active = db.Column(db.Boolean, default=False)

    def __init__(self,username,password,active=False):
        self.username = username.strip()
        self.password = sha256(password).hexdigest()
        self.active = active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True 

    def get_id(self):
        return unicode(self.id)
    
    def __repr__(self):
        return "<Admin %s>"%self.username
