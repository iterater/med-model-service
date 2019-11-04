import pandas as pd
import ThromboembolicComplications.Helpers as helper
from ThromboembolicComplications.Estimator import *
from ThromboembolicComplications.PatientInfo import PatientInfo

class ModelDataPreparator:

    def __init__(self, features_file_path, persons_file_path, csv_file_path, features_list, personal_data_list, join_key):
        self.features_file_path = features_file_path
        self.persons_file_path = persons_file_path
        self.csv_file_path = csv_file_path
        self.features_list = features_list
        self.personal_data_list = personal_data_list
        self.join_key = join_key

    def start(self):
        print('Reading features file...')
        features_df = pd.read_csv(self.features_file_path, encoding='cp1251', sep='\t', engine='python')
        print('Filtering features file...')
        features_df_filtered = features_df.dropna(subset=self.features_list)[self.features_list]
        print('Features preparation complete.\nBefore:', len(features_df), '\nAfter: ', len(features_df_filtered))

        print('\nReading persons file...')
        persons_df = pd.read_csv(self.persons_file_path, encoding='cp1251', sep='\t', engine='python')
        print('Filtering persons file...')
        persons_df_filtered = persons_df.dropna(subset=self.personal_data_list)[self.personal_data_list]
        print('Persons preparation complete.\nBefore:', len(persons_df), '\nAfter: ', len(persons_df_filtered))

        out = pd.merge(features_df_filtered, persons_df_filtered, on=self.join_key)
        self.__save(model=out, save_file_path=self.csv_file_path)

        return out

    def __save(self, model, save_file_path):
        print('\nSaving...')
        model.to_csv(path_or_buf=save_file_path)
        print('Saved', len(model))

    def classify(self, model_path, updated_model_path):
        model = pd.read_csv(model_path)
        model['Age'] = -1
        model['Sex'] = 0
        model['Stroke_feature'] = False
        model['Arterial_hypertension_feature'] = False
        model['Diabetes_feature'] = False
        model['Heart_failure_feature'] = False
        model['Vascular_disease_feature'] = False
        model['Class'] = 0

        number_of_patients = 0
        print("Iterate...")

        for index, row in model.iterrows():
            age = helper.calculate_age(row['Дата_рождения'])
            if age < 0:
                continue
            diagnosis = row['Массив_последнего_диагноза'] + row['Клинический_диагноз']
            info = PatientInfo(
                age=age,
                sex='female' if row['Пол'] == 'Женский' else 'male',
                diagnosis=diagnosis
            )
            feature, risk_point = Estimator.calculate_risk_point(data=info)

            model.at[index, 'Age'] = age
            model.at[index, 'Sex'] = 1 if row['Пол'] == 'Женский' else 0
            model.at[index, 'Stroke_feature'] = feature.stroke_feature
            model.at[index, 'Arterial_hypertension_feature'] = feature.arterial_hypertension_feature
            model.at[index, 'Diabetes_feature'] = feature.diabetes_feature
            model.at[index, 'Heart_failure_feature'] = feature.heart_failure_feature
            model.at[index, 'Vascular_disease_feature'] = feature.vascular_disease_feature
            model.at[index, 'Class'] = RiskDetector.is_has(words=['Тромбоэмболия', 'Фибриляция', 'Трепетание'], diagnosis=diagnosis)

            if risk_point >= 4:
                number_of_patients += 1
        print("Found patients with risk point >= 4:", number_of_patients)

        self.__save(model, updated_model_path)
