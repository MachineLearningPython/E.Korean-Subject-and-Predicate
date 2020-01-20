'''
    ----------------------------------------------------------------------------------------
    해당 코드는 https://machinelearningforkids.co.uk/ 사이트에서 만든 데이터를 학습시킨 내용물을
    적용할 수 있도록 파이썬으로 불러오는 코드 내용입니다.

    해당 코드는 홈페이지에서 제공해주는 코드를 그대로 가져와 약간 변형하여 사용한 것입니다.

    해당 코드는 단독으로 실행해도 나오는 출력이 없습니다.
    pyqt5_ui.py를 실행해주세요
    ----------------------------------------------------------------------------------------
'''

# import requests는 파이썬에서 HTTP에 요청을 보내기 위한 모듈입니다.
import requests


CheckSubject = False
CheckPredicate = False
'''
    ----------------------------------------------------------------------------------------
    classify 함수는 위에서 언급한 홈페이지에 학습된 데이터에 접근하여
    입력된 텍스트(text)가 어느 레이블(유형)에 해당되는지 찾아 반환해주는 함수입니다. 
    현재 사용된 레이블 종류 -> ( 주어, 서술어 )

    해당 주소(url)와 키(key)값을 가지고 해당 경로에 접근합니다.

    만약 오류가 발생되거나 정상적인 출력이 나오지 않으시다면 key가 잘못되지 않았는지, 해당 홈페이지에서 제대로 학습되었는지 확인하시기 바랍니다.
    ----------------------------------------------------------------------------------------
'''
# This function will pass your text to the machine learning model
# and return the top result with the highest confidence
def classify(text):
    key = "53e5bc00-3769-11ea-81e3-719bc52f8a3b7379aa2c-e21e-415d-97d3-0a40f7fa30b8"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.get(url, params={ "data" : text })

    # 정상적으로 수행되면 결과값을 반환합니다. 문제가 있다면 오류를 출력합니다.
    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()

'''
    ----------------------------------------------------------------------------------------
    listen 함수는 위 classify 함수를 통해 받은 결과값을 가지고
    주어인지, 서술어인지 확인하여 레이블에 맞는 색을 입혀 반환합니다.
    ----------------------------------------------------------------------------------------
'''
# CHANGE THIS to something you want your machine learning model to classify
def listen(text):
    demo = classify(text)

    # global을 붙이면 함수 밖에 있는 변수를 사용할 수 있게 됩니다.
    global CheckSubject 
    global CheckPredicate 
    ''' 
        ----------------------------------------------------------------------------------------
        label은 subject(주어)인지, predicate(서술어)인지에 대한 정보를 갖게 됩니다.
        confidence는 해당 레이블에 대해 얼마나 일치하는지 (0 ~ 100 %)에 대한 수치정보를 갖게 됩니다.
        
        # <- 이것은 주석입니다. 코드에 영향을 주지 않습니다. 지금 내용도 주석과 동일합니다.
        ----------------------------------------------------------------------------------------
    '''
    label = demo["class_name"]
    #confidence = demo["confidence"]

    '''
        ----------------------------------------------------------------------------------------
        해당 레이블에 따라 텍스트에 색을 입혀 반환합니다. <span></span>은 HTML 태그를 이용한 것입니다.

        color:#ff0000 => 빨간색
        color:#0000ff => 파란색
        color:#00ff00 => 초록색

        주어    --  빨간색  #ff0000
        목적어  --  주황색  #b8860b
        보어    --  노란색  #ffd700
        관용어  --  초록색  #008000
        부사어  --  파란색  #0000ff
        감탄사  --  남색    #4b0082
        서술어  --  보라색  #800080
        ----------------------------------------------------------------------------------------
    '''
    if label == "subject":
        if not CheckSubject:
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

    #이 아래 주석문을 사용하게 되면 콘솔창에 label정보와 confidence정보가 출력되게 합니다.
    #print ("result: '%s' with %d%% confidence" % (label, confidence))