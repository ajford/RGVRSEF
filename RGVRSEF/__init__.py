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
    return base64.urlsafe_b64decode(str(x)+'='*(-len(x)%4))

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

@app.route('/reg/sponsor',methods=['GET','POST'])
def sponsorreg():
    district_id = request.args.get('district_id',None)
    form = SponsorForm(request.form)
    query = School.query.order_by('name')
    if district_id:
        query = query.filter_by(district_id=district_id)
    form.school_id.choices=[(x.id,x.name) for x in query.all()]
    if request.method=="POST" and form.validate():
        user=models.Sponsor()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return render_template("sponsor_complete.html",sponsor=user)
    return render_template("sponsor.html",form=form)

@app.route('/sponsor/review',methods=['GET','POST'])
def sponsor_review():
    form = SponsorLoginForm()
    if form.validate_on_submit():
        sponsid = decode(form.id.data)
        sponsor = Sponsor.query.get_or_404(sponsid)
        if sha256(form.password.data) == sponsor.password:
            return render_template("sponsor_review.html",sponsor=sponsor)
    else:
        return render_template("sponsor_login.html",form=form)

@app.route('/reg/student/sponsorcode',methods=['GET','POST'])
def studentreg1():
    form=StudentSponsorForm()
    if form.validate_on_submit():
        return redirect(url_for('studentreg2'))            
    return render_template("studentreg1.html",form=form)            

@app.route('/reg/student/personalinfo')
def studentreg2():
    form=StudentForm()
    if form.validate_on_submit():
        return redirect(url_for('studentreg3'))
    return render_template("studentreg2.html",form=form)

@app.route('/reg/student/projectinfo')
def studentreg3():
    form=ProjectForm()
    if form.validate_on_submit():
        return redirect(url_for('studentreg4'))
    return render_template("studentreg3.html",form=form)

@app.route('/reg/student/forms')
def studentreg4():
    return NYI()

@app.route('/reg/sponsor/district')
def sponsordistrict():
    form=SponsorDistrictForm()
    form.district_id.choices=[(x.id,x.name) for x in 
            District.query.order_by('name')]
    return render_template("district.html",form=form)

@app.route('/contact')
def contact():
    return NYI()            

app.register_blueprint(admin_blueprint, url_prefix='/admin')
