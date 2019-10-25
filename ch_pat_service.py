from flask import Flask, request, jsonify, render_template
import ch_pat_models_management

models = ch_pat_models_management.load_models('models')

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
    return render_template('resp_template.html', states=data['states'] if 'states' in data else [])

@app.route('/')
def main_ui():
    return render_template('main_template.html', fields=[['icd10','МКБ-10'], ['max_sbp','САД (max)']])

@app.route('/ch_pat_thromboembolic_complications_scale_model', methods=['POST', 'GET'])
def thromboembolic_complications_ui():
    return render_template('main_template.html', fields=[
        ['age', 'Возраст'], ['sex', 'Пол (male/female)'], ['anamnesis', 'Анамнез']
    ])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
