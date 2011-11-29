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

@manager.command
def testdb():
    try:
        import test_rgvrsef
    except ImportError:
        print "Unable to load module 'test_rgvrsef' required to build test db"
        return 1
    test_rgvrsef.build_and_populate()
    print "Test database created and populated"

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to loose all data?"):
        passwd = sha256(prompt_pass("Please enter admin password")).hexdigest()
        if passwd == admin_models.Admin.query.filter_by(username='root').\
                        first().password:
            models.db.drop_all()
            print 'Database dropped'
        else:
            print 'Invalid Password. Database operation aborted.'

@manager.command
def builddb():
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
def admin():
    rootpasswd = sha256(prompt_pass("Please enter admin password")).hexdigest()
    if rootpasswd == admin_models.Admin.query.filter_by(username='root').\
                    first().password:
        username = None
        while username is None:
            username = prompt("Please enter new admin username")
        passwd = None
        while passwd is None:
            passwd = prompt_pass("Please enter new admin password")
            passwd_confirm = prompt_pass("Please confirm password")
            if passwd != passwd_confirm:
                print "Passwords do not match."
                passwd = None
        models.db.session.add(admin_models.Admin(username,passwd,True))
        models.db.session.commit()



if __name__ == '__main__':
    manager.run()
