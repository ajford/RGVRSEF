from tempfile import TemporaryFile
from csv import DictReader
import subprocess 
from datetime import date,timedelta

from flaskext.script import Manager,Server
from main import app
from models import *

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
    models.db.drop_all()
    print 'Database dropped'

@manager.command
def builddb():
    models.db.create_all()
    print 'Blank database created'

if __name__ == '__main__':
    manager.run()
