
from flaskext.wtf import (Form, TextField, TextAreaField,DateField, Required, 
                        Length )

class Deadline(Form):
    text = TextField('Deadline Text', validators=[Required(),Length(3)])
    date = DateField('Deadline Date', validators=[Required()])

class NewsForm(Form):
    title = TextField('Title', validators=[Required(),Length(3)])
    text = TextAreaField('Text', validators=[Required(),Length(3)])
    date = DateField('Date', validators=[Required()])
