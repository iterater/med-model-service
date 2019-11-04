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
        self.__save(model=out)

        return out

    def __save(self, model):
        print('\nSaving...')
        model.to_csv(path_or_buf=self.csv_file_path)
        print('Saved', len(model))

    def classify(self, model_path):
        model = pd.read_csv(model_path)
        model['Class'] = 0
        number_of_patients = 0
        print("Iterate...")
        for index, row in model.iterrows():
            age = helper.calculate_age(row['Дата_рождения'])
            if age < 0:
                continue
            info = PatientInfo(
                age=age,
                sex='female' if row['Пол'] == 'Женский' else 'male',
                diagnosis=row['Массив_последнего_диагноза'] + row['Клинический_диагноз']
            )
            risk_point = Estimator.calculate_risk_point(data=info)

            if risk_point >= 4:
                number_of_patients += 1
                model.at[index, 'Class'] = 1
        print("Found patients with risk point >= 4:", number_of_patients)
        self.__save(model)
