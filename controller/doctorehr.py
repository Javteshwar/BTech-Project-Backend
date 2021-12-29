import hashlib
import os
from flask import jsonify
import jwt
from model.doctor import Doctor
from reader.doctor import put_args, post_args
from flask_restful import Resource, abort
from flask import request
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
load_dotenv('../.env')


class DoctorList(Resource):
    def get(self):
        con = None
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            cur.execute(
                "SELECT uid,name,specialization from doctor"
            )
            rows = cur.fetchall()
            todos = []
            for row in rows:
                todos.append({
                    'uid': row[0], 'name': row[1],
                    'specialization': row[2],
                })
            return jsonify(result=todos, error=False)
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return jsonify(error= True, message= error.args)
        finally:
            if con is not None:
                cur.close()
                con.close()


class DoctorApi(Resource):
    # Register User
    def post(self):
        args = post_args.parse_args()
        con = None
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            hash_object = hashlib.sha1(bytes(args['password'], 'utf-8'))
            hashed_pass = hash_object.hexdigest()
            insert_query = """INSERT INTO doctor (email,password,name,specialization,phone) VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (
                args['email'], hashed_pass, args['name'],
                args['specialization'], args['phone']
            )
            cur.execute(insert_query, record_to_insert)
            con.commit()
            return {'error': False}
        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()
            return {'error': True, 'message': error.args}
        finally:
            if con is not None:
                cur.close()
                con.close()

    # Delete User Data
    def delete(self):
        authorizationHeader = request.headers.get('authorization')
        token = authorizationHeader.replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            os.getenv('AUTHSECRET'),
            algorithms=['HS256']
        )
        con = psycopg2.connect(
            host="localhost", database=os.getenv('DBNAME'),
            user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
        )
        cur = con.cursor()
        delete_query = "DELETE from doctor where uid=%s"
        cur.execute(delete_query, (decoded['uid'],))
        con.commit()
        return jsonify(error=False)

    # Update User Data
    def put(self):
        authorizationHeader = request.headers.get('authorization')
        token = authorizationHeader.replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            os.getenv('AUTHSECRET'),
            algorithms=['HS256']
        )
        args = put_args.parse_args()
        con = psycopg2.connect(
            host="localhost", database=os.getenv('DBNAME'),
            user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
        )
        cur = con.cursor()
        select_query = "SELECT * from doctor where uid=%s"
        cur.execute(select_query, (decoded['uid'],))
        d_record = cur.fetchone()
        if not d_record:
            abort(404)
        for vl in args:
            if args[vl]:
                tup = (args[vl], decoded['uid'])
                update_query = sql.SQL("UPDATE doctor set {}=%s where uid=%s").format(
                    sql.Identifier(vl)
                )
                cur.execute(update_query, tup)
        con.commit()
        cur.execute(select_query, (decoded['uid'],))
        d_record = cur.fetchone()
        ans = Doctor(
            uid=d_record[0], email=d_record[1], name=d_record[3],
            specialization=d_record[4], phone=d_record[5]
        )
        con.close()
        return jsonify(result=ans.__dict__, error=False)
