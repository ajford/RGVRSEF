from os import environ
from flask import json

SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL',None)

SECRET_KEY = environ.get('SECRET_KEY',None)
SIGNING_KEY = environ.get('SIGNING_KEY',None)
SIGNING_MAX_AGE = environ.get('SIGNING_MAX_AGE',1800)
DEVELOPMENT = bool(environ.get('DEVELOPMENT',False))
TESTING = bool(environ.get('TESTING',False))
DEBUG = bool(environ.get('DEBUG',False))
GOOGLE_ANALYTICS = environ.get('GOOGLE_ANALYTICS',None)

TITLE = "RGV Regional Science and Engineering Fair"
YEAR = environ.get('YEAR',None)
CONTACTS = json.loads(environ.get('CONTACTS',
            '''[{"phone": "1235436789", "title": "Example Title", "email":
            "contact@example.com", "name": "Contact Person"}, {"phone":
            "1235436789", "title": "Example Title", "email" :
            "contact@example.com", "name": "Contact 2"}]'''
        ))
WEBMASTER = json.loads(environ.get('WEBMASTER',
        '''{"phone": "1235436789", "email": "Webmaster@example.com", "name":
        "Webmaster"}'''
        ))

STUDENT_ACTIVE = bool(environ.get('STUDENT_ACTIVE',False))

# Mail settings
MAIL_SERVER = environ.get('MAIL_SERVER',None)
MAIL_PORT = int(environ.get('MAIL_PORT',None))
MAIL_USERNAME = environ.get('MAIL_USERNAME',None)
MAIL_PASSWORD = environ.get('MAIL_PASSWORD',None)
MAIL_FAIL_SILENTLY = bool(environ.get('MAIL_FAIL_SILENTLY',True))
DEFAULT_MAIL_SENDER = environ.get('DEFAULT_MAIL_SENDER',None)

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
