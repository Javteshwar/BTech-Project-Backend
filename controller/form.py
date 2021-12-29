import os
from flask_restful import Resource
from flask import request
from OCR.form import FormData


class Form(Resource):
    def post(self):
        file = request.files['image']
        file.save(os.path.join('OCR\\user_form', file.filename))
        res = {}
        # if status == True:
        obj = FormData('form1')
        res.update(obj.getFormData())
        res['error'] = False
        return res
