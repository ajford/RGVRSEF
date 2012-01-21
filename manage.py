from tempfile import TemporaryFile
from csv import DictReader
import subprocess 
from datetime import date,timedelta
from hashlib import sha256

from flaskext.script import Manager,Server,prompt_pass,prompt,prompt_bool
from RGVRSEF import app
import RGVRSEF.models as models
import RGVRSEF.admin.models as admin_models

manager = Manager(app)
manager.add_command("runserver", Server())

def password_valid():
    passwd = sha256(prompt_pass("Please enter admin password")).hexdigest()
    admin = admin_models.Admin.query.filter_by(username='root').first()
    if admin is None:
        return True
    if passwd == admin.password:
        return True
    else:
        print "Invalid Password"
        return False


# Build Test DB
@manager.command
def testdb():
    """ Management function to create test DB. Requires root admin access. """
    if prompt_bool("Are you sure you want to loose all data?"):
        if password_valid():
            try:
                import test_rgvrsef
            except ImportError:
                print "Unable to load module 'test_rgvrsef' \
                      required to build test db"
                return 1
            test_rgvrsef.build_and_populate()
            print "Test database created and populated"
        else:
            print 'Database operation aborted.'

# Drop DB
@manager.command
def dropdb():
    """ Management function to drob DB. Requires root admin access. """
    if prompt_bool("Are you sure you want to loose all data?"):
        if password_valid(): 
            models.db.drop_all()
            print 'Database dropped'
        else:
            print 'Database operation aborted.'

# Build DB
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

# sponspad 
@manager.command
def sponspad():
   padding = models.Sponsor()
   padding.id = 1000
   padding.firstname = 'PAD'
   padding.lastname = 'PAD'
   models.db.session.add(padding)
   modesl.db.session.commit()

# Add Admin
@manager.command
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

# Delete Admin
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
        else:
            print "User does not exist"

# Add Categories
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
