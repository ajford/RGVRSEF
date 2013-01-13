from hashlib import sha256
from datetime import date
from StringIO import StringIO

from flask import Blueprint, render_template, abort, request, url_for,\
                  flash, redirect, make_response
from flask.ext.login import current_user, login_required, fresh_login_required
from flask.ext.wtf import Optional

from RGVRSEF import app, mail, Message
from RGVRSEF.models import *
from RGVRSEF import forms as mainforms
from RGVRSEF import utils as utils
from RGVRSEF.admin.forms import DeadlineForm, NewsForm, DistrictForm, SchoolForm, MailForm

def NYI():
    return render_template('admin/message.html', message="Not Yet Implemented")

admin = Blueprint('admin', __name__, template_folder='templates',
                                   static_folder='static')

from .auth import *

@admin.route('/')
@login_required
def index():
    seniors = Project.query.filter_by(division='senior')
    juniors = Project.query.filter_by(division='junior')
    
    return render_template('admin/index.html', seniors=seniors,juniors=juniors)

@admin.route('/deadlines')
@login_required
def deadlines():
    #deadlines = Deadline.query.filter(Deadline.date>=date.today())
    deadlines = Deadline.query.order_by('date').all()
    return render_template('admin/deadlines.html',deadlines=deadlines)

@admin.route('/deadline/<int:id>', methods=["GET","POST"])
@login_required
def deadline(id):
    date_obj = date.today()
    deadline_obj = Deadline.query.get_or_404(id)
    deadline_form = DeadlineForm(obj=deadline_obj)
    if request.method == "GET":
        return render_template('admin/deadline.html',form=deadline_form,
                                target=url_for('.deadline',id=id),id=id)
    else:
        deadline_form.populate_obj(deadline_obj)
        db.session.commit()
        flash('Deadline successfully updated.','info')
        return redirect(url_for('.deadlines'))

@admin.route('/deletedeadline/<int:id>', methods=["GET","POST"])
@login_required
def deletedeadline(id):
    deadline_obj = Deadline.query.get_or_404(id)
    db.session.delete(deadline_obj)
    db.session.commit()
    flash('Deadline successfully deleted.','info')
    return redirect(url_for('.deadlines'))

@admin.route('/newdeadline', methods=["GET","POST"])
@login_required
def newdeadline():
    deadline_form = DeadlineForm()
    if request.method == "GET":
        return render_template('admin/deadline.html',form=deadline_form,
                                target=url_for('.newdeadline'))
    else:
        deadline_obj = Deadline(deadline_form.text.data,deadline_form.date.data)
        db.session.add(deadline_obj)
        db.session.commit()
        flash('Deadline successfully created.','info')
        return redirect(url_for('.deadlines'))

@admin.route('/projects')
@login_required
def projects():
    div = request.args.get('division',None)
    cat = request.args.get('category',None,type=int)
    district = request.args.get('district',None,type=int)
    categories = Category.query.order_by('name').all()
    districts = District.query.order_by('name').all()
    projects = Project.query.order_by('title')
    print "_____%s"%district
    if request.args.get('category',None): 
        projects = projects.filter_by(category_id = request.args['category']) 
    if request.args.get('division',None):
        projects = projects.filter_by(division = request.args['division']) 
    if request.args.get('district',None):
        projects = projects.join(Student).join(School)
        projects = projects.filter(School.district_id == district)
    projects = projects.all()
    return render_template('admin/projects.html', projects=projects, 
                            categories=categories,districts=districts,
                            endpoint='.projects',
                            div_narrow=div,cat_narrow=cat,
                            dist_narrow=district)

@admin.route('/project/<int:id>', methods=['GET','POST'])
@login_required
def project(id):
    project = Project.query.get_or_404(id)
    leader =project.student.filter(Student.team_leader==True).first()
    form = mainforms.ProjectForm(obj=project)
    query=Category.query.order_by('id')
    form.category_id.choices=[(x.id,x.name) for x in query.all()]
    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.commit()
        return redirect(url_for('.projects'))
    return render_template('admin/project.html',form=form, id=id,
                            project=project, leader=leader)

@admin.route('/deleteproject/<int:id>', methods=["GET","POST"])
@login_required
def deleteproject(id):
    project = Project.query.get_or_404(id)
    forms = project.forms.all()
    for form in forms:
        db.session.delete(form)
    students = project.student.all()
    for student in students:
        db.session.delete(student)
    db.session.delete(project)
    db.session.commit()
    flash('Project successfully deleted.','info')
    return redirect(url_for('.projects'))

@admin.route('/forms/<int:id>', methods=['GET','POST'])
@login_required
def formedit(id):
    forms = Forms.query.get_or_404(id)
    form = mainforms.FormsForm(obj=forms)
    if form.validate_on_submit():
        form.populate_obj(forms)
        db.session.commit()
        return redirect(url_for('.project',id=forms.project_id))
    return render_template('admin/forms.html',form=form, id=id,
                            forms=forms)

@admin.route('/student/<int:id>',methods=['GET','POST'])
@login_required
def studentedit(id):
    student = Student.query.get_or_404(id)
    form = mainforms.StudentForm(obj=student)
    form.address.validators=[]
    form.city.validators=[]
    form.zip.validators=[]
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash('Student successfully updated.','info')
        return redirect(url_for('.project',id=student.project_id))
    return render_template('admin/student.html',form=form, id=id,
                        student=student,proj_id=student.project_id,
                        endpoint=url_for('.studentedit',id=id))

@admin.route('/project/<int:id>/newstudent',methods=['GET','POST'])
@login_required
def newstudent(id):
    form = mainforms.StudentForm()
    form.address.validators=[]
    form.city.validators=[]
    form.zip.validators=[]
    if form.validate_on_submit():
        student = Student()
        student.project_id=id
        proj = Project.query.get_or_404(id)
        student.sponsor_id = proj.student.first().sponsor_id
        form.populate_obj(student)
        db.session.add(student)
        db.session.commit()
        flash('Student successfully created.','info')
        return redirect(url_for('.project',id=id))
    return render_template('admin/student.html',form=form, id=id,
                        endpoint=url_for('.newstudent',id=id))

    
@admin.route('/project/<int:proj_id>/deletestudent/<int:id>', 
                methods=["GET","POST"])
@login_required
def deletestudent(proj_id,id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student successfully deleted.','info')
    return redirect(url_for('.project',id=proj_id))

@admin.route('/sponsors')
@login_required
def sponsors():
    district_narrow = request.args.get('district','')
    sponsors = Sponsor.query.order_by('lastname')
    if district_narrow != '':
        sponsors = sponsors.join(School).filter_by(district_id=district_narrow)
    districts = District.query.all()
    
    return render_template('admin/sponsors.html',sponsors=sponsors,
                        district_narrow=district_narrow,
                        districts=districts)

@admin.route('/sponsor/<int:id>', methods=['GET','POST'])
@login_required
def sponsor(id):
    sponsor = Sponsor.query.get(id)
    form = mainforms.SponsorForm(obj=sponsor)
    form.password.validators = []
    form.confirm.validators = []
    query = School.query.order_by(School.name)
    form.school_id.choices=[(x.id,"%s - %s"%(x.name,x.district.name)) 
                            for x in query.all()]
    if form.validate_on_submit():
        form.populate_obj(sponsor)
        db.session.commit()
        flash("Sponsor Updated")
        return redirect(url_for('.sponsors'))

    students = sponsor.students.filter(Student.team_leader==True).all()
    return render_template('admin/sponsor.html',form=form,id=id,
                            sponsor=sponsor, students=students)

@admin.route('/deletesponsor/<int:id>', methods=["GET","POST"])
@login_required
def deletesponsor(id):
    sponsor_obj = Sponsor.query.get_or_404(id)
    db.session.delete(sponsor_obj)
    db.session.commit()
    flash('Sponsor successfully deleted.','info')
    return redirect(url_for('.sponsors'))

@admin.route('/districts')
@login_required
def districts():
    districts = District.query.all()
    return render_template('admin/districts.html',districts=districts)

@admin.route('/district/<int:id>', methods=["GET","POST"])
@login_required
def district(id):
    district_obj = District.query.get_or_404(id)
    district_form = DistrictForm(obj=district_obj)
    if request.method == "GET":
        return render_template('admin/district.html',form=district_form,
                                target=url_for('.district',id=id),id=id,
                                schools=district_obj.schools)
    else:
        district_form.populate_obj(district_obj)
        db.session.commit()
        flash('District successfully updated.','info')
        return redirect(url_for('.districts'))

@admin.route('/deletedistrict/<int:id>', methods=["GET","POST"])
@login_required
def deletedistrict(id):
    district_obj = District.query.get_or_404(id)
    db.session.delete(district_obj)
    db.session.commit()
    flash('District successfully deleted.','info')
    return redirect(url_for('.districts'))

@admin.route('/newdistrict', methods=["GET","POST"])
@login_required
def newdistrict():
    district_form = DistrictForm()
    if request.method == "GET":
        return render_template('admin/district.html',form=district_form,
                                target=url_for('.newdistrict'))
    else:
        district_obj = District(district_form.name.data)
        db.session.add(district_obj)
        db.session.commit()
        flash('District successfully created.','info')
        return redirect(url_for('.districts'))


@admin.route('/download/csv')
@login_required
def downloadcsv():
    resp = make_response()
    resp.mimetype = 'text/csv'
    resp.data = utils.tocsv()
    resp.headers.add('Content-Disposition', 'attachment', 
                    filename='registrants.csv')
    return resp

@admin.route('/download/participantcsv')
@login_required
def studentcsv():
    resp = make_response()
    resp.mimetype = 'text/csv'
    resp.data = utils.studentcsv()
    resp.headers.add('Content-Disposition', 'attachment', 
                    filename='participants.csv')
    return resp

@admin.route('/news')
@login_required
def news():
    #news = News.query.filter(News.date>=date.today())
    news = News.query.order_by('date').all()
    return render_template('admin/news.html',news=news)

@admin.route('/editnews/<int:id>', methods=["GET","POST"])
@login_required
def editnews(id):
    news_obj = News.query.get_or_404(id)
    news_form = NewsForm(obj=news_obj)
    if request.method == "GET":
        return render_template('admin/editnews.html',form=news_form,
                                target=url_for('.editnews',id=id),id=id)
    else:
        news_form.populate_obj(news_obj)
        db.session.commit()
        flash('News successfully updated.','info')
        return redirect(url_for('.news'))

@admin.route('/deletenews/<int:id>', methods=["GET","POST"])
@login_required
def deletenews(id):
    news_obj = News.query.get_or_404(id)
    db.session.delete(news_obj)
    db.session.commit()
    flash('News successfully deleted.','info')
    return redirect(url_for('.news'))

@admin.route('/newnews', methods=["GET","POST"])
@login_required
def newnews():
    news_form = NewsForm()
    if request.method == "GET":
        date_obj = date.today()
        return render_template('admin/editnews.html',form=news_form,
                                target=url_for('.newnews'),today=date_obj)
    else:
        news_obj = News(news_form.title.data,news_form.text.data,
                        news_form.date.data)
        db.session.add(news_obj)
        db.session.commit()
        flash('News successfully created.','info')
        return redirect(url_for('.news'))


@admin.route('/schools')
@login_required
def schools():
    district_narrow = request.args.get('district','')
    schools = School.query
    if district_narrow != '':
        schools = schools.filter_by(district_id=district_narrow)
    districts = District.query.all()
    
    return render_template('admin/schools.html',schools=schools,
                        district_narrow=district_narrow,
                        districts=districts)

@admin.route('/school/<int:id>', methods=["GET","POST"])
@login_required
def school(id):
    school_obj = School.query.get_or_404(id)
    school_form = SchoolForm(obj=school_obj)
    school_form.district_id.choices = [(d.id,d.name) for d 
        in District.query.order_by('name')]
    if request.method == "GET":
        return render_template('admin/school.html',form=school_form, id=id,
                            target=url_for('.school',id=id),school=school_obj)
    else:
        school_form.populate_obj(school_obj)
        db.session.commit()
        flash('School successfully updated.','info')
        return redirect(url_for('.schools'))

@admin.route('/deleteschool/<int:id>', methods=["GET","POST"])
@login_required
def deleteschool(id):
    school_obj = School.query.get_or_404(id)
    db.session.delete(school_obj)
    db.session.commit()
    flash('School successfully deleted.','info')
    return redirect(url_for('.schools'))

@admin.route('/newschool', methods=["GET","POST"])
@login_required
def newschool():
    school_form = SchoolForm()
    school_form.district_id.choices = [(d.id,d.name) for d 
        in District.query.order_by('name')]
    if request.method == "GET":
        return render_template('admin/school.html',form=school_form,
                                target=url_for('.newschool'))
    else:
        school_obj = School(school_form.name.data, school_form.phone.data,
                            school_form.fax.data, school_form.district_id.data)
        db.session.add(school_obj)
        db.session.commit()
        flash('School successfully created.','info')
        return redirect(url_for('.schools'))


@admin.route('/mailer', methods=['POST','GET'])
@login_required
def mailer():
    form = MailForm()
    contacts = app.config['CONTACTS']
    senders = [(x,contacts[x]['name']) for x in range(len(contacts))]
    form.sender.choices = senders
    if form.validate_on_submit():
        if form.to.data == 1:
            queries = (Sponsor.query,)
        if form.to.data == 2:
            queries = (Student.query,)
        if form.to.data == 3:
            queries = (Sponsor.query,Student.query)
        if form.to.data == 4:
            msg = Message(recipients=[contacts[form.sender.data].get('email')],
                          body=form.message.data,
                          subject=form.subject.data,
                          sender = contacts[form.sender.data].get('email'))
            mail.send(msg)
            return render_template('admin/message.html',message="Mail Sent.")
        with mail.connect() as conn:
            for query in queries:
                for user in query.all():
                    msg = Message(recipients=[user.email],
                              body=form.message.data,
                              subject=form.subject.data,
                              sender = contacts[form.sender.data].get('email'))
                    conn.send(msg)
        return render_template('admin/message.html',message="Mail Sent.")
    return render_template('admin/mail.html',form=form)

@admin.route('/mailer/confirmation/sponsor/<int:id>')
@login_required
def sponsorconf(id):
    sponsor = Sponsor.query.get_or_404(id)
    print "Sending: %s(%s) - %s"%(sponsor.firstname+' '+sponsor.lastname,
                         sponsor.id, sponsor.email)
    utils.sponsor_mail(sponsor)
    message = "Confirmation resent to %s, %s <%s>"%(sponsor.lastname,
                            sponsor.firstname,sponsor.email)
    return render_template('admin/message.html',message=message)

@admin.route('/mailer/confirmation/project/<int:id>')
@login_required
def projectconf(id):
    project = Project.query.get_or_404(id)
    utils.project_reg_mail(project)
    message = "Confirmation resent about project #%s, %s"%(project.id,
                                    project.title)
    return render_template('admin/message.html',message=message)
