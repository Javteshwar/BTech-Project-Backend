from flask_restful import fields,reqparse

disease_field={
    'diseaseid':fields.Integer,
    'name':fields.String,
    'discription':fields.String,
}

post_args=reqparse.RequestParser()
post_args.add_argument("diseaseid",type=int,help='uid is required',required=True)
post_args.add_argument("name",type=str)
post_args.add_argument("discription",type=str)

put_args=reqparse.RequestParser()
put_args.add_argument("name",type=str)
put_args.add_argument("discription",type=str)