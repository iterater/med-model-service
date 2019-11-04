import pandas as pd


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
