import pickle
from ch_pat_model import ChPatModel
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

class DiabetesPrediction(ChPatModel):
    def __init__(self):
        self._model_description = 'DM risk for 5 years'
        self._need_features = ['bmi', 'mean_dbp', 'age', 'mean_sbp', "weight", "bsa"]
        self._model_file = 'DiabetesRisk/DiabetesPrediction.pkl'
        self._model = 'Diab5YearsRisk'
        self._fname = "diab_5_years_risk.pkl"
        self.comment = "Расcчитан в результате предсказательного моделирования,достоверность 80%"

    def take_features(self, patient_dict):
        def float_value(value, feat):
            if feat != "sex":
                TrueFalseDict = {'True': 1, 'False': 0}
                if value not in TrueFalseDict:
                    return float(value)
                else:
                    return TrueFalseDict[value]
            else:
                return value

        feat_for_model = {feat: float_value(value, feat) for feat, value in zip(patient_dict, patient_dict.values()) if
                          feat in self._need_features}

        if ("weight" in patient_dict) & ("height" in patient_dict):
            feat_for_model['bmi'] = int(patient_dict["weight"]) / (int(patient_dict["height"]) / 100) ** 2
        return feat_for_model

    def check_applicability(self, patient_dict, take_features=take_features):
        feat_for_model = take_features(self, patient_dict)
        return len(feat_for_model) == len(self._need_features)

    def diab_predict(self, patient_dict, take_features=take_features):
        feat_for_model = take_features(self, patient_dict)
        X = pd.DataFrame(feat_for_model, index=[0])[self._need_features]
        model = pickle.load(open(self._model_file, "rb"))
        predict = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]

        if probability < 0.5:
            probability = 0
        probability_to_percent = str(round(probability * 100, 0)) + "%"

        if predict:
            risk_text = "Высокий риск"
        else:
            risk_text = "Невысокий риск"

        return {'title': '5-летний риск сахарного диабета 2 типа', 'value': probability_to_percent,
                'risk_text': risk_text, 'comment': self.comment}

    def findrisk_func(self, patient_dict, take_features=take_features):
        feat_for_model = take_features(self, patient_dict)
        findrisk = pickle.load(open(self._model_file, "rb"))

        def ScoreInfindrisk(Value, Feature, dictionary=findrisk):
            ValueInInterval = list(dictionary[Feature])[0]  # За странное значение 0 баллов
            for Interval in dictionary[Feature]:
                if (Value >= Interval[0]) & (Value <= Interval[1]):
                    ValueInInterval = Interval
            Score = dictionary[Feature][ValueInInterval]
            return Score

        SumScore = sum([ScoreInfindrisk(float(Value), Feature, findrisk) for Feature, Value in
                        zip(feat_for_model, feat_for_model.values()) if (Feature != "sex") & (Feature != "waistline")])

        dict_waistline = {"male": {(0, 94): 0, (94, 102): 3, (102, 300): 4},
                          "female": {(0, 80): 0, (80, 88): 3, (88, 300): 4}}
        SumScore += ScoreInfindrisk(Value=feat_for_model['waistline'], Feature=feat_for_model["sex"],
                                    dictionary=dict_waistline)

        probability = ScoreInfindrisk(Feature=feat_for_model['sex'], Value=SumScore, dictionary=findrisk)

        if SumScore <= 12:
            risk_text = "Низкий риск"
        elif (SumScore > 12) & (SumScore <= 20):
            risk_text = "Умеренный риск"
        elif SumScore > 20:
            risk_text = "Высокий риск"

        return {'title': '10-летний риск сахарного диабета 2 типа', 'value': probability,
                'risk_text': risk_text, 'comment': self.comment, 'SumScore': SumScore}

    predict_models = {'Diab5YearsRisk': diab_predict, "FINDRISK": findrisk_func}

    def apply(self, patient_dict, take_features=take_features, predict_models=predict_models):
        feat_for_model = take_features(self, patient_dict=patient_dict)
        res_dict = patient_dict.copy()

        if 'states' not in res_dict:
            res_dict['states'] = []

        model = predict_models[self._model]

        res_dict['states'] += [model(self, feat_for_model)]
        return res_dict


class FINDRISK(DiabetesPrediction):
    def __init__(self):
        self._model_description = 'DM risk for 10 years'
        self._model_description_full = "FINDRISK_full_description.pkl"
        self._need_features = ['sex', 'age', 'bmi', 'physical_activity',
                               'often_vegetables', "AG_drags", 'degree_kinship_with_diabetic', 'waistline',
                               'high_glucose']
        self._model_file = 'DiabetesRisk/FINDRISK.pkl'
        self._model = "FINDRISK"
        self.comment = "Расcчитан c помощью шкалы FINDRISK, достоверность 85%"
        self._fname = "findrisk.pkl"

    def show_model_description_full(self):
        open(self._model_description_full, "rb")()


# a = DiabetesPrediction()
# dicipat = {'weight': 80, 'height': "80", 'mean_dbp': "100", 'age': 80, 'mean_sbp': 80, "bsa": 2}
# print(DiabetesPrediction.check_applicability(a, dicipat))

# a = FINDRISK()
# dicipat = {'icd10': 'I10', 'max_sbp': '120', 'mean_sbp': '110', 'sex': 'male', 'age': '55', 'anamnesis': 'хсн аг пол',
#            'height': '165', 'weight': '80', 'smoking': 'False', 'alcohol_regularity': 'rarely', 'creatinine_level': '3',
#            'effusions': 'False', 'arrhythmia': 'False', 'stenocardia': 'False', 'heart_attack': 'False',
#            'mean_dbp': '80', 'bsa': '1.73', 'physical_activity': 'False', 'often_vegetables': 'False',
#            'AG_drags': 'False', 'waistline': '90', 'degree_kinship_with_diabetic': '0', 'high_glucose': 'False'}
# print(FINDRISK.apply(a, dicipat))
