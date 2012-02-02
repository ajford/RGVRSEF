from os import environ

try: 
    from bundle_config import config
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s'%(
                config['postgres']['username'],
                config['postgres']['password'],
                config['postgres']['host'],
                config['postgres']['database'])
except ImportError:
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_URI',
                                    'sqlite:///rgvrsef.db')

SECRET_KEY = 'developmentKey'
SIGNING_KEY = 'signingKey'
SIGNING_MAX_AGE = 18000 
DEVELOPMENT = True
TESTING = False
DEBUG = True

TITLE = "RGV Regional Science and Engineering Fair"
YEAR = "2012"
CONTACT = {'email':'contact@example.com','phone':'1235436789',
            'name':'Contact Person'}
WEBMASTER = {'email':'Webmaster@example.com','phone':'1235436789',
        'name':'Webmaster'}

STUDENT_ACTIVE = True

# Mail settings
MAIL_SERVER = "mail.example.com"
MAIL_PORT = 25
MAIL_USERNAME = "TEST"
MAIL_PASSWORD = "Wouldn't You Like To Know"
MAIL_FAIL_SILENTLY = False
DEFAULT_MAIL_SENDER = "test@example.com"

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
