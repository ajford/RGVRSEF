from pprint import pformat

from flask import redirect, render_template, url_for, make_response,session

from .. import app
from .. import models
from .. import utils

@app.route('/testing/session')
def test_session_view():
    return render_template('premessage.html',message=pformat(vars(session)))

@app.route('/testing/session/clear')
def test_session_clear():
    utils.clear()
    return redirect(url_for('test_session_view'))


@app.route('/testing/projectreview/<int:id>',methods=['GET'])
def test_project_review(id):
    project = models.Project.query.get_or_404(id)
    
    leader = project.student.filter(models.Student.team_leader==True).first()
    return render_template('complete.html', leader=leader)
