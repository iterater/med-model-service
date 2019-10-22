import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import ch_pat_models_management

models = ch_pat_models_management.load_models('models')

def call_form():
    form_seq = [dbc.FormGroup([dbc.Label(par['label']), dbc.Input(id=par['id'], value=par['default'])]) for par in ch_pat_models_management.params_list()]
    return dbc.Form([html.H2('Params')] + form_seq + [dbc.Button("Call", id="example-button")])

def loaded_models():
    list_seq = [html.Li(m.model_description) for m in models]
    return html.Div([html.H2('Loaded models'), html.Ul(list_seq)])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True

app.layout = html.Div([call_form(), loaded_models()])

if __name__ == '__main__':
    app.run_server(debug=True)