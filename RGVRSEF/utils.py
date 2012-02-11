from hashlib import sha256
from datetime import date
from smtplib import SMTPException
from StringIO import StringIO
from csv import DictWriter

#import xlwt

from flask import (Flask, make_response,redirect, url_for,
                    render_template,json,request,flash,session)

from RGVRSEF import app, mail, Message
import RGVRSEF.models as models

CSV_FIELDS = ['Student 1','Student 2', 'Student 3', 'Project Title',
                  'School','District','Sponsor Name']

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
                record = {CSV_FIELDS[0]: "%s %s"%(student.firstname,
                                                student.lastname),
                          CSV_FIELDS[3]: student.project.title,
                          CSV_FIELDS[4]: student.school.name,
                          CSV_FIELDS[5]: student.school.district.name,
                          CSV_FIELDS[6]: "%s %s"%(student.sponsor.firstname,
                                                student.sponsor.lastname)}
                team = student.project.student
                team = team.filter(models.Student.team_leader==False).limit(2)
                team = team.all()
                i = 1
                for student in team:
                    record[CSV_FIELDS[i]]= "%s %s"%(student.firstname,
                                                    student.lastname)
                    i += 1 

                writer.writerow(record)

    return f.getvalue()

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

