TODO
====

Models
------

Need to define models.

    Probable models:

    * Student
    * Project
        - foreign key to Student(s)

    Possible Others:

    * School
    * District

Views
-----

Views needed:

    * Index
        - Give deadlines (Registration, hardcopy submission)
        - List needed info and ask if ready to start registration
    * Registration
        - One page? Multiple?
        - Register student first, then add project? Would allow continuation.
    * Administration
        - Allow downloading of DB in CSV format
        - Allow deletion of project

Possible Others:

    * Statistics 
        - Number of entrants by category,grade,etc. 

Templates
---------

*Note:Templates should be designed using divs and CSS.*

Templates should be based off ``layout.html`` in ``templates/``. Further layout
work will be done in ``layout.html``, as well as via CSS. Macros should be added
to ``macros.html`` and imported. 

Needed templates:

    * Index
    * Registration
    * Administration

CSS needed to complement the templates. 

