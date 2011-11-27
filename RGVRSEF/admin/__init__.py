from hashlib import sha256
from datetime import date

from flask import Blueprint, render_template, abort, request, url_for,\
                  flash, redirect
from flaskext.login import current_user, login_required, fresh_login_required

from RGVRSEF import app
from RGVRSEF.models import *
from .forms import Deadline as Deadline_form

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
    deadlines = Deadline.query.all()
    return render_template('admin/deadlines.html',deadlines=deadlines)

@admin.route('/deadline/<int:id>', methods=["GET","POST"])
@login_required
def deadline(id):
    date_obj = date.today()
    deadline_obj = Deadline.query.get_or_404(id)
    deadline_form = Deadline_form(obj=deadline_obj)
    if request.method == "GET":
        return render_template('admin/deadline.html',form=deadline_form,
                                target=url_for('.deadline',id=id))
    else:
        deadline_form.populate_obj(deadline_obj)
        db.session.commit()
        flash('Deadline successfully updated.','info')
        return redirect(url_for('.deadlines'))

@admin.route('/newdeadline', methods=["GET","POST"])
@login_required
def newdeadline():
    deadline_form = Deadline_form()
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
    return NYI() 

@admin.route('/news')
@login_required
def news():
    return NYI() 
