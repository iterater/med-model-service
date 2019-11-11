from flask import Flask, request, jsonify, render_template
import ch_pat_models_management

models = ch_pat_models_management.load_models('models')
params = ch_pat_models_management.load_params('params_list.csv')

app = Flask(__name__)


@app.route('/ch_pat_service', methods=['POST', 'GET'])
def main_service():
    data = request.args.to_dict() if request.method == 'GET' else request.get_json(force=True)
    data = ch_pat_models_management.call_models(data, models)
    return jsonify(data)


@app.route('/ch_pat_service_ui', methods=['POST', 'GET'])
def main_service_ui():
    data = request.args.to_dict() if request.method == 'GET' else request.get_json(force=True)
    data = ch_pat_models_management.call_models(data, models)
    render_states = data['states'] if 'states' in data else []
    render_errors = data['errors'].items() if 'errors' in data else []
    return render_template('resp_template.html', states=render_states, errors=render_errors)


@app.route('/')
def main_ui():
    return render_template('main_template.html', fields=[[p['id'], p['label']] for p in params])


if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)
