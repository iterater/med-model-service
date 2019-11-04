from ThromboembolicComplications.ModelDataPreparator import *

model_path = '/Users/kabyshev/Desktop/Developing/chronic-patient-model-service/models/personal_data_with_diagnosises.csv'

dp = ModelDataPreparator(
    features_file_path='/Users/kabyshev/Desktop/Developing/medicine/Table2Object174part1.txt',
    persons_file_path='/Users/kabyshev/Downloads/Table2Download153ObjectFeatures.txt',
    csv_file_path=model_path,
    features_list=['Name', 'Массив_последнего_диагноза', 'Клинический_диагноз'],
    personal_data_list=['Name', 'Пол', 'Дата_рождения'],
    join_key='Name'
)
dp.start()
dp.classify(
    model_path=model_path,
    updated_model_path='/Users/kabyshev/Desktop/Developing/chronic-patient-model-service/models/new_personal_data_with_diagnosises.csv'
)
