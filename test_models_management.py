import pytest
from ch_pat_models_management import validate_data, generate_default_data, load_params


def test_default_values_validation():
    params = load_params('params_list.csv')
    d = generate_default_data(params)
    for p in params:
        assert p['id'] in d
    errors = validate_data(d)
    assert len(errors) == 0
