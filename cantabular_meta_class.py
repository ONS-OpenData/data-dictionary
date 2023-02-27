import datetime, os, time, requests
from cantabular_request import get_variable_details
from data_dict_dicts import get_topic_dict

environment = "test"
collection_name = "Data dict SEO update"
release_date = '' # use dd/mm/yy, leave empty for todays date

list_of_all_topics = [
        'demography', 'international migration', 'UK armed forces veterans', 
        'eilr', 'labour market', 'travel to work', 
        'housing', 'sogi', 'education', 'health'
        ] 

pages_to_run = {
        "dd_landing_page": False, # only - True/False
        "variables_by_topic_landing_page": False, # only - True/False TODO -> only True if all topics included in topic_dict
        "list_of_variables_landing_page": False, # only - True/False
        "variables_page": True, # only - True/False
        "classifications_page": True, # only - True/False
        "topics": ["*"], # * for all, otherwise specify
        "variables": ["*"] # * for all, otherwise specify
        }



class making_request():
    # class object that makes requests
    # set as functions so can control what is being called depending on environment
    
    def curl_request(self, request_type, url, **kwargs):
        # request_type - GET/POST
        # kwargs will be data required for POST
        # returns url if environment is set to test
        
        if self.environment == 'test':
            """
            if request_type.lower() == 'get':
                print(f"GET request to {url}")
                
            elif request_type.lower() == 'post':
                print(f"POST request to {url}")
            """
            return
                
        if request_type.lower() == 'get':
            response_dict = self.get_curl_request(url)
            
        elif request_type.lower() == 'post':
            response_dict = self.post_curl_request(url, **kwargs)
            
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
        # all POST requests to send page to reviewed status are the same 
        
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
    def __init__(self, environment, collection_name, dict_of_pages_to_upload, release_date):
        self.environment = environment
        self.dict_of_pages_to_upload = dict_of_pages_to_upload
        self.collection_name = collection_name
        if not release_date:
            self.release_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT00:00:00.000Z')
        else:
            self.release_date = datetime.datetime.strftime(datetime.datetime.strptime(release_date, '%d/%m/%y'), '%Y-%m-%dT00:00:00.000Z')
        self.languages = ['en', 'cy']
        
        self.get_access_token()
        self.topic_dict = get_topic_dict(self.dict_of_pages_to_upload['topics'], variables=self.dict_of_pages_to_upload['variables'])
        self.variables_uploaded = []
        self.classifications_uploaded = []
        self.get_metadata_version_number()
          
    def run(self):
        self.get_collection_id()
        
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
                    except:
                        print(f'could not find varibale - {variable}')
                        
                    self.create_variable_page(variable_details)
                   
                    if self.dict_of_pages_to_upload['classifications_page']:
                        if variable_details['en']['has_multi_classifications']:
                            self.create_variable_classifications_page(variable_details)
                            
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
            login = {"email": email, "password": password}
            
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
            
    def create_collection(self, collection_name):
        if self.environment == 'test':
            print("test collection created")
            self.collection_id = 'collection_id'
            return
        
        elif self.environment == "prod":
            collection_url = f"{self.url}/collection"
            
        elif self.environment == "sandbox":
            collection_url = f"{self.url}/dataset/collection"
        
        r = requests.post(collection_url, headers=self.headers, json={'name': collection_name})
        print(f"POST returned - {r.status_code}")
        print(f"collection '{collection_name}' created")
        return
    
    def get_collection_id(self):
        if self.environment == 'test':
            self.collection_id = 'collection_id'
            return
        
        self.get_all_collections()
        for collection in self.collection_list:
            if collection["name"] == self.collection_name:
                collection_id = collection["id"]
                break
        
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
        
        for language in self.languages:
            
            page_info = {
                    'en': {
                            'page_title': 'Census 2021 dictionary',
                            'page_summary': 'Definitions, variables and classifications to help when using Census 2021 data.',
                            'section_title': 'Variables by topic',
                            'section_summary': 'Variables for use with research and analysis using Census 2021 data.'
                            },
                    'cy': {
                            'page_title': 'Geiriadur Cyfrifiad 2021', 
                            'page_summary': 'Diffiniadau, newidynnau a dosbarthiadau er mwyn helpu wrth ddefnyddio data Cyfrifiad 2021.',
                            'section_title': 'Newidynnau yn ôl pwnc',
                            'section_summary': "Newidynnau i'w defnyddio wrth ymchwilio a dadansoddi gan ddefnyddio data Cyfrifiad 2021."
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
                    "fileName":uri_name,
                    "topics":["7779"]
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
        
        for language in self.languages:

            page_info = {
                    'en': {
                            'page_title': 'Variables by topic',
                            'page_summary': 'Variables for use with research and analysis using Census 2021 data.'
                            },
                    'cy': {
                            'page_title': 'Newidynnau yn ôl pwnc',
                            'page_summary': "Newidynnau i'w defnyddio wrth ymchwilio a dadansoddi gan ddefnyddio data Cyfrifiad 2021."
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
                    "fileName":uri_name,
                    "topics":["7779"]
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
        
        for language in self.languages:
        
            page_title = self.topic_dict[topic][language]['title_for_page']
            page_summary = self.topic_dict[topic][language]['summary_for_page']
            topic_heading = self.topic_dict[topic][language]['title_topic_page']
            
            if language == 'en':
                markdown = f"""
## **{topic_heading}**  

"""
            elif language == 'cy':
                markdown = f"""
## **{topic_heading}**  
      
"""
            for variable in self.topic_dict[topic]['en']['list_of_variables']:
                topic_for_url = uri_name
                variable_for_url = self.slugize(self.topic_dict[topic]['en']['list_of_variables'][variable])
                link = f"/census/census2021dictionary/variablesbytopic/{topic_for_url}/{variable_for_url}"
                # TODO - sort hardcode
                if variable == 'residence_type':
                    link = "/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/residencetype"
                # TODO - sort hardcode
                if variable == 'legal_partnership_status':
                    link = "/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/maritalandcivilpartnershipstatus"
                # TODO - sort hardcode
                if variable == 'resident_age':
                    link = "/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/age"
                
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
                    "fileName":uri_name,
                    "topics":["7779"]
                    }
                    
            if language == 'en':
                uri = f"/census/{topic_location}/{uri_name}/data.json"
                
            elif language == 'cy':
                uri = f"/census/{topic_location}/{uri_name}/data_cy.json"
            
            if self.environment == "prod" or self.environment == "test":
                content_path = f"/content/{self.collection_id}?uri={uri}"
                review_path = f"/complete/{self.collection_id}?uri={uri}"
            
            elif self.environment == "sandbox":
                content_path = f"/zebedee/content/{self.collection_id}?uri={uri}"
                review_path = f"/zebedee/complete/{self.collection_id}?uri={uri}"
                
            content_url = f"{self.url}{content_path}"
            review_url = f"{self.url}{review_path}"
                
            self.curl_request('post', content_url, json=metadata_payload)
            print(f"{topic} - list of variables page sent - {language}")
            self.send_for_review(review_url)
            print(f"{topic} - list of variables page reviewed")
            
        return markdown
    
    def create_variable_page(self, variable_details):
        # currently creates a static_page 
        
        variable_mnemonic = variable_details['en']['mnemonic']
        if variable_mnemonic in self.variables_uploaded:
            # stops any duplication of variable pages
            print(f"already uploaded")
            return
        
        for language in self.languages:
            
            page_title = self.variable_title(variable_details[language]['title'], language, "variable")
            uri_name = self.slugize(variable_details['en']['title']) # used for url
            topic = self.slugize(variable_details['en']['topic_label'])
                
            summary = self.create_variable_summary(variable_details, language, "variable")
            markdown = self.create_static_page_markdown(variable_details, language)
            
            # static_page page
            metadata_payload = {
                    "description":{
                            "title":page_title,
                            "summary":summary,
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
                    "fileName":uri_name,
                    "topics":["7779"],
                    "subtopics":[self.topic_code(variable_details)]
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
            
            elif self.environment == "sandbox":
                content_path = f"/zebedee/content/{self.collection_id}?uri={uri}"
                review_path = f"/zebedee/complete/{self.collection_id}?uri={uri}"
                
            content_url = f"{self.url}{content_path}"
            review_url = f"{self.url}{review_path}"
                
            self.curl_request('post', content_url, json=metadata_payload)
            print(f"Page created for {variable_details['en']['title']} - {language}")
            self.send_for_review(review_url)
            print(f"Page reviewed")
            
            self.variables_uploaded.append(variable_mnemonic)
        
        return
    
    def create_variable_classifications_page(self, variable_details):
        variable_mnemonic = variable_details['en']['mnemonic']
        if variable_mnemonic in self.classifications_uploaded:
            # stops any duplication of variable pages
            print(f"classification already uploaded")
            return
        
        for language in self.languages:
            
            page_title = self.variable_title(variable_details[language]['title'], language, "classification") 
            uri_name = f"{self.slugize(variable_details['en']['title'])}/classifications" # used for url
            topic = self.slugize(variable_details['en']['topic_label'])
            
            summary = self.create_variable_summary(variable_details, language, "classification")
            markdown = self.markdown_multi_classifications(variable_details, language)
            
            # static_page page
            metadata_payload = {
                    "description":{
                            "title":page_title,
                            "summary":summary,
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
                    "fileName":uri_name,
                    "topics":["7779"],
                    "subtopics":[self.topic_code(variable_details)]
                    }
                    
            if language == 'en':
                uri = f"census/census2021dictionary/variablesbytopic/{topic}variablescensus2021/{uri_name}/data.json"
                # TODO - sort hardcode
                if variable_details['en']['title'] == 'Legal partnership status':
                    uri = "census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/maritalandcivilpartnershipstatus/classifications/data.json"
            
            elif language == 'cy':
                uri = f"census/census2021dictionary/variablesbytopic/{topic}variablescensus2021/{uri_name}/data_cy.json"
                # TODO - sort hardcode
                if variable_details['en']['title'] == 'Legal partnership status':
                    uri = "census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/maritalandcivilpartnershipstatus/classifications/data_cy.json"
            
            if self.environment == "prod" or self.environment == "test":
                content_path = f"/content/{self.collection_id}?uri={uri}"
                review_path = f"/complete/{self.collection_id}?uri={uri}"
            
            elif self.environment == "sandbox":
                content_path = f"/zebedee/content/{self.collection_id}?uri={uri}"
                review_path = f"/zebedee/complete/{self.collection_id}?uri={uri}"
                
            content_url = f"{self.url}{content_path}"
            review_url = f"{self.url}{review_path}"
                
            self.curl_request('post', content_url, json=metadata_payload)
            print(f"Classifications page created for {variable_details['en']['title']} - {language}")
            self.send_for_review(review_url)
            print(f"Page reviewed")
            
            self.classifications_uploaded.append(variable_mnemonic)
        
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
        question = self.question_text_builder(variable_details, language)
        question_reason = self.question_reason_text_builder(variable_details, language)
        
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

{self.classification_text_builder(variable_details, 'en', variable_details['en']['has_multi_classifications'])}
{self.quality_information_text_builder(variable_details, 'en')}
## **Question asked**

{question}

## **Background**

Read about how we [developed and tested the questions for Census 2021.]({background_link})

## **Why we ask the question**

{question_reason}

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

{self.classification_text_builder(variable_details, 'cy', variable_details['en']['has_multi_classifications'])}
{self.quality_information_text_builder(variable_details, 'cy')}
## **Cwestiwn a ofynnwyd**

{question}

## **Cefndir**

Darllenwch am sut y gwnaethom [ddatblygu a phrofi'r cwestiynau ar gyfer Cyfrifiad 2021 (yn Saesneg).]({background_link})

## **Pam rydym ni’n gofyn y cwestiwn hwn**

{question_reason}

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

{self.classification_text_builder(variable_details, 'en', variable_details['en']['has_multi_classifications'])}
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

{self.classification_text_builder(variable_details, 'cy', variable_details['en']['has_multi_classifications'])}
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
    
    def markdown_multi_classifications(self, variable_details, language):
        # creates the markdown for /classifications page
        number_of_classifications = len(variable_details['en']['multi_classifications'])
        variable_title = variable_details[language]['title']
        
        if language == 'en':
    
            markdown = f""" 
**Applicability:** {variable_details['en']['statistical unit']}   
**Type:** {variable_details['en']['type_label']}  

## **Overview**

The {self.capitalise_text(variable_title.lower(), 'en')} variable has {self.number_to_text(number_of_classifications, 'en')} classifications that can be used when analysing Census 2021 data.

When data are sorted, we group categories about the same topic together into a variable. A group of categories is called a “classification.”  There can be more than one classification about the same topic and each one is different. You should choose the one that is the most suitable for your research and analysis.

"""
        elif language == 'cy': 
            markdown = f"""
**Cymhwysedd:** {variable_details['cy']['statistical unit']}   
**Math:** {variable_details['cy']['type_label']} 

## **Trosolwg** 

Mae gan newidyn {self.capitalise_text(variable_title.lower(), 'cy')} {self.number_to_text(number_of_classifications, 'cy')} o ddosbarthiadau y gellir eu defnyddio wrth ddadansoddi data Cyfrifiad 2021.

Pan gaiff data eu didoli, byddwn yn grwpio categorïau am yr un pwnc gyda'i gilydd. “Dosbarthiad” yw'r enw am grŵp o gategorïau.  Mae'n bosibl cael mwy nag un dosbarthiad am yr un pwnc ac mae pob un yn wahanol. Dylech ddewis yr un sydd fwyaf addas ar gyfer eich ymchwil a'ch dadansoddiad.

"""
    
        for classification in variable_details['en']['multi_classifications']:
            # build a new 'variable dict to send to classification_text_builder
            mnemonic = variable_details[language]['mnemonic']
            classification_code = classification.split(f"{mnemonic}_")
            if len(classification_code) == 2:
                classification_code = f" {classification_code[-1]}"
            
            elif len(classification_code) == 1:
                classification_code = ''
                
            no_of_categories = len(variable_details['en']['classifications'][classification]['category'])
                
            if language == 'en':
                markdown += f"""
## **{variable_title} classification{classification_code}**
                
**Mnemonic:** {classification}

Total number of categories: {no_of_categories}
"""
            
            elif language == 'cy':
                markdown += f"""
## **Dosbarthiad{classification_code} {self.capitalise_text(variable_title.lower(), 'cy')}** 
                
**Cofair:** {classification}

Cyfanswm nifer y categorïau: {no_of_categories}
"""
            
            variable_details_to_send = variable_details.copy()
            variable_details_to_send['en']['preferred_classification'] = classification
            variable_details_to_send['cy']['preferred_classification'] = classification
            
            classification_text = self.classification_text_builder(variable_details_to_send, language, False)
            markdown += classification_text
        
        markdown += """
   
"""
        return markdown
    
    def classification_text_builder(self, variable_details, language, multiple_classifications):
        # creates the classification section of the markdown
        
        classification_mnemonic = variable_details['en']['preferred_classification']
        
        # does this variable have multiple classifications
        if multiple_classifications:
            topic = self.slugize(variable_details['en']['topic_label'])
            uri_name = f"{self.slugize(variable_details['en']['title'])}"
            multi_classifications_link = f"/census/census2021dictionary/variablesbytopic/{topic}variablescensus2021/{uri_name}/classifications"
            if variable_details['en']['title'] == 'Legal partnership status':
                multi_classifications_link = "/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/maritalandcivilpartnershipstatus/classifications"
            
                
        if language == 'en':
        
            text = f"""
| Code | Name |
| :--- | :--- |
"""
            for key in variable_details['en']['classifications'][classification_mnemonic]['category'].keys():
                text += f"| {key} | {variable_details['en']['classifications'][classification_mnemonic]['category'][key]} | \n"
            
            if multiple_classifications:
                text += f"\nView all [{variable_details['en']['title'].lower()} classifications.]({multi_classifications_link}) \n"
            
        elif language == 'cy':
        
            text = f"""
| Cod | Enw |
| :--- | :--- |
"""
            for key in variable_details['cy']['classifications'][classification_mnemonic]['category'].keys():
                text += f"| {key} | {variable_details['cy']['classifications'][classification_mnemonic]['category'][key]} | \n"
            
            if multiple_classifications:
                text += f"\nGweld pob [dosbarthiad {variable_details['cy']['title'].lower()}.]({multi_classifications_link}) \n"
            
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
        
        if variable_details['en']['has_quality_information']:
            comparison_link = variable_details['en']['quality_statement_url']
            
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

            topic = variable_details['en']['topic_label']
            if topic == 'Demography':
                
                if language == 'en':
                    text += f"""
[Read more in our Demography and migration quality information for Census 2021 methodology.]({comparison_link})
"""
                elif language == 'cy':
                    text += f"""
[Darllenwch fwy yn ein Gwybodaeth am ansawdd a methodoleg demograffeg a mudo ar gyfer Cyfrifiad 2021 (yn Saesneg).]({comparison_link})
"""

            elif topic == 'UK armed forces veterans':
                
                if language == 'en':
                    text += f"""
[Read more in our UK armed forces veterans quality information for Census 2021 methodology.]({comparison_link})
"""
                elif language == 'cy':
                    text += f"""
[Darllenwch fwy yn ein Gwybodaeth am ansawdd a methodoleg cyn-filwyr lluoedd arfog y Deyrnas Unedig ar gyfer Cyfrifiad 2021 (yn Saesneg).]({comparison_link})
"""

            elif topic == 'Ethnic group, national identity, language and religion':
                
                if language == 'en':
                    text += f"""
[Read more in our Ethnic group, national identity, language and religion quality information for Census 2021 methodology.]({comparison_link})
"""
                elif language == 'cy':
                    text += f"""
[Darllenwch fwy yn ein Gwybodaeth am ansawdd a methodoleg grŵp ethnig, hunaniaeth genedlaethol, iaith a chrefydd ar gyfer Cyfrifiad 2021 (yn Saesneg).]({comparison_link})
""" 
            elif topic == 'Housing':
                
                if language == 'en':
                    text += f"""
[Read more in our housing quality information for Census 2021 methodology.]({comparison_link})
"""
                elif language == 'cy':
                    text += f"""
[Darllenwch fwy yn ein methodoleg ar wybodaeth am ansawdd data am dai o Gyfrifiad 2021 (yn Saesneg).]({comparison_link})
""" 
            elif topic == 'Education':
                
                if language == 'en':
                    text += f"""
[Read more in our Education quality information for Census 2021 methodology.]({comparison_link})
"""
                elif language == 'cy':
                    text += f"""
[Darllenwch fwy yn ein methodoleg ar wybodaeth am ansawdd data am Addysg ar gyfer Cyfrifiad 2021 (yn Saesneg).]({comparison_link})
""" 
            
            elif topic == 'Health, Disability and Unpaid Care':
                
                if language == 'en':
                    text += f"""
[Read more in our Health, disability and unpaid care quality information for Census 2021 methodology.]({comparison_link})
"""
                elif language == 'cy':
                    text += f"""
[Darllenwch fwy yn ein Gwybodaeth am ansawdd a methodoleg iechyd, anabledd a gofal di-dâl ar gyfer Cyfrifiad 2021 (yn Saesneg).]({comparison_link})
""" 

        else:
            text = ""
            
        if variable_mnemonic in ('religion_tb'):
            comparison_link = ""
            if language == 'en':
                text = f"""

## **Quality information**

There are some quality issues in the data that may affect how you use the data.
"""
        
            elif language == 'cy':
                text = f"""

## **Ansawdd gwybodaeth**

Mae rhai materion ansawdd yn y data a allai effeithio ar sut rydych chi’n defnyddio’r data.
"""
        
        return text
    
    def question_text_builder(self, variable_details, language):
        # builds text of question(s)
        if variable_details['en']['has_multi_questions']:
            text = ''
            for question in variable_details[language]['question']:
                text += question['question']
                text += '\n\n'
                
            text = text.strip('\n\n')
            return text
        
        else:
            return variable_details[language]['question'][0]['question']
        
    def question_reason_text_builder(self, variable_details, language):
        # builds text of reason for question(s)
        if variable_details['en']['has_multi_questions']:
            text = ''
            for question in variable_details[language]['question']:
                text += question['reason']
                text += '\n\n'
                
            text = text.strip('\n\n')
            return text
        
        else:
            return variable_details[language]['question'][0]['reason']
        
    def capitalise_text(self, text, language):
        # some text is lower cased but requires certain words to be capitalised
            
        if language == 'en':
            if "uk " in text:
                text = text.replace("uk ", "UK ")
                
            if "english" in text:
                text = text.replace("english", "English")
                
            if "welsh" in text:
                text = text.replace("welsh", "Welsh")
        
        elif language == 'cy':
            if "deyrnas unedig" in text:
                text = text.replace("deyrnas unedig", "Deyrnas Unedig")
                   
            if "saesneg" in text:
                text = text.replace("saesneg", "Saesneg")
                
            if "cymraeg" in text:
                text = text.replace("cymraeg", "Cymraeg")
            
        return text
    
    def variable_title(self, page_title, language, page_type):
        # changes variable page title based on language
        if page_type == "variable":
            if language == 'en':
                new_value = f"{page_title} variable: Census 2021"
            
            elif language == 'cy':
                # because of the order of the welsh - variable will start with lower case
                updated_page_title = f"{self.capitalise_text(page_title.lower(), 'cy')}"
                new_value = f"Newidyn {updated_page_title}: Cyfrifiad 2021" 
                
        elif page_type == "classification":
            if language == 'en':
                new_value = f"{page_title} classifications: Census 2021"
            
            elif language == 'cy':
                # because of the order of the welsh - variable will start with lower case
                updated_page_title = f"{self.capitalise_text(page_title.lower(), 'cy')}"
                new_value = f"Dosbarthiadau {updated_page_title}: Cyfrifiad 2021" 
                
        else:
            raise Exception(f"Page type - '{page_type}' does not have a variable title option")
            
        return new_value
    
    def create_variable_summary(self, variable_details, language, page_type):
        variable = self.capitalise_text(variable_details[language]['title'].lower(), language)
        
        if page_type == "variable":
            if language == 'en':
                summary_text = f"Definition of {variable}, categories, and changes since the 2011 Census for use with research and analysis using Census 2021 data."
            
            elif language == 'cy':
                summary_text = f"Diffiniad o newidyn {variable}, categorïau, a newidiadau ers Cyfrifiad 2011 i'w defnyddio gydag ymchwil a dadansoddiad gan ddefnyddio data Cyfrifiad 2021."
            
        elif page_type == "classification":
            if language == 'en':
                summary_text = f"Use these groups of categories to research and analyse Census 2021 {variable} data."
            
            elif language == 'cy':
                summary_text = f"Defnyddiwch y grwpiau o gategorïau yma i ymchwilio ac i ddadansoddi data {variable} Cyfrifiad 2021."
                
        else:
            raise Exception(f"Page type - '{page_type}' does not have a summary option")
            
        return summary_text
    
    def slugize(self, text):
        new_text = text.replace(' ', '').replace(',', '').replace('(', '').replace(')', '').lower()
        return new_text
    
    def number_to_text(self, number, language):
        # numbers < 10 are changed to words
        # numbers > 10 remain as numbers
        number = str(number)
        if language == 'en':
            lookup = {
                    '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
                    '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
                    }
        elif language == 'cy':
            lookup = {
                    '1': 'un', '2': 'dau', '3': 'tri', '4': 'pedwar', '5': 'pump',
                    '6': 'chwech', '7': 'saith', '8': 'wyth', '9': 'naw'
                    }
            
        return lookup.get(number, number)
    
    def topic_code(self, variable_details):
        # returns topic code to be used as subtopic
        topic_label = variable_details['en']['topic_label'].lower().strip()
        lookup = {
                #"Ageing": "9731",
                "demography":"6646",
                "education": "3845",
                #"Equalities": "7267",
                "ethnic group, national identity, language and religion": "9497",
                "health, disability and unpaid care": "4262",
                #"Historic census": "8463",
                "housing": "4128",
                "international migration": "7755",
                "labour market": "4994",
                "sexual orientation and gender identity": "6885",
                "travel to work": "9724",
                "uk armed forces veterans": "7367"
                }
        return lookup[topic_label]
    
    def get_metadata_version_number(self):
        print(f"Using metadata from {location.split('/')[1]}")
        
    def variable_links_text_builder(self, variable_details, language):
        # creates the section that has links to where the variable is used
        # TODO 
        # - get links & text for links
        # - get Welsh
        # - is it for all variables?
        # - are variable_details needed - would mnemonic be enough?
        # - implement method
        if language == "en":
            text = """
### **Census 2021 data that uses this variable**

We use variables from Census 2021 data to show findings in different ways.

You can:
* [get the age dataset]()
* [view the age data on a map]()
* [read about how an area has changed in 10 years]()
* [view age data for an area on Nomis (an Office for National Statistics service)]()

**Other datasets that use this variable**
"""
        elif language == "cy":
            text = """"""
            
        return text

            
    
    


if __name__ == '__main__':
    dd = data_dictionary_upload(environment, collection_name, pages_to_run, release_date)
