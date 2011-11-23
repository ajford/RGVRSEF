
from flaskext.wtf import Form, TextField, TextAreaField, BooleanField,\
                         SelectField, RadioField, Required, Length, Optional,\
                         Email, NumberRange

class Info(Form):
    firstname = TextField('First Name', validators=[Required(),Length(3)])
    lastname = TextField('Last Name', validators=[Required(),Length(3)])
    email = TextField('Email', validators=[Required(),Email()])

class Student(Info):
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

class Sponsor(Info):
    relation = TextField('Relation to student', 
            validators=[Required(),Length(3)])
    phone = TextField('Phone', validators=[Required(),Length(3)])
