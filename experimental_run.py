import requests
import timeit
from ch_pat_models_management import load_params, generate_default_data

params = load_params('params_list.csv')
in_dict = generate_default_data(params)
url = 'http://195.222.181.179:5000/ch_pat_service'
    
def request():        
    resp = requests.post(url, json=in_dict)

if __name__ == '__main__':
    t = timeit.timeit(request, number=100)
    print(t)

