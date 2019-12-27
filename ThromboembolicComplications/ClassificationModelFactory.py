import pandas as pd
import numpy as np
import ThromboembolicComplications.Helpers as helper
from ThromboembolicComplications.Estimator import *
from ThromboembolicComplications.PatientInfo import PatientInfo

from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


class ClassificationModelFactory:

    @staticmethod
    def prepare_data(features_file_path, persons_file_path, csv_file_path, features_list, personal_data_list, join_key):
        print('Reading features file', features_file_path)
        features_df = pd.read_csv(features_file_path, encoding='cp1251', sep='\t', engine='python')
        print('Filtering features file...')
        features_df_filtered = features_df.dropna(subset=features_list)[features_list]
        print('Features preparation complete.\nBefore elements:', len(features_df),
              '\nAfter elements: ', len(features_df_filtered))

        print('Reading persons file', persons_file_path)
        persons_df = pd.read_csv(persons_file_path, encoding='cp1251', sep='\t', engine='python')
        print('Filtering persons file...')
        persons_df_filtered = persons_df.dropna(subset=personal_data_list)[personal_data_list]
        print('Persons preparation complete.\nBefore elements:', len(persons_df),
              '\nAfter elements: ', len(persons_df_filtered))

        out = pd.merge(features_df_filtered, persons_df_filtered, on=join_key)
        ClassificationModelFactory.__save(model=out, save_file_path=csv_file_path)

        return out

    @staticmethod
    def __save(model, save_file_path):
        print('==> Saving model to csv file at', save_file_path)
        model.to_csv(path_or_buf=save_file_path)
        print('Done. Saved elements:', len(model))

    @staticmethod
    def classify(model_path, updated_model_path):
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
        print("Iterate rows in the model...")

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
            model.at[index, 'Class'] = RiskDetector.find_class(diagnosis=diagnosis)

            if risk_point >= 4:
                number_of_patients += 1
        print("Found patients with risk point >= 4:", number_of_patients)

        ClassificationModelFactory.__save(model, updated_model_path)

        return model

    """
    Creates a new classifier model.
    
    Parameters
    ----------
    classifier_type : string, optional (default='rf')
        Specifies the type of classifier.
        It must be one of 'rf', 'svm', 'gb', 'dt'.
        If none or undefuned value is given, 'rf' will be used.
        
    df : dataframe, optional (default='None')
        Dataframe for training.
        If none is given, df_path parameter will be used.
    
    df_path : string, optional (default='None')
        If none is given, 'df' parameter will be used.
        If none is given for both 'df' and 'df_path', it will occur an error and return 'None'.
        
    n_estimators : integer, optional (default=100)
        The number of estimators in RF and GB classifiers.
    """
    @staticmethod
    def create_model(classifier_type="rf", df=None, df_path=None, n_estimators=100):

        if df is None:
            if df_path is None:
                print("Error. Data frame and his path are None. The method requires one of this params.")
                return None
            print("==> Reading CSV file at", df_path)
            df = pd.read_csv(df_path)

        features = ['Sex', 'Age', 'Stroke_feature', 'Arterial_hypertension_feature', 'Diabetes_feature',
                    'Heart_failure_feature', 'Vascular_disease_feature']

        print("Creating model...")

        # Separate majority and minority classes
        df_majority = df[df.Class == 0]
        df_minority = df[df.Class == 1]

        # Downsample majority class
        df_majority_downsampled = resample(df_majority,
                                           replace=False,
                                           n_samples=len(df_minority),
                                           random_state=123)

        # Combine minority class with downsampled majority class
        df_downsampled = pd.concat([df_majority_downsampled, df_minority])

        print("Using", classifier_type, "classifier")

        if classifier_type == 'svc':
            classifier = SVC()
        elif classifier_type == 'gb':
            classifier = GradientBoostingClassifier(n_estimators=n_estimators, random_state=123)
        elif classifier_type == 'dt':
            classifier = DecisionTreeClassifier(random_state=123)
        else:
            classifier = RandomForestClassifier(n_estimators=n_estimators, random_state=123)

        return ClassificationModelFactory.__train_classifier(classifier, df_downsampled, features)

    @staticmethod
    def __train_classifier(classifier, df, features):
        X = df[features].values
        y = df.Class.values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=123)
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        print("Training model...")

        classifier = classifier.fit(X_train, y_train)
        print("\nAccuracy on training set: {:.3f}".format(classifier.score(X_train, y_train)))
        print("Accuracy on test set: {:.3f}".format(classifier.score(X_test, y_test)))

        try:
            importance = classifier.feature_importances_
            indices = np.argsort(importance)[::-1]
            print("\n=== Feature ranking ===")
            for index, feature in enumerate(features[:-1]):
                print("%d. %s (%f)" % (index + 1, features[indices[index]], importance[indices[index]]))
        except AttributeError:
            print("Classifier has not contain feature_importances_ attribute")

        y_pred = classifier.predict(X_test)

        print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
        print("\nReport:\n", classification_report(y_test, y_pred))
        print("Accuracy score:", accuracy_score(y_test, y_pred))

        return classifier
