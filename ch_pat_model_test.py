# Test 1: creating model pickle
import model_ah_state
import model_test
import model_thromboembolic_complications
import model_diab_predict
#import pickle

test_model = model_test.StubStateModel()
test_model.store_model('models\\stub_model.pkl')
test_model = model_test.TestAHModel()
test_model.store_model('models\\test_ah_model.pkl')
test_model = model_thromboembolic_complications.ThromboembolicComplicationsScaleModel()
test_model.store_model('models\\thromboembolic_complications_scale_model.pkl')
test_model = model_ah_state.StateAHModel()
test_model.store_model('models\\ah_state_classifier_model.pkl')
test_model = model_diab_predict.DiabetesPrediction()
test_model.store_model('models\\diab_5_years_risk.pkl')
test_model = model_diab_predict.FINDRISK()
test_model.store_model('models\\findrisk.pkl')
# test_model = pickle.load(open('models\\test_ah_model.pkl', 'rb'))
# print(test_model.model_description)

# Test 2: running flask app
# import requests
# url = 'http://localhost:5000/ch_pat_service'
# url = 'http://195.222.181.179:5000/ch_pat_service'
# r = requests.post(url,json={'icd10':'I10','max_sbp':160})
# print(r.json())

'''
from ThromboembolicComplications.ModelDataPreparator import *


ModelDataPreparator(
    features_file_path='/Users/kabyshev/Desktop/Developing/medicine/Table2Object174part1.txt',
    persons_file_path='/Users/kabyshev/Downloads/Table2Download153ObjectFeatures.txt',
    csv_file_path='/Users/kabyshev/Desktop/Developing/chronic-patient-model-service/models/personal_data_with_diagnosises.csv',
    features_list=['Name', 'Массив_последнего_диагноза', 'Клинический_диагноз'],
    personal_data_list=['Name', 'Пол', 'Дата_рождения'],
    join_key='Name'
).start()
'''
