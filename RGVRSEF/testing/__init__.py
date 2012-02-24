from RGVRSEF import models

class DummyDistrict(object):
    id = 789
    name = "Springfield ISD"

class DummySchool(object):
    id = 123
    name = "Memorial HS"
    district = DummyDistrict()

class DummySponsor(object):
    id = 1001
    firstname = "John"
    lastname = "Doe"
    phone = "1234567890"
    email = "JDoe@example.com"
    school = DummySchool()

class DummyCategory(object):
    id = 1
    name = "Physics"

class DummyProject(object):
    id = 1001
    title = "Potato Battery"
    category=DummyCategory()
    division = "jr"
    table = False
    electricity = False

class DummyStudent(object):
    id = 1001
    firstname = "John"
    lastname = "Doe"
    email = "JDoe@example.com"
    grade = 6
    gender = "Male"
    project = DummyProject()
    sponsor = DummySponsor()
    school = DummySchool()

def populate_test_db():
    district = models.District("UT System")
    models.db.session.add(district)
    models.db.session.commit()
    print "District 'UT System' added"
    school = models.School('ARCC','9568828810','9568826779',district.id)
    models.db.session.add(school)
    models.db.session.commit()
    print "School 'ARCC' added"
    sponsor = models.Sponsor()
    sponsor.firstname = "John"
    sponsor.lastname = "Doe"
    sponsor.phone = "1234567890"
    sponsor.email = "JDoe@example.com"
    sponsor.school_id = school.id
    models.db.session.add(sponsor)
    models.db.session.commit()
    print "Sponsor 'Doe,John' added"

