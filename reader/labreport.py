from flask_restful import fields,reqparse
labreport_field={
    'labid':fields.Integer,
    'patientid':fields.Integer,
    'labname':fields.String,
    'resultstatus':fields.Boolean,
}

post_args=reqparse.RequestParser()
post_args.add_argument("labid",type=int,help='uid is required',required=True)
post_args.add_argument("patientid",type=int)
post_args.add_argument("labname",type=str)
post_args.add_argument("resultstatus",type=bool)

put_args=reqparse.RequestParser()
put_args.add_argument("labname",type=str)
put_args.add_argument("resultstatus",type=bool)