from datetime import date

from flask import render_template, url_for, flash, redirect, request
from flaskext.login import login_required

from . import admin
from .. import forms as mainforms
from .. import models
from . import forms as adminforms

@admin.route('/news')
@login_required
def news():
    #news = models.News.query.filter(News.date>=date.today())
    news = models.News.query.order_by('date').all()
    return render_template('admin/news.html',news=news)

@admin.route('/editnews/<int:id>', methods=["GET","POST"])
@login_required
def editnews(id):
    news_obj = models.News.query.get_or_404(id)
    news_form = adminforms.NewsForm(obj=news_obj)
    if news_form.is_submitted():
        news_form.populate_obj(news_obj)
        models.db.session.commit()
        flash('News successfully updated.','info')
        return redirect(url_for('.news'))
    return render_template('admin/editnews.html',form=news_form,
                            target=url_for('.editnews',id=id),id=id)

@admin.route('/deletenews/<int:id>', methods=["GET","POST"])
@login_required
def deletenews(id):
    news_obj = models.News.query.get_or_404(id)
    models.db.session.delete(news_obj)
    models.db.session.commit()
    flash('News successfully deleted.','info')
    return redirect(url_for('.news'))

@admin.route('/newnews', methods=["GET","POST"])
@login_required
def newnews():
    news_form = adminforms.NewsForm()
    date_obj = date.today()
    if news_form.is_submitted():
        news_obj = models.News(news_form.title.data,news_form.text.data,
                        news_form.date.data)
        models.db.session.add(news_obj)
        models.db.session.commit()
        flash('News successfully created.','info')
        return redirect(url_for('.news'))
    return render_template('admin/editnews.html',form=news_form,
                            target=url_for('.newnews'),today=date_obj)

