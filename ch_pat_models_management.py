import logging
import pickle
import os

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(ch)

def load_models(basic_model_path):
    models = []
    for fn in os.listdir(basic_model_path):
        m = pickle.load(open(os.path.join(basic_model_path, fn), 'br'))
        logger.info('Loading model: \'{0}\''.format(m.model_description))
        models.append(m)
    return models


def call_models(data, models):
    logger.info('Input: {0}'.format(data))
    has_applicable_models = True
    model_application_flag = [False] * len(models)
    while has_applicable_models:
        has_applicable_models = False
        for i, m in enumerate(models):
            if m.check_applicability(data) and not model_application_flag[i]:
                has_applicable_models = True
                model_application_flag[i] = True
                logger.info('Applying mode: \'{0}\''.format(m.model_description))
                data = m.apply(data)    
    logger.info('Output: {0}'.format(data))
    return data

def params_list():
    return [{'id':'icd10', 'label':'МКБ-10', 'default':'I10'}, {'id':'max_sbp', 'label':'САД (max)', 'default':'120'}]