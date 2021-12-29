from flask_restful import reqparse, fields
doctor_field = {
    'uid': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'phone': fields.String,
    'specialization': fields.String
}

post_args = reqparse.RequestParser()
post_args.add_argument(
    "email", type=str, help='email is required', required=True
)
post_args.add_argument(
    "password", type=str, help='password is required', required=True
)
post_args.add_argument("name", type=str)
post_args.add_argument("phone", type=str)
post_args.add_argument("specialization", type=str)

put_args = reqparse.RequestParser()
post_args.add_argument("email", type=str)
put_args.add_argument("name", type=str)
put_args.add_argument("phone", type=str)
put_args.add_argument("specialization", type=str)
