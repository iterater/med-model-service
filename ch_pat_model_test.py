# Test 1: creating model pickle
import ch_pat_model
import pickle
test_model = ch_pat_model.TestAHModel()
test_model.store_model('models\\test_ah_model.pkl')
print(test_model.model_description)
# test_model = pickle.load(open('models\\test_ah_model.pkl', 'rb'))

# Test 2: running flask app
# import requests
# url = 'http://localhost:5000/ch_pat_service'
# url = 'http://195.222.181.179:5000/ch_pat_service'
# r = requests.post(url,json={'icd10':'I10','max_sbp':160})
# print(r.json())
