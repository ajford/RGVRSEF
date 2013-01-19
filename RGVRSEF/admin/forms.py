
from flask.ext.wtf import (Form, TextField, TextAreaField, DateField,
        SelectField, BooleanField, Required, Length, NumberRange, AnyOf )

class DeadlineForm(Form):
    text = TextField('Deadline Text', validators=[Required(),Length(3)])
    date = DateField('Deadline Date', validators=[Required()])

class NewsForm(Form):
    title = TextField('Title', validators=[Required(),Length(3)])
    text = TextAreaField('Text', validators=[Required(),Length(3)])
    date = DateField('Date', validators=[Required()])

class DistrictForm(Form):
    name = TextField('District Name', validators=[Required(),Length(3)])

class SchoolForm(Form):
    name = TextField('School Name', validators=[Required(),Length(3)])
    phone = TextField('Phone', validators=[Required(),Length(10)])
    fax = TextField('Fax', validators=[Required(),Length(10)])
    district_id = SelectField('District', coerce=int)

class MailForm(Form):
    to = SelectField('To', choices = [(1,'Sponsors'),(2,'Students'),
                     (3,'Students and Sponsors'),
                     (4,'Test - Sent to CONTACT')],coerce=int,
                     validators=[Required(), AnyOf((1,2,3),
                     message="You have selected an invalid choice")])
    sender = SelectField('From',coerce=int)
    subject = TextField('Subject', validators=[Required(),Length(3)])
    message = TextAreaField('Message', validators=[Required(),Length(3)])

class FormsSubmittedForm(Form):
    forms_submitted = BooleanField('Forms Submitted')
