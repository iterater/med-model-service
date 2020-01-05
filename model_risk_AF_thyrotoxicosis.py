import pickle
from ch_pat_model import ChPatModel
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


class AFPrediction(ChPatModel):
    def __init__(self):
        self._model_description = 'Risk AF (patients with thyrotoxicosis)'
        self._need_features = ['sex',
                               'age',
                               'bmi',
                               'smoking',
                               'total_cholesterol',
                               'triglycerides',
                               'ldl_cholesterol',
                               'hdl_cholesterol',
                               'creatinine',
                               'HGB_blood_level',
                               'i493',
                               'i500',
                               'ah',
                               'diabetes',
                               'NormCarMet',
                               'ImpairedFastingGlycemia',
                               'gtt']

        self._model_file = 'AFRiskThyrotoxicosis/risk_AF_in_TT.pickle'
        self._model = 'AF_TT_Risk'
        self._fname = "risk_AF_TT.pkl"
        self.comment = "Расcчитан в результате предсказательного моделирования"

    def take_features(self, patient_dict):
        def float_value(value):
            TrueFalseDict = {'True': 1, 'False': 0, "male": 1, "female": 0}
            if value not in TrueFalseDict:
                return float(value)
            else:
                return TrueFalseDict[value]

        def ValueIsCorrect(Value):
            CorrectStrValues = ["True", "False", "male", "female"]
            return (str(Value).replace(".", "", 1).isdigit()) | (str(Value) in CorrectStrValues)

        feat_for_model = {feat: float_value(value) for feat, value in zip(patient_dict, patient_dict.values()) if
                          (feat in self._need_features) & (ValueIsCorrect(value))}

        if ("weight" in patient_dict) & ("height" in patient_dict):
            if ValueIsCorrect(patient_dict["weight"]) & ValueIsCorrect(patient_dict["height"]):
                feat_for_model['bmi'] = int(patient_dict["weight"]) / (int(patient_dict["height"]) / 100) ** 2

        # Создаем 2 признака - NormCarMet - нормальный УО, ImpairedFastingGlycemia - нарушенная глюкоза натощак.
        feat_for_model['NormCarMet'], feat_for_model['ImpairedFastingGlycemia'] = 0, 0
        if ("fbs" in patient_dict):
            if ValueIsCorrect(patient_dict["fbs"]):
                fbs = float_value(patient_dict["fbs"])
                feat_for_model['NormCarMet'] += int(fbs >= 6.1)
                feat_for_model['ImpairedFastingGlycemia'] += int(fbs >= 6.1)
        elif ('gtt' in patient_dict):
            if ValueIsCorrect(patient_dict["gtt"]):
                gtt = float_value(patient_dict["gtt"])
                feat_for_model['NormCarMet'] = int((feat_for_model['NormCarMet']) | int(gtt))
                feat_for_model['ImpairedFastingGlycemia'] = int((feat_for_model['ImpairedFastingGlycemia']) | int(gtt))
        return feat_for_model

    def check_applicability(self, patient_dict, take_features=take_features):
        feat_for_model = take_features(self, patient_dict.copy())
        return set(feat_for_model) == set(self._need_features)

    def AF_predict(self, patient_dict, take_features=take_features):
        feat_for_model = take_features(self, patient_dict.copy())
        X = pd.DataFrame(feat_for_model, index=[0])[self._need_features]
        model = pickle.load(open(self._model_file, "rb"))
        predict = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]

        if probability < 0.5:
            probability = 0
        probability_to_percent = str(round(probability * 100, 0)) + "%"

        if predict == 1:
            risk_text = "Высокий"
            color = "red"
            top_comment = 'Опасное состояние'
        else:
            risk_text = "Невысокий"
            color = 'green'
            top_comment = 'Информация'

        return {'title': 'Риск развития Фибрилляции Предсердий (для пациентов с тиреотоксикозом)',
                'value': probability_to_percent,
                'risk_text': risk_text,
                'comment': self.comment,
                'source': "Используется предсказательная модель (достоверность 73%)",
                'color': color,
                'top_comment': top_comment
                }

    def apply(self, patient_dict, take_features=take_features, model=AF_predict):
        feat_for_model = take_features(self, patient_dict=patient_dict.copy())
        res_dict = patient_dict.copy()

        if 'states' not in res_dict:
            res_dict['states'] = []

        res_dict['states'] += [model(self, feat_for_model.copy())]
        return res_dict


# a = AFPrediction()
# dicipat = {'sex': "female",
#            'age': "55",
#            'height': "165",
#            "weight": "60",
#            'smoking': "False",
#            'total_cholesterol': "3.0",
#            'triglycerides': "1.5",
#            'ldl_cholesterol': "2.0",
#            'hdl_cholesterol': "2.1",
#            'creatinine': "2",
#            'HGB_blood_level': "138",
#            'i493': "1",
#            'i500': "1",
#            'ah': "1",
#            'diabetes': "False",
#            'gtt': "1"}

# print(AFPrediction.check_applicability(a, dicipat))
# print(AFPrediction.apply(a, dicipat))
