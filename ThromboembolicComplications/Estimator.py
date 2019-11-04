from ThromboembolicComplications.RiskDetector import *
import ThromboembolicComplications.PatientInfo as PatientInfo


class Estimator:

    @staticmethod
    def calculate_risk_point(data: PatientInfo):
        detector = RiskDetector()
        point = 0
        point += detector.calculate_age(data.age)
        point += detector.calculate_sex(data.sex)
        point += detector.calculate_stroke(data.diagnosis)
        point += detector.calculate_arterial_hypertension(data.diagnosis)
        point += detector.calculate_diabetes(data.diagnosis)
        point += detector.calculate_heart_failure(data.diagnosis)
        point += detector.calculate_vascular_disease(data.diagnosis)
        return point

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
            Антагонист витамина К ≥2 (например, варфарин) с целевым МНО 2,5 (2,0-3,0) 
            (при механических протезах клапанов сердца целевое МНО может быть выше)
            """
        if scale == 1:
            return "Пероральный антикоагулянт 1 (предпочтительно) или аспирин 75-325 мг в сутки"
        return "Аспирин 75-325 мг в сутки или 0 отсутствие антитромботической терапии (предпочтительно)"
