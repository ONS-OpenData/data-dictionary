from cantabular_request import get_variable_title

def get_topic_dict(list_of_topics, **kwargs):
    # first key is topic (not used directly) 
    # title_topic_page -> title of tiles on variable by topic page
    #                  -> heading on list of variables page
    # summary_topic_page -> summary in tile on variable by topic page
    # uri_ending_topic_page -> used as link for tiles on variable by topic page
    #                       -> url of list of variables page
    # title_for_page -> page title on list of variables page
    # summary_for_page -> page summary on list of variables page
    # list_of_variables -> variables to be used for each topic
    #   key -> mnemonic to pull metadata from model
    #   value -> link & url for each variable page, how variable is displayed on list of variables page
    
    assert type(list_of_topics) == list, "list_of_topics must be in a list"
    
    all_topic_dict = {
                "demography": {
                        "en": {
                            "title_topic_page": "Demography variables",
                            "summary_topic_page": "Includes age, sex, household composition and legal partnership status.",
                            "uri_ending_topic_page": "demographyvariablescensus2021",
                            "title_for_page": "Demography variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes age, sex, household composition and legal partnership status.",
                            "list_of_variables": {
                                    "adult_lifestage": get_variable_title("adult_lifestage", 'en'),
                                    "hh_adults_and_children": get_variable_title("hh_adults_and_children", 'en'),
                                    "resident_age": get_variable_title("resident_age", 'en'),
                                    "resident_age_extended": get_variable_title("resident_age_extended", 'en'),
                                    "frp_age": get_variable_title("frp_age", 'en'),
                                    "hrp_age": get_variable_title("hrp_age", 'en'),
                                    "concealed_family_type": get_variable_title("concealed_family_type", 'en'),
                                    "dependent_child_age": get_variable_title("dependent_child_age", 'en'),
                                    #"family_dependent_children": get_variable_title("family_dependent_children", 'en'),
                                    "hh_dependent_children": get_variable_title("hh_dependent_children", 'en'),
                                    #"family_status": get_variable_title("family_status", 'en'),
                                    "family_status_by_workers_in_generation_1": get_variable_title("family_status_by_workers_in_generation_1", 'en'),
                                    #"families_and_children": get_variable_title("families_and_children", 'en'),
                                    "hh_family_composition": get_variable_title("hh_family_composition", 'en'),
                                    "hh_deprivation": get_variable_title("hh_deprivation", 'en'),
                                    "hh_deprivation_education": get_variable_title("hh_deprivation_education", 'en'),
                                    "hh_deprivation_employment": get_variable_title("hh_deprivation_employment", 'en'),
                                    "hh_deprivation_health": get_variable_title("hh_deprivation_health", 'en'),
                                    "hh_deprivation_housing": get_variable_title("hh_deprivation_housing", 'en'),
                                    "hh_migration_country_inflow": get_variable_title("hh_migration_country_inflow", 'en'),
                                    "hh_migration_country_outflow": get_variable_title("hh_migration_country_outflow", 'en'),
                                    "hh_migration_ltla_inflow": get_variable_title("hh_migration_ltla_inflow", 'en'),
                                    "hh_migration_ltla_outflow": get_variable_title("hh_migration_ltla_outflow", 'en'),
                                    "hh_migration_msoa_inflow": get_variable_title("hh_migration_msoa_inflow", 'en'),
                                    "hh_migration_msoa_outflow": get_variable_title("hh_migration_msoa_outflow", 'en'),
                                    "hh_migration_national_inflow": get_variable_title("hh_migration_national_inflow", 'en'),
                                    "hh_migration_region_inflow": get_variable_title("hh_migration_region_inflow", 'en'),
                                    "hh_migration_region_outflow": get_variable_title("hh_migration_region_outflow", 'en'),
                                    "hh_migration_utla_inflow": get_variable_title("hh_migration_utla_inflow", 'en'),
                                    "hh_migration_utla_outflow": get_variable_title("hh_migration_utla_outflow", 'en'),
                                    "hh_size": get_variable_title("hh_size", 'en'),
                                    "hh_families_type": get_variable_title("hh_families_type", 'en'),
                                    "hh_away_student": get_variable_title("hh_away_student", 'en'),
                                    "hh_lifestage": get_variable_title("hh_lifestage", 'en'),
                                    "living_arrangements": get_variable_title("living_arrangements", 'en'),
                                    "legal_partnership_status": get_variable_title("legal_partnership_status", 'en'),
                                    "migration_country_inflow": get_variable_title("migration_country_inflow", 'en'),
                                    "migration_country_outflow": get_variable_title("migration_country_outflow", 'en'),
                                    "migration_lsoa_inflow": get_variable_title("migration_lsoa_inflow", 'en'),
                                    "migration_lsoa_outflow": get_variable_title("migration_lsoa_outflow", 'en'),
                                    "migration_ltla_inflow": get_variable_title("migration_ltla_inflow", 'en'),
                                    "migration_ltla_outflow": get_variable_title("migration_ltla_outflow", 'en'),
                                    "migration_msoa_inflow": get_variable_title("migration_msoa_inflow", 'en'),
                                    "migration_msoa_outflow": get_variable_title("migration_msoa_outflow", 'en'),
                                    "migration_oa_inflow": get_variable_title("migration_oa_inflow", 'en'),
                                    "migration_oa_outflow": get_variable_title("migration_oa_outflow", 'en'),
                                    "migration_national_inflow": get_variable_title("migration_national_inflow", 'en'),
                                    "migration_region_inflow": get_variable_title("migration_region_inflow", 'en'),
                                    "migration_region_outflow": get_variable_title("migration_region_outflow", 'en'),
                                    "migration_utla_inflow": get_variable_title("migration_utla_inflow", 'en'),
                                    "migration_utla_outflow": get_variable_title("migration_utla_outflow", 'en'),
                                    "hh_multi_generation": get_variable_title("hh_multi_generation", 'en'),
                                    "hh_adults_num": get_variable_title("hh_adults_num", 'en'),
                                    "hh_families_count": get_variable_title("hh_families_count", 'en'),
                                    "hh_17_plus": get_variable_title("hh_17_plus", 'en'),
                                    "residence_type": get_variable_title("residence_type", 'en'),
                                    "sex": get_variable_title("sex", 'en'),
                                    "hh_composition_welsh": get_variable_title("hh_composition_welsh", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau demograffeg",
                            "summary_topic_page": "Yn cynnwys oedran, rhyw, cyfansoddiad y cartref a statws partneriaeth sifil.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau demograffeg Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys oedran, rhyw, cyfansoddiad y cartref a statws partneriaeth sifil.",
                            "list_of_variables": {
                                    "adult_lifestage": get_variable_title("adult_lifestage", 'cy'),
                                    "hh_adults_and_children": get_variable_title("hh_adults_and_children", 'cy'),
                                    "resident_age": get_variable_title("resident_age", 'cy'),
                                    "resident_age_extended": get_variable_title("resident_age_extended", 'cy'),
                                    "frp_age": get_variable_title("frp_age", 'cy'),
                                    "hrp_age": get_variable_title("hrp_age", 'cy'),
                                    "concealed_family_type": get_variable_title("concealed_family_type", 'cy'),
                                    "dependent_child_age": get_variable_title("dependent_child_age", 'cy'),
                                    #"family_dependent_children": get_variable_title("family_dependent_children", 'cy'),
                                    "hh_dependent_children": get_variable_title("hh_dependent_children", 'cy'),
                                    #"family_status": get_variable_title("family_status", 'cy'),
                                    "family_status_by_workers_in_generation_1": get_variable_title("family_status_by_workers_in_generation_1", 'cy'),
                                    #"families_and_children": get_variable_title("families_and_children", 'cy'),
                                    "hh_family_composition": get_variable_title("hh_family_composition", 'cy'),
                                    "hh_deprivation": get_variable_title("hh_deprivation", 'cy'),
                                    "hh_deprivation_education": get_variable_title("hh_deprivation_education", 'cy'),
                                    "hh_deprivation_employment": get_variable_title("hh_deprivation_employment", 'cy'),
                                    "hh_deprivation_health": get_variable_title("hh_deprivation_health", 'cy'),
                                    "hh_deprivation_housing": get_variable_title("hh_deprivation_housing", 'cy'),
                                    "hh_migration_country_inflow": get_variable_title("hh_migration_country_inflow", 'cy'),
                                    "hh_migration_country_outflow": get_variable_title("hh_migration_country_outflow", 'cy'),
                                    "hh_migration_ltla_inflow": get_variable_title("hh_migration_ltla_inflow", 'cy'),
                                    "hh_migration_ltla_outflow": get_variable_title("hh_migration_ltla_outflow", 'cy'),
                                    "hh_migration_msoa_inflow": get_variable_title("hh_migration_msoa_inflow", 'cy'),
                                    "hh_migration_msoa_outflow": get_variable_title("hh_migration_msoa_outflow", 'cy'),
                                    "hh_migration_national_inflow": get_variable_title("hh_migration_national_inflow", 'cy'),
                                    "hh_migration_region_inflow": get_variable_title("hh_migration_region_inflow", 'cy'),
                                    "hh_migration_region_outflow": get_variable_title("hh_migration_region_outflow", 'cy'),
                                    "hh_migration_utla_inflow": get_variable_title("hh_migration_utla_inflow", 'cy'),
                                    "hh_migration_utla_outflow": get_variable_title("hh_migration_utla_outflow", 'cy'),
                                    "hh_size": get_variable_title("hh_size", 'cy'),
                                    "hh_families_type": get_variable_title("hh_families_type", 'cy'),
                                    "hh_away_student": get_variable_title("hh_away_student", 'cy'),
                                    "hh_lifestage": get_variable_title("hh_lifestage", 'cy'),
                                    "living_arrangements": get_variable_title("living_arrangements", 'cy'),
                                    "legal_partnership_status": get_variable_title("legal_partnership_status", 'cy'),
                                    "migration_country_inflow": get_variable_title("migration_country_inflow", 'cy'),
                                    "migration_country_outflow": get_variable_title("migration_country_outflow", 'cy'),
                                    "migration_lsoa_inflow": get_variable_title("migration_lsoa_inflow", 'cy'),
                                    "migration_lsoa_outflow": get_variable_title("migration_lsoa_outflow", 'cy'),
                                    "migration_ltla_inflow": get_variable_title("migration_ltla_inflow", 'cy'),
                                    "migration_ltla_outflow": get_variable_title("migration_ltla_outflow", 'cy'),
                                    "migration_msoa_inflow": get_variable_title("migration_msoa_inflow", 'cy'),
                                    "migration_msoa_outflow": get_variable_title("migration_msoa_outflow", 'cy'),
                                    "migration_oa_inflow": get_variable_title("migration_oa_inflow", 'cy'),
                                    "migration_oa_outflow": get_variable_title("migration_oa_outflow", 'cy'),
                                    "migration_national_inflow": get_variable_title("migration_national_inflow", 'cy'),
                                    "migration_region_inflow": get_variable_title("migration_region_inflow", 'cy'),
                                    "migration_region_outflow": get_variable_title("migration_region_outflow", 'cy'),
                                    "migration_utla_inflow": get_variable_title("migration_utla_inflow", 'cy'),
                                    "migration_utla_outflow": get_variable_title("migration_utla_outflow", 'cy'),
                                    "hh_multi_generation": get_variable_title("hh_multi_generation", 'cy'),
                                    "hh_adults_num": get_variable_title("hh_adults_num", 'cy'),
                                    "hh_families_count": get_variable_title("hh_families_count", 'cy'),
                                    "hh_17_plus": get_variable_title("hh_17_plus", 'cy'),
                                    "residence_type": get_variable_title("residence_type", 'cy'),
                                    "sex": get_variable_title("sex", 'cy'),
                                    "hh_composition_welsh": get_variable_title("hh_composition_welsh", 'cy')
                                    }
                            }
                },
                "education": {
                        "en": {
                            "title_topic_page": "Education variables",
                            "summary_topic_page": "Includes the highest qualification people have gained and people who are in full-time education.",
                            "uri_ending_topic_page": "educationvariablescensus2021",
                            "title_for_page": "Education variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes the highest qualification people have gained and people who are in full-time education.",
                            "list_of_variables": {
                                    "highest_qualification": get_variable_title("highest_qualification", 'en'),
                                    "in_full_time_education": get_variable_title("in_full_time_education", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau addysg",
                            "summary_topic_page": "Yn cynnwys y cymhwyster uchaf sydd gan bobl a phobl sydd mewn addysg amser llawn.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau addysg Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021 sy'n cynnwys y cymhwyster uchaf sydd gan bobl a phobl sydd mewn addysg amser llawn.",
                            "list_of_variables": {
                                    "highest_qualification": get_variable_title("highest_qualification", 'cy'),
                                    "in_full_time_education": get_variable_title("in_full_time_education", 'cy')
                                    }
                            }
                },
                "eilr": {
                        "en": {
                            "title_topic_page": "Ethnic group, national identity, language and religion variables",
                            "summary_topic_page": "Includes languages, national identity, ethnic group, multiple religions in household and main language.",
                            "uri_ending_topic_page": "ethnicgroupnationalidentitylanguageandreligionvariablescensus2021", 
                            "title_for_page": "Ethnic group, national identity, language and religion variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes languages, national identity, ethnic group, multiple religions in household and main language.",
                            "list_of_variables": {
                                    "hh_multi_ethnic_combination": get_variable_title("hh_multi_ethnic_combination", 'en'),
                                    "hh_multi_religion_combination": get_variable_title("hh_multi_religion_combination", 'en'),
                                    "ethnic_group_tb": get_variable_title("ethnic_group_tb", 'en'),
                                    "ethnic_group": get_variable_title("ethnic_group", 'en'),
                                    "hrp_ethnic_group_tb": get_variable_title("hrp_ethnic_group_tb", 'en'),
                                    "families_and_children_welsh_speaker_parents": get_variable_title("families_and_children_welsh_speaker_parents", 'en'),
                                    "hh_language": get_variable_title("hh_language", 'en'),
                                    "main_language": get_variable_title("main_language", 'en'),
                                    "main_language_detailed": get_variable_title("main_language_detailed", 'en'),
                                    "hh_multi_ethnic_group": get_variable_title("hh_multi_ethnic_group", 'en'),
                                    "hh_multi_language": get_variable_title("hh_multi_language", 'en'),
                                    "hh_multi_religion": get_variable_title("hh_multi_religion", 'en'),
                                    "national_identity_all": get_variable_title("national_identity_all", 'en'),
                                    "national_identity_detailed": get_variable_title("national_identity_detailed", 'en'),
                                    "welsh_speaking_3_plus": get_variable_title("welsh_speaking_3_plus", 'en'),
                                    "english_proficiency": get_variable_title("english_proficiency", 'en'),
                                    "religion_tb": get_variable_title("religion_tb", 'en'),
                                    "religion": get_variable_title("religion", 'en'),
                                    "welsh_skills_all": get_variable_title("welsh_skills_all", 'en'),
                                    "welsh_skills_read": get_variable_title("welsh_skills_read", 'en'),
                                    "hh_welsh_speak_3_plus": get_variable_title("hh_welsh_speak_3_plus", 'en'),
                                    "welsh_skills_speak": get_variable_title("welsh_skills_speak", 'en'),
                                    "welsh_speaking_dependent_child": get_variable_title("welsh_speaking_dependent_child", 'en'),
                                    "hh_welsh_speaking_adults": get_variable_title("hh_welsh_speaking_adults", 'en'),
                                    "hh_adult_welsh_speakers": get_variable_title("hh_adult_welsh_speakers", 'en'),
                                    "welsh_skills_understand": get_variable_title("welsh_skills_understand", 'en'),
                                    "welsh_skills_write": get_variable_title("welsh_skills_write", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau grŵp ethnig, hunaniaeth genedlaethol, iaith a chrefydd",
                            "summary_topic_page": "Yn cynnwys ieithoedd, hunaniaeth genedlaethol, grŵp ethnig, sawl crefydd mewn cartref a phrif iaith.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau grŵp ethnig, hunaniaeth genedlaethol, iaith a chrefydd Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys ieithoedd, hunaniaeth genedlaethol, grŵp ethnig, sawl crefydd mewn cartref a phrif iaith.",
                            "list_of_variables": {
                                    "hh_multi_ethnic_combination": get_variable_title("hh_multi_ethnic_combination", 'cy'),
                                    "hh_multi_religion_combination": get_variable_title("hh_multi_religion_combination", 'cy'),
                                    "ethnic_group_tb": get_variable_title("ethnic_group_tb", 'cy'),
                                    "ethnic_group": get_variable_title("ethnic_group", 'cy'),
                                    "hrp_ethnic_group_tb": get_variable_title("hrp_ethnic_group_tb", 'cy'),
                                    "families_and_children_welsh_speaker_parents": get_variable_title("families_and_children_welsh_speaker_parents", 'cy'),
                                    "hh_language": get_variable_title("hh_language", 'cy'),
                                    "main_language": get_variable_title("main_language", 'cy'),
                                    "main_language_detailed": get_variable_title("main_language_detailed", 'cy'),
                                    "hh_multi_ethnic_group": get_variable_title("hh_multi_ethnic_group", 'cy'),
                                    "hh_multi_language": get_variable_title("hh_multi_language", 'cy'),
                                    "hh_multi_religion": get_variable_title("hh_multi_religion", 'cy'),
                                    "national_identity_all": get_variable_title("national_identity_all", 'cy'),
                                    "national_identity_detailed": get_variable_title("national_identity_detailed", 'cy'),
                                    "welsh_speaking_3_plus": get_variable_title("welsh_speaking_3_plus", 'cy'),
                                    "english_proficiency": get_variable_title("english_proficiency", 'cy'),
                                    "religion_tb": get_variable_title("religion_tb", 'cy'),
                                    "religion": get_variable_title("religion", 'cy'),
                                    "welsh_skills_all": get_variable_title("welsh_skills_all", 'cy'),
                                    "welsh_skills_read": get_variable_title("welsh_skills_read", 'cy'),
                                    "hh_welsh_speak_3_plus": get_variable_title("hh_welsh_speak_3_plus", 'cy'),
                                    "welsh_skills_speak": get_variable_title("welsh_skills_speak", 'cy'),
                                    "welsh_speaking_dependent_child": get_variable_title("welsh_speaking_dependent_child", 'cy'),
                                    "hh_welsh_speaking_adults": get_variable_title("hh_welsh_speaking_adults", 'cy'),
                                    "hh_adult_welsh_speakers": get_variable_title("hh_adult_welsh_speakers", 'cy'),
                                    "welsh_skills_understand": get_variable_title("welsh_skills_understand", 'cy'),
                                    "welsh_skills_write": get_variable_title("welsh_skills_write", 'cy')
                                    }
                            }
                },
                "health": {
                        "en": {
                            "title_topic_page": "Health, disability, and unpaid care variables",
                            "summary_topic_page": "Includes general health, disability, number of disabled people in household and unpaid care.",
                            "uri_ending_topic_page": "healthdisabilityandunpaidcarevariablescensus2021",
                            "title_for_page": "Health, disability and unpaid care variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes general health, disability, number of disabled people in household and unpaid care.",
                            "list_of_variables": {
                                    "disability": get_variable_title("disability", 'en'),
                                    "health_in_general": get_variable_title("health_in_general", 'en'),
                                    "hh_adults_disabled": get_variable_title("hh_adults_disabled", 'en'),
                                    "hh_disabled": get_variable_title("hh_disabled", 'en'),
                                    "hh_number_limited_little": get_variable_title("hh_number_limited_little", 'en'),
                                    "hh_number_limited_lot": get_variable_title("hh_number_limited_lot", 'en'),
                                    "hh_not_limited": get_variable_title("hh_not_limited", 'en'),
                                    "hh_no_condition": get_variable_title("hh_no_condition", 'en'),
                                    "hh_carers": get_variable_title("hh_carers", 'en'),
                                    "is_carer": get_variable_title("is_carer", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau iechyd, anabledd a gofal di-dâl",
                            "summary_topic_page": "Yn cynnwys iechyd cyffredinol, anabledd, nifer y bobl anabl yn y cartref a gofal di-dâl.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau iechyd, anabledd a gofal di-dâl Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys iechyd cyffredinol, anabledd, nifer y bobl anabl yn y cartref a gofal di-dâl.",
                            "list_of_variables": {
                                    "disability": get_variable_title("disability", 'cy'),
                                    "health_in_general": get_variable_title("health_in_general", 'cy'),
                                    "hh_adults_disabled": get_variable_title("hh_adults_disabled", 'cy'),
                                    "hh_disabled": get_variable_title("hh_disabled", 'cy'),
                                    "hh_number_limited_little": get_variable_title("hh_number_limited_little", 'cy'),
                                    "hh_number_limited_lot": get_variable_title("hh_number_limited_lot", 'cy'),
                                    "hh_not_limited": get_variable_title("hh_not_limited", 'cy'),
                                    "hh_no_condition": get_variable_title("hh_no_condition", 'cy'),
                                    "hh_carers": get_variable_title("hh_carers", 'cy'),
                                    "is_carer": get_variable_title("is_carer", 'cy')
                                    }
                            }
                },
                "housing": {
                        "en": {
                            "title_topic_page": "Housing variables",
                            "summary_topic_page": "Includes accommodation type, tenure, number of bedrooms, communal establishments, second addresses and number of cars.",
                            "uri_ending_topic_page": "housingvariablescensus2021",
                            "title_for_page": "Housing variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes accommodation type, tenure, number of bedrooms, communal establishments, second addresses and number of cars.",
                            "list_of_variables": {
                                    "accom_by_dwelling_type": get_variable_title("accom_by_dwelling_type", 'en'),
                                    "accommodation_type": get_variable_title("accommodation_type", 'en'),
                                    "ce_management_type": get_variable_title("ce_management_type", 'en'),
                                    "dwelling_hmo_unrelated": get_variable_title("dwelling_hmo_unrelated", 'en'),
                                    "number_bedrooms": get_variable_title("number_bedrooms", 'en'),
                                    "number_of_cars": get_variable_title("number_of_cars", 'en'),
                                    "hh_spaces_shared_dwelling": get_variable_title("hh_spaces_shared_dwelling", 'en'),
                                    "hh_persons_per_bedroom": get_variable_title("hh_persons_per_bedroom", 'en'),
                                    "hh_persons_per_room": get_variable_title("hh_persons_per_room", 'en'),
                                    "voa_number_of_rooms": get_variable_title("voa_number_of_rooms", 'en'),
                                    "occupancy_rating_bedrooms": get_variable_title("occupancy_rating_bedrooms", 'en'),
                                    "occupancy_rating_rooms": get_variable_title("occupancy_rating_rooms", 'en'),
                                    "position_in_ce": get_variable_title("position_in_ce", 'en'),
                                    "ce_position_age": get_variable_title("ce_position_age", 'en'),
                                    "ce_position_ethnic_group": get_variable_title("ce_position_ethnic_group", 'en'),
                                    "ce_position_religion": get_variable_title("ce_position_religion", 'en'),
                                    "ce_position_sex_age": get_variable_title("ce_position_sex_age", 'en'),
                                    "alternative_address_indicator": get_variable_title("alternative_address_indicator", 'en'),
                                    "second_address_type_priority": get_variable_title("second_address_type_priority", 'en'),
                                    "student_accommodation_type": get_variable_title("student_accommodation_type", 'en'),
                                    "hh_tenure": get_variable_title("hh_tenure", 'en'),
                                    "heating_type": get_variable_title("heating_type", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau tai",
                            "summary_topic_page": "Yn cynnwys math o gartref, deiliadaeth, nifer yr ystafelloedd gwely, sefydliadau cymunedol, ail gyfeiriadau a nifer y ceir.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau tai Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys math o gartref, deiliadaeth, nifer yr ystafelloedd gwely, sefydliadau cymunedol, ail gyfeiriadau a nifer y ceir.",
                            "list_of_variables": {
                                    "accom_by_dwelling_type": get_variable_title("accom_by_dwelling_type", 'cy'),
                                    "accommodation_type": get_variable_title("accommodation_type", 'cy'),
                                    "ce_management_type": get_variable_title("ce_management_type", 'cy'),
                                    "dwelling_hmo_unrelated": get_variable_title("dwelling_hmo_unrelated", 'cy'),
                                    "number_bedrooms": get_variable_title("number_bedrooms", 'cy'),
                                    "number_of_cars": get_variable_title("number_of_cars", 'cy'),
                                    "hh_spaces_shared_dwelling": get_variable_title("hh_spaces_shared_dwelling", 'cy'),
                                    "hh_persons_per_bedroom": get_variable_title("hh_persons_per_bedroom", 'cy'),
                                    "hh_persons_per_room": get_variable_title("hh_persons_per_room", 'cy'),
                                    "voa_number_of_rooms": get_variable_title("voa_number_of_rooms", 'cy'),
                                    "occupancy_rating_bedrooms": get_variable_title("occupancy_rating_bedrooms", 'cy'),
                                    "occupancy_rating_rooms": get_variable_title("occupancy_rating_rooms", 'cy'),
                                    "position_in_ce": get_variable_title("position_in_ce", 'cy'),
                                    "ce_position_age": get_variable_title("ce_position_age", 'cy'),
                                    "ce_position_ethnic_group": get_variable_title("ce_position_ethnic_group", 'cy'),
                                    "ce_position_religion": get_variable_title("ce_position_religion", 'cy'),
                                    "ce_position_sex_age": get_variable_title("ce_position_sex_age", 'cy'),
                                    "alternative_address_indicator": get_variable_title("alternative_address_indicator", 'cy'),
                                    "second_address_type_priority": get_variable_title("second_address_type_priority", 'cy'),
                                    "student_accommodation_type": get_variable_title("student_accommodation_type", 'cy'),
                                    "hh_tenure": get_variable_title("hh_tenure", 'cy'),
                                    "heating_type": get_variable_title("heating_type", 'cy')
                                    }
                            }
                },
                "international migration": {
                        "en": {
                            "title_topic_page": "International migration variables",
                            "summary_topic_page": "Includes the year that people arrived in the UK and their age, country of birth, length of residence, and migrant indicator.",
                            "uri_ending_topic_page": "internationalmigrationvariablescensus2021", 
                            "title_for_page": "International migration variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes the year that people arrived in the UK and their age, country of birth, length of residence, and migrant indicator.",
                            "list_of_variables": {
                                    "age_arrival_uk": get_variable_title("age_arrival_uk", 'en'),
                                    "country_of_birth": get_variable_title("country_of_birth", 'en'),
                                    "country_of_birth_extended": get_variable_title("country_of_birth_extended", 'en'),
                                    "residence_length": get_variable_title("residence_length", 'en'),
                                    "migrant_ind": get_variable_title("migrant_ind", 'en'),
                                    "multi_passports": get_variable_title("multi_passports", 'en'),
                                    "passports_all": get_variable_title("passports_all", 'en'),
                                    "year_arrival_uk": get_variable_title("year_arrival_uk", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau mudo rhyngwladol",
                            "summary_topic_page": "Yn cynnwys y flwyddyn y cyrhaeddodd pobl y Deyrnas Unedig a'u hoedran, eu gwlad enedigol, cyfnod preswylio, a dangosydd mudwyr.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau mudo rhyngwladol Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys y flwyddyn y cyrhaeddodd pobl y Deyrnas Unedig a'u hoedran, eu gwlad enedigol, cyfnod preswylio, a dangosydd mudwyr.",
                            "list_of_variables": {
                                    "age_arrival_uk": get_variable_title("age_arrival_uk", 'cy'),
                                    "country_of_birth": get_variable_title("country_of_birth", 'cy'),
                                    "country_of_birth_extended": get_variable_title("country_of_birth_extended", 'cy'),
                                    "residence_length": get_variable_title("residence_length", 'cy'),
                                    "migrant_ind": get_variable_title("migrant_ind", 'cy'),
                                    "multi_passports": get_variable_title("multi_passports", 'cy'),
                                    "passports_all": get_variable_title("passports_all", 'cy'),
                                    "year_arrival_uk": get_variable_title("year_arrival_uk", 'cy')
                                    }
                            }
                },
                "labour market": {
                        "en": {
                            "title_topic_page": "Labour market variables",
                            "summary_topic_page": "Includes, economic activity status, current occupation, current industry, hours worked and unemployment history.",
                            "uri_ending_topic_page": "labourmarketvariablescensus2021",
                            "title_for_page": "Labour market variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data includes, economic activity status, current occupation, current industry, hours worked and unemployment history.",
                            "list_of_variables": {
                                    "approx_social_grade": get_variable_title("approx_social_grade", 'en'),
                                    "economic_activity": get_variable_title("economic_activity", 'en'),
                                    "economic_activity_hours_worked": get_variable_title("economic_activity_hours_worked", 'en'),
                                    "activity_last_week": get_variable_title("activity_last_week", 'en'),
                                    "hrp_economic_activity": get_variable_title("hrp_economic_activity", 'en'),
                                    "has_ever_worked": get_variable_title("has_ever_worked", 'en'),
                                    "hours_per_week_worked": get_variable_title("hours_per_week_worked", 'en'),
                                    "industry_current": get_variable_title("industry_current", 'en'),
                                    "industry_former": get_variable_title("industry_former", 'en'),
                                    "ns_sec": get_variable_title("ns_sec", 'en'),
                                    "hrp_ns_sec": get_variable_title("hrp_ns_sec", 'en'),
                                    "hh_adults_employment": get_variable_title("hh_adults_employment", 'en'),
                                    "occupation_current": get_variable_title("occupation_current", 'en'),
                                    "occupation_former": get_variable_title("occupation_former", 'en'),
                                    "place_of_work_ind": get_variable_title("place_of_work_ind", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau'r farchnad lafur",
                            "summary_topic_page": "Yn cynnwys statws gweithgarwch economaidd, galwedigaeth gyfredol, diwydiant cyfredol, oriau gwaith a hanes diweithdra.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau'r farchnad lafur Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021 sy'n cynnwys statws gweithgarwch economaidd, galwedigaeth gyfredol, diwydiant cyfredol, oriau gwaith a hanes diweithdra.",
                            "list_of_variables": {
                                    "approx_social_grade": get_variable_title("approx_social_grade", 'cy'),
                                    "economic_activity": get_variable_title("economic_activity", 'cy'),
                                    "economic_activity_hours_worked": get_variable_title("economic_activity_hours_worked", 'cy'),
                                    "activity_last_week": get_variable_title("activity_last_week", 'cy'),
                                    "hrp_economic_activity": get_variable_title("hrp_economic_activity", 'cy'),
                                    "has_ever_worked": get_variable_title("has_ever_worked", 'cy'),
                                    "hours_per_week_worked": get_variable_title("hours_per_week_worked", 'cy'),
                                    "industry_current": get_variable_title("industry_current", 'cy'),
                                    "industry_former": get_variable_title("industry_former", 'cy'),
                                    "ns_sec": get_variable_title("ns_sec", 'cy'),
                                    "hrp_ns_sec": get_variable_title("hrp_ns_sec", 'cy'),
                                    "hh_adults_employment": get_variable_title("hh_adults_employment", 'cy'),
                                    "occupation_current": get_variable_title("occupation_current", 'cy'),
                                    "occupation_former": get_variable_title("occupation_former", 'cy'),
                                    "place_of_work_ind": get_variable_title("place_of_work_ind", 'cy')
                                    }
                            }
                },
                "sogi": {
                        "en": {
                            "title_topic_page": "Sexual orientation and gender identity variables",
                            "summary_topic_page": "Includes gender identity and sexual orientation.",
                            "uri_ending_topic_page": "sexualorientationandgenderidentityvariablescensus2021",
                            "title_for_page": "Sexual orientation and gender identity variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes gender identity and sexual orientation.",
                            "list_of_variables": {
                                    "gender_identity": get_variable_title("gender_identity", 'en'),
                                    "sexual_orientation": get_variable_title("sexual_orientation", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau cyfeiriadedd rhywiol a hunaniaeth o ran rhywedd",
                            "summary_topic_page": "Yn cynnwys hunaniaeth o ran rhywedd a chyfeiriadedd rhywiol.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau cyfeiriadedd rhywiol a hunaniaeth o ran rhywedd Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021 sy'n cynnwys hunaniaeth o ran rhywedd a chyfeiriadedd rhywiol.",
                            "list_of_variables": {
                                    "gender_identity": get_variable_title("gender_identity", 'cy'),
                                    "sexual_orientation": get_variable_title("sexual_orientation", 'cy')
                                    }
                            }
                },
                "travel to work": {
                        "en": {
                            "title_topic_page": "Travel to work variables",
                            "summary_topic_page": "Includes method used to travel to work and distance travelled to work.",
                            "uri_ending_topic_page": "traveltoworkvariablescensus2021",
                            "title_for_page": "Travel to work variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes method used to travel to work and distance travelled to work.",
                            "list_of_variables": {
                                    "workplace_travel": get_variable_title("workplace_travel", 'en'),
                                    "transport_to_workplace": get_variable_title("transport_to_workplace", 'en'),
                                    "workers_transport": get_variable_title("workers_transport", 'en')
                                    }
                                },
                        "cy": {
                            "title_topic_page": "Newidynnau teithio i'r gwaith",
                            "summary_topic_page": "Yn cynnwys dull o deithio i'r gwaith a phellter teithio i'r gwaith.",
                            "uri_ending_topic_page": "",
                            "title_for_page": "Newidynnau teithio i'r gwaith Cyfrifiad 2021",
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys dull o deithio i'r gwaith a phellter teithio i'r gwaith.",
                            "list_of_variables": {
                                    "workplace_travel": get_variable_title("workplace_travel", 'cy'),
                                    "transport_to_workplace": get_variable_title("transport_to_workplace", 'cy'),
                                    "workers_transport": get_variable_title("workers_transport", 'cy')
                                    }
                            }
                },
                "UK armed forces veterans": {
                        "en": {
                            "title_topic_page": "UK armed forces veterans variables",
                            "summary_topic_page": "Includes number of people in household who previously served in the UK armed forces and UK armed forces veteran indicator.",
                            "uri_ending_topic_page": "ukarmedforcesveteransvariablescensus2021",
                            "title_for_page": "UK armed forces veterans variables Census 2021",
                            "summary_for_page": "Variables used in Census 2021 data, includes people in a household who previously served in the UK armed forces and UK armed forces veteran indicator.",
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
                            "summary_for_page": "Newidynnau a ddefnyddir yn nata Cyfrifiad 2021, sy'n cynnwys pobl mewn cartref sydd wedi gwasanaethu yn lluoedd arfog y Deyrnas Unedig yn y gorffennol a dangosydd cyn-filwr yn lluoedd arfog y Deyrnas Unedig.",
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

