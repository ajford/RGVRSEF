from hashlib import sha256
from datetime import date
from smtplib import SMTPException
from StringIO import StringIO
from csv import DictWriter
from unicodedata import normalize

#import xlwt

from flask import (Flask, make_response,redirect, url_for,
                    render_template,json,request,flash,session)
from flask.ext.celery import Celery

from RGVRSEF import app, mail, Message
import RGVRSEF.models as models

celery = Celery(app)

fx = lambda x: normalize('NFKD',x).encode('ascii','ignore')

PROJECT_CSV_FIELDS = ['Project ID','Student 1','Student 2', 'Student 3', 
                'Project Title', 'Category', 'Division', 'School',
                'District','Sponsor Name']
PARTICIPANT_CSV_FIELDS = ['Student','Project ID',
                'Project Title', 'Category', 'Division', 'School',
                'District','Sponsor Name']

def toexcel():
   pass 

@celery.task(name="tasks.projectcsv")
def projectcsv():
    CSV_FIELDS = PROJECT_CSV_FIELDS
    f = StringIO()
    writer = DictWriter(f,CSV_FIELDS)
    writer.writerow( dict( (x,x) for x in CSV_FIELDS) )
    districts = models.District.query.order_by('name').all()
    for district in districts:
        schools = district.schools.order_by('name').all()
        for school in schools:
            students = school.students.join(models.Project).order_by('title')
            students = students.filter(models.Student.team_leader==True).all()
            for student in students:
                try:
                    record = {CSV_FIELDS[0]: student.project.id,
                              CSV_FIELDS[1]: fx("%s %s"%(student.firstname,
                                                    student.lastname)),
                              CSV_FIELDS[4]: fx(student.project.title),
                              CSV_FIELDS[5]: fx(student.project.category.name),
                              CSV_FIELDS[6]: fx(student.project.division),
                              CSV_FIELDS[7]: student.school.name,
                              CSV_FIELDS[8]: student.school.district.name,
                              CSV_FIELDS[9]: fx("%s %s"%(student.sponsor.firstname,
                                                    student.sponsor.lastname))}
                    team = student.project.student
                    team = team.filter(models.Student.team_leader==False).limit(2)
                    team = team.all()
                    i = 2
                    for student in team:
                        record[CSV_FIELDS[i]]= fx("%s %s"%(student.firstname,
                                                        student.lastname))
                        i += 1
                except AttributeError as error:
                    app.logger.error('ProjID:%s - ID:%s - %s %s\n%s\n%s' % 
                            (student.id, student.project.id, student.firstname,
                             student.lastname,pformat(vars(student.project)),
                             error))


                try:
                    writer.writerow(record)
                except UnicodeEncodeError:
                    app.logger.error("Unicode Error:\n%s"%record)

    return f.getvalue()

@celery.task(name="tasks.participantcsv")
def participantcsv():
    CSV_FIELDS = PARTICIPANT_CSV_FIELDS
    f = StringIO()
    writer = DictWriter(f,CSV_FIELDS)
    writer.writerow( dict( (x,x) for x in CSV_FIELDS) )
    districts = models.District.query.order_by('name').all()
    for district in districts:
        schools = district.schools.order_by('name').all()
        for school in schools:
            students = school.students.join(models.Project).order_by('title')
            for student in students:
                try:
                    record = {CSV_FIELDS[0]: fx("%s %s"%(student.firstname,
                                               student.lastname)),
                        CSV_FIELDS[1]: student.project.id,
                        CSV_FIELDS[2]: fx(student.project.title),
                        CSV_FIELDS[3]: fx(student.project.category.name),
                        CSV_FIELDS[4]: fx(student.project.division),
                        CSV_FIELDS[5]: student.school.name,
                        CSV_FIELDS[6]: student.school.district.name,
                        CSV_FIELDS[7]: fx("%s %s"%(student.sponsor.firstname,
                                           student.sponsor.lastname))}
                except AttributeError as error:
                    app.logger.error('ProjID:%s - ID:%s - %s %s\n%s\n%s' % 
                            (student.id, student.project.id, student.firstname,
                             student.lastname,pformat(vars(student.project)),
                             error))
                try:
                    writer.writerow(record)
                except UnicodeEncodeError:
                    app.logger.error("Unicode Error:\n%s"%record)

    return f.getvalue()

def mailtest():
   pass

@celery.task(name="tasks.sponsor_mail")
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

@celery.task(name="tasks.project_reg_mail")
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

@celery.task(name="tasks.mail")
def mail(to,message,subject):
    if to == 1:
        queries = (Sponsor.query,)
    if to == 2:
        queries = (Student.query,)
    if to == 3:
        queries = (Sponsor.query,Student.query)
    if to == 4:
        msg = Message(recipients=[app.config['CONTACT'].get('email')],
                      body=message,
                      subject=subject)
        mail.send(msg)
        return None
    with mail.connect() as conn:
        for query in queries:
            for user in query.all():
                msg = Message(recipients=[user.email],
                              body=message,
                              subject=subject)
                conn.send(msg)
    return None
