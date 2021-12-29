from calendar import c
import hashlib
import os
import json
from flask import jsonify, request
from flask_restful import Resource, marshal_with
from psycopg2 import sql
from model.doctor import Doctor
from model.patient import Patient
import psycopg2
import jwt
from dotenv import load_dotenv
load_dotenv('../.env')


class Authenticate(Resource):

    def post(self):
        # Login User
        con = None
        args = request.json
        hash_object = hashlib.sha1(bytes(args['password'], 'utf-8'))
        hashed_pass = hash_object.hexdigest()
        try:
            con = psycopg2.connect(
                host="localhost", database=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
            )
            cur = con.cursor()
            if args['val'] == 0:
                tbl = 'patient'
            else:
                tbl = 'doctor'
            select_query = sql.SQL(
                "SELECT * from {} where email=%s and password=%s"
            ).format(sql.Identifier(tbl))
            cur.execute(select_query, (args['email'], hashed_pass))
            rows = cur.fetchall()
            if cur.rowcount == 0:
                return {'error': True, 'message': 'User not found'}
            payload = None
            if args['val'] == 0:
                payload = Patient(
                    uid=rows[0][0], email=rows[0][1], name=rows[0][3],
                    gender=rows[0][4], age=rows[0][5], phone=rows[0][6]
                )
            else:
                payload = Doctor(
                    uid=rows[0][0], email=rows[0][1], name=rows[0][3],
                    specialization=rows[0][4], phone=rows[0][5]
                )
            encoded_jwt = jwt.encode(
                payload.__dict__, os.getenv('AUTHSECRET'), algorithm='HS256'
            )
            return jsonify(token=encoded_jwt, error=False)

        except (Exception, psycopg2.DatabaseError) as error:
            if con is not None:
                cur.close()
                con.close()

            return jsonify(error=True, message=error)
        finally:
            if con is not None:
                cur.close()
                con.close()
