
from flask import render_template, url_for, flash, redirect, request
from flaskext.login import login_required

from . import admin
from . import forms as adminforms
from .. import forms as mainforms
from .. import models

@admin.route('/sponsors')
@login_required
def sponsors():
    district_narrow = request.args.get('district','')
    sponsors = models.Sponsor.query.order_by('lastname')
    if district_narrow != '':
        sponsors = sponsors.join(School).filter_by(district_id=district_narrow)
    districts = models.District.query.all()
    
    return render_template('admin/sponsors.html',sponsors=sponsors,
                        district_narrow=district_narrow,
                        districts=districts)

@admin.route('/sponsor/<int:id>', methods=['GET','POST'])
@login_required
def sponsor(id):
    sponsor = models.Sponsor.query.get(id)
    form = mainforms.SponsorForm(obj=sponsor)
    form.password.validators = []
    form.confirm.validators = []
    query = models.School.query.order_by(models.School.name)
    form.school_id.choices=[(x.id,"%s - %s"%(x.name,x.district.name)) 
                            for x in query.all()]
    if form.validate_on_submit():
        form.populate_obj(sponsor)
        models.db.session.commit()
        flash("Sponsor Updated")
        return redirect(url_for('.sponsors'))

    students = sponsor.students.filter(models.Student.team_leader==True).all()
    return render_template('admin/sponsor.html',form=form,id=id,
                            sponsor=sponsor, students=students)

@admin.route('/deletesponsor/<int:id>', methods=["GET","POST"])
@login_required
def deletesponsor(id):
    sponsor_obj = models.Sponsor.query.get_or_404(id)
    models.db.session.delete(sponsor_obj)
    models.db.session.commit()
    flash('Sponsor successfully deleted.','info')
    return redirect(url_for('.sponsors'))

