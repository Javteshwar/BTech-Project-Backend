from reader.disease import disease_field, put_args, post_args
from model.diseases import Diseases
from flask_restful import Resource, marshal_with, abort
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv('../.env')

con = psycopg2.connect(
    host="localhost", database=os.getenv('DBNAME'),
    user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD')
)
cur = con.cursor()


class DiseaseList(Resource):
    def get(self):
        cur.execute("SELECT diseaseid,name,discription from DISEASE")
        rows = cur.fetchall()
        todos = {}
        i = 0
        for row in rows:
            todos[i] = {'diseaseid': row[0],
                        'name': row[1], 'discriptiom': row[2]}
            i = i+1
        return todos

    def post(self):
        args = post_args.parse_args()
        insert_query = """INSERT INTO DISEASE (diseaseid,name,discription) VALUES (%s,%s,%s)"""
        record_to_insert = (args['diseaseid'],
                            args['name'], args['discription'])
        cur.execute(insert_query, record_to_insert)
        con.commit()
        return args


class DiseaseApi(Resource):
    @marshal_with(disease_field)
    def get(self, disease_id):
        select_query = "SELECT diseaseid,name,discription from DISEASE where diseaseid=%s"
        cur.execute(select_query, (disease_id,))
        d_record = cur.fetchone()
        if not d_record:
            abort(404)
        ans = Diseases(
            diseaseid=d_record[0], name=d_record[1], discription=d_record[2])
        return ans

    def delete(self, disease_id):
        delete_query = "DELETE from DISEASE where diseaseid=%s"
        cur.execute(delete_query, (disease_id,))
        con.commit()
        return 'recored delted', 204

    @marshal_with(disease_field)
    def put(self, disease_id):
        args = put_args.parse_args()
        select_query = "SELECT diseaseid,name,discription from DISEASE where diseaseid=%s"
        cur.execute(select_query, (disease_id,))
        d_record = cur.fetchone()
        if not d_record:
            abort(404)

        if args['name']:
            tup = (args['name'], disease_id)
            update_query = "UPDATE DISEASE set name=%s where diseaseid=%s"
            cur.execute(update_query, tup)
        if args['discription']:
            tup = (args['discription'], disease_id)
            update_query = "UPDATE DISEASE set discription=%s where diseaseid=%s"
            cur.execute(update_query, tup)
        con.commit()
        cur.execute(select_query, (disease_id,))
        d_record = cur.fetchone()
        ans = Diseases(
            diseaseid=d_record[0], name=d_record[1], discription=d_record[2])
        return ans
