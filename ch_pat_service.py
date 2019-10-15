from flask import Flask, request, jsonify
import pickle
import os
import logging

# logging setup
logger = logging.getLogger('model_service')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(ch)

# initialising service
logger.info('Starting service')
app = Flask(__name__)
basic_model_path = 'models'
models = []
for fn in os.listdir(basic_model_path):
    m = pickle.load(open(os.path.join(basic_model_path, fn), 'br'))
    logger.info('Loading model: \'{0}\''.format(m.model_description))
    models.append(m)

@app.route('/ch_pat_service',methods=['POST'])
def main_service():
    data = request.get_json(force=True)
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
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
