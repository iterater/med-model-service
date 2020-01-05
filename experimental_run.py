import requests
import timeit
import joblib
import datetime
from ch_pat_models_management import load_params, generate_default_data

params = load_params('params_list.csv')
in_dict = generate_default_data(params)
url = 'http://195.222.181.179:5000/ch_pat_service'
    
def request():        
    resp = requests.post(url, json=in_dict)
    return resp.status_code == 200

def single_series(n, i):
    print('Run {} with {} requests'.format(i, n))
    t = timeit.timeit(request, number=n)
    return t

if __name__ == '__main__':
    for n_par in range(1,7):
        start_date_time = datetime.datetime.now()
        run_res = joblib.Parallel(n_jobs=n_par)(joblib.delayed(single_series)(100, i) for i in range(16))
        stop_date_time = datetime.datetime.now()        
        dt = (stop_date_time - start_date_time) / datetime.timedelta(milliseconds=1)
        print('{}, {}, {}'.format(n_par, dt, ', '.join(run_res)))

