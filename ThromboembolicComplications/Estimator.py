from ThromboembolicComplications.RiskDetector import *
import ThromboembolicComplications.PatientInfo as PatientInfo


class Point:
    def __init__(self, stroke_feature, arterial_hypertension_feature, diabetes_feature, heart_failure_feature,
                 vascular_disease_feature):
        self.stroke_feature = stroke_feature
        self.arterial_hypertension_feature = arterial_hypertension_feature
        self.diabetes_feature = diabetes_feature
        self.heart_failure_feature = heart_failure_feature
        self.vascular_disease_feature = vascular_disease_feature


class Estimator:

    @staticmethod
    def calculate_risk_point(data: PatientInfo):

        detector = RiskDetector()
        age = detector.calculate_age(data.age)
        sex = detector.calculate_sex(data.sex)
        stroke = detector.calculate_stroke(data.diagnosis)
        hypertension = detector.calculate_arterial_hypertension(data.diagnosis)
        diabetes = detector.calculate_diabetes(data.diagnosis)
        heart_failure = detector.calculate_heart_failure(data.diagnosis)
        vascular_disease = detector.calculate_vascular_disease(data.diagnosis)

        point = Point(bool(stroke), bool(hypertension), bool(diabetes), bool(heart_failure), bool(vascular_disease))

        return point, sum([age, sex, stroke, hypertension, diabetes, heart_failure, vascular_disease])

    @staticmethod
    def find_complications_frequency(scale):
        if scale > 10 or scale < 0:
            return -1
        points = {
            0: 0,
            1: 1.3,
            2: 2.2,
            3: 3.2,
            4: 4.0,
            5: 6.7,
            6: 9.8,
            7: 9.6,
            8: 6.7,
            9: 15.2,
            10: 15.2
        }
        return points[scale]

    @staticmethod
    def category(scale):
        if scale > 10 or scale < 0:
            return ""
        if scale >= 2:
            return "1 “крупный” фактор риска или ≥2 клинически значимых “не крупных” факторов риска"
        if scale == 1:
            return "1 клинически значимый “не крупный” фактор риска"
        return "Нет факторов риска"

    @staticmethod
    def therapy(scale):
        if scale > 10 or scale < 0:
            return ""
        if scale >= 2:
            return """
            антагонист витамина К ≥2 (например, варфарин) с целевым МНО 2,5 (2,0-3,0) 
            (при механических протезах клапанов сердца целевое МНО может быть выше)
            """
        if scale == 1:
            return "пероральный антикоагулянт 1 (предпочтительно) или аспирин 75-325 мг в сутки"
        return "аспирин 75-325 мг в сутки или 0 отсутствие антитромботической терапии (предпочтительно)"
