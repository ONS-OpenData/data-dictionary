# reading in from csvs
import pandas as pd
import datetime

# points to folder of metadata csvs
location = "cantabular/ar2776-c21ew_metadata-v1-5_cantab_20230905-66/"

def run():
    variable = "hrp_economic_activity"
    variable_details = get_variable_details(variable)
    return variable_details


def get_variable_details(variable):
    variable_df = pd.read_csv(f"{location}Variable.csv", dtype=str)
    df = variable_df[variable_df["Variable_Mnemonic"] == variable]
    
    if len(df) == 0:
        raise Exception(f"Cannot find variable {variable}")
    assert len(df) == 1, f"found more than one line of data for the variable {variable}"

    variable_mnemonic = variable
    
    variable_details = {'en': {}, 'cy': {}}
    
    variable_details['en']['title'] = df.iloc[0]['Variable_Title'].strip()
    variable_details['en']['mnemonic'] = df.iloc[0]['Variable_Mnemonic']
    variable_details['en']['2011 mnemonic'] = df.iloc[0]['Variable_Mnemonic_2011']
    variable_details['en']['type_code'] = df.iloc[0]['Variable_Type_Code']
    variable_details['en']['topic_code'] = df.iloc[0]['Topic_Mnemonic']
    variable_details['en']['description'] = df.iloc[0]['Variable_Description']
    variable_details['en']['number of classifications'] = df.iloc[0]['Number_Of_Classifications']
    variable_details['en']['statistical unit'] = df.iloc[0]['Statistical_Unit']
    variable_details['en']['comparability'] = df.iloc[0]['Comparability_Comments']
    variable_details['en']['quality_statement'] = df.iloc[0]['Quality_Statement_Text']
    variable_details['en']['quality_statement_url'] = quality_statement_url_parser(df.iloc[0]['Quality_Summary_URL'])
    variable_details['en']['preferred_classification'] = classification_to_use(variable_details['en']['mnemonic'])
    variable_details['en']['multi_classifications'] = multi_classifications(variable_details['en']['mnemonic'])
    variable_details['en']['has_multi_classifications'] = has_multi_classifications(variable_details['en']['multi_classifications'])
    variable_details['en']['has_quality_information'] = has_quality_information(variable_details['en']['quality_statement'])
    
    variable_details['cy']['title'] = df.iloc[0]['Variable_Title_Welsh'].strip()
    variable_details['cy']['mnemonic'] = df.iloc[0]['Variable_Mnemonic']
    variable_details['cy']['2011 mnemonic'] = df.iloc[0]['Variable_Mnemonic_2011']
    variable_details['cy']['type_code'] = df.iloc[0]['Variable_Type_Code']
    variable_details['cy']['topic_code'] = df.iloc[0]['Topic_Mnemonic']
    variable_details['cy']['description'] = df.iloc[0]['Variable_Description_Welsh']
    variable_details['cy']['number of classifications'] = df.iloc[0]['Number_Of_Classifications']
    variable_details['cy']['statistical unit'] = english_to_welsh(df.iloc[0]['Statistical_Unit'])
    variable_details['cy']['comparability'] = df.iloc[0]['Comparability_Comments_Welsh']
    variable_details['cy']['quality_statement'] = df.iloc[0]['Quality_Statement_Text_Welsh']
    
    del variable_df
    
    # pulling through some labels for codes
    variable_type_df = pd.read_csv(f"{location}Variable_Type.csv", dtype=str)
    # create a dict
    variable_type_dict = {}
    variable_type_dict['en'] = dict(zip(list(variable_type_df['Variable_Type_Code']), list(variable_type_df['Variable_Type_Description'])))
    variable_type_dict['cy'] = dict(zip(list(variable_type_df['Variable_Type_Code']), list(variable_type_df['Variable_Type_Description_Welsh'])))
    del variable_type_df
    
    variable_details['en']['type_label'] = variable_type_dict['en'][variable_details['en']['type_code']]
    variable_details['cy']['type_label'] = variable_type_dict['cy'][variable_details['cy']['type_code']]
    del variable_type_dict
    
    #####
    
    topic_df = pd.read_csv(f"{location}Topic.csv", dtype=str)
    # create a dict
    topic_dict = {}
    topic_dict['en'] = dict(zip(list(topic_df['Topic_Mnemonic']), list(topic_df['Topic_Description'])))
    topic_dict['cy'] = dict(zip(list(topic_df['Topic_Mnemonic']), list(topic_df['Topic_Description_Welsh'])))
    del topic_df
    
    variable_details['en']['topic_label'] = topic_dict['en'][variable_details['en']['topic_code']].strip()
    variable_details['cy']['topic_label'] = topic_dict['cy'][variable_details['cy']['topic_code']].strip()
    del topic_dict
    
    #####
    
    classification_df = pd.read_csv(f"{location}Classification.csv", dtype=str)
    category_df = pd.read_csv(f"{location}Category.csv", dtype=str)
    df = category_df[category_df['Variable_Mnemonic'] == variable_details['en']['mnemonic']]
    
    variable_details['en']['classifications'] = {}
    variable_details['cy']['classifications'] = {}
    for classification in df['Classification_Mnemonic'].unique():
        df_classification = df[df['Classification_Mnemonic'] == classification]
        df_classification_labels = classification_df[classification_df['Classification_Mnemonic'] == classification]
        assert len(df_classification_labels) == 1, "df_classification_labels has len != 1, more than one variable with same name"
        
        english_label = df_classification_labels['External_Classification_Label_English'].iloc[0]
        welsh_label = df_classification_labels['External_Classification_Label_Welsh'].iloc[0]
        
        variable_details['en']['classifications'][classification] = {}
        variable_details['cy']['classifications'][classification] = {}
        variable_details['en']['classifications'][classification]['label'] = english_label
        variable_details['cy']['classifications'][classification]['label'] = welsh_label
        variable_details['en']['classifications'][classification]['category'] = dict(zip(df_classification['Category_Code'], df_classification['External_Category_Label_English']))
        variable_details['cy']['classifications'][classification]['category'] = dict(zip(df_classification['Category_Code'], df_classification['External_Category_Label_Welsh']))
        
    #assert str(len(variable_details['en']['classifications'].keys())) == variable_details['en']['number of classifications'], f"number of classifications stated {variable_details['en']['number of classifications']} does not match number found {len(variable_details['en']['classifications'].keys())}"
    del df, df_classification, category_df, classification_df, df_classification_labels, english_label, welsh_label
    
    #####
    
    question_df = pd.read_csv(f"{location}Question.csv", dtype=str)
    question_mapping_df = pd.read_csv(f"{location}Variable_Source_Question.csv", dtype=str)
    
    question_mapping_dict = {}
    for i in question_mapping_df.index:
        variable_code = question_mapping_df.iloc[i]['Variable_Mnemonic']
        question_code = question_mapping_df.iloc[i]['Source_Question_Code']
        if variable_code not in question_mapping_dict.keys():
            question_mapping_dict[variable_code] = [question_code]
        else:
            question_mapping_dict[variable_code].append(question_code)
    
    del question_mapping_df
    
    if variable_mnemonic in question_mapping_dict.keys():
        question_id_list = question_mapping_dict[variable_mnemonic]
        variable_details['en']['question'] = []
        variable_details['cy']['question'] = []
        
        for i, question_id in enumerate(question_id_list):
            question_variable_df = question_df[question_df['Question_Code'] == question_id]
            assert len(question_variable_df) == 1, f"found more than one line of data for the question_variable_df"
            
            loop_dict_en, loop_dict_cy = {}, {}

            loop_dict_en['question'] = question_variable_df.iloc[0]['Question_Label']
            loop_dict_en['reason'] = question_variable_df.iloc[0]['Reason_For_Asking_Question']
            loop_dict_en['first_asked'] = question_variable_df.iloc[0]['Question_First_Asked_In_Year']
            
            loop_dict_cy['question'] = question_variable_df.iloc[0]['Question_Label_Welsh']
            loop_dict_cy['reason'] = question_variable_df.iloc[0]['Reason_For_Asking_Question_Welsh']
            loop_dict_cy['first_asked'] = question_variable_df.iloc[0]['Question_First_Asked_In_Year']
            
            variable_details['en']['question'].append(loop_dict_en)
            variable_details['cy']['question'].append(loop_dict_cy)
            
        if len(variable_details['en']['question']) == 1:
            variable_details['en']['has_multi_questions'] = False
        else:
            variable_details['en']['has_multi_questions'] = True
            
    del question_df, question_mapping_dict 
    
    byo_only_variables_list = byo_only_variables()
    if variable in byo_only_variables_list:
        variable_details['en']['is_byo_only'] = True
    else:
        variable_details['en']['is_byo_only'] = False
    
    del byo_only_variables_list
    
    variable_details = variable_details_amender(variable_details)
    
    return variable_details


def english_to_welsh(value):
    # some text does not have a place in the model for welsh
    # doing translation here
    lookup = {
            "Person": "Person",
            "Household": "Cartref",
            "Family": "Teulu",
            "Communal Establishment": "Sefydliad cymunedol",
            "Dwelling": "Annedd"
            }
    
    return lookup.get(value, value)


def classification_to_use(mnemonic):
    # specifies which classification to use in the dictionary
    lookup = {
            "resident_age": "resident_age_101a",
            "hh_family_composition": "hh_family_composition_15a",
            "hh_deprivation": "hh_deprivation",
            "hh_size": "hh_size_9a",
            "living_arrangements": "living_arrangements_11a",
            "legal_partnership_status": "legal_partnership_status",
            "residence_type": "residence_type",
            "sex": "sex",
            "age_arrival_uk": "age_arrival_uk_18a",
            "country_of_birth": "country_of_birth_60a",
            "residence_length": "residence_length_6b",
            "migrant_ind": "migrant_ind",
            "passports_all": "passports_all_52a",
            "year_arrival_uk": "year_arrival_uk",
            "uk_armed_forces": "uk_armed_forces",
            "hh_veterans": "hh_veterans_5a",
            "hh_hrp_veteran": "hh_hrp_veteran",
            "english_proficiency": "english_proficiency",
            "ethnic_group": "ethnic_group_288a",
            "ethnic_group_tb": "ethnic_group_tb_20b",
            "hh_language": "hh_language",
            "hh_multi_ethnic_group": "hh_multi_ethnic_group",
            "hh_multi_language": "hh_multi_language",
            "hh_multi_religion": "hh_multi_religion_7a",
            "main_language_detailed": "main_language_detailed",
            "national_identity_all": "national_identity_all",
            "national_identity_detailed": "national_identity_detailed",
            "religion": "religion_58a",
            "religion_tb": "religion_tb",
            "welsh_skills_all": "welsh_skills_all",
            "welsh_skills_read": "welsh_skills_read",
            "welsh_skills_speak": "welsh_skills_speak",
            "welsh_skills_understand": "welsh_skills_understand",
            "welsh_skills_write": "welsh_skills_write",
            "economic_activity": "economic_activity",
            "has_ever_worked": "has_ever_worked",
            "hours_per_week_worked": "hours_per_week_worked",
            "industry_current": "industry_current_88a",
            "ns_sec": "ns_sec_10a",
            "occupation_current": "occupation_current_105a",
            "accom_by_dwelling_type": "accom_by_dwelling_type",
            "accommodation_type": "accommodation_type",
            "alternative_address_indicator": "alternative_address_indicator",
            "ce_management_type": "ce_management_type_26a",
            "ce_position_sex_age": "ce_position_sex_age_19a",
            "heating_type": "heating_type",
            "hh_tenure": "hh_tenure_9a",
            "number_bedrooms": "number_bedrooms_5a",
            "number_of_cars": "number_of_cars_5a",
            "occupancy_rating_bedrooms": "occupancy_rating_bedrooms_5a",
            "occupancy_rating_rooms": "occupancy_rating_rooms_5a",
            "second_address_type_priority": "second_address_type_priority",
            "voa_number_of_rooms": "voa_number_of_rooms_9a",
            "disability": "disability",
            "health_in_general": "health_in_general",
            "hh_disabled": "hh_disabled_4a",
            "is_carer": "is_carer",
            "gender_identity": "gender_identity_8a",
            "sexual_orientation": "sexual_orientation_9a",
            "highest_qualification": "highest_qualification",
            "in_full_time_education": "in_full_time_education",
            "transport_to_workplace": "transport_to_workplace_12a",
            "workplace_travel": "workplace_travel",
            "concealed_family_type": "concealed_family_type_11a",
            "dependent_child_age": "dependent_child_age_6a",
            "dwelling_hmo_unrelated": "dwelling_hmo_unrelated",
            "economic_activity_hours_worked": "economic_activity_hours_worked",
            "families_and_children": "families_and_children_9a",
            "families_and_children_welsh_speaker_parents": "families_and_children_welsh_speaker_parents_9a",
            "family_dependent_children": "family_dependent_children_5a",
            "family_status_by_workers_in_generation_1": "family_status_by_workers_in_generation_1_8a",
            "frp_age": "frp_age_5a",
            "hh_17_plus": "hh_17_plus_4a",
            "hh_composition_welsh": "hh_composition_welsh_7a",
            "hh_dependent_children": "hh_dependent_children_3a",
            "hh_families_type": "hh_families_type_6a",
            "hh_multi_generation": "hh_multi_generation",
            "hh_persons_per_room": "hh_persons_per_room",
            "hh_spaces_shared_dwelling": "hh_spaces_shared_dwelling_3a",
            "hh_welsh_speak_3_plus": "hh_welsh_speak_3_plus_8a",
            "hrp_ethnic_group_tb": "hrp_ethnic_group_tb_8a",
            "student_accommodation_type": "student_accommodation_type_7a",
            "activity_last_week": "activity_last_week",
            "ce_position_age": "ce_position_age_11a",
            "ce_position_ethnic_group": "ce_position_ethnic_group",
            "ce_position_religion": "ce_position_religion",
            "country_of_birth_extended": "country_of_birth_190a",
            "hh_adult_welsh_speakers": "hh_adult_welsh_speakers",
            "hh_adults_and_children": "hh_adults_and_children",
            "hh_adults_disabled": "hh_adults_disabled_4a",
            "hh_adults_employment": "hh_adults_employment_5a",
            "hh_adults_num": "hh_adults_num_3a",
            "hh_away_student": "hh_away_student",
            "hh_carers": "hh_carers_6a",
            "hh_deprivation_education": "hh_deprivation_education",
            "hh_deprivation_employment": "hh_deprivation_employment",
            "hh_deprivation_health": "hh_deprivation_health",
            "hh_deprivation_housing": "hh_deprivation_housing",
            "hh_families_count": "hh_families_count",
            "hh_lifestage": "hh_lifestage_13a",
            "hh_multi_ethnic_combination": "hh_multi_ethnic_combination_8a", 
            "hh_multi_religion_combination": "hh_multi_religion_combination", 
            "hh_no_condition": "hh_no_condition_4a", 
            "hh_not_limited": "hh_not_limited_4a", 
            "hh_number_limited_little": "hh_number_limited_little_4a", 
            "hh_number_limited_lot": "hh_number_limited_lot_4a",
            "hh_persons_per_bedroom": "hh_persons_per_bedroom",
            "hh_welsh_speaking_adults": "hh_welsh_speaking_adults_3a", 
            "industry_former": "industry_former_17a", 
            "main_language": "main_language_23a",
            "multi_passports": "multi_passports",
            "occupation_former": "occupation_former",
            "place_of_work_ind": "place_of_work_ind",
            "position_in_ce": "position_in_ce",
            "resident_age_extended": "resident_age_extended_17a",
            "welsh_speaking_3_plus": "welsh_speaking_3_plus",
            "welsh_speaking_dependent_child": "welsh_speaking_dependent_child",
            "workers_transport": "workers_transport",
            "approx_social_grade": "approx_social_grade",
            "adult_lifestage": "adult_lifestage_12a",
            "migration_msoa_inflow": "migration_msoa_inflow",
            "migration_msoa_outflow": "migration_msoa_outflow",
            "migration_ltla_inflow": "migration_ltla_inflow",
            "migration_ltla_outflow": "migration_ltla_outflow",
            "migration_utla_inflow": "migration_utla_inflow",
            "migration_utla_outflow": "migration_utla_outflow",
            "migration_region_inflow": "migration_region_inflow",
            "migration_region_outflow": "migration_region_outflow",
            "migration_country_inflow": "migration_country_inflow",
            "migration_country_outflow": "migration_country_outflow",
            "migration_national_inflow": "migration_national_inflow",
            "migration_lsoa_inflow": "migration_lsoa_inflow",
            "migration_lsoa_outflow": "migration_lsoa_outflow",
            "migration_oa_inflow": "migration_oa_inflow",
            "migration_oa_outflow": "migration_oa_outflow",
            "family_status":"family_status",
            "hh_migration_msoa_inflow": "hh_migration_msoa_inflow",
            "hh_migration_msoa_outflow": "hh_migration_msoa_outflow",
            "hh_migration_ltla_inflow": "hh_migration_ltla_inflow",
            "hh_migration_ltla_outflow": "hh_migration_ltla_outflow",
            "hh_migration_utla_inflow": "hh_migration_utla_inflow",
            "hh_migration_utla_outflow": "hh_migration_utla_outflow",
            "hh_migration_region_inflow": "hh_migration_region_inflow",
            "hh_migration_region_outflow": "hh_migration_region_outflow",
            "hh_migration_country_inflow": "hh_migration_country_inflow",
            "hh_migration_country_outflow": "hh_migration_country_outflow",
            "hh_migration_national_inflow": "hh_migration_national_inflow",
            "hrp_age": "hrp_age_4a",
            "hrp_economic_activity": "hrp_economic_activity_status_10a",
            "hrp_ns_sec": "hrp_ns_sec_10a",
            }
    
    if mnemonic not in lookup.keys():
        raise Exception(f"No specified classification for {mnemonic}")
    
    return lookup[mnemonic]

def get_variable_title(variable, language):
    # gets variable title to populate topic_dict
    variable_df = pd.read_csv(f"{location}Variable.csv", dtype=str)
    df = variable_df[variable_df["Variable_Mnemonic"] == variable]
    if language == 'en':
        title = df.iloc[0]['Variable_Title'].strip('.')
    elif language == 'cy':
        title = df.iloc[0]['Variable_Title_Welsh'].strip('.')
        
    if variable == 'migration_region_inflow' and language == 'cy':
        title = 'Mudo i mewn i Ranbarth (mewnlif)'
    return title


def multi_classifications(mnemonic):
    # some variables will use more than one classification
    lookup = {
            'accommodation_type': ['accommodation_type', 'accommodation_type_7a', 'accommodation_type_5a', 'accommodation_type_3a', 'accommodation_type_2a'],
            'country_of_birth': ['country_of_birth_66a', 'country_of_birth_60a', 'country_of_birth_25a', 'country_of_birth_22a', 'country_of_birth_13a', 'country_of_birth_12a', 'country_of_birth_8a', 'country_of_birth_3a'],
            'disability': ['disability', 'disability_4a', 'disability_3a'],
            'economic_activity': ['economic_activity', 'economic_activity_status_12a', 'economic_activity_status_10a', 'economic_activity_status_7a', 'economic_activity_status_4a', 'economic_activity_status_3a'],
            'english_proficiency': ['english_proficiency', 'english_proficiency_5a', 'english_proficiency_4a'],
            'ethnic_group_tb': ['ethnic_group_tb_20b', 'ethnic_group_tb_8a', 'ethnic_group_tb_6a'],
            'gender_identity': ['gender_identity_8a', 'gender_identity_7a', 'gender_identity_4a'],
            'health_in_general': ['health_in_general', 'health_in_general_4a', 'health_in_general_3a'],
            'heating_type': ['heating_type', 'heating_type_5a', 'heating_type_3a'],
            'hh_family_composition': ['hh_family_composition_37a', 'hh_family_composition_15a', 'hh_family_composition_14b', 'hh_family_composition_8a', 'hh_family_composition_6a', 'hh_family_composition_4a'],
            'hh_multi_language': ['hh_multi_language', 'hh_multi_language_3a'],
            'hh_size': ['hh_size_9a', 'hh_size_7a', 'hh_size_5a', 'hh_size_2a'],
            'hh_tenure': ['hh_tenure', 'hh_tenure_9a', 'hh_tenure_7a', 'hh_tenure_7b', 'hh_tenure_5a', 'hh_tenure_4a'],
            'highest_qualification': ['highest_qualification', 'highest_qualification_7a', 'highest_qualification_6a'],
            'hours_per_week_worked': ['hours_per_week_worked', 'hours_per_week_worked_3a'],
            'industry_current': ['industry_current_88a', 'industry_current_22a', 'industry_current_19a', 'industry_current_16a', 'industry_current_9a'],
            'is_carer': ['is_carer', 'is_carer_5a'],
            'legal_partnership_status': ['legal_partnership_status', 'legal_partnership_status_7a', 'legal_partnership_status_6a', 'legal_partnership_status_3a'],
            'main_language_detailed': ['main_language_detailed', 'main_language_detailed_26a', 'main_language_detailed_23a'],
            'national_identity_all': ['national_identity_all', 'national_identity_all_9a', 'national_identity_all_4a'],
            'number_of_cars': ['number_of_cars_6a', 'number_of_cars_5a', 'number_of_cars_4a', 'number_of_cars_3a'],
            'occupation_current': ['occupation_current_105a', 'occupation_current_27a', 'occupation_current_10a'],
            'passports_all': ['passports_all_52a', 'passports_all_27a', 'passports_all_18a', 'passports_all_13a', 'passports_all_11a', 'passports_all_4a'],
            'resident_age': [
                    'resident_age_101a', 'resident_age_91a', 'resident_age_86a', 'resident_age_61a', 'resident_age_23a', 'resident_age_18a', 'resident_age_18b', 
                    'resident_age_17a', 'resident_age_14a', 'resident_age_14b', 'resident_age_13a', 'resident_age_12a', 'resident_age_12b', 'resident_age_12c', 
                    'resident_age_11a', 'resident_age_11b', 'resident_age_11c', 'resident_age_11d', 'resident_age_10a', 'resident_age_10b', 'resident_age_9a', 
                    'resident_age_8a', 'resident_age_8b', 'resident_age_8c', 'resident_age_8d', 'resident_age_7a', 'resident_age_7b', 'resident_age_7d', 'resident_age_7f',
                    'resident_age_6a', 'resident_age_6b', 'resident_age_5a', 'resident_age_5b', 'resident_age_5c', 'resident_age_5d', 
                    'resident_age_4a', 'resident_age_4b', 'resident_age_4c', 'resident_age_3a', 'resident_age_3b', 'resident_age_3c', 'resident_age_3d', 'resident_age_2a'
                    ],
            'sexual_orientation': ['sexual_orientation_9a', 'sexual_orientation_6a', 'sexual_orientation_4a'],
            'welsh_skills_all': ['welsh_skills_all', 'welsh_skills_all_8a', 'welsh_skills_all_6a', 'welsh_skills_all_4a', 'welsh_skills_all_4b'],
            'workplace_travel': ['workplace_travel', 'workplace_travel_10a', 'workplace_travel_8a', 'workplace_travel_5a', 'workplace_travel_4a'],
            'year_arrival_uk': ['year_arrival_uk', 'year_arrival_uk_11a', 'year_arrival_uk_6a'],
            'dependent_child_age': ['dependent_child_age_6a', 'dependent_child_age_4a', 'dependent_child_age_3a'],
            'families_and_children': ['families_and_children_9a', 'families_and_children_7a', 'families_and_children_3a'],
            'family_dependent_children': ['family_dependent_children_5a', 'family_dependent_children_4a'],
            'hh_dependent_children': ['hh_dependent_children_6a', 'hh_dependent_children_6b', 'hh_dependent_children_3a', 'hh_dependent_children_3b'],
            'accom_by_dwelling_type': ['accom_by_dwelling_type', 'accom_by_dwelling_type_8a'],
            'age_arrival_uk': ['age_arrival_uk_23a', 'age_arrival_uk_18a', 'age_arrival_uk_8a'],
            'living_arrangements': ['living_arrangements_11a', 'living_arrangements_10a', 'living_arrangements_5a'],
            'occupancy_rating_bedrooms': ['occupancy_rating_bedrooms_6a', 'occupancy_rating_bedrooms_5a', 'occupancy_rating_bedrooms_3a'],
            'occupancy_rating_rooms': ['occupancy_rating_rooms_6a', 'occupancy_rating_rooms_5a', 'occupancy_rating_rooms_3a'],
            'voa_number_of_rooms': ['voa_number_of_rooms_9a', 'voa_number_of_rooms_8a', 'voa_number_of_rooms_6a'],
            'activity_last_week': ['activity_last_week', 'activity_last_week_3a'],
            'ce_position_ethnic_group': ['ce_position_ethnic_group', 'ce_position_ethnic_group_9a'],
            'hh_adults_and_children': ['hh_adults_and_children', 'hh_adults_and_children_11a'],
            'hh_away_student': ['hh_away_student', 'hh_away_student_4a'],
            'hh_disabled': ['hh_disabled_4a', 'hh_disabled_3a'],
            'hh_families_type': ['hh_families_type_12a', 'hh_families_type_6a', 'hh_families_type_4a'],
            'hh_multi_religion_combination': ['hh_multi_religion_combination', 'hh_multi_religion_combination_6a'],
            'hh_veterans': ['hh_veterans_5a', 'hh_veterans_4a', 'hh_veterans_3a'],
            'industry_former': ['industry_former_17a', 'industry_former_10a'],
            'main_language': ['main_language_23a', 'main_language_11a'],
            'multi_passports': ['multi_passports', 'multi_passports_9a'],
            'ns_sec': ['ns_sec', 'ns_sec_12a', 'ns_sec_10a'],
            'number_bedrooms': ['number_bedrooms_6a', 'number_bedrooms_5a'],
            'religion_tb': ['religion_tb', 'religion_tb_5a'],
            'resident_age_extended': ['resident_age_extended_17a', 'resident_age_extended_14b', 'resident_age_extended_8b', 'resident_age_extended_3d'],
            'transport_to_workplace': ['transport_to_workplace_12a', 'transport_to_workplace_5a'],
            'welsh_speaking_dependent_child': ['welsh_speaking_dependent_child', 'welsh_speaking_dependent_child_3a'],
            'hh_multi_religion': ['hh_multi_religion', 'hh_multi_religion_7a'],
            'adult_lifestage': ['adult_lifestage_12a', 'adult_lifestage_11a', 'adult_lifestage_9a']
            }
    
    return lookup.get(mnemonic, '')

def has_multi_classifications(value):
    # returns true or false
    if type(value) == list:
        return True
    else:
        return False

def has_quality_information(value):
    # returns true or false
    if pd.isnull(value):
        return False
    elif value == "":
        return False
    else:
        return True
    
def quality_statement_url_parser(url):
    if pd.isnull(url):
        return
    assert url.startswith("https://"), f"{url} does not follow normal format"
    new_url = url.split('https://www.ons.gov.uk')[1]
    return new_url

def get_measurements_used_dict():
    measurements_dict = {}
    df = pd.read_csv(f"{location}Statistical_Unit.csv", dtype=str)
    description_dict = dict(zip(df['Statistical_Unit'], df['Statistical_Unit_Description']))
    description_welsh_dict = dict(zip(df['Statistical_Unit'], df['Statistical_Unit_Description_Welsh']))
    
    for unit in df['Statistical_Unit'].unique():
        measurements_dict[unit] = {'en': {}, 'cy': {}}
        measurements_dict[unit]['en']['label'] = unit
        measurements_dict[unit]['cy']['label'] = english_to_welsh(unit)
        measurements_dict[unit]['en']['description'] = description_dict[unit]
        measurements_dict[unit]['cy']['description'] = description_welsh_dict[unit]
    
    del df, description_dict, description_welsh_dict
    
    df = pd.read_csv(f"{location}Variable.csv", dtype=str)
    for variable in ('hh_reference_person_pop', 'uprn'):
        df_loop = df[df['Variable_Mnemonic'] == variable]
        
        measurements_dict[variable] = {'en': {}, 'cy': {}}
        measurements_dict[variable]['en']['label'] = df_loop['Variable_Title'].iloc[0]
        measurements_dict[variable]['cy']['label'] = df_loop['Variable_Title_Welsh'].iloc[0]
        measurements_dict[variable]['en']['description'] = df_loop['Variable_Description'].iloc[0]
        measurements_dict[variable]['cy']['description'] = df_loop['Variable_Description_Welsh'].iloc[0]
    
    del df, df_loop
    return measurements_dict
    

def get_datasets_dict():
    dataset_df = pd.read_excel("cantabular/dictionary_master.xlsx", sheet_name="datasets to use")
    datasets_dict = {}
    
    for variable in dataset_df['variable mnemonic'].unique():
        loop_df = dataset_df[dataset_df['variable mnemonic'] == variable]
        datasets_dict[variable] = {'en': {}, 'cy': {}, 'TS_dataset': ''}
        
        for dataset_id in loop_df['Dataset ID']:
            if pd.isnull(dataset_id):
                continue
            
            if dataset_id.startswith('TS'):
                if not datasets_dict[variable]['TS_dataset']:
                    datasets_dict[variable]['TS_dataset'] = dataset_id
                    datasets_dict[variable]['TS_dataset'] = dataset_id
            
            loop_dataset_df = loop_df[loop_df['Dataset ID'] == dataset_id]
            
            description = loop_dataset_df.iloc[0]['Dataset title English']
            descritpion_welsh = loop_dataset_df.iloc[0]['Dataset title Welsh']
            dataset_url = loop_dataset_df.iloc[0]['Dataset URL']
            
            to_include = loop_dataset_df.iloc[0]['Published?']
            if to_include.lower() == 'no':
                # check publish data
                publish_date = loop_dataset_df.iloc[0]['Publication date']
                if publish_date == 'TBC':
                    pass
                else:
                    # TODO - make more robust
                    #todays_date = datetime.datetime.now()
                    todays_date = datetime.datetime(2023, 9, 7)
                    if publish_date < todays_date: # ie publish date has passed
                        to_include = 'Yes'
            
            datasets_dict[variable]['en'][dataset_id] = {
                    'title': description,
                    # TODO - do not split the link if it is a nomis link
                    'url': dataset_url.split('https://www.ons.gov.uk')[-1],
                    'include': true_or_false(to_include)
                    }
            datasets_dict[variable]['cy'][dataset_id] = {
                    'title': descritpion_welsh
                    }
            
        if "https://www.ons.gov.uk/datasets/create" in loop_df['Dataset URL'].unique():
            datasets_dict[variable]['has_byo_link'] = True
        else:
            datasets_dict[variable]['has_byo_link'] = False
            
    # some overwrites where order is incorrect
    datasets_dict['gender_identity']['TS_dataset'] = 'TS078'
            
    del dataset_df
    return datasets_dict

def get_rich_content_dict():
    content_df = pd.read_excel("cantabular/dictionary_master.xlsx", sheet_name="rich content products")
    content_dict = {}
    
    for variable in content_df['variable'].unique():
        loop_df = content_df[content_df['variable'] == variable]
        
        census_maps_url = loop_df.iloc[0]['Census Maps URL']
        change_over_time_url = loop_df.iloc[0]['Change over time']
        nomis_area_url = loop_df.iloc[0]['Nomis Area Profiles']
        
        content_dict[variable] = {
                'census_maps_url': nan_to_string(census_maps_url),
                'change_over_time_url': nan_to_string(change_over_time_url).split('https://www.ons.gov.uk')[-1],
                'nomis_area_url': nan_to_string(nomis_area_url)
                }
        
    del content_df 
    return content_dict

def get_area_type_dict(area):
    variable_df = pd.read_csv(f"{location}Variable.csv", dtype=str)
    df = variable_df[variable_df["Variable_Title"] == area]
    assert len(df) == 1, f"df has length {len(df)} for {area} - should be unique"
    
    area_dict = {
            'en': {
                    'title': df.iloc[0]['Variable_Title'],
                    'description': df.iloc[0]['Variable_Description']
                    },
            'cy': {
                    'title': df.iloc[0]['Variable_Title_Welsh'],
                    'description': df.iloc[0]['Variable_Description_Welsh']
                    }
            }
            
    return area_dict   

def byo_only_variables():
    # list of BYO variables
    # has a different variable page template
    byo_variables = (
            "activity_last_week", "ce_position_age", "ce_position_ethnic_group", 
            "ce_position_religion", "country_of_birth_extended", "hh_adult_welsh_speakers",
            "hh_adults_and_children", "hh_adults_disabled", "hh_adults_employment",
            "hh_adults_num", "hh_away_student", "hh_carers", "hh_deprivation_education",
            "hh_deprivation_employment", "hh_deprivation_health", "hh_deprivation_housing",
            "hh_families_count", "hh_lifestage", "hh_multi_ethnic_combination", 
            "hh_multi_religion_combination", "hh_no_condition", "hh_not_limited",
            "hh_number_limited_little", "hh_number_limited_lot", "hh_persons_per_bedroom",
            "hh_welsh_speaking_adults", "industry_former", "main_language", "multi_passports",
            "occupation_former", "place_of_work_ind", "position_in_ce", "resident_age_extended",
            "welsh_speaking_3_plus", "workers_transport"
            )
    return byo_variables

def check_byo_only_variables():
    # checking list of byo only variables to see if any are no longer byo only
    byo_only_variables_list = byo_only_variables()
    # check rich content first
    content_df = pd.read_excel("cantabular/dictionary_master.xlsx", sheet_name="rich content products")
    for variable in byo_only_variables_list:
        if variable in content_df['variable'].unique():
            raise Exception(f"{variable} is no longer a BYO only variable - has rich content")
    del content_df       
    
    # check dataset links
    dataset_df = pd.read_excel("cantabular/dictionary_master.xlsx", sheet_name="datasets to use")
    for variable in byo_only_variables_list:
        df = dataset_df[dataset_df['variable mnemonic'] == variable]
        if df['Dataset ID'].unique().size != 1:
            raise Exception(f"{variable} is no longer a BYO only variable - has other dataset links")
        else:
            if pd.notnull(df['Dataset ID'].unique()[0]):
                raise Exception(f"{variable} is no longer a BYO only variable - has a dataset link")
    return

def nan_to_string(value):
    if pd.isnull(value):
        return ''
    else:
        return value
    
def true_or_false(value):
    # converts yes/no to boolean
    if value.lower() == 'yes':
        return True
    elif value.lower() == 'no':
        return False
    else:
        raise TypeError(f"Unknown value to convert - {value}") 
        

def variable_details_amender(variable_details):
    mnemonic = variable_details['en']['mnemonic']
    
    if mnemonic in ("hrp_economic_activity", "hrp_ns_sec"):
        variable_details['en']['title'] = variable_details['en']['title'].strip('.')
        variable_details['cy']['title'] = variable_details['cy']['title'].strip('.')
        
    if mnemonic == 'migration_region_inflow':
        variable_details['cy']['title'] =  'Mudo i mewn i Ranbarth (mewnlif)'
        
    if mnemonic == 'migration_country_outflow':
        variable_details['cy']['title'] =  'Mudo allan o Wlad (all-lif)'
        
    if mnemonic == 'migration_national_inflow':
        variable_details['cy']['description'] = "Yn nodi preswylwyr arferol yng Nghymru a Lloegr sy'n byw yn yr un ardal a'r rheini a symudodd allan o’r ardal i rywle arall yng Nghymru a Lloegr yn ystod y flwyddyn cyn y cyfrifiad. Mae'r term “ardal” yn diffinio'r lefel ddaearyddol sy'n cael ei dangos yn y tabl. Mae'r term “ardal gysylltiedig” yn cyfeirio at y lefel ddaearyddol uchaf nesaf i fyny'r hierarchaeth. Nid yw hyn yn cyfrif yr holl bobl a symudodd allan o ardal am nad yw’n cynnwys pobl a symudodd y tu allan i Gymru a Lloegr."
    
    if mnemonic in ('migration_country_inflow', 'migration_country_outflow', 
                    'migration_lsoa_inflow', 'migration_lsoa_outflow', 
                    'migration_national_inflow',
                    'migration_ltla_inflow', 'migration_ltla_outflow',
                    'migration_msoa_inflow', 'migration_msoa_outflow',
                    'migration_region_inflow', 'migration_region_outflow', 
                    'migration_utla_inflow', 'migration_utla_outflow',
                    'migration_oa_inflow', 'migration_oa_outflow', 
                    'hh_migration_ltla_inflow', 'hh_migration_ltla_outflow',
                    'hh_migration_region_inflow','hh_migration_region_outflow', 
                    'hh_migration_country_inflow','hh_migration_country_outflow',
                    'hh_migration_national_inflow', 
                    'hh_migration_msoa_inflow', 'hh_migration_msoa_outflow',
                    'hh_migration_utla_inflow', 'hh_migration_utla_outflow'):
        
        if variable_details['en']['comparability'].startswith('Broadly'):
            variable_details['cy']['comparability'] = 'Cymaradwy yn fras\n\nNid yw Cyfrifiad 2021 yn cofnodi symudiadau’r rheini dan 1 oed ar Ddiwrnod y Cyfrifiad (21 Mawrth 2021) gan nad oes ganddynt gyfeiriad flwyddyn yn ôl. Cafodd amcangyfrif ei wneud ar gyfer y symudiadau hyn yn 2011, ond nid yw hyn wedi’i wneud ar gyfer 2021.'
            
        elif variable_details['en']['comparability'].startswith('Not'):
            variable_details['cy']['comparability'] = 'Ddim yn gymaradwy\n\nNid yw Cyfrifiad 2021 yn cofnodi symudiadau’r rheini dan 1 oed ar Ddiwrnod y Cyfrifiad (21 Mawrth 2021) gan nad oes ganddynt gyfeiriad flwyddyn yn ôl. Cafodd amcangyfrif ei wneud ar gyfer y symudiadau hyn yn 2011, ond nid yw hyn wedi’i wneud ar gyfer 2021.\n\nRoeddem wedi cyfuno data mudo mewnol y Deyrnas Unedig ar gyfer 2011, o gymharu â 2021 nad oeddem wedi gwneud hynny. Nid oes gennym ddata ar gyfer Gogledd Iwerddon (oherwydd gwahaniaethau mewn amserlenni prosesu data) na’r Alban (gan fod yr Alban wedi cynnal eu Cyfrifiad ym mis Mawrth 2022). Mae hyn yn golygu bod cyfrifiadau all-lif yn eithrio pobl a oedd yng Nghymru a Lloegr y flwyddyn cyn Cyfrifiad 2021 ond a oedd wedi symud i Ogledd Iwerddon, a’r Alban cyn 21 Mawrth 2021.'
            
        else:
            raise Exception(f"Welsh comparability not covered for {mnemonic}")
    
    if mnemonic == 'hh_migration_national_inflow':
        variable_details['cy']['description'] = "Yn nodi cartrefi preswyl arferol yng Nghymru a Lloegr sy’n byw yn yr un ardal a’r rheini a symudodd i mewn i’r ardal yn ystod y flwyddyn cyn y cyfrifiad. Mae'r term “ardal” yn diffinio'r lefel ddaearyddol sy'n cael ei dangos yn y tabl."
        
    return variable_details 



if __name__ == '__main__':
    variable_details = run()








