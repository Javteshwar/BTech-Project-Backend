from reader.medicine import medicine_field, put_args, post_args
from model.medicine import Medicine
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


class MedicineList(Resource):
    def get(self):
        cur.execute("SELECT medid,name,diseaseid from MEDICINE")
        rows = cur.fetchall()
        todos = {}
        i = 0
        for row in rows:
            todos[i] = {'medid': row[0], 'name': row[1], 'diseaseid': row[2]}
            i = i+1
        return todos

    def post(self):
        args = post_args.parse_args()
        insert_query = """INSERT INTO MEDICINE (medid,name,diseaseid) VALUES (%s,%s,%s)"""
        record_to_insert = (args['medid'], args['name'], args['diseaseid'])
        cur.execute(insert_query, record_to_insert)
        con.commit()
        return args


class MedicineApi(Resource):
    @marshal_with(medicine_field)
    def get(self, medicine_id):
        select_query = "SELECT medid,name,diseaseid from MEDICINE where medid=%s"
        cur.execute(select_query, (medicine_id,))
        m_record = cur.fetchone()
        if not m_record:
            abort(404)
        ans = Medicine(medid=m_record[0],
                       name=m_record[1], diseaseid=m_record[2])
        return ans

    def delete(self, medicine_id):
        delete_query = "DELETE from MEDICINE where medid=%s"
        cur.execute(delete_query, (medicine_id,))
        con.commit()
        return 'recored delted', 204

    @marshal_with(medicine_field)
    def put(self, medicine_id):
        args = put_args.parse_args()
        select_query = "SELECT medid,name,diseaseid from MEDICINE where medid=%s"
        cur.execute(select_query, (medicine_id,))
        m_record = cur.fetchone()
        if not m_record:
            abort(404)

        if args['name']:
            tup = (args['name'], medicine_id)
            update_query = "UPDATE MEDICINE set name=%s where medid=%s"
            cur.execute(update_query, tup)
        con.commit()
        cur.execute(select_query, (medicine_id,))
        m_record = cur.fetchone()
        ans = Medicine(medid=m_record[0],
                       name=m_record[1], diseaseid=m_record[2])
        return ans
