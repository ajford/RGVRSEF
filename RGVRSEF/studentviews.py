
from flask import render_template,url_for,redirect

from . import app, models, forms 
from . import tasks
from . import utils

@app.route('/reg/student/sponsorcode',methods=['GET','POST'])
def studentreg1():
    if not app.config['STUDENT_ACTIVE']:
        return render_template('message.html',
                            message="Student Registration is currently closed")
    form=forms.StudentSponsorForm()
    if form.validate_on_submit():
        sponsor_id = decode(form.sponsor_id.data)
        sponsor = models.Sponsor.query.get(sponsor_id)
        if sponsor:
            finished = utils.retrieve('finished')
            utils.store(sponsor_id=sponsor.id)
            return redirect(url_for('studentreg2'))            
        else:
            message = "This Sponsor ID is invalid. \
                    Please verify and reneter."
            return render_template("studentreg1.html",form=form,
                        message=message)
    return render_template("studentreg1.html",form=form, 
                    endpoint=url_for('studentreg1'))

@app.route('/reg/student/code',methods=['GET','POST'])
def studentbackdoor():
    form=forms.StudentSponsorForm()
    if form.validate_on_submit():
        sponsor_id = decode(form.sponsor_id.data)
        sponsor = models.Sponsor.query.get(sponsor_id)
        if sponsor:
            finished = utils.retrieve('finished')
            utils.store(sponsor_id=sponsor.id)
            return redirect(url_for('studentreg2'))            
        else:
            message = "This Sponsor ID is invalid. \
                    Please verify and reneter."
            return render_template("studentreg1.html",form=form,
                        message=message)
    return render_template("studentreg1.html",form=form, 
                    endpoint=url_for('studentbackdoor'))

@app.route('/reg/student/personalinfo',methods=['GET','POST'])
def studentreg2():
    utils.store(viewed=False)
    form=forms.StudentForm()
    if form.validate_on_submit():
        sponsor_id = utils.retrieve('sponsor_id')
        if sponsor_id is None:
            message = "Your session has expired. \
                    Please restart your registration"
            return render_template('message.html', message=message)
        if sponsor_id == SIG_EXPIRED:
            message = "Your session has expired. \
                    Please restart your registration"
            return render_template('message.html', message=message)
        student = models.Student()
        sponsor = models.Sponsor.query.get(sponsor_id)
        student.sponsor_id = sponsor.id
        student.school_id = sponsor.school_id
        student.team_leader = True
        form.populate_obj(student)
        utils.store(leader=student.serialize())
        utils.store(sponsor_id=sponsor.id)
        return redirect(url_for('studentreg3'))
    return render_template("studentreg2.html",form=form)

@app.route('/reg/student/projectinfo',methods=['GET','POST'])
def studentreg3():
    form=forms.ProjectForm()
    query=models.Category.query.order_by('id')
    form.category_id.choices=[(x.id,x.name) for x in query.all()]
    if form.validate_on_submit():
        project = models.Project()
        form.populate_obj(project)

        utils.store(project=project.serialize())
        utils.refresh('sponsor_id')
        utils.refresh('leader')
        if form.individual.data != 'True':
            return redirect(url_for('teammembers'))
        return redirect(url_for('studentreg4'))
    return render_template("studentreg3.html",form=form)

@app.route('/reg/student/teaminfo',methods=['GET','POST'])
def teammembers():
    form=forms.StudentBaseForm()
    team = utils.retrieve('team')
    if not team:
        team = []
    else:
        utils.store(team=team)


    if form.validate_on_submit():
        student = models.Student()
        form.populate_obj(student)

        team.append(student.serialize())

        utils.store(team=team)
        utils.refresh('sponsor_id')
        utils.refresh('leader')
        utils.refresh('project')
        
        return redirect(url_for('teammembers'))
    return render_template("team_members.html",form=form,team=team)

@app.route('/reg/student/forms',methods=['GET','POST'])
def studentreg4():
    form=forms.FormsForm()
    if form.validate_on_submit():
        forms = forms.Forms()
        form.populate_obj(forms)
        utils.store(forms=forms.serialize())
        utils.store(complete=True)
        utils.refresh('sponsor_id')
        utils.refresh('leader')
        utils.refresh('project')
        utils.refresh('team')
        return redirect(url_for('complete'))
    return render_template("forms.html",form=form)

@app.route('/reg/student/review',methods=['GET','POST'])
def complete():
    viewed = utils.retrieve('viewed')
    if viewed:
        message = ["Your confirmation page has been viewed already.",
            "If you do not recieve your confirmation email, please contact us"]
        utils.store(viewed=True)
        return render_template('message.html', message=message)
    
    complete = utils.retrieve('complete')
    if complete is None:
        message = ["Your registration is not marked as complete.",
                "If you think you've recieved this mesage in error,\
                please return to the previous page and try again."]
        return render_template('message.html', message=message)
    if complete == SIG_EXPIRED:
        message = "Your session has expired. \
                Please restart your registration"
        return render_template('message.html', message=message)


    sponosor_id = utils.retrieve('sponsor_id')
    sponsor = models.Sponsor.query.get(sponsor_id)

    project = models.Project()
    utils.populate(project,utils.retrieve('project'))
    project.school_id = sponsor.school.id
    models.db.session.add(project)
    models.db.session.commit()

    leader = models.Student()
    utils.populate(leader,utils.retrieve('student'))
    leader.project_id = project.id
    models.db.session.add(leader)
    models.db.session.commit()

    forms = models.Forms()
    utils.populate(forms,utils.retrieve('forms'))
    forms.project_id = project.id
    models.db.session.add(forms)
    models.db.session.commit()

    team = utils.retrieve('team')
    for member in team:
        student = models.Student()
        utils.populate(student,member)
        student.project_id = project.id
        student.sponsor_id = sponsor_id
        student.school_id = sponsor.school.id
        models.db.session.add(student)
        models.db.session.commit()

    tasks.project_reg_mail(project)

    if app.config['TESTING']:
        utils.store(student_id=leader_id)
    else:
        utils.store(finished=True)
    return render_template('complete.html', leader=leader)

