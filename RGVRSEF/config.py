from os import environ

from RGVRSEF import json

try: 
    from bundle_config import config
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s'%(
                config['postgres']['username'],
                config['postgres']['password'],
                config['postgres']['host'],
                config['postgres']['database'])
except ImportError:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rgvrsef.db'

SECRET_KEY = 'developmentKey'
DEVELOPMENT = True
TESTING = False
DEBUG = False

TITLE = "RGV Regional Science and Engineering Fair"
YEAR = "2012"
CONTACT = json.loads(environ.get("CONTACT"))
WEBMASTER = json.loads(environ.get("WEBMASTER"))

STUDENT_ACTIVE = False

# Mail settings
MAIL_SERVER = environ.get("MAIL_SERVER")
MAIL_PORT = environ.get("MAIL_PORT")
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
DEFAULT_MAIL_SENDER = environ.get("DEFAULT_MAIL_SENDER")

# Category settings
CATEGORIES = (  ("Animal Science",False),
                ("Behavioral and Social Science",False),
                ("Biochemistry",False),
                ("Cellular and Molecular Biology",False),
                ("Chemistry",False),
                ("Computer Science",False),
                ("Earth and Planetary Science",False),
                ("Engineering: Electrical and Mechanical",False),
                ("Engineering: Materials and Bioengineering",False),
                ("Energy and Transportation",False),
                ("Environmental Management",False),
                ("Environmental Sciences",False),
                ("Mathematical Sciences",False),
                ("Medicine and Health Sciences",False),
                ("Microbiology",False),
                ("Physics and Astronomy",False),
                ("Plant Sciences",False))
