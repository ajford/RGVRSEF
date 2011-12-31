import re
from datetime import date

from flask import Flask, make_response,redirect, url_for, render_template,json,request,flash
from werkzeug import ImmutableDict

app = Flask(__name__)

from .models import *
from .admin import admin as admin_blueprint
from .forms import *

app.config.from_object('RGVRSEF.config')
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
    deadlines = Deadline.query.order_by(Deadline.date).all()
    news = News.query.order_by(News.date.desc()).first()
    return render_template("index.html", deadlines=deadlines, news=news)

@app.route('/news')
def news():
    news = News.query.order_by(News.date).all()
    return render_template("news.html", news=news)

@app.route('/school',methods=['GET','POST'])
def school():
    form = SchoolInfo(request.form)
    form.district_id.choices = [(d.id,d.name) for d 
        in District.query.order_by('name')]
    if request.method=="POST" and form.validate():
        info=School(form.name.data,form.phone.data,form.fax.data,1)
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('school'))
    return render_template("school.html", form=form)

@app.route('/sponsor',methods=['GET','POST'])
def sponsor():
    form = Sponsor(request.form)
    if request.method=="POST" and form.validate():
        user=models.Sponsor()
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.email = form.email.data
        user.relation = form.relation.data
        user.phone = form.phone.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('sponsor'))
    return render_template("sponsor.html",form=form)

app.register_blueprint(admin_blueprint, url_prefix='/admin')
