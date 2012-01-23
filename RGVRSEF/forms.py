from hashlib import sha256

from flaskext.wtf import (Form, TextField, TextAreaField, BooleanField,
                         SelectField, RadioField, PasswordField, Required,
                         Length, Optional, Email, NumberRange, EqualTo)

class InfoForm(Form):
    firstname = TextField('First Name', validators=[Required(),Length(3)])
    lastname = TextField('Last Name', validators=[Required(),Length(3)])
    email = TextField('Email', validators=[Required(),Email()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(InfoForm, self).__init__(*args, **kwargs)

class StudentForm(InfoForm):
    address = TextField('Mailing Address', validators=[Required(),Length(3)])
    city = TextField('City', validators=[Required(),Length(3)])
    zipcode = TextField('Zip Code', validators=[Required(),Length(5,10)])
    grade = SelectField('Grade', coerce=int,
            choices=[(x,'%sth'%x) for x in range(6,13)],
            validators=[Required(),NumberRange(6,12, 'Please select a grade')])
    age = SelectField('Age', coerce=int,
            choices=[(x,x) for x in range(10,19)],
            validators=[Required(),NumberRange(10,18,'Please select your age')])
    gender = SelectField('Gender',coerce=unicode,
            choices=[('male','Male'),('female','Female')],
            validators=[Required()])

class SponsorForm(InfoForm):
    school_id = SelectField('School', coerce=int)
    phone = TextField('Phone', validators=[Required(),Length(3)])
    password = PasswordField('Password', validators=[Required(),Length(6),
                            EqualTo('confirm')])
    confirm = PasswordField('Confirm Password', 
                            validators=[Required(),Length(6)])
    def encrypt(form):
        form.password.data = sha256(form.password.data).hexdigest()
        form.confirm.data = sha256(form.confirm.data).hexdigest()

class SponsorLoginForm(Form):
    id = TextField('Sponsor ID', validators=[Required(),Length(6)])
    password = PasswordField('Password', validators=[Required(),Length(6)])

    def encrypt(form):
        form.password.data = sha256(form.password.data).hexdigest()

class SponsorDistrictForm(Form):
    district_id = SelectField('District',coerce=int)

class StudentSponsorForm(Form):
    sponsor_id=TextField('Sponsor ID',validators=[Required(),Length(6)])

class ProjectForm(Form):
    title=TextField('Project Title', validators=[Required(),Length(5)])
    team=RadioField('Is it a Team Project', coerce=unicode,
            choices=[('true','yes'),('false','no')],validators=[Required()])
    category=SelectField('Category',coerce=int)
    division=RadioField('Division',
            choices=[('Jr','junior'),('Sr','senior')],
            validators=[Required()])
    table=RadioField('Will you need a table',coerce=unicode,
            choices=[('true','Yes'),('false','No')],validators=[Required()])
    elect=RadioField('Will you need electricity',coerce=unicode,
            choices=[('true','Yes'),('false','No')],validators=[Required()])
