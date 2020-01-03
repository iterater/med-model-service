kb_list = {
    'ACUTEHEARTATTACKMODEL.PKL': ['AH', 'ACS'],
    'AH_STATE_CLASSIFIER_MODEL.PKL': ['AH'],
    'CHF_OUTCOME_MODEL.PKL': ['CHF'],
    'CHF_RISK.PKL': ['CHF'],
    'CHF_STROKE_MODEL.PKL': ['CHF'],
    'CHF_TAKH_MODEL.PKL': ['CHF'],
    'CHF_TRANS_HEART_MODEL.PKL': ['CHF'],
    'DIAB_5_YEARS_RISK.PKL': ['DM'],
    'E063MODEL.PKL': ['DM'],
    'FINDRISK.PKL': ['DM'],
    'I48MODEL.PKL': ['AH', 'ACS', 'CHF'],
    'I50MODEL.PKL': ['CHF'],
    'I65_2MODEL.PKL': ['AH'],
    'I67_2MODEL.PKL': ['AH'],
    'M42_1MODEL.PKL': ['*'],
    'SCOREMODEL.PKL': ['AH'],
    'STUB_MODEL.PKL': ['*'],
    'TEST_AH_MODEL.PKL': ['*'],
    'THROMBOEMBOLIC_COMPLICATIONS_MODEL.PKL': ['AH', 'CHF'],
    'THROMBOEMBOLIC_COMPLICATIONS_SCALE_MODEL.PKL': ['AH', 'CHF'],
    'TOTALRISKMODEL.PKL': ['AH']
}


def get_kb_stats(model_fnames):    
    res = dict()
    for m_file in model_fnames:
        if m_file.upper() in kb_list:            
            for kb_name in kb_list[m_file.upper()]:
                if kb_name not in res:
                    res[kb_name] = []
                res[kb_name].append(m_file)
    return res
