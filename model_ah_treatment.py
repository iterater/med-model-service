import json
import pickle
from ch_pat_model import ChPatModel

class AhTreatmentDecisionTreeModel(ChPatModel):
    '''Work with treatment model in decision tree.'''
    def __init__(self, dt_pickle_path, model_decsription, therapy_class_name):
        self._model_description = model_decsription
        self._dt = pickle.load(open(dt_pickle_path, 'br'))
        self._therapy_class_name = therapy_class_name

    def check_applicability(self, patient_dict):
        params_list = ['icd10', 'last_sbp', 'last_dbp', 'sex', 'age', 'bmi', 'smoking',
                       'hereditary', 'dyslipidemia', 'diabetes', 'igt', 'left_ventricular_hypertrophy', 'microalbuminuria',
                       'chronic_kidney_disease', 'chf_dia', 'coronary_heart_disease']
        return all((p_name in patient_dict) for p_name in params_list) and ('I10' in patient_dict['icd10'])

    def apply(self, patient_dict):
        features_vec = [patient_dict['last_sbp'],
                        patient_dict['last_dbp'],
                        patient_dict['sex'].lower() != 'female',
                        patient_dict['age'],
                        patient_dict['bmi'],
                        patient_dict['smoking'],
                        patient_dict['hereditary'],
                        patient_dict['dyslipidemia'],
                        patient_dict['diabetes'],
                        patient_dict['igt'],
                        patient_dict['left_ventricular_hypertrophy'],
                        patient_dict['microalbuminuria'],
                        patient_dict['chronic_kidney_disease'],
                        patient_dict['chf_dia'],
                        patient_dict['coronary_heart_disease']]        
        res_dict = patient_dict.copy()
        res = self._dt.predict([features_vec])[0]
        rec_str = 'Рекомендована терапия: ' if res else 'Не рекомендована терапия: '
        if 'recommendations' not in res_dict:
            res_dict['recommendations'] = rec_str + self._therapy_class_name + '.'
        else:
            res_dict['recommendations'] = rec_str + self._therapy_class_name + '. ' + res_dict['recommendations']
        return res_dict

