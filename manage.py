from tempfile import TemporaryFile
from csv import DictReader
import subprocess 
from datetime import date,timedelta
from hashlib import sha256

from flaskext.script import Manager,Server,Shell,prompt_pass,prompt,prompt_bool
from sqlalchemy.exc import ProgrammingError

from RGVRSEF import app
import RGVRSEF.models as models
import RGVRSEF.admin.models as admin_models
import RGVRSEF.utils as utils
import RGVRSEF.tasks as tasks

manager = Manager(app)
manager.add_command("runserver", Server())

def password_valid():
    """ Prompts for root admin password and checks against db """
    passwd = sha256(prompt_pass("Please enter admin password")).hexdigest()
    try:
        admin = admin_models.Admin.query
        if admin.count() < 1:
            print "No Admins exist. Dropping DB."
            return True

        admin = admin.filter_by(username='root').first()
    except ProgrammingError as progerror:
        if progerror.args[0].find('relation "admin" does not exist'):
            print "DB does not exist. Dropping just in case"
            admin_models.db.session.close_all()
            return True
        else:
            return False

    if passwd == admin.password:
        admin_models.db.session.close_all()
        return True
    else:
        print "Invalid Password"
        return False

def _make_context():
    return dict(app=app, models=models, admin_models=admin_models,
                ctx=app.test_request_context(),utils=utils,tasks=tasks)

try:
    manager.add_command("shell", Shell(use_bpython=True,
                        make_context=_make_context))
except TypeError:
    manager.add_command("shell", Shell(make_context=_make_context))


@manager.command
def testvals():
    """ Management function to create test DB. Requires root admin access. """
    if prompt_bool("Are you sure you want to loose all data?"):
        if password_valid():
            try:
                from RGVRSEF import testing
            except ImportError:
                print "Unable to load module 'testing' from RGVRSEF\
                      required to build test db"
                return 1
            models.db.drop_all()
            testing.populate_test_db() 
            print "Test values populated"
        else:
            print 'Database operation aborted.'

@manager.command
def dropdb():
    """ Management function to drob DB. Requires root admin access. """
    if prompt_bool("Are you sure you want to loose all data?"):
        if password_valid(): 
            models.db.drop_all()
            print 'Database dropped'
        else:
            print 'Database operation aborted.'

@manager.command
def builddb():
    """ Management function to create the required DB. """ 
    models.db.create_all()
    print 'Blank database created'
    passwd = None
    while passwd is None:
        passwd = prompt_pass("Please enter primary admin password")
        passwd_confirm = prompt_pass("Please confirm password")
        if passwd != passwd_confirm:
            print "Passwords do not match."
            passwd = None
    models.db.session.add(admin_models.Admin('root',passwd,True))
    models.db.session.commit()

@manager.command
def addnewtables():
    """ Management function. Runs create_all to add any newly added models"""
    if password_valid():
        models.db.create_all()

def admin():
    """ Management function to add admins. """
    if password_valid(): 
        username = None
        while username is None:
            username = prompt("Please enter new admin username")
        passwd = None
        while passwd is None:
            passwd = prompt_pass("Please enter password for user '%s'"%username)
            passwd_confirm = prompt_pass("Please confirm password")
            if passwd != passwd_confirm:
                print "Passwords do not match."
                passwd = None
        models.db.session.add(admin_models.Admin(username,passwd,True))
        models.db.session.commit()
    else:
        print "Admin creation aborted"

@manager.command
def deladmin():
    """ Management function to delete admins. """
    if password_valid(): 
        username = None
        while username is None:
            username = prompt("Please enter admin username").strip()
        user = admin_models.Admin.query.filter_by(username=username).first()
        if user:
            if prompt_bool("Are you sure you want to delete user %s"%user.name):
                models.db.session.delete(user)
                models.db.session.commit()
                print "User %s successfully deleted"%username
        else:
            print "User does not exist"

@manager.command
def categories():
    """ Management function to import categories. 
    At the moment, only takes a list of two-tuples from the app config variable
    'CATEGORIES'. The structure of the two-tuple is ('Cat. Name',[True/False]),
    where the second value is True if the category is a team category, false
    otherwise.
    """ 
    if password_valid():
        for category in app.config['CATEGORIES']:
            cat = models.Category(category[0],category[1])
            models.db.session.add(cat)
        models.db.session.commit()
        print "Categories successully added."
    else:
        print "Category import aborted."



if __name__ == '__main__':
    manager.run()
