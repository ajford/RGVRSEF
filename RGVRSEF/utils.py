from hashlib import sha256
from datetime import date
from smtplib import SMTPException

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
        try:
            mail.send(conf_email)
        except SMTPException as error:
            app.logger.warning("SMTP ERROR\n%s"%error)

def project_reg_mail(project):
    if not app.config['DEVELOPMENT']:
        leader =project.student.filter(models.Student.team_leader==True).first()
        conf_email = Message("RGV RSEF - Registration")
        conf_email.html = render_template('email_confirmation.html',
                                    contact=app.config['CONTACT'],
                                    leader=leader, project=project)
        conf_email.recipients = [x.email for x in leader.project.student]
        try:
            mail.send(conf_email)
            app.logger.debug("Student confirmation sent")
        except SMTPException as error:
            app.logger.warning("SMTP ERROR\n%s"%error)

        spons_email = Message("RGV RSEF - Your student has registered")
        spons_email.html = render_template('email_student_confirmation.html',
                                    contact=app.config['CONTACT'],
                                    leader=leader, project=project)
        spons_email.add_recipient(leader.sponsor.email)
        try:
            mail.send(spons_email)
            app.logger.debug("Sponsor confirmation sent")
        except SMTPException as error:
            app.logger.warning("SMTP ERROR\n%s"%error)

