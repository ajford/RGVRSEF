
from flask import render_template,url_for,redirect,request

from . import app, models, forms 
from . import tasks
from . import utils

@app.route('/reg/sponsor/district',methods=['GET','POST'])
def sponsordistrict():
    form=forms.SponsorDistrictForm()
    form.district_id.choices=[(x.id,x.name) for x in 
            models.District.query.order_by('name')]
    return render_template("district.html",form=form)

@app.route('/reg/sponsor',methods=['GET','POST'])
def sponsorreg():
    district_id = request.args.get('district_id',None)
    form = forms.SponsorForm(request.form)
    query = models.School.query.order_by('name')
    if district_id:
        query = query.filter_by(district_id=district_id)
    form.school_id.choices=[(x.id,x.name) for x in query.all()]
    if form.validate_on_submit():
        form.encrypt()
        sponsor=models.Sponsor()
        form.populate_obj(sponsor)
        models.db.session.add(sponsor)
        models.db.session.commit()
        tasks.sponsor_mail(sponsor)
        utils.store(sponsor_id=sponsor.id)
        return redirect(url_for('sponsorcomplete'))
    return render_template("sponsor.html",form=form)

@app.route('/reg/sponsor/complete')
def sponsorcomplete():
    sponsor_id = utils.retrieve('sponsor_id')
    if sponsor_id == utils.VIEWED:
        message = ["Your confirmation page has already been viewed.",
           "If you do not recieve your confirmation email, please contact us"]
        return render_template('message.html', message=message)
    sponsor = models.Sponsor.query.get_or_404(sponsor_id)
    utils.store(sponsor_id=utils.VIEWED)
    return render_template("sponsor_complete.html",sponsor=sponsor)


@app.route('/sponsor/review',methods=['GET','POST'])
def sponsor_review():
    form = forms.SponsorLoginForm()
    if form.validate_on_submit():
        form.encrypt()
        sponsid = decode(form.id.data)
        sponsor = models.Sponsor.query.get_or_404(sponsid)
        if form.password.data == sponsor.password:
            return render_template("sponsor_review.html",sponsor=sponsor)
        else:
            message = "Your login information is invalid."
            return render_template("sponsor_login.html",form=form, 
                                message=message)
    else:
        return render_template("sponsor_login.html",form=form)

