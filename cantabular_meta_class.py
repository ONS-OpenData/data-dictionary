import datetime, os, time, requests
from cantabular_request import get_variable_details
from data_dict_dicts import get_topic_dict

environment = "test"

collection_name = "dd test"

list_of_all_topics = ['demography', 'international migration', 'UK armed forces veterans'] # used for updating list of topics page


# TODO - add some kind of tagging system
pages_to_run = {
        "dd_landing_page": False, # only - True/False
        "variables_by_topic_landing_page": False, # only - True/False TODO -> only True if all topics included in topic_dict
        "list_of_variables_landing_page": True, # only - True/False
        "variables_page": True, # only - True/False
        "topics": ["UK armed forces veterans"], # * for all, otherwise specify
        "variables": ["uk_armed_forces"] # * for all, otherwise specify
        }

#topic_dict = get_topic_dict(pages_to_run['topics'], variables=pages_to_run['variables'])

class making_request():
    # class object that makes requests
    # set as functions so can control what is being called depending on environment
    
    def curl_request(self, request_type, url, **kwargs):
        # request_type - GET/POST
        # kwargs will be data required for POST
        # returns url if environment is set to test
        
        if self.environment == 'test':
            '''
            if request_type.lower() == 'get':
                print(f"GET request to {url}")
                
            elif request_type.lower() == 'post':
                print(f"POST request to {url}")
            '''
            return
                
        if request_type.lower() == 'get':
            response_dict = self.get_curl_request(url)
            
        elif request_type.lower() == 'post':
            response_dict = self.post_curl_request(url,  **kwargs)
            
        return response_dict

    def get_curl_request(self, url):
        # assuming response is a json
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            raise Exception(f"GET - {url} returned a {r.status_code}")
        response_dict = r.json()
        return response_dict
    
    def post_curl_request(self, url, **kwargs):
        if 'json' in kwargs.keys():
            data = kwargs['json']
            r = requests.post(url, headers=self.headers, json=data)
            if r.status_code != 200:
                raise Exception(f"POST - {url} returned a {r.status_code}")
            return
        
    def send_for_review(self, url):
        # all POSTs to send page to reviewed status are the same 
        
        if self.environment == 'test':
            #print("Test reviewed")
            return
        
        review_payload = {
                "trigger":{
                        "elementClasses":[
                                "btn",
                                "btn--positive",
                                "btn-edit-save-and-submit-for-review"
                                ]
                        },
                "collection":{
                        "id":self.collection_id,
                        "name":self.collection_name,
                        "type":"manual"
                        }
                }
        r = requests.post(url, headers=self.headers, json=review_payload)
        if r.status_code != 200:
            raise Exception(f"Page review - {url} returned a {r.status_code}")
        return


class data_dictionary_upload(making_request):
    def __init__(self, environment, collection_name, dict_of_pages_to_upload):
        self.environment = environment
        self.dict_of_pages_to_upload = dict_of_pages_to_upload
        self.collection_name = collection_name
        
        self.get_access_token()
        self.topic_dict = get_topic_dict(self.dict_of_pages_to_upload['topics'], variables=self.dict_of_pages_to_upload['variables'])
        
        self.get_collection_id()
        self.release_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT00:00:00.000Z')
    
    def run(self):
        if self.dict_of_pages_to_upload['dd_landing_page']:
            # creates dd landing page - mostly will be left untouched
            self.create_dd_landing_page()
            time.sleep(1)
            
        if self.dict_of_pages_to_upload['variables_by_topic_landing_page']:
            # creates variable by topic landing page - mostly will be left untouched
            self.create_variable_by_topic_landing_page()
            time.sleep(1)
            
        if self.dict_of_pages_to_upload['list_of_variables_landing_page']:
            # creates list of variables page for each included topic
            if self.dict_of_pages_to_upload['variables'] != ["*"]:
                raise Exception(f"Must include all variables in a topic to upload the list of variables page")
            for topic in self.topic_dict:
                self.create_list_of_variables_page(topic)
                time.sleep(1)
                
        if self.dict_of_pages_to_upload['variables_page']:
            # creates variable page for each included variable
            for topic in self.topic_dict:
                for variable in self.topic_dict[topic]['en']['list_of_variables']:
                    print(variable)
                    try:
                        variable_details = get_variable_details(variable)
                        self.create_variable_page(variable_details)
                    except:
                        print(f'could not find varibale - {variable}')
                    print('---')
                    time.sleep(1)
        
        
    
    def set_up_url(self):
        if self.environment == "prod" or self.environment == "test":
            self.url = 'http://localhost:10800/v1'
        
        elif self.environment == 'sandbox':
            self.url = 'https://publishing.dp.aws.onsdigital.uk'
            
        else:
            raise Exception(f"environment must be given as either 'prod/sandbox/test' not {self.environment}")
    
    def get_access_token(self):
        self.set_up_url()
        
        if self.environment == 'prod':
            email = os.getenv('FLORENCE_EMAIL')
            password = os.getenv('FLORENCE_PASSWORD')
            assert email != None, "FLORENCE_EMAIL not found in environment variables"
            assert password != None, "FLORENCE_PASSWORD not found in environment variables"
            login = login = {"email": email, "password": password}
            
            login_url = f"{self.url}/login"
            r = requests.post(login_url, json=login)
            
            if r.status_code == 200:
                access_token = r.text.strip('"')
                self.headers = {"X-Florence-Token": access_token}
            
            else:
                raise Exception(f"access_token not generated - {r.status_code} error")
                     
        elif self.environment == 'test':
            self.headers = '' 
            
        elif self.environment == 'sandbox':
            access_token = ""
            if access_token == "":
                raise Exception("will need to manually assign access_token")
            self.headers = {"X-Florence-Token": access_token}
            
    def get_collection_id(self):
        if self.environment == 'test':
            self.collection_id = 'collection_id'
            return
        
        self.get_all_collections()
        for collection in self.collection_list:
            if collection["name"] == self.collection_name:
                collection_id = collection["id"]
                break
        
        # TODO - should create collection if doesnt exist?
        self.collection_id = collection_id
            
    def get_all_collections(self):
        if self.environment == 'prod':
            collection_url = f"{self.url}/collections"
            
        elif self.environment == 'sandbox':
            collection_url = f"{self.url}/dataset/collections"
            
        r = requests.get(collection_url, headers=self.headers)
        if r.status_code != 200:
            raise Exception(f"{collection_url} returned a {r.status_code}")
        
        self.collection_list = r.json()
        
    def create_dd_landing_page(self):
        # creates landing page for the data dictionary
        # POSTs to /census
        uri_name = 'census2021dictionary'
        
        for language in ('en', 'cy'):
            if language == 'cy':
                return
            
            page_info = {
                    'en': {
                            'page_title': 'Census 2021 dictionary',
                            'page_summary': 'Detailed information about variables, definitions and classifications to help when using Census 2021 data.',
                            'section_title': 'Variables by topic',
                            'section_summary': 'Lists variables by topic to help when using Census 2021 data.'
                            },
                    'cy': {
                            'page_title': 'Geiriadur Cyfrifiad 2021', 
                            'page_summary': 'Gwybodaeth fanwl am newidynnau, diffiniadau a dosbarthiadau er mwyn helpu wrth ddefnyddio data Cyfrifiad 2021.',
                            'section_title': 'Newidynnau yn ôl pwnc',
                            'section_summary': 'Rhestr o newidynnau yn ôl pwnc er mwyn helpu wrth ddefnyddio data Cyfrifiad 2021.'
                            }
                    }
            
            page_title = page_info[language]['page_title']
            page_summary = page_info[language]['page_summary']
            section_title = page_info[language]['section_title']
            section_summary = page_info[language]['section_summary']
            
            sections = [
                    {
                        'title': section_title,
                        'summary': section_summary,
                        'uri': f'/census/{uri_name}/variablesbytopic' 
                            }
                    ]
            
            # static_landing_page 
            metadata_payload = {
                    "description":{
                            "title":page_title,
                            "summary":page_summary,
                            "releaseDate":self.release_date,
                            "keywords":[],
                            "metaDescription":"",
                            "language":language,
                            "survey":"census"
                            },
                    "markdown":[],
                    "sections":sections,
                    "charts":[],
                    "tables":[],
                    "equations":[],
                    "images":[],
                    "downloads":[],
                    "type":"static_landing_page",
                    "anchors":[],
                    "links":[],
                    "fileName":uri_name
                    }
            
            if language == 'en':
                uri = f"/census/{uri_name}/data.json"
                
            elif language == 'cy':
                uri = f"/census/{uri_name}/data_cy.json"
                
            
            if self.environment == "prod" or self.environment == "test":
                content_path = f"/content/{self.collection_id}?uri={uri}"
                review_path = f"/complete/{self.collection_id}?uri={uri}"
                
            elif self.environment == "sandbox":
                content_path = f"/zebedee/content/{self.collection_id}?uri={uri}"
                review_path = f"/zebedee/complete/{self.collection_id}?uri={uri}" 
                
            content_url = f"{self.url}{content_path}"
            review_url = f"{self.url}{review_path}"
        
            self.curl_request('post', content_url, json=metadata_payload)
            print(f"DD landing page sent - {language}")
            
            self.send_for_review(review_url)
            print("DD landing page reviewed")
            
        return 
    
    def create_variable_by_topic_landing_page(self):
        # creates landing page for each topic
        # POSTs to /census
        
        dd_location = 'census2021dictionary'
        uri_name = 'variablesbytopic'
        for language in ('en', 'cy'):
            if language == 'cy':
                return
    
            page_info = {
                    'en': {
                            'page_title': 'Variables by topic',
                            'page_summary': 'Lists variables by topic to help when using Census 2021 data.'
                            },
                    'cy': {
                            'page_title': 'Newidynnau yn ôl pwnc',
                            'page_summary': 'Rhestr o newidynnau yn ôl pwnc er mwyn helpu wrth ddefnyddio data Cyfrifiad 2021.'
                            }
                    }
            page_title = page_info[language]['page_title']
            page_summary = page_info[language]['page_summary']
            
            sections = []
            for topic in self.topic_dict:
                loop_dict = {}
                loop_dict['title'] = self.topic_dict[topic][language]['title_topic_page']
                loop_dict['summary'] = self.topic_dict[topic][language]['summary_topic_page']
                loop_dict['uri'] = f"/census/census2021dictionary/{uri_name}/{self.topic_dict[topic]['en']['uri_ending_topic_page']}"
                sections.append(loop_dict)
            
            # static_landing_page 
            metadata_payload = {
                    "description":{
                            "title":page_title,
                            "summary":page_summary,
                            "releaseDate":self.release_date,
                            "keywords":[],
                            "metaDescription":"",
                            "language":language,
                            "survey":"census"
                            },
                    "markdown":[],
                    "sections":sections,
                    "charts":[],
                    "tables":[],
                    "equations":[],
                    "images":[],
                    "downloads":[],
                    "type":"static_landing_page",
                    "anchors":[],
                    "links":[],
                    "fileName":uri_name
                    }
            
            if language == 'en':
                uri = f"/census/{dd_location}/{uri_name}/data.json"
                
            elif language == 'cy':
                uri = f"/census/{dd_location}/{uri_name}/data_cy.json"
            
            if self.environment == "prod" or self.environment == "test":
                content_path = f"/content/{self.collection_id}?uri={uri}"
                review_path = f"/complete/{self.collection_id}?uri={uri}"
            
            elif self.environment == "sandbox":
                content_path = f"/zebedee/content/{self.collection_id}?uri={uri}"
                review_path = f"/zebedee/complete/{self.collection_id}?uri={uri}"
                
            content_url = f"{self.url}{content_path}"
            review_url = f"{self.url}{review_path}"
            
            self.curl_request('post', content_url, json=metadata_payload)
            print(f"Topic landing page sent - {language}")
            self.send_for_review(review_url)
            print("Topic landing page reviewed")
            
        return
    
    def create_list_of_variables_page(self, topic):
        # creates a page listing all variables for each topic
        # POSTs to /census
        
        topic_location = f"census2021dictionary/variablesbytopic"
        uri_name = self.topic_dict[topic]['en']['uri_ending_topic_page']
        for language in ('en', 'cy'):
            if language == 'cy':
                return
        
            page_title = self.topic_dict[topic][language]['title_for_page']
            page_summary = self.topic_dict[topic][language]['summary_for_page']
            
            if language == 'en':
                topic_heading = self.capitalise_uk(self.topic_dict[topic][language]['title_topic_page'].lower())
                markdown = f"""
## **List of {topic_heading}**  

"""
            elif language == 'cy':
                topic_heading = self.capitalise_uk(self.topic_dict[topic][language]['title_topic_page'].lower())
                markdown = f"""
## **Rhestr o {topic_heading}**  
      
"""
            for variable in self.topic_dict[topic]['en']['list_of_variables']:
                topic_for_url = topic.lower().replace(' ', '')
                variable_for_url = self.topic_dict[topic]['en']['list_of_variables'][variable].lower().replace(' ', '')
                link = f"/census/census2021dictionary/variablesbytopic/{topic_for_url}variablescensus2021/{variable_for_url}"
                # TODO - sort hardcode
                if variable == 'residence_type':
                    link = "/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/residencetype"
                # TODO - sort hardcode
                if variable == 'legal_partnership_status':
                    link = "/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/maritalandcivilpartnershipstatus"
                
                markdown += f"* [{self.topic_dict[topic][language]['list_of_variables'][variable]}]({link})  \n"
            
            # static_page page
            metadata_payload = {
                    "description":{
                            "title":page_title,
                            "summary":page_summary,
                            "releaseDate":self.release_date,
                            "keywords":[],
                            "metaDescription":"",
                            "language":language,
                            "survey":"census"
                            },
                    "markdown":[markdown],
                    "charts":[],
                    "tables":[],
                    "equations":[],
                    "images":[],
                    "downloads":[],
                    "type":"static_page",
                    "anchors":[],
                    "links":[],
                    "fileName":uri_name
                    }
                    
            if language == 'en':
                uri = f"/census/{topic_location}/{uri_name}/data.json"
                
            elif language == 'cy':
                uri = f"/census/{topic_location}/{uri_name}/data_cy.json"
            
            if self.environment == "prod" or self.environment == "test":
                content_path = f"/content/{self.collection_id}?uri={uri}"
                review_path = f"/complete/{self.collection_id}?uri={uri}"
            
            elif environment == "sandbox":
                content_path = f"/zebedee/content/{self.collection_id}?uri={uri}"
                review_path = f"/zebedee/complete/{self.collection_id}?uri={uri}"
                
            content_url = f"{self.url}{content_path}"
            review_url = f"{self.url}{review_path}"
                
            self.curl_request('post', content_url, json=metadata_payload)
            print(f"{topic} - list of variables page sent - {language}")
            self.send_for_review(review_url)
            print(f"{topic} - list of variables page reviewed")
            
        return
    
    def create_variable_page(self, variable_details):
        # currently creates a static_page 
        for language in ('en', 'cy'):
            if language == 'cy':
                return
            
            page_title = variable_details[language]['title']
            uri_name = f"{variable_details['en']['title'].lower().replace(' ', '')}" # used for url
            topic = variable_details['en']['topic_label'].lower().replace(' ', '')
                
            markdown = self.create_static_page_markdown(variable_details, language)
            
            # static_page page
            metadata_payload = {
                    "description":{
                            "title":page_title,
                            "summary":"",
                            "releaseDate":self.release_date,
                            "keywords":[],
                            "metaDescription":"",
                            "language":language,
                            "survey":"census"
                            },
                    "markdown":[markdown],
                    "charts":[],
                    "tables":[],
                    "equations":[],
                    "images":[],
                    "downloads":[],
                    "type":"static_page",
                    "anchors":[],
                    "links":[],
                    "fileName":uri_name
                    }
            
            if language == 'en':
                uri = f"census/census2021dictionary/variablesbytopic/{topic}variablescensus2021/{uri_name}/data.json"
                # TODO - sort hardcode
                if variable_details['en']['title'] == 'Legal partnership status':
                    uri = "census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/maritalandcivilpartnershipstatus/data.json"
            
            elif language == 'cy':
                uri = f"census/census2021dictionary/variablesbytopic/{topic}variablescensus2021/{uri_name}/data_cy.json"
                # TODO - sort hardcode
                if variable_details['en']['title'] == 'Legal partnership status':
                    uri = "census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/maritalandcivilpartnershipstatus/data_cy.json"
            
            if self.environment == "prod" or self.environment == "test":
                content_path = f"/content/{self.collection_id}?uri={uri}"
                review_path = f"/complete/{self.collection_id}?uri={uri}"
            
            elif environment == "sandbox":
                content_path = f"/zebedee/content/{self.collection_id}?uri={uri}"
                review_path = f"/zebedee/complete/{self.collection_id}?uri={uri}"
                
            content_url = f"{self.url}{content_path}"
            review_url = f"{self.url}{review_path}"
                
            self.curl_request('post', content_url, json=metadata_payload)
            print(f"Page created for {variable_details['en']['title']} - {language}")
            self.send_for_review(review_url)
            print(f"Page reviewed")
        
        return
    
    def create_static_page_markdown(self, variable_details, language):
        variable_type = variable_details['en']['type_label']
        
        if variable_type.lower() == "standard variable":
            markdown = self.markdown_standard_variable(variable_details, language)
        
        elif variable_type.lower() == "derived variable":
            markdown = self.markdown_derived_variable(variable_details, language)
        
        return markdown
    
    def markdown_standard_variable(self, variable_details, language):
        # markdown is the bulk of the text on the page
        classification_mnemonic = variable_details['en']['preferred_classification']
        number_of_categories = len(variable_details['en']['classifications'][classification_mnemonic]['category'])
        
        comparability_type, comparability_definition = self.comparability_text_builder(variable_details, language)
        
        if language == 'en':
            background_link = 'https://www.ons.gov.uk/census/planningforcensus2021/questiondevelopment'
            comparison_link = 'https://www.ons.gov.uk/census/planningforcensus2021/ukcensusdata'
        
            markdown = f"""
**Mnemonic:** {variable_details['en']['mnemonic']}  
**Applicability:** {variable_details['en']['statistical unit']}   
**Type:** {variable_details['en']['type_label']}  

## **Definition**

{variable_details['en']['description']}

## **Classification**

Total number of categories: {number_of_categories} 

{self.classification_text_builder(variable_details, 'en')}
{self.quality_information_text_builder(variable_details, 'en')}
## **Question asked**

{variable_details['en']['question']['question']}

## **Background**

Read about how we [developed and tested the questions for Census 2021.]({background_link})

## **Why we ask the question**

{variable_details['en']['question']['reason']}

## **Comparability with the 2011 Census** 

{variable_details['en']['comparability']}

{comparability_type}

{comparability_definition}

## **England, Wales, Northern Ireland and Scotland comparisons**

This information is not yet available. Find out more about [UK Census data.]({comparison_link})

"""
        elif language == 'cy':
            background_link = 'https://cy.ons.gov.uk/census/planningforcensus2021/questiondevelopment'
            comparison_link = 'https://cy.ons.gov.uk/census/planningforcensus2021/ukcensusdata'
    
            markdown = f"""
**Cofair:** {variable_details['cy']['mnemonic']}  
**Cymhwysedd:** {variable_details['cy']['statistical unit']}   
**Math:** {variable_details['cy']['type_label']}  

## **Diffiniad**

{variable_details['cy']['description']}

## **Dosbarthiad**

Cyfanswm nifer y categorïau: {number_of_categories} 

{self.classification_text_builder(variable_details, 'cy')}
{self.quality_information_text_builder(variable_details, 'cy')}
## **Cwestiwn a ofynnwyd**

{variable_details['cy']['question']['question']}

## **Cefndir**

Darllenwch am sut y gwnaethom [ddatblygu a phrofi'r cwestiynau ar gyfer Cyfrifiad 2021 (yn Saesneg).]({background_link})

## **Pam rydym ni’n gofyn y cwestiwn hwn**

{variable_details['cy']['question']['reason']}

## **Cymharedd â Chyfrifiad 2011** 

{variable_details['cy']['comparability']}

{comparability_type}

{comparability_definition}

## **Cymariaethau rhwng Cymru, Lloegr, Gogledd Iwerddon a'r Alban**

Nid yw'r wybodaeth hon ar gael eto. Dysgwch fwy am [ddata cyfrifiad y Deyrnas Unedig.]({comparison_link})

"""
        return markdown
    
    def markdown_derived_variable(self, variable_details, language):
        # markdown is the bulk of the text on the page
        classification_mnemonic = variable_details['en']['preferred_classification']
        number_of_categories = len(variable_details[language]['classifications'][classification_mnemonic]['category'])
        
        comparability_type, comparability_definition = self.comparability_text_builder(variable_details, language)
        
        if language == 'en':
            background_link = 'https://www.ons.gov.uk/census/planningforcensus2021/questiondevelopment'
            comparison_link = 'https://www.ons.gov.uk/census/planningforcensus2021/ukcensusdata'
        
        
            markdown = f"""
**Mnemonic:** {variable_details['en']['mnemonic']}  
**Applicability:** {variable_details['en']['statistical unit']}   
**Type:** {variable_details['en']['type_label']}  

## **Definition**

{variable_details['en']['description']}

## **Classification**

Total number of categories: {number_of_categories} 

{self.classification_text_builder(variable_details, 'en')}
{self.quality_information_text_builder(variable_details, 'en')}
## **Background**

Read about how we [developed and tested the questions for Census 2021.]({background_link})

## **Comparability with the 2011 Census**

{variable_details['en']['comparability']}

{comparability_type}

{comparability_definition}

## **England, Wales, Northern Ireland and Scotland comparisons**

This information is not yet available. Find out more about [UK Census data.]({comparison_link})

"""
    
        elif language == 'cy':
            background_link = 'https://cy.ons.gov.uk/census/planningforcensus2021/questiondevelopment'
            comparison_link = 'https://cy.ons.gov.uk/census/planningforcensus2021/ukcensusdata'
            
            markdown = f"""
**Cofair:** {variable_details['cy']['mnemonic']}  
**Cymhwysedd:** {variable_details['cy']['statistical unit']}   
**Math:** {variable_details['cy']['type_label']}  

## **Diffiniad**

{variable_details['cy']['description']}

## **Dosbarthiad**

Cyfanswm nifer y categorïau: {number_of_categories} 

{self.classification_text_builder(variable_details, 'cy')}
{self.quality_information_text_builder(variable_details, 'cy')}
## **Cefndir**

Darllenwch am sut y gwnaethom [ddatblygu a phrofi'r cwestiynau ar gyfer Cyfrifiad 2021 (yn Saesneg).]({background_link})

## **Cymharedd â Chyfrifiad 2011**

{variable_details['cy']['comparability']}

{comparability_type}

{comparability_definition}

## **Cymariaethau rhwng Cymru, Lloegr, Gogledd Iwerddon a'r Alban**

Nid yw'r wybodaeth hon ar gael eto. Dysgwch fwy am [ddata cyfrifiad y Deyrnas Unedig.]({comparison_link})

"""
        return markdown
    
    def classification_text_builder(self, variable_details, language):
        # creates the classification section of the markdown
        
        classification_mnemonic = variable_details['en']['preferred_classification']
        
        if language == 'en':
        
            text = f"""
| Code | Name |
| :--- | :--- |
"""
            for key in variable_details['en']['classifications'][classification_mnemonic]['category'].keys():
                text += f"| {key} | {variable_details['en']['classifications'][classification_mnemonic]['category'][key]} | \n"
            
        elif language == 'cy':
        
            text = f"""
| Cod | Enw |
| :--- | :--- |
"""
            for key in variable_details['cy']['classifications'][classification_mnemonic]['category'].keys():
                text += f"| {key} | {variable_details['cy']['classifications'][classification_mnemonic]['category'][key]} | \n"
            
        return text
    
    def comparability_text_builder(self, variable_details, language):
        # hardcoded to make check against english
        if variable_details['en']['comparability'].lower().startswith('broadly'):
            if language == 'en':
                comparability_type = '### **What does broadly comparable mean?**'
                definition = "A variable that is broadly comparable means that it can be generally compared with the same variable used in the 2011 Census. However, changes may have been made to the question or options that people could choose from or how write-in answers are classified."
            elif language == 'cy':
                comparability_type = "### **Beth yw ystyr cymaradwy yn fras?**"
                definition = "Mae newidyn sy’n gymaradwy yn fras yn golygu y gellir ei gymharu’n gyffredinol â’r un newidyn a ddefnyddiwyd yng Nghyfrifiad 2011. Fodd bynnag, efallai bod newidiadau wedi'u gwneud i'r cwestiwn neu'r opsiynau y gallai pobl ddewis ohonynt neu sut mae atebion ysgrifenedig yn cael eu dosbarthu."
            
        elif variable_details['en']['comparability'].lower().startswith('not'):
            if language == 'en':
                comparability_type = '### **What does not comparable mean?**'
                definition = "A variable that is not comparable means that it cannot be compared with a variable from the 2011 Census."
            elif language == 'cy':
                comparability_type = "### **Beth yw ystyr ddim yn gymaradwy?**"
                definition = "Mae newidyn sydd ddim yn gymaradwy yn golygu na ellir ei gymharu â newidyn o Gyfrifiad 2011."
                
        elif variable_details['en']['comparability'].lower().startswith('highly'):
            if language == 'en':
                comparability_type = '### **What does highly comparable mean?**'
                definition = "A variable that is highly comparable means that it can be directly compared with the variable from the 2011 Census. The questions and options that people could choose from may be slightly different, for example the order of the options may be swapped around, but the data collected is the same."
            elif language == 'cy':
                comparability_type = "### **Beth yw ystyr cymaradwy iawn?**"
                definition = "Mae newidyn sy’n gymaradwy iawn yn golygu y gellir ei gymharu’n uniongyrchol â’r newidyn o Gyfrifiad 2011. Gall y cwestiynau a’r opsiynau y gallai pobl ddewis fod ychydig yn wahanol, er enghraifft efallai bod trefn yr opsiynau wedi’u newid, ond mae’r data a gesglir yr un peth."
                
        else:
            raise Exception(f"Comparability statement is not one of Broadly/Highly/Not - {variable_details['en']['comparability']}")
        
        return comparability_type, definition
    
    def quality_information_text_builder(self, variable_details, language):
        variable_mnemonic = variable_details['en']['mnemonic']
        if variable_mnemonic in ('legal_partnership_status', 'hh_family_composition', 'passports_all', 'resident_age'):
            comparison_link = "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/demographyandmigrationqualityinformationforcensus2021"
            if language == 'en': #TODO - is wording for the link included in metadata model or not
                text = f"""

## **Quality information**

{variable_details['en']['quality_statement']}

[Read more in our Demography and migration quality information for Census 2021 methodology.]({comparison_link})
"""

            elif language == 'cy':
                text = f"""

## **Ansawdd gwybodaeth**

{variable_details['cy']['quality_statement']}

[Darllenwch fwy yn ein Gwybodaeth am ansawdd a methodoleg demograffeg a mudo ar gyfer Cyfrifiad 2021 (yn Saesneg).]({comparison_link})
"""

        elif variable_mnemonic in ('hh_hrp_veteran', 'hh_veterans', 'uk_armed_forces'):
            comparison_link = ""
            if language == 'en':
                text = f"""

## **Quality information**

{variable_details['en']['quality_statement']}
"""
        
            elif language == 'cy':
                text = f"""

## **Ansawdd gwybodaeth**

{variable_details['cy']['quality_statement']}
"""

        else:
            text = ""
        
        return text
    
    def capitalise_uk(self, text):
        # TODO - make more robust so has no side effects
        if "uk " in text:
            text = text.replace("uk ", "UK ")
        if "deyrnas unedig" in text:
            text = text.replace("deyrnas unedig", "Deyrnas Unedig")
        return text

    


if __name__ == '__main__':
    dd = data_dictionary_upload(environment, collection_name, pages_to_run)

