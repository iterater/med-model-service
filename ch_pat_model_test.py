# Test 1: creating model pickle
import ch_pat_model
import ch_pat_thromboembolic_complications_scale_model
import pickle

test_model = ch_pat_model.StubStateModel()
test_model.store_model('models/stub_model.pkl')
test_model = ch_pat_model.TestAHModel()
test_model.store_model('models/test_ah_model.pkl')
test_model = ch_pat_thromboembolic_complications_scale_model.ThromboembolicComplicationsScaleModel()
test_model.store_model('models/thromboembolic_complications_scale_model.pkl')
# test_model = pickle.load(open('models\\test_ah_model.pkl', 'rb'))
# print(test_model.model_description)

# Test 2: running flask app
# import requests
# url = 'http://localhost:5000/ch_pat_service'
# url = 'http://195.222.181.179:5000/ch_pat_service'
# r = requests.post(url,json={'icd10':'I10','max_sbp':160})
# print(r.json())
