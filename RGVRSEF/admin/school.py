
from flask import render_template, url_for, flash, redirect, request
from flaskext.login import login_required

from . import admin
from .. import models
from . import forms as adminforms

@admin.route('/schools')
@login_required
def schools():
    district_narrow = request.args.get('district','')
    schools = models.School.query
    if district_narrow != '':
        schools = schools.filter_by(district_id=district_narrow)
    districts = models.District.query.all()
    
    return render_template('admin/schools.html',schools=schools,
                        district_narrow=district_narrow,
                        districts=districts)

@admin.route('/school/<int:id>', methods=["GET","POST"])
@login_required
def school(id):
    school_obj = models.School.query.get_or_404(id)
    school_form = adminforms.SchoolForm(obj=school_obj)
    school_form.district_id.choices = [(d.id,d.name) for d 
        in models.District.query.order_by('name')]
    if school_form.is_submitted():
        school_form.populate_obj(school_obj)
        models.db.session.commit()
        flash('School successfully updated.','info')
        return redirect(url_for('.schools'))
    return render_template('admin/school.html',form=school_form, id=id,
                        target=url_for('.school',id=id),school=school_obj)

@admin.route('/deleteschool/<int:id>', methods=["GET","POST"])
@login_required
def deleteschool(id):
    school_obj = models.School.query.get_or_404(id)
    models.db.session.delete(school_obj)
    models.db.session.commit()
    flash('School successfully deleted.','info')
    return redirect(url_for('.schools'))

@admin.route('/newschool', methods=["GET","POST"])
@login_required
def newschool():
    school_form = adminforms.SchoolForm()
    school_form.district_id.choices = [(d.id,d.name) for d 
        in models.District.query.order_by('name')]
    if school_form.is_submitted():
        school_obj = models.School(school_form.name.data,
                school_form.phone.data, school_form.fax.data,
                school_form.district_id.data)
        models.db.session.add(school_obj)
        models.db.session.commit()
        flash('School successfully created.','info')
        return redirect(url_for('.schools'))
    return render_template('admin/school.html',form=school_form,
                            target=url_for('.newschool'))
