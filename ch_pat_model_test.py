# Test 1: creating model pickle
import model_ah_state
import model_thromboembolic_complications
import model_diab_predict
import model_score
import model_chf_risk

#import pickle

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


test_model = model_chf_risk.CHFRiskModel()
test_model.store_model('models\\chf_risk.pkl')


# Test 2: running flask app
# import requests
# url = 'http://localhost:5000/ch_pat_service'
# url = 'http://195.222.181.179:5000/ch_pat_service'
# r = requests.post(url,json={'icd10':'I10','max_sbp':160})
# print(r.json())
