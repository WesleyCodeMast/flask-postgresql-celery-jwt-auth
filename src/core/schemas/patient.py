from marshmallow import Schema, fields

class PatientSchema(Schema):
    id = fields.Int(data_key='patient_id')
    name = fields.Str(data_key='patient_name')
    email = fields.Str(data_key='patient_email')
    phone = fields.Int(data_key='patient_phone')