
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

