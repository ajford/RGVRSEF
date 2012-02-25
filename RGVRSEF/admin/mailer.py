
from flask import render_template, url_for, flash, redirect, request
from flaskext.login import login_required

from . import admin
from . import forms as adminforms
from .. import forms as mainforms
from .. import models
from .. import tasks
from .. import utils
from .. import mail, Message

@admin.route('/mailer', methods=['POST','GET'])
@login_required
def mailer():
    form = adminforms.MailForm()
    if form.validate_on_submit():
        tasks.mail(form.to.data,form.message.data,form.subject.data)
        return render_template('admin/message.html',message="Mail Sent.")
    return render_template('admin/mail.html',form=form)

@admin.route('/mailer/confirmation/sponsor/<int:id>')
@login_required
def sponsorconf(id):
    sponsor = models.Sponsor.query.get_or_404(id)
    tasks.sponsor_mail(sponsor)
    message = "Confirmation resent to %s, %s <%s>"%(sponsor.lastname,
                            sponsor.firstname,sponsor.email)
    return render_template('admin/message.html',message=message)

@admin.route('/mailer/confirmation/project/<int:id>')
@login_required
def projectconf(id):
    project = models.Project.query.get_or_404(id)
    tasks.project_reg_mail(project)
    message = "Confirmation resent about project #%s, %s"%(project.id,
                                    project.title)
    return render_template('admin/message.html',message=message)

