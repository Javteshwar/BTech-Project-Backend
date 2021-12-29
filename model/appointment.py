class Appointment:
    uid = str
    patient_uid = str
    doctor_uid = str
    status = str
    date = str
    time = str

    def __init__(self, uid='', patient_uid='', doctor_uid='', status='', date='', time=''):
        self.uid = uid
        self.patient_uid = patient_uid
        self.doctor_uid = doctor_uid
        self.status = status
        self.date = date
        self.time = time
