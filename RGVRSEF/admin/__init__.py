from hashlib import sha256
from datetime import date
from StringIO import StringIO

from flask import Blueprint, render_template, abort, request, url_for,\
                  flash, redirect, make_response
from flaskext.login import current_user, login_required, fresh_login_required
from flaskext.wtf import Optional

from .. import app, mail, Message
from .. import utils
from .. import tasks

admin = Blueprint('admin', __name__, template_folder='templates',
                                   static_folder='static')

from .auth import *
from .. import models
from . import deadline
from . import project
from . import sponsors
from . import district
from . import school
from . import news
from . import mailer

@admin.route('/')
@login_required
def index():
    seniors = models.Project.query.filter_by(division='senior')
    juniors = models.Project.query.filter_by(division='junior')
    
    return render_template('admin/index.html', seniors=seniors,juniors=juniors)

@admin.route('/download/csv/projects')
@login_required
def projectcsv():
    resp = make_response()
    resp.mimetype = 'text/csv'
    resp.data = tasks.projectcsv()
    resp.headers.add('Content-Disposition', 'attachment', 
                    filename='projects.csv')
    return resp

@admin.route('/download/csv/participants')
@login_required
def participantcsv():
    resp = make_response()
    resp.mimetype = 'text/csv'
    resp.data = tasks.participantcsv()
    resp.headers.add('Content-Disposition', 'attachment', 
                    filename='participants.csv')
    return resp
