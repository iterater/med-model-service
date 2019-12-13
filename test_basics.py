import pytest
import socket
import requests
from ch_pat_models_management import load_params, generate_default_data
from model_basics import StubStateModel, BasicAHModel


@pytest.fixture(scope='module')
def generate_test_data_for_stub_model():
    params = load_params('params_list.csv')
    default_in_dict = generate_default_data(params)
    return [dict(), default_in_dict]


def test_StubStateModel_applicability(generate_test_data_for_stub_model):
    model = StubStateModel()
    for in_dict in generate_test_data_for_stub_model:
        assert model.check_applicability(in_dict)


def test_StubStateModel_application(generate_test_data_for_stub_model):
    model = StubStateModel()
    for in_dict in generate_test_data_for_stub_model:
        out_dict = model.apply(in_dict)
        assert any((state['title'] == 'Тест') and (state['value'] == 'ОК') for state in out_dict['states'])


@pytest.fixture(scope='module')
def generate_test_data_for_ah_model():
    tests_list = [(dict(), False, False)] 
    params = load_params('params_list.csv')
    basic_dict = generate_default_data(params)
    basic_dict['icd10'] = 'I10'
    tests_list.append((basic_dict, True, False))
    high_pressure_dict = basic_dict.copy()
    high_pressure_dict['max_sbp'] = 200
    tests_list.append((high_pressure_dict, True, True))
    wrong_icd_dict = basic_dict.copy()
    wrong_icd_dict['icd10'] = 'X00'
    tests_list.append((wrong_icd_dict, False, False))    
    return tests_list


def test_BasicAHModel_applicability(generate_test_data_for_ah_model):
    model = BasicAHModel()
    for in_dict,applicability_flag,_ in generate_test_data_for_ah_model:
        assert model.check_applicability(in_dict) == applicability_flag


def test_BasicAHModel_application(generate_test_data_for_ah_model):
    model = BasicAHModel()
    for in_dict,applicability_flag,high_blood_pressure_flag in generate_test_data_for_ah_model:
        if applicability_flag:
            out_dict = model.apply(in_dict)
            state_flag = any((state['title'] == 'Монитор давления') and (state['value'] == '>140') for state in out_dict['states'])
            assert state_flag == high_blood_pressure_flag


@pytest.fixture(scope='session')
def generate_local_service_url():
    address = socket.gethostbyname(socket.gethostname())
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address,5000))
    assert result == 0
    sock.close()
    return 'http://{0}:5000/ch_pat_service'.format(address)


def test_external_call(generate_test_data_for_stub_model, generate_local_service_url):
    url = generate_local_service_url
    for in_dict in generate_test_data_for_stub_model:
        resp = requests.post(url, json=in_dict)
        assert resp.status_code == 200        
