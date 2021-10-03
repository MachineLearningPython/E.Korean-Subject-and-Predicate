import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import properties.properties as key

authenticator = IAMAuthenticator(key.api_key)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url('https://api.kr-seo.assistant.watson.cloud.ibm.com')
assistant_id = key.assistant_id

from ibm_watson import ApiException

# 문장에 주어가 포함되어있는지( CheckSubject ), 서술어가 포함되어있는지( CheckPredicate ) 확인하기 위한 변수입니다.
CheckSubject = False
CheckPredicate = False

import machine_learning as ml

def classify(text):
    try:

        # no session
        response = assistant.message_stateless(
            assistant_id=assistant_id,
            input={
                'message_type': 'text',
                'text': text
            }
        ).get_result()
 
        temp = json.dumps(response, indent=2)
        
        #print(json.loads(temp))

        result = json.loads(temp)['output']['intents'][0]['intent'] # { output: { intents : [ intent: {}, confidence: {}]} }

        #print(result)

        return result

    except ApiException as ex:  
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message)
    
    except (IndexError, ValueError, TypeError):
        #정확도가 0.2 미만인 값을 처리가 가능한 기존 웹사이트 코드 활용
        result = ml.classify(text)
        return result["class_name"]
    

def listen(text):
    
    label = classify(text)

    global CheckSubject 
    global CheckPredicate 

    if label == "subject":
        if not CheckSubject: # 해당부분에 아직 주어가 없다면 주어로 정해주고, 주어가 이미 있다면 보어로 정해줍니다.
            CheckSubject = True
            return "<span style=\" font-size:20pt; font-weight:600; color:#ff0000;\" >" + text + " </span>"
        else:
            return "<span style=\" font-size:20pt; font-weight:600; color:#ffd700;\" >" + text + " </span>"
    elif label == "object":
        return "<span style=\" font-size:20pt; font-weight:600; color:#b8860b;\" >" + text + " </span>"
#    elif label == "complement":
#        return "<span style=\" font-size:20pt; font-weight:600; color:#ffff00;\" >" + text + " </span>"
    elif label == "adjective":
        return "<span style=\" font-size:20pt; font-weight:600; color:#008000;\" >" + text + " </span>"
    elif label == "adverbs":
        return "<span style=\" font-size:20pt; font-weight:600; color:#0000ff;\" >" + text + " </span>"
    elif label == "interjection":
        return "<span style=\" font-size:20pt; font-weight:600; color:#4b0082;\" >" + text + " </span>"
    elif label == "predicate":
        CheckPredicate = True
        return "<span style=\" font-size:20pt; font-weight:600; color:#800080;\" >" + text + " </span>"

#print(classify("고대"))

''' If you want use session
import time

    #use session 5min limit
    response = assistant.create_session(
        assistant_id=assistant_id
    ).get_result()

    dumps = json.dumps(response, indent=2)
    session_id = json.loads(dumps)['session_id']
    
    print('session id : ' + session_id)

    for _ in range(2):
        
        response = assistant.message(
        assistant_id=assistant_id,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': '동기들은'
        }
        ).get_result()

        temp = json.dumps(response, indent=2)
        result = json.loads(temp)['output']['intents'][0]['intent'] # { output: { intents : [ intent: {}, confidence: {}]} }

        print('it\'s like '+result)

        print("session test")
        time.sleep(400)                 세션 유지시간 초과시 에러
        print("end sleep for 400 sec")

    response = assistant.delete_session(
        assistant_id=assistant_id,
        session_id=session_id
    ).get_result()
'''