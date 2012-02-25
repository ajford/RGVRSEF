from datetime import date

from flask import render_template, url_for, flash, redirect
from flaskext.login import login_required

from . import admin
from .. import forms as mainforms
from .. import models
from . import forms as adminforms

@admin.route('/deadlines')
@login_required
def deadlines():
    deadlines = models.Deadline.query.order_by('date').all()
    return render_template('admin/deadlines.html',deadlines=deadlines)

@admin.route('/deadline/<int:id>', methods=["GET","POST"])
@login_required
def deadline(id):
    date_obj = date.today()
    deadline_obj = models.Deadline.query.get_or_404(id)
    deadline_form = adminforms.DeadlineForm(obj=deadline_obj)
    if deadline_form.is_submitted():
        deadline_form.populate_obj(deadline_obj)
        models.db.session.commit()
        flash('Deadline successfully updated.','info')
        return redirect(url_for('.deadlines'))
    return render_template('admin/deadline.html',form=deadline_form,
                            target=url_for('.deadline',id=id),id=id)

@admin.route('/deletedeadline/<int:id>', methods=["GET","POST"])
@login_required
def deletedeadline(id):
    deadline_obj = models.Deadline.query.get_or_404(id)
    models.db.session.delete(deadline_obj)
    models.db.session.commit()
    flash('Deadline successfully deleted.','info')
    return redirect(url_for('.deadlines'))

@admin.route('/newdeadline', methods=["GET","POST"])
@login_required
def newdeadline():
    deadline_form = adminforms.DeadlineForm()
    if deadline_form.is_submitted():
        deadline_obj = models.Deadline(deadline_form.text.data,
                        deadline_form.date.data)
        models.db.session.add(deadline_obj)
        models.db.session.commit()
        flash('Deadline successfully created.','info')
        return redirect(url_for('.deadlines'))
    return render_template('admin/deadline.html',form=deadline_form,
                            target=url_for('.newdeadline'))

