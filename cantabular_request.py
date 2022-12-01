# reading in from csvs
import pandas as pd

location = "cantabular/ar2776-c21ew_metadata-v1-3_cantab_20221201-32/"

def run():
    variable = "transport_to_workplace"
    variable_details = get_variable_details(variable)
    return variable_details


def get_variable_details(variable):
    
    variable_details = {'en': {}, 'cy': {}}
    # converted to a loop through when pulling all variables
    variable_df = pd.read_csv(f"{location}Variable.csv", dtype=str)
    df = variable_df[variable_df["Variable_Mnemonic"] == variable]
    
    if len(df) == 0:
        raise Exception(f"Cannot find variable {variable}")
    assert len(df) == 1, f"found more than one line of data for the variable {variable}"

    variable_mnemonic = variable
    
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
    variable_details['cy']['quality_statement'] = quality_information_welsh(df.iloc[0]['Variable_Mnemonic']) # does not currently exist in model
    
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
        assert len(df_classification_labels) == 1, f"df_classification_labels has len != 1, more than one variable with same name"
        
        english_label = df_classification_labels['External_Classification_Label_English'].iloc[0]
        welsh_label = df_classification_labels['External_Classification_Label_Welsh'].iloc[0]
        
        variable_details['en']['classifications'][classification] = {}
        variable_details['cy']['classifications'][classification] = {}
        variable_details['en']['classifications'][classification]['label'] = english_label
        variable_details['cy']['classifications'][classification]['label'] = welsh_label
        variable_details['en']['classifications'][classification]['category'] = dict(zip(df_classification['Category_Code'], df_classification['External_Category_Label_English']))
        variable_details['cy']['classifications'][classification]['category'] = dict(zip(df_classification['Category_Code'], df_classification['External_Category_Label_Welsh']))
        
    assert str(len(variable_details['en']['classifications'].keys())) == variable_details['en']['number of classifications'], f"number of classifications stated {variable_details['en']['number of classifications']} does not match number found {len(variable_details['en']['classifications'].keys())}"
    
    del df, df_classification, category_df, classification_df, df_classification_labels, english_label, welsh_label
    
    #####
    
    question_df = pd.read_csv(f"{location}Question.csv", dtype=str)
    question_mapping_df = pd.read_csv(f"{location}Variable_Source_Question.csv", dtype=str)
    question_mapping_dict = dict(zip(list(question_mapping_df['Variable_Mnemonic']), list(question_mapping_df['Source_Question_Code'])))
    del question_mapping_df
    
    if variable_mnemonic in question_mapping_dict.keys():
        question_id = question_mapping_dict[variable_mnemonic]
        question_variable_df = question_df[question_df['Question_Code'] == question_id]
        assert len(question_variable_df) == 1, f"found more than one line of data for the question_variable_df"

        variable_details['en']['question'] = {}
        variable_details['en']['question']['question'] = question_variable_df.iloc[0]['Question_Label']
        variable_details['en']['question']['reason'] = question_variable_df.iloc[0]['Reason_For_Asking_Question']
        variable_details['en']['question']['first_asked'] = question_variable_df.iloc[0]['Question_First_Asked_In_Year']
        
        variable_details['cy']['question'] = {}
        variable_details['cy']['question']['question'] = question_variable_df.iloc[0]['Question_Label_Welsh']
        variable_details['cy']['question']['reason'] = question_variable_df.iloc[0]['Reason_For_Asking_Question_Welsh']
        variable_details['cy']['question']['first_asked'] = question_variable_df.iloc[0]['Question_First_Asked_In_Year']
    
    # find where question comes from
    del question_df, question_mapping_dict
    
    
    return variable_details


def english_to_welsh(value):
    # some text does not have a place in the model for welsh
    # doing translation here
    lookup = {
            "Person": "Person",
            "Household": "Cartref"
            }
    
    return lookup.get(value, value)


def quality_information_welsh(mnemonic):
    # quality information in welsh is not currently in model so will be pull from here
    # TODO - remove this hard code when welsh is in model
    welsh_version_dict = {
            'legal_partnership_status': """Nid oes amcangyfrifon ar wahân gan bartneriaethau o'r naill ryw ac o'r un rhyw ar gyfer y categorïau statws priodasol “Wedi gwahanu”, “Wedi ysgaru/diddymu” ac “Yn weddw/wedi colli partner” ar gael. Mae hyn am fod prosesau sicrhau ansawdd wedi dangos nad oedd y ffigurau ar gyfer rhai o'r categorïau yn ddibynadwy.""",
            'hh_family_composition': "Efallai na fydd data am gydberthnasau mewn cartref bob amser yn gyson â'r statws partneriaeth gyfreithiol. Mae hyn oherwydd cymhlethdod trefniadau byw a'r ffordd y cafodd y cwestiynau hyn eu dehongli gan bobl. Cymerwch ofal wrth ddefnyddio'r ddau newidyn hyn gyda'i gilydd.",
            'passports_all': """Os cofnododd person fod ganddo fwy nag un pasbort, dim ond unwaith y cafodd ei gyfrif, wedi'i gategoreiddio yn ôl y drefn flaenoriaeth ganlynol: 1. Pasbort y Deyrnas Unedig, 2. Pasbort Iwerddon, 3. Pasbort arall. Dim ond y wlad gyntaf a ysgrifennwyd yn “Pasbort arall” a nodwyd.""",
            'resident_age': "Mae'r amcangyfrifon ar gyfer un flwyddyn o oedran rhwng 90 a 100+ oed yn llai dibynadwy nag oedrannau eraill. Roedd y broses amcangyfrif ac asesu ar yr oedrannau hyn yn seiliedig ar yr ystod oedran 90+ yn hytrach na bandiau oedran o bum mlynedd.",
            'uk_armed_forces': "Bydd llawer o'r rhai sydd wedi gwasanaethu yn Lluoedd Arfog y Deyrnas Unedig yn y gorffennol yn ddynion hŷn oherwydd Gwasanaeth Cenedlaethol. Gwnaethom roi proses sicrhau ansawdd ychwanegol ar waith i gywiro rhai atebion gan bersonél sy'n gwasanaethu ar hyn o bryd.",
            'hh_veterans': "Bydd llawer o'r rhai sydd wedi gwasanaethu yn Lluoedd Arfog y Deyrnas Unedig yn y gorffennol yn ddynion hŷn oherwydd Gwasanaeth Cenedlaethol. Gwnaethom roi proses sicrhau ansawdd ychwanegol ar waith i gywiro rhai atebion gan bersonél sy'n gwasanaethu ar hyn o bryd.",
            'hh_hrp_veteran': "Bydd llawer o'r rhai sydd wedi gwasanaethu yn Lluoedd Arfog y Deyrnas Unedig yn y gorffennol yn ddynion hŷn oherwydd Gwasanaeth Cenedlaethol. Gwnaethom roi proses sicrhau ansawdd ychwanegol ar waith i gywiro rhai atebion gan bersonél sy'n gwasanaethu ar hyn o bryd.",
            'national_identity_all': """Mae’n bosibl bod y cynnydd ers Cyfrifiad 2011 yn nifer y bobl sy’n nodi eu bod nhw’n “Brydeiniwr/Brydeinwraig” a’r gostyngiad yn nifer y bobl sy’n nodi eu bod nhw’n “Sais/Saesnes” yn adlewyrchu’n rhannol y gwir newidiadau mewn hunanganfyddiad. Mae hefyd yn debygol o adlewyrchu bod “Prydeiniwr/Prydeinwraig” wedi cymryd lle “Sais/Saesnes” fel yr opsiwn ymateb cyntaf yn y rhestr ar yr holiadur yn Lloegr.""",
            'national_identity_detailed': """Mae’n bosibl bod y cynnydd ers Cyfrifiad 2011 yn nifer y bobl sy’n nodi eu bod nhw’n “Brydeiniwr/Brydeinwraig” a’r gostyngiad yn nifer y bobl sy’n nodi eu bod nhw’n “Sais/Saesnes” yn adlewyrchu’n rhannol y gwir newidiadau mewn hunanganfyddiad. Mae hefyd yn debygol o adlewyrchu bod “Prydeiniwr/Prydeinwraig” wedi cymryd lle “Sais/Saesnes” fel yr opsiwn ymateb cyntaf yn y rhestr ar yr holiadur yn Lloegr."""
                    }
    return welsh_version_dict.get(mnemonic, '')


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
            "residence_length": "residence_length",
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
            "occupancy_rating_bedrooms": "occupancy_rating_bedrooms_6a",
            "occupancy_rating_rooms": "occupancy_rating_rooms_6a",
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
            "workplace_travel": "workplace_travel"
            }
    
    if mnemonic not in lookup.keys():
        raise Exception(f"No specified classification for {mnemonic}")
    
    return lookup[mnemonic]

def get_variable_title(variable, language):
    # gets variable title to populate topic_dict
    variable_df = pd.read_csv(f"{location}Variable.csv", dtype=str)
    df = variable_df[variable_df["Variable_Mnemonic"] == variable]
    if language == 'en':
        title = df.iloc[0]['Variable_Title']
    elif language == 'cy':
        title = df.iloc[0]['Variable_Title_Welsh']
    return title


def multi_classifications(mnemonic):
    # some variables will use more than one classification
    lookup = {
            'accommodation_type': ['accommodation_type', 'accommodation_type_5a', 'accommodation_type_3a'],
            'country_of_birth': ['country_of_birth_60a', 'country_of_birth_25a', 'country_of_birth_12a', 'country_of_birth_8a', 'country_of_birth_3a'],
            'disability': ['disability', 'disability_3a'],
            'economic_activity': ['economic_activity', 'economic_activity_status_10a', 'economic_activity_status_7a', 'economic_activity_status_4a', 'economic_activity_status_3a'],
            'english_proficiency': ['english_proficiency', 'english_proficiency_4a'],
            'ethnic_group_tb': ['ethnic_group_tb_20b', 'ethnic_group_tb_6a'],
            'gender_identity': ['gender_identity_8a', 'gender_identity_7a', 'gender_identity_4a'],
            'health_in_general': ['health_in_general', 'health_in_general_4a', 'health_in_general_3a'],
            'heating_type': ['heating_type', 'heating_type_3a'],
            'hh_family_composition': ['hh_family_composition_15a', 'hh_family_composition_8a', 'hh_family_composition_4a'],
            'hh_multi_language': ['hh_multi_language', 'hh_multi_language_3a'],
            'hh_size': ['hh_size_9a', 'hh_size_7a', 'hh_size_5a'],
            'hh_tenure': ['hh_tenure_9a', 'hh_tenure_7b', 'hh_tenure_5a'],
            'highest_qualification': ['highest_qualification', 'highest_qualification_6a'],
            'hours_per_week_worked': ['hours_per_week_worked', 'hours_per_week_worked_3a'],
            'industry_current': ['industry_current_88a', 'industry_current_22a', 'industry_current_9a'],
            'is_carer': ['is_carer', 'is_carer_5a'],
            'legal_partnership_status': ['legal_partnership_status', 'legal_partnership_status_6a', 'legal_partnership_status_3a'],
            'main_language_detailed': ['main_language_detailed', 'main_language_detailed_23a'],
            'national_identity_all': ['national_identity_all', 'national_identity_all_9a', 'national_identity_all_4a'],
            'number_of_cars': ['number_of_cars_5a', 'number_of_cars_3a'],
            'occupation_current': ['occupation_current_105a', 'occupation_current_10a'],
            'passports_all': ['passports_all_52a', 'passports_all_27a', 'passports_all_18a', 'passports_all_13a', 'passports_all_4a'],
            'resident_age': ['resident_age_101a', 'resident_age_91a', 'resident_age_86a', 'resident_age_11a', 'resident_age_8c', 'resident_age_3a'],
            'sexual_orientation': ['sexual_orientation_9a', 'sexual_orientation_6a', 'sexual_orientation_4a'],
            'welsh_skills_all': ['welsh_skills_all', 'welsh_skills_all_6a', 'welsh_skills_all_4b'],
            'workplace_travel': ['workplace_travel', 'workplace_travel_5a', 'workplace_travel_4a'],
            'year_arrival_uk': ['year_arrival_uk', 'year_arrival_uk_6a']
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

if __name__ == '__main__':
    variable_details = run()










"""
####################################################################################
# reading in from cantabular
import requests

url = "http://localhost:8492/graphql"
url = 'http://localhost:8492/graphql?query={service{tables{name}}}'

query = '{service(lang: "en"){tables{label name description datasetName vars}}}'
query_url = f"{url}?query={query}"

r = requests.get(query_url)
metadata = r.json()
dataset_list = []
for dataset in metadata['data']['service']['tables']:
    dataset_list.append(dataset['datasetName'])
    
    
    
{
  service(lang: "en") {
    meta {
      description
    }
    tables {
      name
      label
      meta {
        Dataset_Mnemonic_2011
        Last_Updated
      }
    }
  }
}


{
  service {
    tables(names: ["AP001", "AP002"]) {
      datasetName
      description
      label
      name
      vars
    }
  }
}
    
{
  datasets {
    name
    label
		variables(names:["Age"]) {
		  edges {
		    node {
		      description
		      filterOnly
		      label
		      name
          categories {
            edges {
              node {
                code
                label
              }
            }
          }
		    }
		  }
		}
  }
}
              
              
query = '''{
  datasets(lang: "en") {
    variables(base: true, rule: false) {
      edges {
        node {
          name
          label
          description
          isSourceOf {
            edges {
              node {
                categories {
                  edges {
                    node {
                      code
                      label
                    }
                  }
                }
                name
                label
              }
            }
          }
          meta {
            ONS_Variable {
              Comparability_Comments
              Uk_Comparison_Comments
              Statistical_Unit {
                Statistical_Unit
                Statistical_Unit_Description
              }
              Topic {
                Topic_Title
                Topic_Mnemonic
                Topic_Description
              }
              Variable_Mnemonic
              Variable_Mnemonic_2011
              Variable_Type {
                Variable_Type_Code
                Variable_Type_Description
              }
              Quality_Statement_Text
              Quality_Summary_URL
              Questions {
                Question_Code
                Question_Label
                Question_First_Asked_In_Year
                Reason_For_Asking_Question
              }
            }
          }
        }
      }
    }
  }
}
'''

"""  
    
