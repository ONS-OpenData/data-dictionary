# reading in from csvs
import pandas as pd

location = "cantabular/ar2776-c21ew_metadata-v1-3_cantab_20221108-28/"

def run():
    variable = "uk_armed_forces"
    variable_details = get_variable_details(variable)
    return variable_details


def get_variable_details(variable):
    
    variable_details = {'en': {}, 'cy': {}}
    # converted to a loop through when pulling all variables
    variable_df = pd.read_csv(f"{location}Variable.csv", dtype=str)
    df = variable_df[variable_df["Variable_Mnemonic"] == variable]
    #df = variable_df[variable_df["Variable_Title"] == variable]
    if len(df) == 0:
        raise Exception(f"Cannot find variable {variable}")
    assert len(df) == 1, f"found more than one line of data for the variable {variable}"
    i = df.index[0]
    #variable_mnemonic = df.loc[i]['Variable_Mnemonic']
    variable_mnemonic = variable
    
    variable_details['en']['title'] = df.loc[i]['Variable_Title']
    variable_details['en']['mnemonic'] = df.loc[i]['Variable_Mnemonic']
    variable_details['en']['2011 mnemonic'] = df.loc[i]['Variable_Mnemonic_2011']
    variable_details['en']['type_code'] = df.loc[i]['Variable_Type_Code']
    variable_details['en']['topic_code'] = df.loc[i]['Topic_Mnemonic']
    variable_details['en']['description'] = df.loc[i]['Variable_Description']
    variable_details['en']['number of classifications'] = df.loc[i]['Number_Of_Classifications']
    variable_details['en']['statistical unit'] = df.loc[i]['Statistical_Unit']
    variable_details['en']['comparability'] = df.loc[i]['Comparability_Comments']
    variable_details['en']['quality_statement'] = df.loc[i]['Quality_Statement_Text']
    variable_details['en']['preferred_classification'] = classification_to_use(variable_details['en']['mnemonic'])
    
    variable_details['cy']['title'] = df.loc[i]['Variable_Title_Welsh']
    variable_details['cy']['mnemonic'] = df.loc[i]['Variable_Mnemonic']
    variable_details['cy']['2011 mnemonic'] = df.loc[i]['Variable_Mnemonic_2011']
    variable_details['cy']['type_code'] = df.loc[i]['Variable_Type_Code']
    variable_details['cy']['topic_code'] = df.loc[i]['Topic_Mnemonic']
    variable_details['cy']['description'] = df.loc[i]['Variable_Description_Welsh']
    variable_details['cy']['number of classifications'] = df.loc[i]['Number_Of_Classifications']
    variable_details['cy']['statistical unit'] = english_to_welsh(df.loc[i]['Statistical_Unit'])
    variable_details['cy']['comparability'] = df.loc[i]['Comparability_Comments_Welsh']
    variable_details['cy']['quality_statement'] = quality_information_welsh(df.loc[i]['Variable_Mnemonic']) # does not currently exist in model
    
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
    
    variable_details['en']['topic_label'] = topic_dict['en'][variable_details['en']['topic_code']]
    variable_details['cy']['topic_label'] = topic_dict['cy'][variable_details['cy']['topic_code']]
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
        i = question_variable_df.index[0]
        variable_details['en']['question'] = {}
        variable_details['en']['question']['question'] = question_variable_df.loc[i]['Question_Label']
        variable_details['en']['question']['reason'] = question_variable_df.loc[i]['Reason_For_Asking_Question']
        variable_details['en']['question']['first_asked'] = question_variable_df.loc[i]['Question_First_Asked_In_Year']
        
        variable_details['cy']['question'] = {}
        variable_details['cy']['question']['question'] = question_variable_df.loc[i]['Question_Label_Welsh']
        variable_details['cy']['question']['reason'] = question_variable_df.loc[i]['Reason_For_Asking_Question_Welsh']
        variable_details['cy']['question']['first_asked'] = question_variable_df.loc[i]['Question_First_Asked_In_Year']
    
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
            'hh_hrp_veteran': "Bydd llawer o'r rhai sydd wedi gwasanaethu yn Lluoedd Arfog y Deyrnas Unedig yn y gorffennol yn ddynion hŷn oherwydd Gwasanaeth Cenedlaethol. Gwnaethom roi proses sicrhau ansawdd ychwanegol ar waith i gywiro rhai atebion gan bersonél sy'n gwasanaethu ar hyn o bryd."
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
            "hh_hrp_veteran": "hh_hrp_veteran"
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



if __name__ == '__main__':
    variable_details = run()


