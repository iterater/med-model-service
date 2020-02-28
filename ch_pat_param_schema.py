from marshmallow import Schema, fields, validate, ValidationError, INCLUDE

class ParamSchema(Schema):
    '''Parameters validation schema'''
    class Meta:
        unknown = INCLUDE
    icd10 = fields.String(validate=validate.Regexp('[a-zA-Z]\\d+\\.?\\d*'), default='')
    sex = fields.String(validate=validate.OneOf(['male', 'female']), default='male')
    age = fields.Integer(validate=validate.Range(min=0), default=55)
    bmi = fields.Float(default=26.18)
    last_sbp = fields.Integer(validate=validate.Range(min=0, max=500), default=160)
    last_dbp = fields.Integer(validate=validate.Range(min=0, max=500), default=90)
    smoking = fields.Boolean(default=False)
    hereditary = fields.Boolean(default=False)
    dyslipidemia = fields.Boolean(default=True)
    diabetes = fields.Boolean(default=False)
    igt = fields.Boolean(default=True)
    left_ventricular_hypertrophy = fields.Boolean(default=False)
    microalbuminuria = fields.Boolean(default=False)
    chronic_kidney_disease = fields.Integer(validate=validate.Range(min=0, max=4), default=0)
    chf_dia = fields.Boolean(default=True)
    coronary_heart_disease = fields.Boolean(default=False)
