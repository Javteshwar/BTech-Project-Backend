class Doctor:
    uid = int
    email = str
    password = str
    name = str
    phone = str
    specialization = str

    def __init__(self, uid=-1,  email='', name='', phone='', specialization=''):
        self.uid = uid
        self.email = email
        self.name = name
        self.phone = phone
        self.specialization = specialization
