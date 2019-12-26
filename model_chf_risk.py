import pickle
import numpy as np
from ch_pat_model import ChPatModel


class CHFRiskModel(ChPatModel):
    """Prediction of CHF risk for 1 year for AH patients older than 55 y.o.
    """

    def __init__(self):
        super().__init__()
        self._model_description = '1 year CHF risk prediction'
        self.model_path = 'CHFRiskModel/chf_risk_rf_bigger_feature_set.pkl'
        self.chf_risk_model = pickle.load(open(self.model_path, 'br'))
        self.features = ['sex', 'age', 'height', 'weight', 'num_packs_smoke', 'smoking',
                         'alcohol_regularity', 'left_ventricular_ejection_fraction',
                         'left_ventricular_hypertrophy', 'left_atrial_expansion', 'blood_group',
                         'mean_sbp', 'max_sbp', 'min_sbp', 'std_sbp', 'mean_dbp', 'max_dbp',
                         'min_dbp', 'std_dbp', 'waistline', 'bmi', 'bsa', 'diabetes',
                         'coronary_heart_disease', 'heart_attack',
                         ]

        self.categorical_features = ['sex', 'alcohol_regularity', ]
        self.title = 'ХСН'
        self.result_name = 'states'
        self.source = 'Рассчитан в соответствии с результатами предсказательного моделирования' \
                      ' с достоверностью 73% (f1-score)'

    def check_applicability(self, patient_dict):
        # print('ХСН привет')
        if len(self.features) == len(set(patient_dict.keys()).intersection(set(self.features))):
            # print(len(set(patient_dict.keys()).intersection(set(self.features))))
            return all(map(lambda col: col in patient_dict and patient_dict[col] != 'None',
                           self.features))
        else:
            return False

    def preprocess_featuers(self, feature, value):
        if feature in self.categorical_features:
            if feature == 'sex':
                return ['male', 'female'].index(value)
            elif feature == 'alcohol_regularity':
                return ['deny', 'rarely', 'weekly', 'regular'].index(value)
        else:
            if value in ['True', 'False']:
                return float(bool(value))
            else:
                return float(value)

    def check_obesity(self, bmi):
        if float(bmi) > 30:
            return True
        else:
            return False

    def apply(self, patient_dict):
        patient_dict['obesity'] = self.check_obesity(patient_dict['bmi'])
        res_dict = patient_dict.copy()
        # обновление признаков с сохранением порядка, не изменять
        self.features = ['sex', 'age', 'height', 'weight', 'num_packs_smoke', 'smoking',
                         'alcohol_regularity', 'left_ventricular_ejection_fraction',
                         'left_ventricular_hypertrophy', 'left_atrial_expansion', 'blood_group',
                         'mean_sbp', 'max_sbp', 'min_sbp', 'std_sbp', 'mean_dbp', 'max_dbp',
                         'min_dbp', 'std_dbp', 'waistline', 'bmi', 'bsa', 'diabetes',
                         'obesity', 'coronary_heart_disease', 'heart_attack',
                         ]
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        feature_vector = np.array([self.preprocess_featuers(col, patient_dict[col])
                                   for col in self.features]).reshape(1, -1)

        chf_class_probability = self.chf_risk_model.predict_proba(feature_vector)[0][1]
        self.features = ['sex', 'age', 'height', 'weight', 'num_packs_smoke', 'smoking',
                         'alcohol_regularity', 'left_ventricular_ejection_fraction',
                         'left_ventricular_hypertrophy', 'left_atrial_expansion', 'blood_group',
                         'mean_sbp', 'max_sbp', 'min_sbp', 'std_sbp', 'mean_dbp', 'max_dbp',
                         'min_dbp', 'std_dbp', 'waistline', 'bmi', 'bsa', 'diabetes',
                         'coronary_heart_disease', 'heart_attack',
                         ]

        if chf_class_probability < 0.5:
            self.risk_text = 'Низкий'
            color = 'green'
            top_comment = 'Информация'
        elif chf_class_probability < 0.7:
            self.risk_text = 'Средний'
            color = 'yellow'
            top_comment = 'Внимание!'
        else:
            self.risk_text = 'Высокий'
            color = 'red'
            top_comment = 'Опасное состояние'

        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        value = str(np.round(chf_class_probability * 100, 2)) + ' %'
        res_dict[self.result_name].append({
            'title': self.title,
            'source': self.source,
            'risk_perc': chf_class_probability * 100,
            'value': value,
            'risk_text': self.risk_text,
            'comment': 'ХСН будет диагностирована в течение года с вероятностью {}'.format(value),
            'color': color,
            'top_comment': top_comment,

        })

        if 'states' not in res_dict:
            res_dict['states'] = []

        class_value = np.ceil(chf_class_probability)
        comment = 'Вероятно ХСН {}будет диагностирована пациенту в течение следующего года'.format('не ' if class_value == 0 else '')
        res_dict['states'].append({
            'title': 'Диагностика ХСН в течение года',
            'value': class_value,
            'source': self.source,
            'comment': comment,
            'color': color,
            'top_comment': top_comment,
        })

        # print('CHF result', res_dict)
        return res_dict
