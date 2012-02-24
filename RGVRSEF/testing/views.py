from pprint import pformat

from flask import redirect, render_template, url_for, make_response,session

from .. import app
from .. import utils

@app.route('/testing/session')
def test_session_view():
    return render_template('premessage.html',message=pformat(vars(session)))

@app.route('/testing/session/clear')
def test_session_clear():
    utils.clear()
    return redirect(url_for('test_session_view'))
