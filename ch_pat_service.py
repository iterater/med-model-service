from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

import ch_pat_models_management

models = ch_pat_models_management.load_models('models')
params = ch_pat_models_management.load_params('params_list.csv')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/ch_pat_service', methods=['POST', 'GET'])
@cross_origin()
def main_service():
    data = request.args.to_dict() if request.method == 'GET' else request.get_json(force=True)
    data = ch_pat_models_management.call_models(data, models)
    return jsonify(data)


@app.route('/ch_pat_service_ui', methods=['POST', 'GET'])
def main_service_ui():
    data = request.args.to_dict() if request.method == 'GET' else request.get_json(force=True)
    data = ch_pat_models_management.call_models(data, models)
    return render_template('resp_template.html',
                           states=data['states'] if 'states' in data else [],
                           errors=data['errors'].items() if 'errors' in data else [])


@app.route('/')
def main_ui():
    return render_template('main_template.html', fields=[[p['id'], p['label']] for p in params])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    # app.run(host='localhost', port=5000, debug=True, use_reloader=False)
