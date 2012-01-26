
from flaskext.sqlalchemy import SQLAlchemy

from RGVRSEF import app

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(150))
    address = db.Column(db.String(150))
    city = db.Column(db.String(50))
    zip = db.Column(db.String(10))
    grade = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'))
    team_leader = db.Column(db.Boolean, default=False)
    sponsor_id = db.Column(db.Integer,db.ForeignKey('sponsor.id'))
    school_id = db.Column(db.Integer,db.ForeignKey('school.id'))

    def __repr__(self):
        return "<Student %s - %s %s - PID:%s SID:%s>"%(self.id, 
            self.firstname, self.lastname, self.project_id, self.sponsor_id)

    def serialize(self):
        return {'id': self.id, 'firstname': self.firstname,
                'lastname': self.lastname, 'email': self.email,
                'address': self.address, 'city': self.city,
                'zip': self.zip, 'grade': self.grade, 'age':self.age,
                'project': self.project_id,'team_leader': self.team_leader,
                'sponsor': self.sponsor_id}

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    individual = db.Column(db.Boolean, default=True)
    student = db.relationship("Student",backref='project',lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #division = db.Column(db.Integer, default=1)
    division = db.Column(db.String(5), default='')
    table = db.Column(db.Boolean, default=True)
    electricity = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Project %s - Div:%s - CID:%d>"%(self.id,self.division,
                                                 self.category_id)

    def serialize(self):
        return {'id': self.id, 'title':self.title, 
                'individual':self.individual, 'student':self.student.id,
                'team': [ x.id for x in self.team.all() ],
                'category': self.category.name, 'division': self.division,
                'table': self.table, 'electricity': self.electricity}

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(150))
    relation = db.Column(db.String(150))
    phone = db.Column(db.String(15))
    password = db.Column(db.String(64))
    school_id = db.Column(db.Integer,db.ForeignKey('school.id'))
    students = db.relationship('Student', backref='sponsor',lazy='dynamic')

    def __repr__(self):
        return "<Sponsor %s - %s %s >"%(self.id,self.firstname,self.lastname)

    def serialize(self):
        return {'id': self.id, 'firstname': self.firstname,
                'lastname': self.lastname, 'email': self.email,
                'relation': self.relation, 'phone': self.phone,
                'students': [x.id for x in self.students.all()]}

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    team = db.Column(db.Boolean, default=False)
    projects = db.relationship("Project",backref='category',lazy='dynamic')

    def __init__(self,name,team=False):
        self.name = name.strip().title()
        self.team = team

    def __repr__(self):
        return "<Category %s >"%self.name

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    fax = db.Column(db.String(15))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    students = db.relationship('Student', backref='school',lazy='dynamic')
    sponsors = db.relationship('Sponsor', backref='school',lazy='dynamic')

    def __init__(self,name,phone,fax,district_id):
        self.name = name.strip()
        self.phone = phone.replace('-','').strip()
        self.fax = fax.replace('-','').strip()
        self.district_id = district_id

    def __repr__(self):
        return "<School %s - DID: %d>"%(self.name,self.district_id)

    def serialize(self):
        return {'id':self.id, 'phone':self.phone, 'fax':self.fax, 
                'district_id':self.district_id}
    
class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    schools = db.relationship('School', backref='district',lazy='dynamic')

    def __init__(self,name):
        self.name = name.strip()

    def __repr__(self):
        return "<District %s >"%self.name

    def serialize(self):
        return self.name

class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150))
    date = db.Column(db.Date)

    def __init__(self,text,date):
        self.text = text.strip()
        self.date = date
    
    def __repr__(self):
        return "<Deadline %s - %s>"%(self.text,self.date.strftime("%Y-%m-%d"))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.Text())
    date = db.Column(db.Date)

    def __init__(self,title,text,date):
        self.title = title.strip()
        self.text = text.strip()
        self.date = date

    def __repr__(self):
        return "<News %s - %s>"%(self.title,self.date.strftime("%Y-%m-%d")) 

