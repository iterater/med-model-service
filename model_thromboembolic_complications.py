from ch_pat_model import ChPatModel
from ThromboembolicComplications.ClassificationModelFactory import *
import pickle
import os


class ThromboembolicComplicationsScaleModel(ChPatModel):

    """Model for predicting the thromboembolic complications in atrial fibrillation (based on the scale)"""
    def __init__(self):
        super().__init__()

        self._model_description = 'Thromboembolic complications predicting model (by scale)'

    def check_applicability(self, patient_dict):
        return ('age' in patient_dict) and ('sex' in patient_dict) and ('anamnesis' in patient_dict)

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()
        if 'states' not in res_dict:
            res_dict['states'] = []

        age = int(patient_dict['age'])
        sex = str(patient_dict['sex'])
        diagnosis = str(patient_dict['anamnesis'])

        info = PatientInfo(age=age, sex=sex, diagnosis=diagnosis)
        risk_point = Estimator.calculate_risk_point(data=info)
        complications_frequency = Estimator.find_complications_frequency(risk_point)

        res_dict['states'].append(
            {
                'title': 'Сумма баллов по шкале CHA2DS2-VASc',
                'value': risk_point,
                'comment': Estimator.category(risk_point)
            }
        )
        res_dict['states'].append(
            {
                'title': 'Ожидаемая частота инсультов за год',
                'value': str(complications_frequency) + '%',
                'comment': 'Рекомендуется: ' + Estimator.therapy(risk_point)
            }
        )
        return res_dict


class ThromboembolicComplicationsModel(ChPatModel):

    def __init__(self):
        super().__init__()

        self._features_file_path = '/Users/kabyshev/Desktop/Developing/medicine/Table2Object174part1.txt',
        self._persons_file_path = '/Users/kabyshev/Downloads/Table2Download153ObjectFeatures.txt'
        self._model_description = 'Thromboembolic complications predicting model'
        self._ready_classifier_path = 'ThromboembolicComplications/rfc_model.pkl'

        if not os.path.isfile(self._ready_classifier_path):
            self.classifier = self.__create_classifier()
        else:
            self.classifier = pickle.load(open(self._ready_classifier_path, 'rb'))

    def check_applicability(self, patient_dict):
        return ('age' in patient_dict) and ('sex' in patient_dict) and ('anamnesis' in patient_dict)

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()

        if 'states' not in res_dict:
            res_dict['states'] = []

        age = int(patient_dict['age'])
        sex = str(patient_dict['sex'])
        diagnosis = str(patient_dict['anamnesis'])
        info = PatientInfo(age=age, sex=sex, diagnosis=diagnosis)

        feature, risk_point = Estimator.calculate_risk_point(data=info)
        predicted_class = self.classifier.predict([
            [age, 1 if patient_dict['sex'] == 'female' else 0, feature.stroke_feature,
             feature.arterial_hypertension_feature, feature.diabetes_feature, feature.heart_failure_feature, feature.vascular_disease_feature ]
        ])

        res_dict['states'].append(
            {
                'title': 'Риск',
                'value': 'Высокий' if predicted_class[0] == 1 else 'Низкий',
                'comment': ''
            }
        )
        return res_dict

    def __create_classifier(self):
        model_path = 'models/personal_data_with_diagnosises.csv'

        if not os.path.isfile(model_path):
            ClassificationModelFactory.prepare_data(
                features_file_path=self._features_file_path,
                persons_file_path=self._persons_file_path,
                csv_file_path=model_path,
                features_list=['Name', 'Массив_последнего_диагноза', 'Клинический_диагноз'],
                personal_data_list=['Name', 'Пол', 'Дата_рождения'],
                join_key='Name'
            )
            classified_model = ClassificationModelFactory.classify(
                model_path=model_path,
                updated_model_path=model_path
            )
            model = ClassificationModelFactory.create_model(df=classified_model, n_estimators=200)
        else:
            model = ClassificationModelFactory.create_model(df_path=model_path, n_estimators=200)

        print("===> Saving the ready model...")
        pickle.dump(model, open(self._ready_classifier_path, 'wb'))
        print("Done.")

        return model

