# Test 1: creating model pickle
import model_ah_state
import model_thromboembolic_complications
import model_diab_predict
import model_score
import model_chf_risk
import model_chf_outcome
import model_chf_trans_heart
import model_chf_strokes
import model_chf_takhikardia
import model_other_dias_prediction
import model_ah_treatment

# import pickle

test_model = model_ah_state.StateAHModel()
test_model.store_model('models\\ah_state_classifier_model.pkl')
test_model = model_diab_predict.DiabetesPrediction()
test_model.store_model('models/diab_5_years_risk.pkl')
test_model = model_diab_predict.FINDRISK()
test_model.store_model('models\\findrisk.pkl')
test_model = model_thromboembolic_complications.ThromboembolicComplicationsScaleModel()
test_model.store_model('models\\thromboembolic_complications_scale_model.pkl')
test_model = model_score.ScoreModel()
test_model.store_model('models\\scoreModel.pkl')
test_model = model_score.TotalRiskModel()
test_model.store_model('models\\TotalRiskModel.pkl')
test_model = model_chf_outcome.CHFOutcomeClassifier()
test_model.store_model('models\\chf_outcome_model.pkl')
test_model = model_chf_trans_heart.CHFTransHeartClassifier()
test_model.store_model('models\\chf_trans_heart_model.pkl')
test_model = model_chf_strokes.CHFStrokeClassifier()
test_model.store_model('models\\chf_stroke_model.pkl')
test_model = model_chf_takhikardia.CHFTakhClassifier()
test_model.store_model('models\\chf_takh_model.pkl')
test_model = model_chf_risk.CHFRiskModel()
test_model.store_model('models\\chf_risk.pkl')
test_model = model_other_dias_prediction.E063Model()
test_model.store_model('models\\E063Model.pkl')
test_model = model_other_dias_prediction.I48Model()
test_model.store_model('models\\I48Model.pkl')
test_model = model_other_dias_prediction.I50Model()
test_model.store_model('models\\I50Model.pkl')
test_model = model_other_dias_prediction.I65_2Model()
test_model.store_model('models\\I65_2Model.pkl')
test_model = model_other_dias_prediction.I67_2Model()
test_model.store_model('models\\I67_2Model.pkl')
test_model = model_other_dias_prediction.M42_1Model()
test_model.store_model('models\\M42_1Model.pkl')
test_model = model_other_dias_prediction.AcuteHeartAttackModel()
test_model.store_model('models\\AcuteHeartAttackModel.pkl')
test_model = model_risk_AF_thyrotoxicosis.AFPrediction()
test_model.store_model('models\\risk_AF_TT.pkl')
# Test 2: running flask app
# import requests
# url = 'http://localhost:5000/ch_pat_service'
# url = 'http://195.222.181.179:5000/ch_pat_service'
# r = requests.post(url,json={'icd10':'I10','max_sbp':160})
# print(r.json())

# therapy models
m = model_ah_treatment.AhTreatmentDecisionTreeModel(
    'HypertensivePatientTreatmentModel\\Treatment_ARB.pkl', 
    'AH treatment with ARB', 'антагонисты рецепторов к ангиотензину II')
m.store_model('models\\ah_treatment_arb.pkl')

m = model_ah_treatment.AhTreatmentDecisionTreeModel(
    'HypertensivePatientTreatmentModel\\Treatment_BB.pkl', 
    'AH treatment with BB', 'бета-блокаторы')
m.store_model('models\\ah_treatment_bb.pkl')

m = model_ah_treatment.AhTreatmentDecisionTreeModel(
    'HypertensivePatientTreatmentModel\\Treatment_CaCB.pkl', 
    'AH treatment with CaCB', 'антагонисты кальция')
m.store_model('models\\ah_treatment_cacb.pkl')

m = model_ah_treatment.AhTreatmentDecisionTreeModel(
    'HypertensivePatientTreatmentModel\\Treatment_D.pkl', 
    'AH treatment with D', 'диуретики')
m.store_model('models\\ah_treatment_d.pkl')

m = model_ah_treatment.AhTreatmentDecisionTreeModel(
    'HypertensivePatientTreatmentModel\\Treatment_iACE.pkl', 
    'AH treatment with iACE', 'ингибиторы АПФ')
m.store_model('models\\ah_treatment_iace.pkl')
