from flask.json import jsonify
from controller.appointmentehr import *
from controller.authehr import Authenticate
from controller.patientehr import PatientList, PatientApi
from controller.doctorehr import DoctorList, DoctorApi
from controller.form import Form
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Check(Resource):
    def get(self):
        return 'Hello'


api.add_resource(PatientList, '/api/patients/')
api.add_resource(PatientApi, '/api/patients/user/')
api.add_resource(Authenticate, '/api/login/')
api.add_resource(DoctorList, '/api/doctors/')
api.add_resource(DoctorApi, '/api/doctors/user/')
api.add_resource(AppointmentPatient, '/api/patients/appointment/')
api.add_resource(AppointmentArchivePatient,
                 '/api/patients/appointment/archive/')
api.add_resource(AppointmentDoctor, '/api/doctors/appointment/')
api.add_resource(CurrentAppointment, '/api/doctors/current_appointment/')
api.add_resource(AppointmentArchiveDoctor, '/api/doctors/appointment/archive/')
api.add_resource(Form, '/api/form/')
api.add_resource(Check, '/test/')


if __name__ == '__main__':
    app.run(debug=True)
