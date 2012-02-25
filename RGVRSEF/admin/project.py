
from flask import render_template, url_for, flash, redirect, request
from flaskext.login import login_required

from . import admin
from .. import forms as mainforms
from .. import models
from . import forms as adminforms

@admin.route('/projects')
@login_required
def projects():
    div = request.args.get('division',None)
    cat = request.args.get('category',None,type=int)
    district = request.args.get('district',None,type=int)
    categories = models.Category.query.order_by('name').all()
    districts = models.District.query.order_by('name').all()
    projects = models.Project.query.order_by('title')
    if request.args.get('category',None): 
        projects = projects.filter_by(category_id = request.args['category']) 
    if request.args.get('division',None):
        projects = projects.filter_by(division = request.args['division']) 
    if request.args.get('district',None):
        projects = projects.join(Student).join(School)
        projects = projects.filter(School.district_id == district)
    projects = projects.all()
    return render_template('admin/projects.html', projects=projects, 
                            categories=categories,districts=districts,
                            endpoint='.projects',
                            div_narrow=div,cat_narrow=cat,
                            dist_narrow=district)

@admin.route('/project/<int:id>', methods=['GET','POST'])
@login_required
def project(id):
    project = models.Project.query.get_or_404(id)
    leader = project.student.filter(models.Student.team_leader==True).first()
    form = mainforms.ProjectForm(obj=project)
    if form.validate_on_submit():
        form.populate_obj(project)
        models.db.session.commit()
        return redirect(url_for('.projects'))
    return render_template('admin/project.html',form=form, id=id,
                            project=project, leader=leader)

@admin.route('/deleteproject/<int:id>', methods=["GET","POST"])
@login_required
def deleteproject(id):
    project = models.Project.query.get_or_404(id)
    forms = project.forms.all()
    for form in forms:
        models.db.session.delete(form)
    students = project.student.all()
    for student in students:
        models.db.session.delete(student)
    models.db.session.delete(project)
    models.db.session.commit()
    flash('Project successfully deleted.','info')
    return redirect(url_for('.projects'))

@admin.route('/forms/<int:id>', methods=['GET','POST'])
@login_required
def formedit(id):
    forms = models.Forms.query.get_or_404(id)
    form = mainforms.FormsForm(obj=forms)
    if form.validate_on_submit():
        form.populate_obj(forms)
        models.db.session.commit()
        return redirect(url_for('.project',id=forms.project_id))
    return render_template('admin/forms.html',form=form, id=id,
                            forms=forms)

@admin.route('/student/<int:id>',methods=['GET','POST'])
@login_required
def studentedit(id):
    student = models.Student.query.get_or_404(id)
    form = mainforms.StudentForm(obj=student)
    form.address.validators=[]
    form.city.validators=[]
    form.zip.validators=[]
    if form.validate_on_submit():
        form.populate_obj(student)
        models.db.session.commit()
        flash('Student successfully updated.','info')
        return redirect(url_for('.project',id=student.project_id))
    return render_template('admin/student.html',form=form, id=id,
                        student=student,proj_id=student.project_id,
                        endpoint=url_for('.studentedit',id=id))

@admin.route('/project/<int:id>/newstudent',methods=['GET','POST'])
@login_required
def newstudent(id):
    form = mainforms.StudentForm()
    form.address.validators=[]
    form.city.validators=[]
    form.zip.validators=[]
    if form.validate_on_submit():
        student = models.Student()
        student.project_id=id
        proj = models.Project.query.get_or_404(id)
        student.sponsor_id = proj.student.first().sponsor_id
        student.school_id = proj.school_id
        form.populate_obj(student)
        models.db.session.add(student)
        models.db.session.commit()
        flash('Student successfully created.','info')
        return redirect(url_for('.project',id=id))
    return render_template('admin/student.html',form=form, id=id,
                        endpoint=url_for('.newstudent',id=id))

    
@admin.route('/project/<int:proj_id>/deletestudent/<int:id>', 
                methods=["GET","POST"])
@login_required
def deletestudent(proj_id,id):
    student = models.Student.query.get_or_404(id)
    models.db.session.delete(student)
    models.db.session.commit()
    flash('Student successfully deleted.','info')
    return redirect(url_for('.project',id=proj_id))

