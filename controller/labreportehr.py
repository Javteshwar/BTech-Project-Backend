from reader.labreport import labreport_field, post_args, put_args
from model.labreport import LabReport
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


class LabReportList(Resource):
    def get(self):
        cur.execute(
            "SELECT labid,patientid,labname,resultstatus from LABREPORT")
        rows = cur.fetchall()
        todos = {}
        i = 0
        for row in rows:
            todos[i] = {'labid': row[0], 'patientid': row[1],
                        'labname': row[2], 'reultstatus': row[3]}
            i = i+1
        return todos

    def post(self):
        args = post_args.parse_args()
        insert_query = """INSERT INTO LABREPORT (labid,patientid,labname,resultstatus) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (args['labid'], args['patientid'],
                            args['labname'], args['resultstatus'])
        cur.execute(insert_query, record_to_insert)
        con.commit()
        return args


class LabReportApi(Resource):
    @marshal_with(labreport_field)
    def get(self, labreport_id):
        select_query = "SELECT labid,patientid,labname,resultstatus from LABREPORT where labid=%s"
        cur.execute(select_query, (labreport_id,))
        l_record = cur.fetchone()
        if not l_record:
            abort(404)
        ans = LabReport(labid=l_record[0], patientid=l_record[1],
                        labname=l_record[2], resultstatus=l_record[3])
        return ans

    def delete(self, labreport_id):
        delete_query = "DELETE from LABREPORT where labid=%s"
        cur.execute(delete_query, (labreport_id,))
        con.commit()
        return 'recored delted', 204

    @marshal_with(labreport_field)
    def put(self, labreport_id):
        args = put_args.parse_args()
        select_query = "SELECT labid,patientid,labname,resultstatus from LABREPORT where labid=%s"
        cur.execute(select_query, (labreport_id,))
        l_record = cur.fetchone()
        if not l_record:
            abort(404)

        if args['labname']:
            tup = (args['labname'], labreport_id)
            update_query = "UPDATE LABREPORT set labname=%s where labid=%s"
            cur.execute(update_query, tup)
        if args['resultstatus']:
            tup = (args['resultstatus'], labreport_id)
            update_query = "UPDATE LABREPORT set resultstatus=%s where labid=%s"
            cur.execute(update_query, tup)
        con.commit()
        cur.execute(select_query, (labreport_id,))
        l_record = cur.fetchone()
        ans = LabReport(labid=l_record[0], patientid=l_record[1],
                        labname=l_record[2], resultstatus=l_record[3])
        return ans
