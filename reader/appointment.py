from typing import get_args
from flask_restful import reqparse


post_args = reqparse.RequestParser()
post_args.add_argument("patient_uid", type=str)
post_args.add_argument("doctor_uid", type=str)
post_args.add_argument("status", type=str)
post_args.add_argument("date", type=str)
post_args.add_argument("time", type=str)

appointment_update_args = reqparse.RequestParser()
appointment_update_args.add_argument(
    "uid", type=str, help='ID required', required=True
)
appointment_update_args.add_argument(
    "status", type=str, help='ID required', required=True
)
