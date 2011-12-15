TODO
====

Models
------

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


Views
-----

Views needed:

    * Index

        - Give deadlines (Registration, hardcopy submission)
        - List needed info and ask if ready to start registration

    * Registration

        - One page? Multiple?
        - Register student
        - Project Info
        - Paperwork Info

    * Administration

        - /
        - /deadlines
        - /projects
        - /news


Possible Others:

    * Statistics 
        - Number of entrants by category,grade,etc. 

Templates
---------

*Note:Templates should be designed using divs and CSS.*

Templates should be based off ``layout.html`` in ``templates/``. Further layout
work will be done in ``layout.html``, as well as via CSS. Macros should be added
to ``macros.html`` and imported. 

CSS needed to complement the templates. 

