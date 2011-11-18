TODO
====

Models
------

Models are defined. Need some testing and review for logic and good sense.

Models are:
* Student
* Project
* Sponsor
* Category
* School
* District

Relations:
* School -> District (Many to One)
* Student -> School (Many to One)
* Student -> Sponsor (Many to One)
* Student -> Project (Many to One)
* Project -> Category (Many to One)

Basic run though of registration process within a python shell might reveal
any logic problems with the current layout. Are the relations over-constrained? 



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

