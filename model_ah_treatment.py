import json
import pickle
from ch_pat_model import ChPatModel

class AhTreatmentDecisionTreeModel(ChPatModel):
    '''Work with treatment model in decision tree.'''
    def __init__(self, dt_pickle_path, model_decsription):
        self._model_description = model_decsription
        self._dt = pickle.load(open(dt_pickle_path, 'br'))

    def check_applicability(self, patient_dict):
        # TODO: check parameters
        return ('icd10' in patient_dict) and ('I10' in patient_dict['icd10'])

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()
        if 'recommendations' not in res_dict:
            res_dict['recommendations'] = []
        # TODO: feature encoding
        # TODO: request _dt, if True, append res_dict['recommendations']
        return res_dict

# Features:
# 'Systolic' 
# 'Diastolic'
# 'Sex' 
# 'Age' 
# 'BMI' 
# 'Smoke' 
# 'Hereditary' 
# 'Dyslipidemia' 
# 'Diabetes' 
# 'IGT' 
# 'LVH' 
# 'Microalbuminuria' 
# 'CKDStage' 
# 'CHF' 
# 'IHD'

if __name__ == '__main__':
    m = AhTreatmentDecisionTreeModel('HypertensivePatientTreatmentModel\\Treatment_ARB.pkl', 'AH treatment with ARB')
    m.store_model('models\\ah_treatment_arb.pkl')
