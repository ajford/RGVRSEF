from bundle_config import config

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s'%(
                config['postgres']['username'],
                config['postgres']['password'],
                config['postgres']['host'],
                config['postgres']['database'])
SECRET_KEY = 'developmentKey'
CATEGORIES = (  ("Team Physical",1),
                ("Team Biological",1),
                ("Animal Science",0),
                ("Behavioral and Social Science",0),
                ("Biochemistry",0),
                ("Cellular and Molecular Biology",0),
                ("Chemistry",0),
                ("Computer Science",0),
                ("Earth and Planetary Science",0),
                ("Engineering: Electrical and Mechanical",0),
                ("Engineering: Materials and Bioengineering",0),
                ("Energy and Transportation",0),
                ("Environmental Management",0),
                ("Environmental Sciences",0),
                ("Mathematical Sciences",0),
                ("Medicine and Health Sciences",0),
                ("Microbiology",0),
                ("Physics &amp; Astronomy",0),
                ("Plant Sciences",0))
