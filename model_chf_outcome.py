import pickle
import numpy as np
from ch_pat_model import ChPatModel


class CHFOutcomeClassifier(ChPatModel):
    """Prediction of CHF episode outcome
    """

    def __init__(self):
        super().__init__()
        self._model_description = 'CHF episode outcome prediction'
        self.model_path = 'CHFOutcomeClassifier/chf_outcome_rf.pkl'
        self.chf_outcome_model = pickle.load(open(self.model_path, 'br'))
        self.features = ['episode_type',
                         'i10',
                         'd752',
                         'z941',
                         'i48',
                         'i258',
                         'c857',
                         'd45',
                         'i712',
                         'i119',
                         'i208',
                         'pct_max',
                         'i250',
                         'i480',
                         'd509',
                         'i493',
                         'c900',
                         'i489',
                         'mon_max',
                         'i481']

        self.title = 'ХСН исход'
        self.result_name = 'states'
        self.source = 'Рассчитан в соответствии с результатами предсказательного моделирования' \
                      ' с достоверностью 65,2% (f1-score для трех классов)'

    def check_applicability(self, patient_dict):
        if len(self.features) == len(set(patient_dict.keys()).intersection(set(self.features))):
            return all(map(lambda col: col in patient_dict and patient_dict[col] != 'None',
                           self.features))
        else:
            return False


    def apply(self, patient_dict):
        # patient_dict['obesity'] = self.check_obesity(patient_dict['bmi'])
        res_dict = patient_dict.copy()

        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        feature_vector = np.array([float(patient_dict[col])
                                   for col in self.features]).reshape(1, -1)

        chf_outcome_type = self.chf_outcome_model.predict(feature_vector)[0]
        print(chf_outcome_type)

        if chf_outcome_type == 2:
            self.risk_text = 'Улучшение'
            color = 'green'
            top_comment = 'Информация'
        elif chf_outcome_type < 1:
            self.risk_text = 'Без изменений'
            color = 'yellow'
            top_comment = 'Внимание!'
        else:
            self.risk_text = 'Летальный исход'
            color = 'red'
            top_comment = 'Опасное состояние'

        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        res_dict[self.result_name].append({
            'title': self.title,
            'source': self.source,
            'risk_perc': '',
            'value': chf_outcome_type,
            'risk_text': self.risk_text,
            'comment': 'Исход эпизода для пациента с диагнозом ХСН {}'.format(chf_outcome_type),
            'color': color,
            'top_comment': top_comment,

        })

        if 'states' not in res_dict:
            res_dict['states'] = []

        class_value = chf_outcome_type
        comment = 'Вероятно, исход эпизода ХСН будет завершен с результатом: {} '.format(self.risk_text)
        res_dict['states'].append({
            'title': 'Прогноз исхода эпизода с ХСН',
            'value': class_value,
            'source': self.source,
            'comment': comment,
            'color': color,
            'top_comment': top_comment,
        })

        return res_dict
