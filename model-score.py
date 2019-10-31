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
        self.result_name = 'risks'
        
    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict and patient_dict[col] is not None,
                       self.cols_for_model))
        
    def code_feature(self, col_name, value):
        if value is None:
            raise ValueError
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][self.try_cast(value)]
        return value

    @staticmethod
    def try_cast(value):
        try:
            return eval(value)
        except NameError:
            return value
        
    def apply(self, patient_dict):
        # TODO: добавить заполнение пропусков
        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        feature_vector = [[self.code_feature(col, patient_dict[col])
                           for col in self.cols_for_model]]

        # 0 - вторичная, 1 - первичная
        riskS = self.calcSCOREindex(feature_vector[0], feature_vector[1], feature_vector[2], feature_vector[3], feature_vector[4])

        # TODO: добавить комментарий к болезни
        res_dict[self.result_name].append({'title': 'SCORE',
                                           'comment': 'Определение риска смерти обследуемого пациента от ССЗ в ближайшие 10 лет.'}
                                          )
        res_dict[self.result_name][-1]['risk_perc'] = riskS
        
        if riskS > 5:
            res_dict[self.result_name][-1]['risk_text'] = 'высокий'
        else:
            res_dict[self.result_name][-1]['risk_text'] = 'низкий'
        
        print('res_dict', res_dict)
        return res_dict
    
    def calcSCOREindex(age = 40, sex = 0, smoker = 1, cholesterol = 3.0, SBP = 130):
        #print(str(age)+' : '+sex)    
        scoreIDX = 0 
    #/*****************           ПРИСВАИВАЕМ КОЭФФИЦИЕНТЫ ИЗ ТАБЛИЦЫ А (В ЗАВИСИМОСТИ ОТ ПОЛА)   ******************************/    
        alphaCHD = alphaNonCHD = 0
        pCHD = pNonCHD = 0
        if (sex==1):
            alphaCHD = -21.0
            alphaNonCHD = -25.7
            pCHD = 4.62
            pNonCHD = 5.47
        else:
            alphaCHD = -28.7
            alphaNonCHD = -30.0
            pCHD = 6.23
            pNonCHD = 6.42
     #/******************************/
            
    #/*****************   STEP 1. Calculate the underlying risks for CHD & nonCHD CVD             **********************/
        S0ageCHD = exp(-(exp(alphaCHD)*pow(age-20,pCHD)))
        S0ageNonCHD = exp(-(exp(alphaNonCHD)*pow(age-20,pNonCHD)))
            
        S0age10CHD = exp(-(exp(alphaCHD)*pow(age-10,pCHD)))
        S0age10NonCHD = exp(-(exp(alphaNonCHD)*pow(age-10,pNonCHD)))
    #/******************************/
            
    #/*****************   STEP 2. calculate the weighted sum, w, of the risk factors cholesterol, smoking and systolic blood pressure             **********************/
        wCHD = 0.24*(cholesterol-6) + 0.018*(SBP-120) + 0.71*smoker
        wNonCHD = 0.02*(cholesterol-6) + 0.022*(SBP-120) + 0.63*smoker
    #/******************************/
            
    #/*****************   STEP 3. Combine the underlying risks calculated in step 1 with the weighted sum of a person's risk factors from step 2 **********************/
        SageCHD = pow(S0ageCHD,exp(wCHD))
        SageNonCHD = pow(S0ageNonCHD,exp(wNonCHD))
        Sage10CHD = pow(S0age10CHD,exp(wCHD))
        Sage10NonCHD = pow(S0age10NonCHD,exp(wNonCHD))
    #/******************************/
            
    #/*****************   STEP 4. calculate the 10-year survival probability based on the survival probability **********************/        
        S10ageCHD = Sage10CHD / SageCHD
        S10ageNonCHD = Sage10NonCHD / SageNonCHD
    #/******************************/
            
    #/*****************   STEP 5. Calculate the 10 year risk for each end-point  **********************/   
        Risk10CHD = 1 - S10ageCHD
        Risk10NonCHD = 1 - S10ageNonCHD
    #/******************************/
            
    #/*****************   STEP 6. Combine the risks  **********************/   
        scoreIDX = round((Risk10CHD + Risk10NonCHD)*100,2)
        
        return scoreIDX
    
    
class TotalRiskModel(ChPatModel):
    
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
        self.result_name = 'risks'
        
    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict and patient_dict[col] != 'None',
                       self.cols_for_model))
        
    def code_feature(self, col_name, value):
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][self.try_cast(value)]
        return value

    @staticmethod
    def try_cast(value):
        try:
            return eval(value)
        except NameError:
            return value
        
    def apply(self, patient_dict):
        # TODO: добавить заполнение пропусков
        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        feature_vector = [[self.code_feature(col, patient_dict[col])
                           for col in self.cols_for_model]]

        # 0 - вторичная, 1 - первичная
        riskS = self.calcSCOREindex(feature_vector[0], feature_vector[1], feature_vector[2], feature_vector[3], feature_vector[4])

        # TODO: добавить комментарий к болезни
        res_dict[self.result_name].append({'title': 'SCORE',
                                           'comment': 'Определение риска смерти обследуемого пациента от ССЗ в ближайшие 10 лет.'}
                                          )
        res_dict[self.result_name][-1]['risk_perc'] = riskS
        
        if riskS > 5:
            res_dict[self.result_name][-1]['risk_text'] = 'высокий'
        else:
            res_dict[self.result_name][-1]['risk_text'] = 'низкий'
        
        print('res_dict', res_dict)
        return res_dict
    
    def calcSCOREindex(age = 40, sex = 0, smoker = 1, cholesterol = 3.0, SBP = 130):
        #print(str(age)+' : '+sex)    
        scoreIDX = 0 
    #/*****************           ПРИСВАИВАЕМ КОЭФФИЦИЕНТЫ ИЗ ТАБЛИЦЫ А (В ЗАВИСИМОСТИ ОТ ПОЛА)   ******************************/    
        alphaCHD = alphaNonCHD = 0
        pCHD = pNonCHD = 0
        if (sex==1):
            alphaCHD = -21.0
            alphaNonCHD = -25.7
            pCHD = 4.62
            pNonCHD = 5.47
        else:
            alphaCHD = -28.7
            alphaNonCHD = -30.0
            pCHD = 6.23
            pNonCHD = 6.42
     #/******************************/
            
    #/*****************   STEP 1. Calculate the underlying risks for CHD & nonCHD CVD             **********************/
        S0ageCHD = exp(-(exp(alphaCHD)*pow(age-20,pCHD)))
        S0ageNonCHD = exp(-(exp(alphaNonCHD)*pow(age-20,pNonCHD)))
            
        S0age10CHD = exp(-(exp(alphaCHD)*pow(age-10,pCHD)))
        S0age10NonCHD = exp(-(exp(alphaNonCHD)*pow(age-10,pNonCHD)))
    #/******************************/
            
    #/*****************   STEP 2. calculate the weighted sum, w, of the risk factors cholesterol, smoking and systolic blood pressure             **********************/
        wCHD = 0.24*(cholesterol-6) + 0.018*(SBP-120) + 0.71*smoker
        wNonCHD = 0.02*(cholesterol-6) + 0.022*(SBP-120) + 0.63*smoker
    #/******************************/
            
    #/*****************   STEP 3. Combine the underlying risks calculated in step 1 with the weighted sum of a person's risk factors from step 2 **********************/
        SageCHD = pow(S0ageCHD,exp(wCHD))
        SageNonCHD = pow(S0ageNonCHD,exp(wNonCHD))
        Sage10CHD = pow(S0age10CHD,exp(wCHD))
        Sage10NonCHD = pow(S0age10NonCHD,exp(wNonCHD))
    #/******************************/
            
    #/*****************   STEP 4. calculate the 10-year survival probability based on the survival probability **********************/        
        S10ageCHD = Sage10CHD / SageCHD
        S10ageNonCHD = Sage10NonCHD / SageNonCHD
    #/******************************/
            
    #/*****************   STEP 5. Calculate the 10 year risk for each end-point  **********************/   
        Risk10CHD = 1 - S10ageCHD
        Risk10NonCHD = 1 - S10ageNonCHD
    #/******************************/
            
    #/*****************   STEP 6. Combine the risks  **********************/   
        scoreIDX = round((Risk10CHD + Risk10NonCHD)*100,2)
        
        return scoreIDX