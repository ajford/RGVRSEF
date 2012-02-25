
from flask import render_template, url_for, flash, redirect, request
from flaskext.login import login_required

from . import admin
from .. import forms as mainforms
from .. import models
from . import forms as adminforms

@admin.route('/districts')
@login_required
def districts():
    districts = models.District.query.all()
    return render_template('admin/districts.html',districts=districts)

@admin.route('/district/<int:id>', methods=["GET","POST"])
@login_required
def district(id):
    district_obj = models.District.query.get_or_404(id)
    district_form = adminforms.DistrictForm(obj=district_obj)
    if request.method == "GET":
        return render_template('admin/district.html',form=district_form,
                                target=url_for('.district',id=id),id=id,
                                schools=district_obj.schools)
    else:
        district_form.populate_obj(district_obj)
        models.db.session.commit()
        flash('District successfully updated.','info')
        return redirect(url_for('.districts'))

@admin.route('/deletedistrict/<int:id>', methods=["GET","POST"])
@login_required
def deletedistrict(id):
    district_obj = models.District.query.get_or_404(id)
    models.db.session.delete(district_obj)
    models.db.session.commit()
    flash('District successfully deleted.','info')
    return redirect(url_for('.districts'))

@admin.route('/newdistrict', methods=["GET","POST"])
@login_required
def newdistrict():
    district_form = adminforms.DistrictForm()
    if request.method == "GET":
        return render_template('admin/district.html',form=district_form,
                                target=url_for('.newdistrict'))
    else:
        district_obj = models.District(district_form.name.data)
        models.db.session.add(district_obj)
        models.db.session.commit()
        flash('District successfully created.','info')
        return redirect(url_for('.districts'))

