
from flaskext.wtf import (Form, TextField, TextAreaField, DateField,
        SelectField, Required, Length )

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
