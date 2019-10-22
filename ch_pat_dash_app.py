import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import ch_pat_models_management
import json

models = ch_pat_models_management.load_models('models')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True

def call_form():
    param_list = ch_pat_models_management.params_list()
    form_seq = [dbc.FormGroup([dbc.Label(par['label']), dbc.Input(id=par['id'], value=par['default'])]) for par in param_list]
    return dbc.Form([html.H2('Params')] + form_seq + [dbc.Button("Call", id="call_button")], id='input_from')

def loaded_models():
    list_seq = [html.Li(m.model_description) for m in models]
    return html.Div([html.H2('Loaded models'), html.Ul(list_seq)])

def build_all_states(states):
    s_style = {'background-color': 'blanchedalmond', 'margin': '10px', 'padding': '5px'}
    def build_state(s):
        return html.Div([html.B(s['title']), html.P(s['value']), html.P(s['comment'], style={'font-size': '70%'})], style=s_style)
    return html.Div([html.H3('States')] + [build_state(s) for s in states])

@app.callback(Output('output_div', 'children'), [Input('call_button', 'n_clicks'), Input('input_from', 'children')])
def data_process_callback(n, input_form_content):
    def select_first_input_from_form_group(fg):
        return [(i['props']['id'], i['props']['value']) for i in fg['props']['children'] if i['type'] == 'Input'][0]
    if n is None:
        return html.Div('-')
    else:
        in_dict = dict(select_first_input_from_form_group(inp) for inp in input_form_content if inp['type'] == 'FormGroup')
        out_dict = ch_pat_models_management.call_models(in_dict, models)
        return html.Div([build_all_states(out_dict['states'])])

app.layout = dbc.Container([dbc.Row([
    dbc.Col([call_form(), html.Br(), loaded_models()]), 
    dbc.Col([html.H2('Output'), html.Div(id='output_div', children = [])])])])

if __name__ == '__main__':
    app.run_server(debug=True)