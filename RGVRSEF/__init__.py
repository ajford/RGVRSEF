import re
from datetime import date
import base64

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

def decode(x):
    """ Convenience function to decode Sponsor ID. """
    return base64.urlsafe_b64decode(x+'='*(-len(x)%4))

def encode(x):
    """ Convenience function to encode Sponsor ID. """
    return base64.urlsafe_b64encode(str(x)).strip('=')

app.jinja_env.filters['phone']=prettyPhone
app.jinja_env.filters['currency']=currency
app.jinja_env.filters['nonone']=nonone
app.jinja_env.filters['encode']=encode
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

@app.route('/sponsor',methods=['GET','POST'])
def sponsor():
    form = Sponsor(request.form)
    form.school_id.choices=[(x.id,x.name) for x in 
            School.query.order_by('name')]
    if request.method=="POST" and form.validate():
        user=models.Sponsor()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('sponsor'))
    return render_template("sponsor.html",form=form)

@app.route('/sponsor/review',methods=['GET','POST'])
def sponsor_review():
    form = SponsorLogin()
    if form.validate_on_submit():
        sponsid = decode(form.id.data)
        sponsor = Sponsor.query.get_or_404(sponsid)
        if sha256(form.password.data) == sponsor.password:
            return render_template("sponsor_review.html",sponsor=sponsor)
    else:
        return render_template("sponsor_login.html",form=form)

@app.route('/reg/student')
def studentreg():
    return NYI()            

@app.route('/reg/sponsor')
def sponsorreg():
    return redirect(url_for('sponsor'))            

@app.route('/contact')
def contact():
    return NYI()            

app.register_blueprint(admin_blueprint, url_prefix='/admin')
