import logging
import pickle
import os
import pandas as pd
import datetime as dt
from ch_pat_param_schema import ParamSchema

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)
file_suffix = dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
log_file_name = os.path.join('log', 'ew-log-' + file_suffix + '.txt')
fh = logging.FileHandler(log_file_name)
fh.setLevel(logging.WARNING)
fh.setFormatter(formatter)
logger.addHandler(fh)

def load_models(basic_model_path):
    '''Load pckled models from dir'''    
    models = []
    for fn in os.listdir(basic_model_path):
        if not fn.endswith('.pkl'):
            continue
        m = pickle.load(open(os.path.join(basic_model_path, fn), 'br'))
        logger.info('Loading model: {0}'.format(m.model_description))
        models.append(m)
    return models


def call_models(data, models):
    '''Call available models'''
    logger.info('Input: {0}'.format(data))
    errors = validate_data(data)
    if len(errors) > 0:
        logger.error('Termination with {0} errors in input data'.format(len(errors)))
        data['errors'] = errors
        return data
    else:
        logger.info('Validation passed')
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
                    logger.info('Applied model: {0}'.format(m.model_description))
                except Exception as e:
                    logger.error('Model \'{0}\' crashed with exception {1}'.format(m.model_description, e))
    data['errors'] = dict()
    logger.info('Output: {0}'.format(data))
    return data


def load_params(file_name):
    '''Load available parameters list'''
    params_df = pd.read_csv(file_name, sep=',')
    params_df = params_df.fillna('')
    logger.info('Params loaded from CSV: {0}'.format(', '.join(params_df['id'])))
    schema = ParamSchema()
    schema_ids = list(schema.fields.keys())
    for param_id in params_df['id']:
        if param_id not in schema_ids:
            logger.warning('Parameter \'{0}\' is in CSV config but not in validation schema'.format(param_id))
        else:
            schema_ids.remove(param_id)
    for param_id in schema_ids:
        if param_id not in params_df['id'].values:
            logger.warning('Parameter \'{0}\' is in validation schema but not in CSV config'.format(param_id))
    return params_df.T.to_dict().values()


def validate_data(data):
    '''Validate input data with the scheme'''
    schema = ParamSchema()
    errors = schema.validate(data)
    for e in errors:
        logger.error('Invalid parameter \'{0}\': {1}'.format(e, ' / '.join(errors[e])))
    return errors


def generate_default_data(params):
    '''Generate dictionary with default values'''
    generated_default_data = {p['id']:p['default'] for p in params}
    logger.info('Generated data: {0}'.format(generated_default_data))
    return generated_default_data
