import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import ch_pat_models_management
import json
import re

models = ch_pat_models_management.load_models('models')
params = ch_pat_models_management.load_params('params_list.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True


def call_form():
    par_to_fg = lambda par: dbc.FormGroup([dbc.Label(par['label']),
                                           dbc.Input(id=par['id'], value=par['default'])])
    form_seq = [par_to_fg(par) for par in params]
    return dbc.Form([html.H2('Параметры')] + form_seq + [dbc.Button("Запуск", id="call_button")], id='input_from')


def loaded_models():
    list_seq = [html.Li(m.model_description) for m in models]
    return html.Div([html.H2('Загружены модели'), html.Ul(list_seq)])


def build_all_states(states):
    s_style = {'background-color': 'blanchedalmond',
               'margin': '10px',
               'padding': '5px'}
    s_to_html = lambda s: [html.B(s['title']),
                           html.P(s.get('top_comment'), style={'background-color': s.get('color')}),
                           html.P(s['value']),
                           html.P('Риск: {}'.format(s.get('risk_text'))),
                           html.P(s['comment'], style={'font-size': '70%'})]
    return html.Div([html.H3('States')] + [html.Div(s_to_html(s), style=s_style) for s in states])


def build_all_errors(errors):
    e_style = {'background-color': 'red', 'margin': '10px', 'padding': '5px'}
    e_to_html = lambda e: [html.B('Ошибка валидации'), html.P('Параметр: ' + e[0])] + \
                          [html.P(e_msg, style={'font-size': '70%'}) for e_msg in e[1]]
    return html.Div([html.H3('Errors')] + [html.Div(e_to_html(e), style=e_style) for e in errors])


def biud_all_rec(rec_string):
    r_style_rec = {'background-color': 'aquamarine',
                   'margin': '10px',
                   'padding': '5px'}
    r_style_no_rec = {'background-color': 'salmon',
                   'margin': '10px',
                   'padding': '5px'}    
    r_parts_rec = re.findall('Рекомендована терапия: ([^.]*)\\.', rec_string)
    r_parts_no_rec = re.findall('Не рекомендована терапия: ([^.]*)\\.', rec_string)
    rec_to_html = lambda s, titl: [html.B(titl),  html.P(s, style={'font-size': '70%'})]
    return html.Div([html.H3('Сформированные рекомендации')] + 
                    [html.Div(rec_to_html(s, 'Рекомендовано'), style=r_style_rec) for s in r_parts_rec] + 
                    [html.Div(rec_to_html(s, 'Не рекомендовано'), style=r_style_no_rec) for s in r_parts_no_rec])


@app.callback(Output('output_div', 'children'), [Input('call_button', 'n_clicks'), Input('input_from', 'children')])
def data_process_callback(n, input_form_content):
    input_to_tuple = lambda i: (i['props']['id'], i['props']['value'])
    fg_to_input = lambda fg: [input_to_tuple(i) for i in fg['props']['children'] if i['type'] == 'Input'][0]
    if n is None:
        return html.Div('-')
    else:
        in_dict = dict(fg_to_input(inp) for inp in input_form_content if inp['type'] == 'FormGroup')
        out_dict = ch_pat_models_management.call_models(in_dict, models)
        content = []
        if 'states' in out_dict:
            content.append(build_all_states(out_dict['states']))
        if ('errors' in out_dict) and (len(out_dict['errors']) > 0):
            content.append(build_all_errors(out_dict['errors'].items()))
        if ('recommendations' in out_dict):
            content.append(biud_all_rec(out_dict['recommendations']))
        return html.Div(content)


app.layout = dbc.Container([dbc.Row([
    dbc.Col([call_form(), html.Br(), loaded_models()]),
    dbc.Col([html.H2('Результат'), html.Div(id='output_div', children=[])])])])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, use_reloader=False)
