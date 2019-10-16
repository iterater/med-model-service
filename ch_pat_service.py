from flask import Flask, request, jsonify, render_template
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

def call_models(data):
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

@app.route('/ch_pat_service', methods=['POST', 'GET'])
def main_service():
    data = request.args.to_dict() if request.method == 'GET' else request.get_json(force=True)
    data = call_models(data)
    return jsonify(data)

@app.route('/ch_pat_service_ui', methods=['POST', 'GET'])
def main_service_ui():
    data = request.args.to_dict() if request.method == 'GET' else request.get_json(force=True)
    data = call_models(data)
    return render_template('resp_template.html', states=data['states'] if 'states' in data else [])

@app.route('/')
def main_ui():
    return render_template('main_template.html', fields=[['icd10','МКБ-10'], ['max_sbp','САД (max)']])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
