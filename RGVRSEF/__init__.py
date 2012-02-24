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
app.config.from_object('%s.config'%__name__)

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SIGNING_KEY'])
SIG_EXPIRED = 'SIG_EXPIRED'

from . import models
from .admin import admin as admin_blueprint
from . import forms
from . import utils
from . import sponsorviews
from . import studentviews
from . import jinjaconfig
from . import log
from . import exceptions
if app.config['TESTING']:
    from .testing import views

@app.errorhandler(500)
def internal_error(e):
    return render_template('internal_error.html'), 500

@app.errorhandler(BadSignature)
def sig_expired(e):
    message = "Your session has expired. Please restart your registration."
    return render_template('message.html', message=message)

@app.errorhandler(exceptions.NoKeyError)
def sig_expired(e):
    message = ["Your session has expired. Please restart your registration.",
            "This site requires browser cookies to function properly, so verify\
            that your cookies are enabled."]
    return render_template('message.html', message=message)


@app.route('/')
def index():
    deadlines = models.Deadline.query.order_by(models.Deadline.date).all()
    news = models.News.query.order_by(models.News.date.desc()).first()
    return render_template("index.html", deadlines=deadlines, news=news)

@app.route('/news')
def news():
    news = models.News.query.order_by(models.News.date).all()
    return render_template("news.html", news=news)

@app.route('/contact')
def contact():
    return render_template("contact.html", contact=app.config['CONTACT'],
                            webmaster=app.config['WEBMASTER'])

app.register_blueprint(admin_blueprint, url_prefix='/admin')
