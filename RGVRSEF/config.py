from bundle_config import config

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s'%(
                config['postgres']['username'],
                config['postgres']['password'],
                config['postgres']['host'],
                config['postgres']['database'])
SECRET_KEY = 'developmentKey'
CATEGORIES = (  ("Team Physical",True),
                ("Team Biological",True),
                ("Animal Science",False),
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
