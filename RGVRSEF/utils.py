from hashlib import sha256
from datetime import date

#import xlwt

from flask import (Flask, make_response,redirect, url_for,
                    render_template,json,request,flash,session)

from RGVRSEF import app, mail, Message
import RGVRSEF.models as models

def toexcel():
   pass 

def mailtest():
   pass

def sponsor_mail(sponsor):
    if not app.config['DEVELOPMENT']:
        conf_email = Message("RGV RSEF - Sponsor Registration")
        conf_email.html = render_template('email_sponsor_confirmation.html',
                                    contact=app.config['CONTACT'],
                                    sponsor=sponsor)
        conf_email.add_recipient(sponsor.email)
        mail.send(conf_email)

