from hashlib import sha256
from datetime import date
from smtplib import SMTPException
from StringIO import StringIO
from unicodedata import normalize

#import xlwt

from flask import (Flask, make_response,redirect, url_for,
                    render_template,json,request,flash,session)

try:
    from unicodecsv import DictWriter
except ImportError:
    from csv import DictWriter


from RGVRSEF import app, mail, Message
import RGVRSEF.models as models


fx = lambda x: normalize('NFKD',x).encode('ascii','ignore')

CSV_FIELDS = ['Project ID', 'Student 1', 'Student 2', 'Student 3', 
                'Project Title', 'Category', 'Division', 'School',
                'District', 'Sponsor Name', 'Forms Submitted', 'Notes']
STUDENT_FIELDS = ['Project ID', 'Category', 'First Name','Last Name', 'Grade',
                'Gender', 'School', 'Individual', 'Vertabrate', 
                'Human Participant', 'H.B.A.']

def toexcel():
   pass 

def tocsv():
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
                                                    student.sponsor.lastname)),
                              CSV_FIELDS[10]: student.project.forms_submitted,
                              CSV_FIELDS[11]: student.project.notes,
                              }
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
                             student.lastname,vars(student.project),
                             error))


                try:
                    writer.writerow(record)
                except UnicodeEncodeError:
                    app.logger.error("Unicode Error:\n%s"%record)

    return f.getvalue()

def studentcsv():
    f = StringIO()
    writer = DictWriter(f,STUDENT_FIELDS)
    writer.writerow( dict( (x,x) for x in STUDENT_FIELDS) )
    for student in models.Student.query.all():
        if student.project_id:
            try:
                project = student.project
                record = {STUDENT_FIELDS[0]: student.project_id,
                          STUDENT_FIELDS[1]: student.project.category.name,
                          STUDENT_FIELDS[2]: fx(student.firstname),
                          STUDENT_FIELDS[3]: fx(student.lastname),
                          STUDENT_FIELDS[4]: student.grade,
                          STUDENT_FIELDS[5]: student.gender,
                          STUDENT_FIELDS[6]: student.school.name,
                          STUDENT_FIELDS[7]: str(project.individual),
                          STUDENT_FIELDS[8]: str(project.forms.first().vafa or
                                            project.forms.first().vafb),
                          STUDENT_FIELDS[9]: str(project.forms.first().hsf),
                          STUDENT_FIELDS[10]: str(project.forms.first().phbaf)}
            except AttributeError as error:
                app.logger.error('ProjID:%s - ID:%s - %s %s\n%s\n%s' % 
                        (student.id, student.project.id, student.firstname,
                         student.lastname,vars(student.project),
                         error))
            if record:
                try:
                    writer.writerow(record)
                except UnicodeEncodeError:
                    app.logger.error("Unicode Error:\n%s"%record)

    return f.getvalue()

def mailtest():
   pass

def sponsor_resend_all():
    if not app.config['DEVELOPMENT']:
        for sponsor in models.Sponsor.query.all():
            sponsor_mail(sponsor)

def project_resend_all():
    if not app.config['DEVELOPMENT']:
        for project in models.Project.query.all():
            project_reg_mail(project)
          

def sponsor_mail(sponsor):
    if not app.config['DEVELOPMENT']:
        sender = app.config['CONTACTS'][0]
        conf_email = Message("RGV RSEF - Sponsor Registration",
                             sender=(sender['name'],sender['email']))
        conf_email.html = render_template('email_sponsor_confirmation.html',
                                    contact=sender, sponsor=sponsor)
        conf_email.add_recipient(sponsor.email)
        mail.fail_silently = False
        try:
            mail.send(conf_email)
        except SMTPException as error:
            app.logger.warning("SMTP ERROR\n%s"%error)


def project_reg_mail(project):
    if not app.config['DEVELOPMENT']:
        sender = app.config['CONTACTS'][0]
        leader =project.student.filter(models.Student.team_leader==True).first()
        conf_email = Message("RGV RSEF - Registration",
                            sender=(sender['name'],sender['email']))
        conf_email.html = render_template('email_confirmation.html',
                                    contact=sender, leader=leader,
                                    project=project)
        conf_email.recipients = [x.email for x in leader.project.student]
        try:
            mail.send(conf_email)
            app.logger.debug("Student confirmation sent")
        except SMTPException as error:
            app.logger.warning("SMTP ERROR\n%s"%error)

        spons_email = Message("RGV RSEF - Your student has registered")
        spons_email.html = render_template('email_student_confirmation.html',
                                    contact=sender, leader=leader,
                                    project=project)
        spons_email.add_recipient(leader.sponsor.email)
        try:
            mail.send(spons_email)
            app.logger.debug("Sponsor confirmation sent")
        except SMTPException as error:
            app.logger.warning("SMTP ERROR\n%s"%error)
