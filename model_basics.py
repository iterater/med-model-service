import json
import pickle
from ch_pat_model import ChPatModel

class BasicAHModel(ChPatModel):
    '''Test model with simple AH rules.'''
    def __init__(self):
        self._model_description = 'Basic AH model'

    def check_applicability(self, patient_dict):
        return ('icd10' in patient_dict) and ('I10' in patient_dict['icd10']) and ('max_sbp' in patient_dict)

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()
        if 'states' not in res_dict:
            res_dict['states'] = []
        if int(patient_dict['max_sbp']) > 140:
            res_dict['states'].append({'title': 'Монитор давления', 'value': '>140', 'comment': 'Повышенное давление'})
        return res_dict

class StubStateModel(ChPatModel):
    '''Stub model. Works everywhere'''
    def __init__(self):
        self._model_description = 'Stub model'

    def check_applicability(self, patient_dict):
        return True

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()
        if 'states' not in res_dict:
            res_dict['states'] = []
        res_dict['states'].append({'title': 'Тест', 'value': 'ОК', 'comment': 'Тестовая модель отработала'})
        return res_dict

def store_all_models():
    # train and store models
    m1 = BasicAHModel()
    m1.store_model('models\\test_ah_model.pkl')
    m2 = StubStateModel()
    m2.store_model('models\\stub_model.pkl')
