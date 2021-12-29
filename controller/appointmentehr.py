from datetime import date, timedelta
from flask import jsonify
import os
from reader.appointment import post_args, appointment_update_args
from flask_restful import Resource, abort
from flask import request
import psycopg2
import jwt
from dotenv import load_dotenv
load_dotenv('../.env')


class AppointmentPatient(Resource):
    def post(self):
        con = None
        args = post_args.parse_args()
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            query = "SELECT date, time from APPOINTMENT where doctor_uid=%s and date=%s and time=%s"
            cur.execute(query, (
                args['doctor_uid'], args['date'], args['time']
            ))
            if(len(cur.fetchall()) != 0):
                return jsonify(error=True, message='Doctor is busy at that time')
            query = "INSERT INTO APPOINTMENT (patient_uid,doctor_uid,status,date,time) values(%s,%s,%s,%s,%s)"
            values = (
                args['patient_uid'], args['doctor_uid'],
                args['status'], args['date'], args['time']
            )
            cur.execute(query, values)
            con.commit()
            return jsonify(error=False)
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return {'error': True, 'message': error.args}
        finally:
            if con is not None:
                cur.close()
                con.close()

    def get(self):
        authorizationHeader = request.headers.get('authorization')
        token = authorizationHeader.replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            os.getenv('AUTHSECRET'),
            algorithms=['HS256']
        )
        con = None
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            curDate = date.today()
            curDate -= timedelta(days=1)
            query = """select X.uid, X.doctor_uid, X.status, X.date, X.time, Y.name, Y.specialization from 
                    (
                        select A.uid, A.doctor_uid, A.status, A.date, A.time 
                        from appointment as A where A.patient_uid=%s and A.date>%s
                    ) X
                    join
                    (
                        select D.uid, D.name, D.specialization from doctor as D
                    ) Y
                    on X.doctor_uid=Y.uid order by X.date, X.time"""
            values = (decoded['uid'], str(curDate))
            cur.execute(query=query, vars=values)
            rows = cur.fetchall()
            todos = []
            for row in rows:
                todos.append({
                    'uid': row[0],  'doctor_uid': row[1], 'status': row[2],
                    'date': str(row[3]), 'time': str(row[4]), 'doctor_name': row[5],
                    'specialization': row[6],
                })
            con.close()
            cur.close()
            return jsonify(result=todos, error=False)
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return {'error': True, 'message': error.args}
        finally:
            if con is not None:
                cur.close()
                con.close()


class AppointmentDoctor(Resource):
    def put(self):
        authorizationHeader = request.headers.get('authorization')
        token = authorizationHeader.replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            os.getenv('AUTHSECRET'),
            algorithms=['HS256']
        )
        con = None
        args = appointment_update_args.parse_args()
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            query = "UPDATE APPOINTMENT SET status=%s where uid=%s and doctor_uid=%s"
            values = (args['status'], args['uid'], decoded['uid'])
            cur.execute(query, values)
            con.commit()
            return jsonify(error=False)
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return {'error': True, 'message': error.args}
        finally:
            if con is not None:
                cur.close()
                con.close()

    def get(self):
        con = None
        authorizationHeader = request.headers.get('authorization')
        token = authorizationHeader.replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            os.getenv('AUTHSECRET'),
            algorithms=['HS256']
        )
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            curDate = date.today()
            curDate -= timedelta(days=1)
            query = """select X.uid, X.patient_uid, X.status, X.date, X.time, Y.name, Y.age, Y.gender from 
                    (
                        select A.uid, A.patient_uid, A.status, A.date, A.time 
                        from appointment as A where A.doctor_uid=%s and A.date>%s
                    ) X
                    join
                    (
                        select P.uid, P.name, P.age, P.gender from patient as P
                    ) Y
                    on X.patient_uid=Y.uid order by X.date, X.time"""
            values = (decoded['uid'], str(curDate))
            cur.execute(query=query, vars=values)
            rows = cur.fetchall()
            todos = []
            for row in rows:
                todos.append({
                    'uid': row[0],  'patient_uid': row[1], 'status': row[2],
                    'date': str(row[3]), 'time': str(row[4]), 'patient_name': row[5],
                    'age': row[6], 'gender': row[7]
                })
            con.close()
            cur.close()
            return jsonify(result=todos, error=False)
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return {'error': True, 'message': error.args}
        finally:
            if con is not None:
                cur.close()
                con.close()


class AppointmentArchiveDoctor(Resource):
    def get(self):
        con = None
        authorizationHeader = request.headers.get('authorization')
        token = authorizationHeader.replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            os.getenv('AUTHSECRET'),
            algorithms=['HS256']
        )
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            curDate = date.today()
            query = """select X.uid, X.patient_uid, X.status, X.date, X.time, Y.name, Y.age, Y.gender from 
                    (
                        select A.uid, A.patient_uid, A.status, A.date, A.time 
                        from appointment as A where A.doctor_uid=%s and A.date<%s
                    ) X
                    join
                    (
                        select P.uid, P.name, P.age, P.gender from patient as P
                    ) Y
                    on X.patient_uid=Y.uid order by X.date, X.time"""
            values = (decoded['uid'], str(curDate))
            cur.execute(query=query, vars=values)
            rows = cur.fetchall()
            todos = []
            for row in rows:
                todos.append({
                    'uid': row[0],  'patient_uid': row[1], 'status': row[2],
                    'date': str(row[3]), 'time': str(row[4]), 'patient_name': row[5],
                    'age': row[6], 'gender': row[7]
                })
            con.close()
            cur.close()
            return jsonify(result=todos, error=False)
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return {'error': True, 'message': error.args}
        finally:
            if con is not None:
                cur.close()
                con.close()


class AppointmentArchivePatient(Resource):
    def get(self):
        authorizationHeader = request.headers.get('authorization')
        token = authorizationHeader.replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            os.getenv('AUTHSECRET'),
            algorithms=['HS256']
        )
        con = None
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            curDate = date.today()
            query = """select X.uid, X.doctor_uid, X.status, X.date, X.time, Y.name, Y.specialization from 
                    (
                        select A.uid, A.doctor_uid, A.status, A.date, A.time 
                        from appointment as A where A.patient_uid=%s and A.date<%s
                    ) X
                    join
                    (
                        select D.uid, D.name, D.specialization from doctor as D
                    ) Y
                    on X.doctor_uid=Y.uid order by X.date, X.time"""
            values = (decoded['uid'], str(curDate))
            cur.execute(query=query, vars=values)
            rows = cur.fetchall()
            todos = []
            for row in rows:
                todos.append({
                    'uid': row[0],  'doctor_uid': row[1], 'status': row[2],
                    'date': str(row[3]), 'time': str(row[4]), 'doctor_name': row[5],
                    'specialization': row[6],
                })
            con.close()
            cur.close()
            return jsonify(result=todos, error=False)
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return {'error': True, 'message': error.args}
        finally:
            if con is not None:
                cur.close()
                con.close()


class CurrentAppointment(Resource):
    def get(self):
        con = None
        authorizationHeader = request.headers.get('authorization')
        token = authorizationHeader.replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            os.getenv('AUTHSECRET'),
            algorithms=['HS256']
        )
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            curDate = date.today()
            query = """select X.uid, X.patient_uid, X.status, X.date, X.time, Y.name, Y.age, Y.gender from 
                    (
                        select A.uid, A.patient_uid, A.status, A.date, A.time 
                        from appointment as A where A.doctor_uid=%s and A.date>=%s and A.status='accepted'
                    ) X
                    join
                    (
                        select P.uid, P.name, P.age, P.gender from patient as P
                    ) Y
                    on X.patient_uid=Y.uid order by X.date, X.time"""
            values = (decoded['uid'], str(curDate))
            cur.execute(query=query, vars=values)
            rows = cur.fetchall()
            todos = []
            for row in rows:
                todos.append({
                    'uid': row[0],  'patient_uid': row[1], 'status': row[2],
                    'date': str(row[3]), 'time': str(row[4]), 'patient_name': row[5],
                    'age': row[6], 'gender': row[7]
                })
            con.close()
            cur.close()
            return jsonify(result=todos, error=False)
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return {'error': True, 'message': error.args}
        finally:
            if con is not None:
                cur.close()
                con.close()
