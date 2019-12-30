import pickle

from ch_pat_model import ChPatModel


class E063Model(ChPatModel):
    """Test model with simple AH rules."""

    def __init__(self):
        super().__init__()
        self.name = 'E06_3'
        self.full_name = 'Аутоиммунный тиреоидит'
        self._model_description = 'Diagnoses {} risk model'.format(self.name)
        # Feature order for model, don't change
        with open(r'OtherDiagnosesModel\common_features_{}.txt'.format(self.name)) as f:
            self.cols_for_model = f.read().split('\n')
        with open(r'OtherDiagnosesModel\feature_coding_dict.txt') as f:
            self.feature_coding = eval(f.read())
        self.result_name = 'states'
        self.dt_path = 'OtherDiagnosesModel/{}.pkl'.format(self.name)
        self.state_pred_model = pickle.load(open(self.dt_path, 'br'))
        self.title = 'Риск наличия сопутствующего заболевания : {} ({})'.format(self.full_name,
                                                                                self.name)

    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict
                                   and patient_dict[col] is not None,
                       self.cols_for_model))

    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][value]
        return value

    def apply(self, patient_dict):
        try:
            feature_vector = [[self.code_feature(col, patient_dict[col])
                               for col in self.cols_for_model]]
        except ValueError:
            return patient_dict

        state = self.state_pred_model.predict(feature_vector)[0]
        print(feature_vector)
        prob = self.state_pred_model.predict_proba(feature_vector)[0][1]

        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []
        my_prediction = {'title': self.title,
                         'source': 'Используется предсказательная модель',
                         'risk': prob,
                         'value': str(round(prob * 100, 1)) + '%'
                         }
        print(prob)
        if prob <= 0.5:
            my_prediction.update(
                {
                    'top_comment': 'Информация',
                    'color': 'green',
                    'risk_text': 'Низкий',
                    'comment': 'Дополнительная диагностика не требуется.',
                }
            )

        else:
            my_prediction.update(
                {
                    'top_comment': 'Опасное состояние',
                    'color': 'red',
                    'risk_text': 'Высокий',
                    'comment': 'Необходима дополнительная диагностика. ' +
                               'Возможно у пациент есть сопутствующий диагноз: {} ({})'.format(self.full_name,
                                                                                               self.name.replace('_',
                                                                                                                 '.')),
                }
            )

        res_dict[self.result_name].append(my_prediction)
        return res_dict


class I48Model(ChPatModel):
    """Test model with simple AH rules."""

    def __init__(self):
        super().__init__()
        self.name = 'I48'
        self.full_name = 'Фибрилляция и трепетание предсердий'
        self._model_description = 'Diagnoses {} risk model'.format(self.name)
        # Feature order for model, don't change
        with open(r'OtherDiagnosesModel\common_features_{}.txt'.format(self.name)) as f:
            self.cols_for_model = f.read().split('\n')
        with open(r'OtherDiagnosesModel\feature_coding_dict.txt') as f:
            self.feature_coding = eval(f.read())
        self.result_name = 'states'
        self.dt_path = 'OtherDiagnosesModel/{}.pkl'.format(self.name)
        self.state_pred_model = pickle.load(open(self.dt_path, 'br'))
        self.title = 'Риск наличия сопутствующего заболевания : {} ({})'.format(self.full_name,
                                                                                self.name)

    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict
                                   and patient_dict[col] is not None,
                       self.cols_for_model))

    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][value]
        return value

    def apply(self, patient_dict):
        try:
            feature_vector = [[self.code_feature(col, patient_dict[col])
                               for col in self.cols_for_model]]
        except ValueError:
            return patient_dict

        state = self.state_pred_model.predict(feature_vector)[0]
        print(feature_vector)
        prob = self.state_pred_model.predict_proba(feature_vector)[0][1]

        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []
        my_prediction = {'title': self.title,
                         'source': 'Используется предсказательная модель',
                         'risk': prob,
                         'value': str(round(prob * 100, 1)) + '%'
                         }
        print(prob)
        if prob <= 0.5:
            my_prediction.update(
                {
                    'top_comment': 'Информация',
                    'color': 'green',
                    'risk_text': 'Низкий',
                    'comment': 'Дополнительная диагностика не требуется.',
                }
            )

        else:
            my_prediction.update(
                {
                    'top_comment': 'Опасное состояние',
                    'color': 'red',
                    'risk_text': 'Высокий',
                    'comment': 'Необходима дополнительная диагностика. ' +
                               'Возможно у пациент есть сопутствующий диагноз: {} ({})'.format(self.full_name,
                                                                                               self.name.replace('_',
                                                                                                                 '.')),
                }
            )

        res_dict[self.result_name].append(my_prediction)
        return res_dict


class I50Model(ChPatModel):
    """Test model with simple AH rules."""

    def __init__(self):
        super().__init__()
        self.name = 'I50'
        self.full_name = 'Сердечная недостаточность'
        self._model_description = 'Diagnoses {} risk model'.format(self.name)
        # Feature order for model, don't change
        with open(r'OtherDiagnosesModel\common_features_{}.txt'.format(self.name)) as f:
            self.cols_for_model = f.read().split('\n')
        with open(r'OtherDiagnosesModel\feature_coding_dict.txt') as f:
            self.feature_coding = eval(f.read())
        self.result_name = 'states'
        self.dt_path = 'OtherDiagnosesModel/{}.pkl'.format(self.name)
        self.state_pred_model = pickle.load(open(self.dt_path, 'br'))
        self.title = 'Риск наличия сопутствующего заболевания : {} ({})'.format(self.full_name,
                                                                                self.name)

    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict
                                   and patient_dict[col] is not None,
                       self.cols_for_model))

    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][value]
        return value

    def apply(self, patient_dict):
        try:
            feature_vector = [[self.code_feature(col, patient_dict[col])
                               for col in self.cols_for_model]]
        except ValueError:
            return patient_dict

        state = self.state_pred_model.predict(feature_vector)[0]
        print(feature_vector)
        prob = self.state_pred_model.predict_proba(feature_vector)[0][1]

        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []
        my_prediction = {'title': self.title,
                         'source': 'Используется предсказательная модель',
                         'risk': prob,
                         'value': str(round(prob * 100, 1)) + '%'
                         }
        print(prob)
        if prob <= 0.5:
            my_prediction.update(
                {
                    'top_comment': 'Информация',
                    'color': 'green',
                    'risk_text': 'Низкий',
                    'comment': 'Дополнительная диагностика не требуется.',
                }
            )

        else:
            my_prediction.update(
                {
                    'top_comment': 'Опасное состояние',
                    'color': 'red',
                    'risk_text': 'Высокий',
                    'comment': 'Необходима дополнительная диагностика. ' +
                               'Возможно у пациент есть сопутствующий диагноз: {} ({})'.format(self.full_name,
                                                                                               self.name.replace('_',
                                                                                                                 '.')),
                }
            )

        res_dict[self.result_name].append(my_prediction)
        return res_dict


class I65_2Model(ChPatModel):
    """Test model with simple AH rules."""

    def __init__(self):
        super().__init__()
        self.name = 'I65_2'
        self.full_name = 'Закупорка и стеноз сонной артерии'
        self._model_description = 'Diagnoses {} risk model'.format(self.name)
        # Feature order for model, don't change
        with open(r'OtherDiagnosesModel\common_features_{}.txt'.format(self.name)) as f:
            self.cols_for_model = f.read().split('\n')
        with open(r'OtherDiagnosesModel\feature_coding_dict.txt') as f:
            self.feature_coding = eval(f.read())
        self.result_name = 'states'
        self.dt_path = 'OtherDiagnosesModel/{}.pkl'.format(self.name)
        self.state_pred_model = pickle.load(open(self.dt_path, 'br'))
        self.title = 'Риск наличия сопутствующего заболевания : {} ({})'.format(self.full_name,
                                                                                self.name)

    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict
                                   and patient_dict[col] is not None,
                       self.cols_for_model))

    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][value]
        return value

    def apply(self, patient_dict):
        try:
            feature_vector = [[self.code_feature(col, patient_dict[col])
                               for col in self.cols_for_model]]
        except ValueError:
            return patient_dict

        state = self.state_pred_model.predict(feature_vector)[0]
        print(feature_vector)
        prob = self.state_pred_model.predict_proba(feature_vector)[0][1]

        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []
        my_prediction = {'title': self.title,
                         'source': 'Используется предсказательная модель',
                         'risk': prob,
                         'value': str(round(prob * 100, 1)) + '%'
                         }
        print(prob)
        if prob <= 0.5:
            my_prediction.update(
                {
                    'top_comment': 'Информация',
                    'color': 'green',
                    'risk_text': 'Низкий',
                    'comment': 'Дополнительная диагностика не требуется.',
                }
            )

        else:
            my_prediction.update(
                {
                    'top_comment': 'Опасное состояние',
                    'color': 'red',
                    'risk_text': 'Высокий',
                    'comment': 'Необходима дополнительная диагностика. ' +
                               'Возможно у пациент есть сопутствующий диагноз: {} ({})'.format(self.full_name,
                                                                                               self.name.replace('_',
                                                                                                                 '.')),
                }
            )

        res_dict[self.result_name].append(my_prediction)
        return res_dict


class I67_2Model(ChPatModel):
    """Test model with simple AH rules."""

    def __init__(self):
        super().__init__()
        self.name = 'I67_2'
        self.full_name = 'Цереброваскулярные болезни'
        self._model_description = 'Diagnoses {} risk model'.format(self.name)
        # Feature order for model, don't change
        with open(r'OtherDiagnosesModel\common_features_{}.txt'.format(self.name)) as f:
            self.cols_for_model = f.read().split('\n')
        with open(r'OtherDiagnosesModel\feature_coding_dict.txt') as f:
            self.feature_coding = eval(f.read())
        self.result_name = 'states'
        self.dt_path = 'OtherDiagnosesModel/{}.pkl'.format(self.name)
        self.state_pred_model = pickle.load(open(self.dt_path, 'br'))
        self.title = 'Риск наличия сопутствующего заболевания : {} ({})'.format(self.full_name,
                                                                                self.name)

    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict
                                   and patient_dict[col] is not None,
                       self.cols_for_model))

    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][value]
        return value

    def apply(self, patient_dict):
        try:
            feature_vector = [[self.code_feature(col, patient_dict[col])
                               for col in self.cols_for_model]]
        except ValueError:
            return patient_dict

        state = self.state_pred_model.predict(feature_vector)[0]
        print(feature_vector)
        prob = self.state_pred_model.predict_proba(feature_vector)[0][1]

        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []
        my_prediction = {'title': self.title,
                         'source': 'Используется предсказательная модель',
                         'risk': prob,
                         'value': str(round(prob * 100, 1)) + '%'
                         }
        print(prob)
        if prob <= 0.5:
            my_prediction.update(
                {
                    'top_comment': 'Информация',
                    'color': 'green',
                    'risk_text': 'Низкий',
                    'comment': 'Дополнительная диагностика не требуется.',
                }
            )

        else:
            my_prediction.update(
                {
                    'top_comment': 'Опасное состояние',
                    'color': 'red',
                    'risk_text': 'Высокий',
                    'comment': 'Необходима дополнительная диагностика. ' +
                               'Возможно у пациент есть сопутствующий диагноз: {} ({})'.format(self.full_name,
                                                                                               self.name.replace('_',
                                                                                                                 '.')),
                }
            )

        res_dict[self.result_name].append(my_prediction)
        return res_dict


class M42_1Model(ChPatModel):
    """Test model with simple AH rules."""

    def __init__(self):
        super().__init__()
        self.name = 'M42_1'
        self.full_name = 'Остеохондроз позвоночника у взрослых'
        self._model_description = 'Diagnoses {} risk model'.format(self.name)
        # Feature order for model, don't change
        with open(r'OtherDiagnosesModel\common_features_{}.txt'.format(self.name)) as f:
            self.cols_for_model = f.read().split('\n')
        with open(r'OtherDiagnosesModel\feature_coding_dict.txt') as f:
            self.feature_coding = eval(f.read())
        self.result_name = 'states'
        self.dt_path = 'OtherDiagnosesModel/{}.pkl'.format(self.name)
        self.state_pred_model = pickle.load(open(self.dt_path, 'br'))
        self.title = 'Риск наличия сопутствующего заболевания : {} ({})'.format(self.full_name,
                                                                                self.name)

    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict
                                   and patient_dict[col] is not None,
                       self.cols_for_model))

    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][value]
        return value

    def apply(self, patient_dict):
        try:
            feature_vector = [[self.code_feature(col, patient_dict[col])
                               for col in self.cols_for_model]]
        except ValueError:
            return patient_dict

        state = self.state_pred_model.predict(feature_vector)[0]
        print(feature_vector)
        prob = self.state_pred_model.predict_proba(feature_vector)[0][1]

        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []
        my_prediction = {'title': self.title,
                         'source': 'Используется предсказательная модель',
                         'risk': prob,
                         'value': str(round(prob * 100, 1)) + '%'
                         }
        print(prob)
        if prob <= 0.5:
            my_prediction.update(
                {
                    'top_comment': 'Информация',
                    'color': 'green',
                    'risk_text': 'Низкий',
                    'comment': 'Дополнительная диагностика не требуется.',
                }
            )

        else:
            my_prediction.update(
                {
                    'top_comment': 'Опасное состояние',
                    'color': 'red',
                    'risk_text': 'Высокий',
                    'comment': 'Необходима дополнительная диагностика. ' +
                               'Возможно у пациент есть сопутствующий диагноз: {} ({})'.format(self.full_name,
                                                                                               self.name.replace('_',
                                                                                                                 '.')),
                }
            )

        res_dict[self.result_name].append(my_prediction)
        return res_dict


class AcuteHeartAttackModel(ChPatModel):
    """Test model with simple AH rules."""

    def __init__(self):
        super().__init__()
        self.name = 'predict_oim'
        self.full_name = 'Острый инфаркт миокарда'
        self._model_description = 'Diagnoses {} risk model'.format(self.name)
        # Feature order for model, don't change
        with open(r'OtherDiagnosesModel\common_features_oim.txt') as f:
            self.cols_for_model = f.read().split('\n')
        with open(r'OtherDiagnosesModel\feature_coding_dict.txt') as f:
            self.feature_coding = eval(f.read())
        self.result_name = 'states'
        self.dt_path = 'OtherDiagnosesModel/{}.pkl'.format(self.name)
        self.state_pred_model = pickle.load(open(self.dt_path, 'br'))
        self.title = 'Риск наличия сопутствующего заболевания : {} ({})'.format(self.full_name,
                                                                                self.name)
        self.name = 'ОИМ'

    def check_applicability(self, patient_dict):
        print([(col, col in patient_dict) for col in self.cols_for_model])
        return all(map(lambda col: col in patient_dict
                                   and patient_dict[col] is not None,
                       self.cols_for_model))

    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][value]
        return value

    def apply(self, patient_dict):
        try:
            print([(col, patient_dict[col]) for col in self.cols_for_model])
            feature_vector = [[self.code_feature(col, patient_dict[col])
                               for col in self.cols_for_model]]
        except ValueError:
            return patient_dict

        print(feature_vector)
        state = self.state_pred_model.predict(feature_vector)[0]
        prob = self.state_pred_model.predict_proba(feature_vector)[0][1]

        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []
        my_prediction = {'title': self.title,
                         'source': 'Используется предсказательная модель',
                         'risk': prob,
                         'value': str(round(prob * 100, 1)) + '%'
                         }
        print(prob)
        if prob <= 0.5:
            my_prediction.update(
                {
                    'top_comment': 'Информация',
                    'color': 'green',
                    'risk_text': 'Низкий',
                    'comment': 'Дополнительная диагностика не требуется.',
                }
            )

        else:
            my_prediction.update(
                {
                    'top_comment': 'Опасное состояние',
                    'color': 'red',
                    'risk_text': 'Высокий',
                    'comment': 'Необходима дополнительная диагностика. ' +
                               'Возможно у пациент был {} в прошлом'.format(self.full_name),
                }
            )

        res_dict[self.result_name].append(my_prediction)
        return res_dict
