class Patient:
    uid = int
    email = str
    password = str
    name = str
    gender = str
    age = int
    phone = str

    def __init__(self, uid=-1, email='', name='', gender='', age=-1, phone=''):
        self.uid = uid
        self.email = email
        self.name = name
        self.gender = gender
        self.age = age
        self.phone = phone
