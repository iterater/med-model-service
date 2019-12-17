# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 22:49:19 2019

@author: Katerina Bolgova
"""
from ch_pat_model import ChPatModel
from math import exp, pow


class ScoreModel(ChPatModel):
    def __init__(self):
        super().__init__()
        self._model_description = 'Systemic Coronary Risk Evaluation'
        self.cols_for_model = [
            'age',
            'sex',
            'smoking',
            'total_cholesterol',
            'max_sbp'
        ]
        self.feature_coding = {
            'sex': dict(zip(['female', 'male'], [0, 1])),
            'smoking': dict(zip([False, True], [0, 1]))
        }
        self.result_name = 'states'

    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict and patient_dict[col] is not None,
                       self.cols_for_model))

    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][value]
        return value

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        feature_vector = [self.code_feature(col, patient_dict[col])
                          for col in self.cols_for_model]
        # print(feature_vector)
        riskS = self.calcSCOREindex(int(feature_vector[0]), feature_vector[1], feature_vector[2],
                                    float(feature_vector[3]), int(feature_vector[4]))

        res_dict[self.result_name].append(
            {'title': '10-летний абсолютный риск развития фатальных сердечно-сосудистых осложнений',
             'comment': 'Определение риска смерти обследуемого пациента от ССЗ в ближайшие 10 лет.',
             'source': 'Источник: шкала SCORE'}
        )
        res_dict[self.result_name][-1]['value'] = riskS

        if riskS > 10:
            risk_text = 'Очень высокий'
            color = 'red'
            top_comment = 'Тяжелое состояние'
        elif riskS > 5:
            risk_text = 'Высокий'
            color = 'orange'
            top_comment = 'Опасное состояние'
        elif riskS > 1:
            risk_text = 'Умеренно повышенный'
            color = "yellow"
            top_comment = "Внимание!"
        else:
            risk_text = 'Низкий'
            color = "green"
            top_comment = "Информация"

        res_dict[self.result_name][-1]['risk_text'] = risk_text
        res_dict[self.result_name][-1]['color'] = color
        res_dict[self.result_name][-1]['top_comment'] = top_comment

        # print('res_dict', res_dict)
        return res_dict

    def calcSCOREindex(self, age=50, sex=0, smoker=1, cholesterol=3.0, SBP=130):
        # print(str(age)+' : '+sex)
        scoreIDX = 0
        # /*****************           ПРИСВАИВАЕМ КОЭФФИЦИЕНТЫ ИЗ ТАБЛИЦЫ А (В ЗАВИСИМОСТИ ОТ ПОЛА)   ******************************/
        alphaCHD = alphaNonCHD = 0
        pCHD = pNonCHD = 0
        if (sex == 1):
            alphaCHD = -21.0
            alphaNonCHD = -25.7
            pCHD = 4.62
            pNonCHD = 5.47
        else:
            alphaCHD = -28.7
            alphaNonCHD = -30.0
            pCHD = 6.23
            pNonCHD = 6.42
        # /******************************/

        # /*****************   STEP 1. Calculate the underlying risks for CHD & nonCHD CVD             **********************/
        # print(alphaCHD + " "+ age+"   " + alphaCHD + "   " +pCHD)
        S0ageCHD = exp(-(exp(alphaCHD) * pow(age - 20, pCHD)))
        S0ageNonCHD = exp(-(exp(alphaNonCHD) * pow(age - 20, pNonCHD)))

        S0age10CHD = exp(-(exp(alphaCHD) * pow(age - 10, pCHD)))
        S0age10NonCHD = exp(-(exp(alphaNonCHD) * pow(age - 10, pNonCHD)))
        # /******************************/

        # /*****************   STEP 2. calculate the weighted sum, w, of the risk factors cholesterol, smoking and systolic blood pressure             **********************/
        wCHD = 0.24 * (cholesterol - 6) + 0.018 * (SBP - 120) + 0.71 * smoker
        wNonCHD = 0.02 * (cholesterol - 6) + 0.022 * (SBP - 120) + 0.63 * smoker
        # /******************************/

        # /*****************   STEP 3. Combine the underlying risks calculated in step 1 with the weighted sum of a person's risk factors from step 2 **********************/
        SageCHD = pow(S0ageCHD, exp(wCHD))
        SageNonCHD = pow(S0ageNonCHD, exp(wNonCHD))
        Sage10CHD = pow(S0age10CHD, exp(wCHD))
        Sage10NonCHD = pow(S0age10NonCHD, exp(wNonCHD))
        # /******************************/

        # /*****************   STEP 4. calculate the 10-year survival probability based on the survival probability **********************/
        S10ageCHD = Sage10CHD / SageCHD
        S10ageNonCHD = Sage10NonCHD / SageNonCHD
        # /******************************/

        # /*****************   STEP 5. Calculate the 10 year risk for each end-point  **********************/
        Risk10CHD = 1 - S10ageCHD
        Risk10NonCHD = 1 - S10ageNonCHD
        # /******************************/

        # /*****************   STEP 6. Combine the risks  **********************/
        scoreIDX = round((Risk10CHD + Risk10NonCHD) * 100, 2)

        return scoreIDX


class TotalRiskModel(ChPatModel):

    def __init__(self):
        super().__init__()
        self._model_description = 'TotalRiskModel'
        self.cols_for_model = [
            'age',
            'sex',
            'smoking',
            'height',
            'weight',
            'total_cholesterol',
            'max_sbp',
            'ah',
            'ah_stage'
            'fbs',
            'gtt',
            'creatinine',
            'total_cholesterol',
            'ldl_cholesterol',
            'hdl_cholesterol',
            'triglycerides',
            'family_early_heart_disease',
            'pulse_pressure',
            'carotid_wall_thickening',
            'pulse_wave_velocity',
            'ankle_brachia_sbp_index',
            'chronic_kidney_disease',
            'microalbuminuria',
            'cerebrovascular_disease',
            'coronary_heart_disease',
            'heart_failure',
            'severe_retinopathy'
        ]
        # =============================================================================
        #        self.feature_coding = {
        #             'sex': dict(zip(['female', 'male'], [0, 1])),
        #             'smoking': dict(zip([False, True], [0, 1])),
        #             'ah': dict(zip([False, True], [0, 1])),
        #             'gtt': dict(zip([False, True], [0, 1])),
        #             'microalbuminuria': dict(zip([False, True], [0, 1])),
        #             'severe_retinopathy': dict(zip([False, True], [0, 1])),
        #             'carotid_wall_thickening': dict(zip([False, True], [0, 1])),
        #             'cerebrovascular_disease': dict(zip([False, True], [0, 1])),
        #             'coronary_heart_disease': dict(zip([False, True], [0, 1]))

        #        }
        # =============================================================================
        self.result_name = 'states'

    def check_applicability(self, patient_dict):
        return ('age' in patient_dict) and ('sex' in patient_dict) and ('max_sbp' in patient_dict) and (
                'smoking' in patient_dict) and ('ah' in patient_dict) and ('ah_stage' in patient_dict) and (
                       'height' in patient_dict) and ('weight' in patient_dict)
        # return all(map(lambda col: col in patient_dict and patient_dict[col] is not None,
        # self.cols_for_model))

    def apply(self, patient_dict):
        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        riskTotal = self.commonRiskSSZ(patient_dict)
        # print(riskTotal)
        res_dict[self.result_name].append({'title': 'Оценка общего (суммарного) сердечно-сосудистого риска',
                                           'source': 'Клинические рекомендации "Артериальная гипертония у взрослых" 2016 года',
                                           'comment': 'Оценка осуществляется согласно клиническим рекомендациям "Артериальная гипертония у взрослых" 2016 г'}
                                          )

        if riskTotal == 0:
            value = "Отсутствует"
            color = 'green'
            top_comment = "Информация"
        elif riskTotal == 1:
            value = "Низкий"
            color = 'yellow'
            top_comment = "Внимание!"
        elif riskTotal == 2:
            value = "Умеренный"
            color = 'orange'
            top_comment = "Внимание!"
        elif riskTotal == 3:
            value = "Высокий"
            color = 'red'
            top_comment = 'Опасное состояние'
        elif riskTotal == 4:
            value = "Очень высокий"
            color = 'red'
            top_comment = 'Тяжелое состояние'

        res_dict[self.result_name][-1]['risk_text'] = value
        res_dict[self.result_name][-1]['value'] = value
        res_dict[self.result_name][-1]['color'] = color
        res_dict[self.result_name][-1]['top_comment'] = top_comment

        return res_dict

    # %%
    def getRiskFactorsCnt(self, params):
        rfCnt = 0
        IMT = 0.0
        dislypid = 0
        if ("weight" in params.keys()) and ("height" in params.keys()):
            w = int(params.get("weight"))
            h = int(params.get("height")) / 100.0
            IMT = w / (h * h)
        if params.get("sex") == "male":
            rfCnt += 1
            # print("male")
            if int(params.get("age")) >= 55:
                rfCnt += 1
                # print("male + age")
            if "waistline" in params.keys() and int(params.get("waistline")) >= 102:
                rfCnt += 1
                # print("male + waistline")
            if "family_early_heart_disease" in params.keys() and int(params.get("family_early_heart_disease")) < 55:
                rfCnt += 1
                # print("male + family_early_heart_disease")
            if "hdl_cholesterol" in params.keys() and float(params.get("hdl_cholesterol")) < 1:
                dislypid += 1
        else:
            if int(params.get("age")) >= 65:
                rfCnt += 1
                # print("female + age")
            if "waistline" in params.keys() and int(params.get("waistline")) >= 88:
                rfCnt += 1
                # print("female + waistline")
            if "family_early_heart_disease" in params.keys() and int(params.get("family_early_heart_disease")) < 65:
                rfCnt += 1
                # print("female + family_early_heart_disease")
            if "hdl_cholesterol" in params.keys() and float(params.get("hdl_cholesterol")) < 1.2:
                dislypid += 1
        if "smoking" in params.keys() and params.get("smoking"):
            rfCnt += 1
            # print("smoking")

        if "total_cholesterol" in params.keys() and float(params.get("total_cholesterol")) > 4.9:
            dislypid += 1
        if "ldl_cholesterol" in params.keys() and float(params.get("ldl_cholesterol")) > 3.0:
            dislypid += 1
        if "triglycerides" in params.keys() and float(params.get("triglycerides")) > 1.7:
            dislypid += 1

        if dislypid > 0:
            rfCnt += 1
            # print("dislypid")

        if "fbs" in params.keys() and float(params.get("fbs")) >= 5.6 and float(params.get("fbs")) <= 6.9:
            rfCnt += 1
            # print("fbs")
        if "gtt" in params.keys() and params.get("gtt"):
            rfCnt += 1
            # print("gtt")
        if IMT >= 30:
            rfCnt += 1
            # print("IMT")

        return rfCnt

    # %%
    def getPOMCnt(self, params):
        pomCnt = 0
        if "creatinine" in params.keys():
            creatinine = float(params.get("creatinine"))
            age = int(params.get("age"))
            ckd_epi = 0
            ###расчет рСКФ
            mdrd = 186 * pow(creatinine, -1.154) * pow(age, -0.203)
            kok_gau = 88 * (140 - age) * float(params.get("weight")) / 72.0 * creatinine
            if params.get("sex") == "female":
                mdrd *= 0.742
                kok_gau *= 0.85
                if age <= 62 and creatinine <= 0.7:
                    ckd_epi = 144 * pow(creatinine / 0.7, -0.329) * pow(0.993, age)
                if age > 62 and creatinine > 0.7:
                    ckd_epi = 144 * pow(creatinine / 0.7, -1.209) * pow(0.993, age)
            else:
                if age <= 80 and creatinine <= 0.9:
                    ckd_epi = 141 * pow(creatinine / 0.9, -0.411) * pow(0.993, age)
                if age > 80 and creatinine > 0.9:
                    ckd_epi = 141 * pow(creatinine / 0.9, -1.209) * pow(0.993, age)

            if ("chronic_kidney_disease" in params.keys() and int(
                    params.get("chronic_kidney_disease")) > 2 and mdrd >= 30 and mdrd <= 60) or (kok_gau < 60) or (
                    ckd_epi >= 30 and ckd_epi <= 60):
                pomCnt += 1
                # print("formulas")
        if "pulse_pressure" in params.keys() and int(params.get(
                "pulse_pressure")) >= 60:  ####!!!!!!!!!!!!!!!!!!!!! TODO: учесть пожтлой и старческий возраст
            pomCnt += 1
            # print("pulse_pressure")
        if "pulse_wave_velocity" in params.keys() and int(params.get("pulse_wave_velocity")) > 10:
            pomCnt += 1
            # print("pulse_wave_velocity")
        if "ankle_brachia_sbp_index" in params.keys() and float(params.get("ankle_brachia_sbp_index")) < 0.9:
            pomCnt += 1
            # print("ankle_brachia_sbp_index")
        if "carotid_wall_thickening" in params.keys() and params.get("carotid_wall_thickening"):
            pomCnt += 1
            # print("carotid_wall_thickening")
        if "microalbuminuria" in params.keys() and params.get("microalbuminuria"):
            pomCnt += 1
            # print("microalbuminuria")
        if "severe_retinopathy" in params.keys() and params.get("severe_retinopathy"):
            pomCnt += 1
            # print("severe_retinopathy")
        return pomCnt

    # %%
    def commonRiskSSZ(self, params):
        commRisk = 0
        AH = 0

        if ("ah" in params.keys()):
            if params.get("ah"):
                if ("ah_stage" in params.keys()):
                    AH = int(params.get("ah_stage"))
                else:
                    AH = 1

        if AH > 0:
            # print("Степень АГ " + str(AH))

            RFCount = self.getRiskFactorsCnt(params)
            # print("Факторы риска " + str(RFCount))
            POMCount = self.getPOMCnt(params)
            # print("POM " + str(POMCount))
            cvb = False
            if "cerebrovascular_disease" in params.keys():
                cvb = params.get("cerebrovascular_disease")
            ssz = False
            if "heart_failure" in params.keys() and int(params.get("heart_failure")) > 1:
                ssz = True
            if "coronary_heart_disease" in params.keys() and params.get("coronary_heart_disease"):
                ssz = True
            hbp = 0
            if "chronic_kidney_disease" in params.keys():
                hbp = params.get("chronic_kidney_disease")

            diabetes = False
            if "diabetes" in params.keys():
                diabetes = params.get("diabetes")

            # print(str(cvb) + '   ' + str(ssz) + '   ' + str(hbp) + '    ' + str(diabetes))

            if (cvb or ssz or hbp > 3) or (diabetes and POMCount > 0) or (diabetes and RFCount > 0):
                return 4  ## очень высокий риск

            if POMCount > 0 or hbp == 3 or diabetes:
                if AH == 3:
                    return 4
                else:
                    return 3

            if RFCount > 3:
                return 3

            if RFCount == 1 or RFCount == 2:
                if AH == 1:
                    return 2
                else:
                    return 3

            return AH

        return commRisk
