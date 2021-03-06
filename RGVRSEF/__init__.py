import re
from datetime import date
import base64
from pprint import pprint

from flask import (Flask, make_response,redirect, url_for,
                    render_template,json,request,flash,session)
from werkzeug import ImmutableDict
from flask.ext.mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

app = Flask(__name__)
app.config.from_object('RGVRSEF.config')

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SIGNING_KEY'])
SIG_EXPIRED = 'SIG_EXPIRED'

from .models import *
from .admin import admin as admin_blueprint
from .forms import *
from .testing import DummySponsor
import RGVRSEF.utils as utils

jinja_options = dict(app.jinja_options)
jinja_options.update({'trim_blocks':True})
app.jinja_options = ImmutableDict(jinja_options)

repl = lambda x: '%s-%s-%s'%(x.group(1),x.group(2),x.group(3))
phoneRE = re.compile('([0-9]{3})([0-9]{3})([0-9]{4})\Z')
prettyPhone = lambda x: phoneRE.sub(repl,x)

if not app.debug:
    import logging
    from logging import StreamHandler, Formatter
    handler = StreamHandler()
    handler.setLevel(logging.WARNING)
    handler.setFormatter(Formatter("""
        %(asctime)s %(levelname)s: %(message)s
        [in %(pathname)s:%(lineno)d]

        """))
    app.logger.addHandler(handler)

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

def store(**kwargs):
    """ Convenience function to sign and stash values in session."""
    for key in kwargs:
        session[key] = serializer.dumps(kwargs.get(key))
        

def retrieve(key):
    """ Convenience function to retrieved stashed values from session.
        Returns a dictionary containing keys passed in as args.
        """
    try:
        if session.has_key(key):
            return  serializer.loads(session.pop(key),
                        max_age=app.config['SIGNING_MAX_AGE'])
        else:
            app.logger.debug('Error retrieving %s - Not in Session'%key)
            return None

    except SignatureExpired as expired:
        app.logger.warning('EXPIRED SIG - Error retrieving %s\n%s'%(key,
                                                                    expired))
        return SIG_EXPIRED
    except BadSignature as badsig:
        app.logger.warning('BAD SIG - Error retrieving %s\n%s'%(key,badsig))
        return None



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
    active = app.config.get('STUDENT_ACTIVE',False)
    return render_template("index.html", deadlines=deadlines, news=news,
                            active=active)

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
    if form.validate_on_submit():
        form.encrypt()
        sponsor=models.Sponsor()
        form.populate_obj(sponsor)
        db.session.add(sponsor)
        db.session.commit()
        utils.sponsor_mail(sponsor)
        store(sponsor_id=sponsor.id)
        return redirect(url_for('sponsorcomplete'))
    return render_template("sponsor.html",form=form)

@app.route('/reg/sponsor/complete')
def sponsorcomplete():

    sponsor_id = retrieve('sponsor_id')
    if sponsor_id is SIG_EXPIRED:
        message = "Your session has expired. \
            If you do not recieve your confirmation email, please contact us" 
        return render_template('message.html', message=message)
    if sponsor_id is None:
        message = ["Your confirmation page has already been viewed.",
           "If you do not recieve your confirmation email, please contact us"]
        return render_template('message.html', message=message)
    sponsor = Sponsor.query.get_or_404(sponsor_id)
    return render_template("sponsor_complete.html",sponsor=sponsor)


@app.route('/sponsor/review',methods=['GET','POST'])
def sponsor_review():
    form = SponsorLoginForm()
    if form.validate_on_submit():
        form.encrypt()
        sponsid = decode(form.id.data)
        sponsor = Sponsor.query.get_or_404(sponsid)
        if form.password.data == sponsor.password:
            return render_template("sponsor_review.html",sponsor=sponsor)
        else:
            message = "Your login information is invalid."
            return render_template("sponsor_login.html",form=form, 
                                message=message)
    else:
        return render_template("sponsor_login.html",form=form)

@app.route('/reg/student/sponsorcode',methods=['GET','POST'])
def studentreg1():
    if not app.config['STUDENT_ACTIVE']:
        return render_template('message.html',
                            message="Student Registration is currently closed")
    form=StudentSponsorForm()
    if form.validate_on_submit():
        sponsor_id = decode(form.sponsor_id.data)
        sponsor = Sponsor.query.get(sponsor_id)
        if sponsor:
            finished = retrieve('finished')
            store(sponsor_id=sponsor.id)
            return redirect(url_for('studentreg2'))            
        else:
            message = "This Sponsor ID is invalid. \
                    Please verify and reneter."
            return render_template("studentreg1.html",form=form,
                        message=message)
    return render_template("studentreg1.html",form=form, 
                    endpoint=url_for('studentreg1'))

@app.route('/reg/student/code',methods=['GET','POST'])
def studentbackdoor():
    form=StudentSponsorForm()
    if form.validate_on_submit():
        sponsor_id = decode(form.sponsor_id.data)
        sponsor = Sponsor.query.get(sponsor_id)
        if sponsor:
            finished = retrieve('finished')
            store(sponsor_id=sponsor.id)
            return redirect(url_for('studentreg2'))            
        else:
            message = "This Sponsor ID is invalid. \
                    Please verify and reneter."
            return render_template("studentreg1.html",form=form,
                        message=message)
    return render_template("studentreg1.html",form=form, 
                    endpoint=url_for('studentbackdoor'))

@app.route('/reg/student/personalinfo',methods=['GET','POST'])
def studentreg2():
    form=StudentForm()
    if form.validate_on_submit():
        sponsor_id = retrieve('sponsor_id')
        if sponsor_id is None:
            message = "Your session has expired. \
                    Please restart your registration"
            return render_template('message.html', message=message)
        if sponsor_id == SIG_EXPIRED:
            message = "Your session has expired. \
                    Please restart your registration"
            return render_template('message.html', message=message)
        student = Student()
        sponsor = Sponsor.query.get(sponsor_id)
        student.sponsor_id = sponsor.id
        student.school_id = sponsor.school_id
        student.team_leader = True
        form.populate_obj(student)
        db.session.add(student)
        db.session.commit()
        store(student_id=student.id)
        return redirect(url_for('studentreg3'))
    return render_template("studentreg2.html",form=form)

@app.route('/reg/student/projectinfo',methods=['GET','POST'])
def studentreg3():
    form=ProjectForm()
    query=Category.query.order_by('id')
    form.category_id.choices=[(x.id,x.name) for x in query.all()]
    if form.validate_on_submit():
        student_id = retrieve('student_id')
        if student_id is None:
            message = "Your session has expired. \
                    Please restart your registration"
            return render_template('message.html', message=message)
        if student_id == SIG_EXPIRED:
            message = "Your session has expired. \
                    Please restart your registration"
            return render_template('message.html', message=message)
        student = Student.query.get(student_id)

        project = Project()
        form.populate_obj(project)

        db.session.add(project)
        db.session.commit()
        student.project_id = project.id
        db.session.commit()
        store(student_id=student.id)
        if form.individual.data != 'True':
            return redirect(url_for('teammembers'))
        return redirect(url_for('studentreg4'))
    return render_template("studentreg3.html",form=form)

@app.route('/reg/student/teaminfo',methods=['GET','POST'])
def teammembers():
    form=StudentBaseForm()
    leader_id = retrieve('student_id')
    if leader_id is None:
        message = "Your session has expired. \
                Please restart your registration"
        return render_template('message.html', message=message)
    if leader_id == SIG_EXPIRED:
        message = "Your session has expired. \
                Please restart your registration"
        return render_template('message.html', message=message)
    leader = Student.query.get(leader_id)
    store(student_id=leader_id)
    if form.validate_on_submit():
        student = Student()
        student.sponsor_id = leader.sponsor_id
        student.school_id = leader.school_id
        student.project_id = leader.project_id
        form.populate_obj(student)
        db.session.add(student)
        db.session.commit()
        
        return redirect(url_for('teammembers'))
    return render_template("team_members.html",form=form,leader=leader)

@app.route('/reg/student/forms',methods=['GET','POST'])
def studentreg4():
    form=FormsForm()
    if form.validate_on_submit():
        leader_id = retrieve('student_id')
        if leader_id is None:
            message = "Your session has expired. \
                    Please restart your registration"
            return render_template('message.html', message=message)
        if leader_id == SIG_EXPIRED:
            message = "Your session has expired. \
                    Please restart your registration"
            return render_template('message.html', message=message)
        leader = Student.query.get(leader_id)
        forms = Forms()
        forms.project_id = leader.project.id 
        form.populate_obj(forms)
        db.session.add(forms)
        db.session.commit()
        store(student_id=leader_id)
        return redirect(url_for('complete'))
    return render_template("forms.html",form=form)

@app.route('/reg/student/review',methods=['GET','POST'])
def complete():
    finished = retrieve('finished')
    if finished is True:
        message = ["Your confirmation page has been viewed already.",
            "If you do not recieve your confirmation email, please contact us"]
        store(finished=True)
        return render_template('message.html', message=message)

    leader_id = retrieve('student_id')
    if leader_id is None:
        message = "Your session has expired. \
                Please restart your registration"
        return render_template('message.html', message=message)
    if leader_id == SIG_EXPIRED:
        message = "Your session has expired. \
                Please restart your registration"
        return render_template('message.html', message=message)
    leader = Student.query.get(leader_id)
    if leader is None:
        message = "Your session has expired. \
                Please restart your registration"
        return render_template('message.html', message=message)

    utils.project_reg_mail(leader.project)

    if app.config['TESTING']:
        store(student_id=leader_id)
    else:
        store(finished=True)
    return render_template('complete.html', leader=leader)

@app.route('/reg/sponsor/district',methods=['GET','POST'])
def sponsordistrict():
    form=SponsorDistrictForm()
    form.district_id.choices=[(x.id,x.name) for x in 
            District.query.order_by('name')]
    return render_template("district.html",form=form)

@app.route('/contact')
def contact():
    return render_template("contact.html", contacts=app.config['CONTACTS'],
                            webmaster=app.config['WEBMASTER'])

if app.config['TESTING']:
    from pprint import pprint,pformat
    @app.route('/email_preview')
    def emailtest():
        sponsor = DummySponsor()
            
        contact = app.config['CONTACT']
        return render_template('email_sponsor_confirmation.html',
                                sponsor=sponsor,contact=contact)
    
    @app.route('/session_view')
    def sessionview():
        message = pformat(session,width=80)
        resp = make_response(message)
        resp.mimetype = "text/plain"
        return resp 

    @app.route('/set_student_id/<int:id>')
    def setstudid(id):
        store(student_id=id)
        return render_template('message.html',message='Student ID set to %s'%id)

app.register_blueprint(admin_blueprint, url_prefix='/admin')
