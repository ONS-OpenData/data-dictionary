from cantabular_request import get_variable_title

def get_topic_dict(list_of_topics, **kwargs):
    # first key is topic (not used directly) 
    # title_topic_page -> title of tiles on variable by topic page
    #                  -> heading on list of variables page
    # summary_topic_page -> summary in tile on variable by topic page
    # uri_ending_topic_page -> used as link for tiles on variable by topic page
    #                       -> url of list of variables page
    # title_for_page -> page title on list of variables page
    # summary_for_page -> page summary on lost of variables page
    # list_of_variables -> variables to be used for each topic
    #   key -> mnemonic to pull metadata from model
    #   value -> link & url for each variable page, how variable is displayed on list of variables page
    
    assert type(list_of_topics) == list, "list_of_topics must be in a list"
    
    all_topic_dict = {
                "demography": {
                        "en": {
                                "title_topic_page": "Demography variables",
                                "summary_topic_page": "Includes age, sex, household composition and marital and civil partnership status.",
                                "uri_ending_topic_page": "demographyvariablescensus2021",
                                "title_for_page": "Demography variables Census 2021",
                                "summary_for_page": "Lists variables used in Census 2021 data, includes age, sex, household composition and marital and civil partnership status.",
                                "list_of_variables": {
                                        "resident_age": get_variable_title("resident_age", 'en'),
                                        "hh_family_composition": get_variable_title("hh_family_composition", 'en'),
                                        "hh_deprivation": get_variable_title("hh_deprivation",'en'),
                                        "hh_size": get_variable_title("hh_size", 'en'),
                                        "living_arrangements": get_variable_title("living_arrangements", 'en'),
                                        "legal_partnership_status": get_variable_title("legal_partnership_status", 'en'),
                                        "residence_type": get_variable_title("residence_type", 'en'),
                                        "sex": get_variable_title("sex", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau demograffeg",
                            "summary_topic_page": "Yn cynnwys oedran, rhyw, cyfansoddiad y cartref a statws priodasol a phartneriaeth sifil.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau demograffeg Cyfrifiad 2021",
                            "summary_for_page": "Rhestr o newidynnau a ddefnyddir yn nata Cyfrifiad 2021 sy'n cynnwys oedran, rhyw, cyfansoddiad y cartref a statws priodasol a phartneriaeth sifil.",
                            "list_of_variables": {
                                    "resident_age": get_variable_title("resident_age", 'cy'),
                                    "hh_family_composition": get_variable_title("hh_family_composition", 'cy'),
                                    "hh_deprivation": get_variable_title("hh_deprivation", 'cy'),
                                    "hh_size": get_variable_title("hh_size", 'cy'),
                                    "living_arrangements": get_variable_title("living_arrangements", 'cy'),
                                    "legal_partnership_status": get_variable_title("legal_partnership_status", 'cy'),
                                    "residence_type": get_variable_title("residence_type", 'cy'),
                                    "sex": get_variable_title("sex", 'cy')
                                    }
                            }
                },
                "international migration": {
                        "en": {
                                "title_topic_page": "International migration variables",
                                "summary_topic_page": "Includes country of birth, year and age of arrival in the UK, length of residence in the UK and migrant indicator.",
                                "uri_ending_topic_page": "internationalmigrationvariablescensus2021", 
                                "title_for_page": "International migration variables Census 2021",
                                "summary_for_page": "Lists variables used in Census 2021 data, includes country of birth, year and age of arrivals in the UK, length of residence in the UK and migrant indicator.",
                                "list_of_variables": {
                                        "age_arrival_uk": get_variable_title("age_arrival_uk", 'en'),
                                        "country_of_birth": get_variable_title("country_of_birth", 'en'),
                                        "residence_length": get_variable_title("residence_length", 'en'),
                                        "migrant_ind": get_variable_title("migrant_ind", 'en'),
                                        "passports_all": get_variable_title("passports_all", 'en'),
                                        "year_arrival_uk": get_variable_title("year_arrival_uk", 'en')
                                    }
                                },
                        "cy": {
                                "title_topic_page": "Newidynnau mudo rhyngwladol",
                                "summary_topic_page": "Yn cynnwys gwlad enedigol, blwyddyn ac oedran cyrraedd y Deyrnas Unedig, cyfnod preswylio yn y Deyrnas Unedig a dangosydd mudwyr.",
                                "uri_ending_topic_page": "",
                                "title_for_page": "Newidynnau mudo rhyngwladol Cyfrifiad 2021",
                                "summary_for_page": "Rhestr o newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys gwlad enedigol, blwyddyn ac oedran cyrraedd y Deyrnas Unedig, cyfnod preswylio yn y Deyrnas Unedig a dangosydd mudwyr.",
                                "list_of_variables": {
                                        "age_arrival_uk": get_variable_title("age_arrival_uk", 'cy'),
                                        "country_of_birth": get_variable_title("country_of_birth", 'cy'),
                                        "residence_length": get_variable_title("residence_length", 'cy'),
                                        "migrant_ind": get_variable_title("migrant_ind", 'cy'),
                                        "passports_all": get_variable_title("passports_all", 'cy'),
                                        "year_arrival_uk": get_variable_title("year_arrival_uk", 'cy')
                                    }
                            }
                },
                "UK armed forces veterans": {
                        "en": {
                                "title_topic_page": "UK armed forces veterans variables",
                                "summary_topic_page": "Includes number of people in household who previously served in the UK armed forces and UK armed forces veteran indicator.",
                                "uri_ending_topic_page": "ukarmedforcesveteransvariablescensus2021",
                                "title_for_page": "UK armed forces veterans variables Census 2021",
                                "summary_for_page": "Lists variables used in Census 2021 data, includes people in a household who previously served in the UK armed forces and UK armed forces veteran indicator.",
                                "list_of_variables": {
                                        "hh_hrp_veteran": get_variable_title("hh_hrp_veteran", 'en'),
                                        "hh_veterans": get_variable_title("hh_veterans", 'en'),
                                        "residence_type": get_variable_title("residence_type", 'en'),
                                        "uk_armed_forces": get_variable_title("uk_armed_forces", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau cyn-filwyr lluoedd arfog y Deyrnas Unedig",
                            "summary_topic_page": "Yn cynnwys pobl mewn cartref sydd wedi gwasanaethu yn lluoedd arfog y Deyrnas Unedig yn y gorffennol a dangosydd cyn-filwr yn lluoedd arfog y Deyrnas Unedig.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau cyn-filwyr lluoedd arfog y Deyrnas Unedig Cyfrifiad 2021",
                            "summary_for_page": "Rhestr o newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys pobl mewn cartref sydd wedi gwasanaethu yn lluoedd arfog y Deyrnas Unedig yn y gorffennol a dangosydd cyn-filwr yn lluoedd arfog y Deyrnas Unedig.",
                            "list_of_variables": {
                                    "hh_hrp_veteran":get_variable_title("hh_hrp_veteran", 'cy'),
                                    "hh_veterans": get_variable_title("hh_veterans", 'cy'),
                                    "residence_type": get_variable_title("residence_type", 'cy'),
                                    "uk_armed_forces": get_variable_title("uk_armed_forces", 'cy')
                                    }
                            }
                }
        }
                        
    topic_dict = {}
    
    if list_of_topics == ['*']:
        return all_topic_dict
    
    else:
        for topic in all_topic_dict:
            if topic in list_of_topics:
                topic_dict[topic] = all_topic_dict[topic]
                
    if 'variables' in kwargs.keys() and kwargs['variables'] != ['*']:
        assert type(kwargs['variables']) == list, "variables must be a list"
        variables_to_keep = kwargs['variables']
        for topic in topic_dict.copy():
            for variable in topic_dict[topic]['en']['list_of_variables'].copy():
                if variable not in variables_to_keep:
                    del topic_dict[topic]['en']['list_of_variables'][variable]
                    del topic_dict[topic]['cy']['list_of_variables'][variable]
    
    return topic_dict


