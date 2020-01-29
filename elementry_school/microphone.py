'''
    ----------------------------------------------------------------------------------------
    (speech-to-text)
    해당 코드는 파이썬으로 마이크를 인식하여 음성을 텍스트로 변환하기 위한 코드입니다.

    speech_recoginition 라이브러리를 이용하여 창을 생성하였습니다.

    해당 모듈을 이용하기 위해서는 pip에 다운로드받아야 합니다.
    아래 내용을 명령프롬프트(CMD)에 입력해주세요.
    
    우선 python (또는 python3) --version 으로 버젼을 확인해줍니다.
    Python 3.7.6    <-- 다음과 같이 버젼명이 나올텐데

    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio 이 사이트에서 PyAudio로 가서

    PyAudio-버전명-cp파이썬버젼-cp파이썬버젼-win_amd64.whl (또는 32비트운영체제라면 -win32.whl) 을 다운받습니다.
    예 ) 내 버전이 3.7.x 에 64비트 운영체제라면 : PyAudio‑0.2.11‑cp37‑cp37m‑win_amd64.whl

    다운받은 파일을 [자신이 알수있는 경로] ( C:\ )에 위치시킵니다. 이후 아래 코드를 적습니다.
    pip install [경로]PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
    예 ) pip install C:\PyAudio-0.2.11-cp37-cp37m-win_amd64.whl

    설치가 완료되면 아래 내용을 계속 입력합니다.
    pip install speechrecognition

    정상적으로 설치가 완료되면 아래 코드를 사용하실 수 있습니다.

    pip가 설치되어있지 않다면            -> https://slowcode.tistory.com/67
    pip를 설치했는데 경로를 찾지 못한다면 -> https://blog.naver.com/PostView.nhn?blogId=lee95292&logNo=221205091279&proxyReferer=https%3A%2F%2Fwww.google.com%2F

    이제 마이크를 사용하여 텍스트로 바꿔주기 위한 기본적인 구성이 완료되었습니다.

    참고사이트 : https://brunch.co.kr/@entaline/11
    ----------------------------------------------------------------------------------------
'''

# 음성인식및 텍스트로 변환을 위한 모듈
import speech_recognition as sr


'''
    ----------------------------------------------------------------------------------------
    아래 클래스는 mic로 받은 음성을 텍스트로 번역할 수 있는 클래스입니다.
    
    __init__함수는 마이크 기능을 초기화하기 위한 함수입니다.

    self.isConnected로 마이크 연결 여부를 판단합니다. 처음부터 미연결상태면 버튼을 비활성하기위한 용도로 사용됩니다.

    listen함수는 mic에서 받은 음성을 인식하여( self.r.listen(source)) 
        한글 텍스트로 변환( self.r.recognize_google(audio, language='ko-KR') )하여
        list [ 내용, 정상적인 메세지 여부 ] 로 반환하는 함수입니다.

    try:                            <-- try 안에 있는 코드를 수행하게 하여 오류가 발생하면 except로 이동하여 오류처리를 하게 합니다.
        코드수행
    except Errors:                  <-- 해당 에러가 Errors와 관련되어있다면
        코드수행시 에러에대한 처리
    ----------------------------------------------------------------------------------------
'''
class Microphone:

    isConnected = False

    def __init__(self):
        try:
            self.r = sr.Recognizer()
            self.mic = sr.Microphone()
            self.isConnected = True
        except sr.RequestError:
            pass # isConnected = False
        except OSError:
            pass # isConnected = False

    def listen(self):
        try:
            # 마이크 인식 후 listen()으로 음성데이터로 변환 후 google을 통해 한글로 번역해서 반환한다.
            with self.mic as source:
                audio = self.r.listen(source)
            return [self.r.recognize_google(audio,language='ko-KR'), True]
        except sr.UnknownValueError:
            return ["음성을 제대로 인식하지 못하였습니다.",False]
        except sr.RequestError:
            return ["모듈설치 오류입니다.",False]
        except sr.WaitTimeoutError:
            return ["시간초과입니다.",False]
        except OSError as e:
            return ["마이크를 찾을 수 없습니다. {} {} {}".format(e.errno,e.filename,e.strerror),False]

'''
    -----------------------------------------------
    아래와 같이 마이크만 테스트해볼 수 있습니다.

    if __name__ == "__main__":
        mic = Microphone()
        if mic.isConnected == False:
            pass
        else:
            print("인식한 데이터 : ",mic.listen())
    -----------------------------------------------
'''