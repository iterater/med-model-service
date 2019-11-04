import ThromboembolicComplications.const as const
import re


class RiskDetector:

    @staticmethod
    def is_has(words, diagnosis):
        return 1 if RiskDetector.__find_using_re(words=words, text=diagnosis) else 0

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

    @staticmethod
    def __find_using_re(words, text):
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        r = re.compile('|'.join([r'\b%s\b' % w for w in words]), flags=re.I)
        return len(r.findall(text)) > 0
