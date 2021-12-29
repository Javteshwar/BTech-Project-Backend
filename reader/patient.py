from flask_restful import fields, reqparse

patient_field = {
    'uid': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'gender': fields.String,
    'age': fields.Integer,
    'phone': fields.String
}

post_args = reqparse.RequestParser()
post_args.add_argument(
    "email", type=str, help='email is required', required=True
)
post_args.add_argument(
    "password", type=str, help='password is required', required=True
)
post_args.add_argument("name", type=str)
post_args.add_argument("age", type=int)
post_args.add_argument("gender", type=str)
post_args.add_argument("phone", type=str)

put_args = reqparse.RequestParser()
put_args.add_argument("email", type=str)
put_args.add_argument("password", type=str)
put_args.add_argument("name", type=str)
put_args.add_argument("age", type=int)
put_args.add_argument("gender", type=str)
put_args.add_argument("phone", type=str)
