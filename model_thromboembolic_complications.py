from ch_pat_model import ChPatModel
from ThromboembolicComplications.Estimator import *
from ThromboembolicComplications.PatientInfo import *


class ThromboembolicComplicationsScaleModel(ChPatModel):

    """Model for predicting the thromboembolic complications in atrial fibrillation (based on the scale)"""
    def __init__(self):
        self._model_description = 'Thromboembolic complications predicting model (by scale)'

    def check_applicability(self, patient_dict):
        return ('age' in patient_dict) and ('sex' in patient_dict) and ('anamnesis' in patient_dict)

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()
        if 'states' not in res_dict:
            res_dict['states'] = []

        age = int(patient_dict['age'])
        sex = str(patient_dict['sex'])
        diagnosis = str(patient_dict['anamnesis'])

        info = PatientInfo(age=age, sex=sex, diagnosis=diagnosis)
        risk_point = Estimator.calculate_risk_point(data=info)
        complications_frequency = Estimator.find_complications_frequency(risk_point)

        res_dict['states'].append(
            {
                'title': 'Сумма баллов по шкале CHA2DS2-VASc',
                'value': risk_point,
                'comment': Estimator.category(risk_point)
            }
        )
        res_dict['states'].append(
            {
                'title': 'Ожидаемая частота инсультов за год',
                'value': str(complications_frequency) + '%',
                'comment': 'Рекомендуется: ' + Estimator.therapy(risk_point)
            }
        )
        return res_dict
