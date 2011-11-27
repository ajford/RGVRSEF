
from flaskext.wtf import Form, TextField, DateField, Required, Length 

class Deadline(Form):
    text = TextField('Deadline Text', validators=[Required(),Length(3)])
    date = DateField('Deadline Date', validators=[Required()])

