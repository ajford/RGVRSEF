RGV Regional Science and Engineering Fair
=========================================

## About ##

This is the registration site for the RGV Regional Science and Engineering Fair.

Based on [Flask][], [WTForms][] and [Flask-WTF][], [SQLAlchemy][] and
[Flask-SQLAlchemy][], [Flask-Script][], [Flask-Login][], [It's Dangerous][],
[Flask-Mail][] and a few other nuts and bolts.

We run this registration site on [epio][], and have included an epio.ini sample,
for those interested in running this there as well.

## Deployment ##

This site is deployable using any wsgi server interface. 

Simply running `python manage.py runserver` will get you a development server,
but for example, you can run the app in a near production ready mode via
[Gunicorn][] using `gunicorn -w 4 RGVRSEF:app` (assuming you have gunicorn
installed).

For some examples on flask deployment, see the flask documentation section
[Deployment Options][].

Again, we use epio for deployment, and for more on epio deployment of this app,
see `DEPLOYMENT.md`.

## Authors ##
This software is written by Anthony J. Ford and Alejandro Garcia.

## Licensing ##

This software is licensed under the '3-Clause BSD' license, and can be viewed in
the accompanying license file, `LICENSE`. This software is open source and free
to use and modify to suit your needs. The authors of this software would greatly
appreciate being notified if you use this software, especially if it is used to
support a local science fair.

All dependencies of this software are to be held to their own licenses, but at
the time of this writing they too are open source projects.




[Flask][http://flask.pocoo.org]
[WTForms][http://wtforms.simplecodes.com/]
[Flask-WTF][http://packages.python.org/Flask-WTF/]
[SQLAlchemy][http://www.sqlalchemy.org/]
[Flask-SQLAlchemy][http://packages.python.org/Flask-SQLAlchemy/]
[Flask-Script][http://packages.python.org/Flask-Script/]
[Flask-Login][http://packages.python.org/Flask-Login/]
[It's Dangerous][http://packages.python.org/itsdangerous/]
[Flask-Mail][http://packages.python.org/flask-mail/]
[epio][https://www.ep.io/]
[Gunicorn][http://gunicorn.org/]
[Deployment Options][http://flask.pocoo.org/docs/deploying/]
