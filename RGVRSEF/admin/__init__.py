from hashlib import sha256
from datetime import date

from flask import Blueprint, render_template, abort, request, url_for,\
                  flash, redirect
from flaskext.login import current_user, login_required, fresh_login_required

from RGVRSEF import app, mail, Message
from RGVRSEF.models import *
from RGVRSEF import forms as mainforms
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
    categories = Category.query.order_by('name').all()
    projects = Project.query
    if request.args.get('category',None): 
        projects = projects.filter_by(category_id = request.args['category']) 
    if request.args.get('division',None):
        projects = projects.filter_by(division = request.args['division']) 
    projects = projects.all()
    return render_template('admin/projects.html', projects=projects, 
                            categories=categories,endpoint='.projects',
                            div_narrow=div,cat_narrow=cat)

@admin.route('/project/<int:id>')
@login_required
def project(id):
    return NYI()
    project = Project.query.get_or_404(id)
    form = mainforms.ProjectForm(obj=project)
    if form.validate_on_submit():
        form.populate_obj(project)
        return redirect(url_for('.projects'))
    return render_template('admin/project.html',form=form)


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

@admin.route('/sponsor/<int:id>')
@login_required
def sponsor(id):
    sponsor = Sponsor.query.get(id)
    return render_template('admin/sponsor.html',sponsor=sponsor)


@admin.route('/school/<int:id>')
@login_required
def school(id):
    school = School.query.get(id)
    return render_template('admin/school.html',school=school)



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
    return NYI()

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
    if form.validate_on_submit():
        if form.to.data == 1:
            queries = (Sponsor.query,)
        if form.to.data == 2:
            queries = (Student.query,)
        if form.to.data == 3:
            queries = (Sponsor.query,Student.query)

        with mail.connect() as conn:
            for query in queries:
                for user in query.all():
                    msg = Message(recipients=[user.email],
                                  body=form.message.data,
                                  subject=form.subject.data)
                    conn.send(msg)
        return render_template('admin/message.html',message="Mail Sent.")
    return render_template('admin/mail.html',form=form)

