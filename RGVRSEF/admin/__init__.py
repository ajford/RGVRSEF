from hashlib import sha256
from datetime import date

from flask import Blueprint, render_template, abort, request, url_for,\
                  flash, redirect
from flaskext.login import current_user, login_required, fresh_login_required

from RGVRSEF import app
from RGVRSEF.models import *
from .forms import DeadlineForm, NewsForm

def NYI():
    return render_template('admin/message.html', message="Not Yet Implemented")

admin = Blueprint('admin', __name__, template_folder='templates',
                                   static_folder='static')

from .auth import *

@admin.route('/')
@login_required
def index():
    seniors = Project.query.filter_by(division='sr')
    juniors = Project.query.filter_by(division='jr')
    
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
    projects = Project.query.all()
    return render_template('admin/projects.html',projects=projects)

@admin.route('/project/<int:id>')
@login_required
def project():
    return NYI()

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
                                target=url_for('.news',id=id),id=id)
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

