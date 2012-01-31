
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
