import speech_recognition as sr

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
            with self.mic as source:
                audio = self.r.listen(source)
            return [self.r.recognize_google(audio,language='ko-KR'), True]
        except sr.UnknownValueError:
            return ["인식하지 못하였습니다.",False]
        except sr.RequestError:
            return ["모듈설치 오류입니다.",False]
        except sr.WaitTimeoutError:
            return ["시간초과입니다.",False]
        except OSError:
            return ["마이크를 찾을 수 없습니다.",False]

'''
    -----------------------------------------------
    if __name__ == "__main__":
        mic = Microphone()
        if mic.isConnected == False:
            pass
        else:
            print("인식한 데이터 : ",mic.listen())
    -----------------------------------------------
'''