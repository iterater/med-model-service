import logging
import pickle
import os
import pandas as pd

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(ch)

def load_models(basic_model_path):
    '''Load pckled models from dir'''    
    models = []
    for fn in os.listdir(basic_model_path):
        if not fn.endswith('.pkl'):
            continue
        m = pickle.load(open(os.path.join(basic_model_path, fn), 'br'))
        logger.info('Loading model: \'{0}\''.format(m.model_description))
        models.append(m)
    return models


def call_models(data, models):
    '''Call available models'''
    logger.info('Input: {0}'.format(data))
    has_applicable_models = True
    model_application_flag = [False] * len(models)
    while has_applicable_models:
        has_applicable_models = False
        for i, m in enumerate(models):
            if m.check_applicability(data) and not model_application_flag[i]:
                has_applicable_models = True
                model_application_flag[i] = True
                try:
                    data = m.apply(data)
                    logger.info('Applied model: \'{0}\''.format(m.model_description))
                except Exception as e:
                    logger.error('Model \'{0}\' crashed with exception {1}'.format(m.model_description, e))
    logger.info('Output: {0}'.format(data))
    return data

def load_params(file_name):
    '''Load available parameters list'''
    params_df = pd.read_csv(file_name, sep=',')
    logger.info('Params loaded from CSV: {0}'.format(', '.join(params_df['id'])))
    return params_df.T.to_dict().values()