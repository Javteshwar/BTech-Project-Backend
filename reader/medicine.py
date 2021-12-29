from flask_restful import fields,reqparse
medicine_field={
    'medid':fields.Integer,
    'name':fields.String,
    'diseaseid':fields.Integer,
}

post_args=reqparse.RequestParser()
post_args.add_argument("medid",type=int,help='uid is required',required=True)
post_args.add_argument("name",type=str)
post_args.add_argument("diseaseid",type=str)

put_args=reqparse.RequestParser()
put_args.add_argument("name",type=str)