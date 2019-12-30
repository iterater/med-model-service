import pickle
import numpy as np
from ch_pat_model import ChPatModel


class CHFTransHeartClassifier(ChPatModel):
    """Prediction of transplanted heart for CHF patient
    """

    def __init__(self):
        super().__init__()
        self._model_description = 'Prediction of transplanted heart for CHF patient'
        self.model_path = 'CHFTransHeartClassifier/chf_trans_heart_rf.pkl'
        self.chf_trans_heart_model = pickle.load(open(self.model_path, 'br'))
        self.features = ['age',
                         'i252',
                         'i208',
                         'i119',
                         'pdw_max',
                         'sex',
                         'bil_max',
                         'neut1_max',
                         'neut_max',
                         'i48',
                         'mpw_max',
                         'i352',
                         'pct_max',
                         'i251',
                         'hct_max',
                         'plt_max']
        self.categorical_features = ['sex']

        self.title = 'Трансплантация сердца для пациента с ХСН'
        self.result_name = 'states'
        self.source = 'Рассчитан в соответствии с результатами предсказательного моделирования' \
                      ' с достоверностью 86,8% (f1-score для двух классов)'

    def check_applicability(self, patient_dict):
        print(self.features, len(self.features), len(set(patient_dict.keys()).intersection(set(self.features))))

        if len(self.features) == len(set(patient_dict.keys()).intersection(set(self.features))):
            return all(map(lambda col: col in patient_dict and patient_dict[col] != 'None',
                           self.features))
        else:
            return False

    def preprocess_featuers(self, feature, value):
        if feature in self.categorical_features:
            if feature == 'sex':
                return ['male', 'female'].index(value)
        else:
            if value in ['True', 'False']:
                return float(bool(value))
            else:
                return float(value)

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()

        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        feature_vector = np.array([self.preprocess_featuers(col, patient_dict[col])
                                   for col in self.features]).reshape(1, -1)

        chf_trans_heart_type = self.chf_trans_heart_model.predict(feature_vector)[0]

        if chf_trans_heart_type == 0:
            self.risk_text = 'Отсутствие трасплантации сердца'
            color = 'green'
            top_comment = 'Информация'

        else:
            self.risk_text = 'Наличие трансплантации сердца'
            color = 'red'
            top_comment = 'Опасное состояние'

        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        res_dict[self.result_name].append({
            'title': self.title,
            'source': self.source,
            'risk_perc': '',
            'value': chf_trans_heart_type,
            'risk_text': self.risk_text,
            'comment': 'Наличие трансплантированного сердца {}'.format(chf_trans_heart_type),
            'color': color,
            'top_comment': top_comment,

        })

        if 'states' not in res_dict:
            res_dict['states'] = []

        class_value = chf_trans_heart_type
        comment = 'Вероятно, у пациента была трансплантация сердца {} '.format('не ' if class_value == 0 else '')
        res_dict['states'].append({
            'title': 'Предсказание трансплантации сердца',
            'value': class_value,
            'source': self.source,
            'comment': comment,
            'color': color,
            'top_comment': top_comment,
        })

        return res_dict
