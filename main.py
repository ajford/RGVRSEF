import re

from flask import Flask, make_response,redirect, url_for, render_template,json
from werkzeug import ImmutableDict

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
app.config['URLBASE'] = 'http://localhost:5000'
jinja_options = dict(app.jinja_options)
jinja_options.update({'trim_blocks':True})
app.jinja_options = ImmutableDict(jinja_options)

repl = lambda x: '%s-%s-%s'%(x.group(1),x.group(2),x.group(3))
phoneRE = re.compile('([0-9]{3})([0-9]{3})([0-9]{4})\Z')
prettyPhone = lambda x: phoneRE.sub(repl,x)

def currency(x):
    try:
        return '$%.2f'%x
    except TypeError:
        return x

def nonone(x):
    if x is None:
        return ''
    else:
        return x

app.jinja_env.filters['phone']=prettyPhone
app.jinja_env.filters['currency']=currency
app.jinja_env.filters['nonone']=nonone
app.jinja_env.add_extension('jinja2.ext.do')


def NYI():
    return render_template('message.html',message='Not Yet Implemented.')
           
@app.route('/')
def index():
    return NYI()
