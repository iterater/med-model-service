from enum import Enum
import ThromboembolicComplications.const as const
import re


class RiskFactor(Enum):
    STROKE = 1
    AGE_75_MORE = 2
    ARTERIAL_HYPERTENSION = 3
    DIABETES = 4
    HEART_FAILURE = 5
    VASCULAR_DISEASE = 6
    AGE_65_74 = 7
    IS_FEMALE = 8


class RiskDetector:

    def calculate_age(self, age):
        if age >= 75:
            return 2
        if age >= 65:
            return 1
        return 0

    def calculate_sex(self, sex):
        if sex == 'female':
            return 1
        return 0

    def calculate_stroke(self, info):
        if self.__find_using_re(words=const.STROKE_KEY_WORDS, text=info):
            return 2
        return 0

    def calculate_arterial_hypertension(self, info):
        if self.__find_using_re(words=const.HYPERTENSION_KEY_WORDS, text=info):
            return 1
        return 0

    def calculate_diabetes(self, info):
        if self.__find_using_re(words=const.DIABETES_KEY_WORDS, text=info):
            return 1
        return 0

    def calculate_heart_failure(self, info):
        if self.__find_using_re(words=const.HEART_FAILURE_KEY_WORDS, text=info):
            return 1
        return 0

    def calculate_vascular_disease(self, info):
        if self.__find_using_re(words=const.VASCULAR_DISEASE_KEY_WORDS, text=info):
            return 1
        return 0

    def __find_using_re(self, words, text):
        r = re.compile('|'.join([r'\b%s\b' % w for w in words]), flags=re.I)
        return len(r.findall(text.lower())) > 0
