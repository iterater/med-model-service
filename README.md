# Chronic patient model service
Predictive modeling of chronic patients within a Flask service

Running with python:
```bash
python ch_pat_service.py
```

Running with flask:
```bash
export FLASK_APP=~/chronic-patient-model-service/ch_pat_service.py
cd ~/chronic-patient-model-service
flask run --host=0.0.0.0 &
```

Killing flask process:
```bash
killall flask
```

# TODO
* HTML/CSS template
* Images in response
* Model chains and dependencies
* Dockerize
