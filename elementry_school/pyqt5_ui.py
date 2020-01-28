'''
    ----------------------------------------------------------------------------------------
    해당 코드는 파이썬으로 컴퓨터 화면에 창을 띄워 내용물을 출력하기 위한 코드입니다.

    PyQt5를 이용하여 창을 생성하였습니다.

    해당 모듈을 이용하기 위해서는 pip에 다운로드받아야 합니다.
    아래 내용을 명령프롬프트(CMD)에 입력해주세요.
    pip install PyQt5

    pip가 설치되어있지 않다면            -> https://slowcode.tistory.com/67
    pip를 설치했는데 경로를 찾지 못한다면 -> https://blog.naver.com/PostView.nhn?blogId=lee95292&logNo=221205091279&proxyReferer=https%3A%2F%2Fwww.google.com%2F

    이제 화면에 대하여 개발하기위한 기본적인 구성이 완료되었습니다.
    ----------------------------------------------------------------------------------------
'''

'''
    ----------------------------------------------------------------------------------------
    import sys는 시스템에 대한 작업을 수행하기 위해 불러오는 모듈입니다.
    
    from PyQt5.QtWidgets import *                   QWidget클래스를 사용하기 위함
    from PyQt5.QtCore import *                      Qt클래스를 사용하기 위함 
    from PyQt5 import QtCore, QtGui, QtWidgets      QtGui.QFont를 사용하기 위함

    위 코드들은 화면을 구성하고 버튼, 입력창등을 띄우고 상호작용하기 위한 모듈입니다.
    ----------------------------------------------------------------------------------------
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

# 기존에 만들어놓은 machine_learning.py 코드를 불러옵니다. as ml은 코드작성시 ml로 줄여 작성하겠다는 뜻입니다.
import machine_learning as ml
import microphone


mic = microphone.Microphone()

'''
    ----------------------------------------------------------------------------------------
    아래 클래스는 실제화면을 그리고 이벤트처리동작을 수행하기 위한 클래스입니다.

    class MyWindow(QWidget)은 PyQt5.QtWidgets에 있는 QWidget 클래스를 상속받아 작성됩니다.

    self는 자기자신(MyWindow)을 뜻합니다.
    자신이 가진 함수나 변수를 접근하기 위해 사용됩니다.
    self.변수명
    self.함수명()

    __init__ 함수       : 초기화
    initUI 함수         : 화면 내부 구성
    addbtn_clicked 함수 : 버튼이 눌러졌을 때 이벤트를 처리
    keyPressEvent 함수  : 키보드 버튼이 눌러졌을때(엔터) 이벤트를 처리
    ----------------------------------------------------------------------------------------
'''
class MyWindow(QWidget):

    # 클래스가 만들어졌을 때 초기화하기 위한 함수입니다. super은 자기자신의 부모인 QWidget을 가리킵니다.
    def __init__(self):
        super().__init__()
        self.initUI()
        global mic

    # 화면을 구성하기 위한 함수입니다.
    def initUI(self):

        # widget : 화면 내부에 있는 [입력창, 버튼] 같은 위젯들을 구성합니다.
        '''
            ------------------------------------------
            QLineEdit() : 한줄 텍스트를 입력받을 수 있는 위젯입니다.
            QTextEdit() : 여러줄 텍스트를 입력받을 수 있는 위젯입니다.
            QLabel() : 텍스트를 화면에 표시하기 위한 라벨 위젯입니다. (입력불가)

            setReadOnly(True)를 하면 텍스트를 입력할 수 없게 됩니다.
            setFixedHeight(숫자) 를 하면 숫자 크기만큼의 높이영역을 위젯이 가지게 됩니다.
            setFixedWidth(숫자) 도 마찬가지입니다.
            setText 함수로 글자를 담을 수 있습니다.
            ------------------------------------------
        '''
        self.inputTextEdit = QLineEdit()
        self.resultEdit = QTextEdit()
        self.resultEdit.setReadOnly(True)

        self.staticLabel = QLabel()
        self.staticLabel.setFixedHeight(25)

        self.staticLabel.setText("<span style=\" font-size:15pt; font-weight:600; color:#ff0000;\" >'주어'</span>와 <span style=\" font-size:15pt; font-weight:600; color:#800080;\" >'서술어'</span>가 포함된 '평서문'이되도록 해보세요")

        self.infoLabel = QLabel()
        self.infoLabel.setText("""
        <span style=\" font-size:12pt; font-weight:600; color:#ff0000;\" >주어    :  빨간색</span><p>
        <span style=\" font-size:12pt; font-weight:600; color:#b8860b;\" >목적어  :  주황색</span><p>
        <span style=\" font-size:12pt; font-weight:600; color:#ffd700;\" >보어    :  노란색</span><p>
        <span style=\" font-size:12pt; font-weight:600; color:#008000;\" >관형어  :  초록색</span><p>
        <span style=\" font-size:12pt; font-weight:600; color:#0000ff;\" >부사어  :  파란색</span><p>
        <span style=\" text-decoration:line-through; font-size:12pt; font-weight:600; color:#4b0082;\" >감탄사  :  남색</span><p>
        <span style=\" font-size:12pt; font-weight:600; color:#800080;\" >서술어  :  보라색</span><p>
                            """)

        self.addbtn = QPushButton("입력하기")

        # 버튼이 클릭되면 연결될 함수를 지정해줍니다. self.addbtn이 클릭되면( 여기에 지정한 함수 수행 )
        self.addbtn.clicked.connect(self.addbtn_clicked)
        

        # 음성인식 버튼을 만드는 과정입니다. 마이크가 연결되어있지 않다면 비활성화합니다. self.voiceInputbtn이 클릭되면( 지정한 함수 수행 )
        self.voiceInputbtn = QPushButton("음성으로 입력하기")

        if mic.isConnected == False:
            self.voiceInputbtn.setEnabled(False)

        self.voiceInputbtn.clicked.connect(self.voiceInputbtn_clicked)

        # font : 화면에 표시할 텍스트의 Font(글씨체)를 구성합니다. setBold(True)는 텍스트를 굵게 한다는 뜻입니다.
        font = QtGui.QFont('굴림', 13)
        font.setBold(True)
        self.setFont(font)

        #layouts : 화면에 widget들의 위치를 원하는 곳에 배치하기위해 화면구성을 하는 내용입니다.
        '''
            ----------------------------------------------------------------------------------------
            QGridLayout : widget에 좌표정보를 넣어주어 격자에 맞게 하기 위한 'layout 종류'중 하나입니다.
            layout 종류
                QVBoxLayout
                QHBoxLayout
                QBoxLayout
            ****QGridLayout****
                QLayout

            addwidget 함수를 통해 widget들을 알맞은 위치에 추가시킵니다.
            addwidget(위젯변수명, X좌표, Y좌표)

            setVerticalSpacing(숫자값) 수직으로 widget끼리의 간격을 정합니다.
            serHorizontalSpacing(숫자값) 수평으로 widget끼리의 간격을 정합니다.

            setWindowTitle(문자열) 문자열을 창 제목에 띄웁니다.
            setGeometry(x,y, width, height) 창이나올 (x,y) 좌표를 주고, 그 기준으로 가로와 세로길이를 정해줍니다.

            show() 함수를 사용하면 창이 표시가 됩니다.
            ----------------------------------------------------------------------------------------
        '''
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(0)
        self.grid.setHorizontalSpacing(10)

        self.grid.addWidget(self.inputTextEdit,1,0)
        self.grid.addWidget(self.addbtn,1,1)

        self.grid.addWidget(self.staticLabel,2,0)
        self.grid.addWidget(self.voiceInputbtn,2,1)
        
        # resultEdit는 여러줄에 대한 표시를 해야되므로 (X시작좌표, Y시작좌표, X끝좌표, Y끝좌표)를 넣어야 합니다.
        self.grid.addWidget(self.resultEdit,3,0,5,1)
        self.grid.addWidget(self.infoLabel,3,1,5,2)

        self.setLayout(self.grid)

        self.setWindowTitle("문장과 성분 구성")
        self.setGeometry(300, 300, 900, 500)
        self.show()

    
    # 입력하기 버튼이 눌러졌을 때 수행되는 함수입니다.
    '''
        split(문자) 함수는 문자열을 문자 기준으로 자를때 사용됩니다.

        문자를 빈칸으로 두면 띄어쓰기로 나눠져 리스트(배열) 형태로 저장됩니다.
        --> [split(문자), 함수는, 문자열을, 문자, 기준으로, 자를때, 사용됩니다.]

        len(배열) 함수를 사용하면 리스트에 들어있는 원소 개수가 몇개인지 세줍니다.
        이를 통하여 주어와 서술어를 구분합니다.
        [미입력시]  --> 0
        나는달린다  --> 1
        나는 달린다 --> 2
        나 는 달린다--> 3
        이를 통해 비교를하여 2개가 아니게 되면 작업을 수행하지 않고 다른 메세지를 사용자에게 전달해줍니다.

        if 조건이 참이면[len(text) == 1]:                             <-- 원소개수가 1개면
            해당 구문 수행
        elif 위 조건에 해당되지않고 이 조건이 참이면[len(text) >= 3]:   <-- 원소개수가 3개이상이라면
            해당 구문 수행
        else:                                                        <-- 위 내용에 전부 거짓이라면
            해당 구문 수행

        for 첨자 in 리스트:   <-- 리스트의 각 원소들을 첨자를 통해 앞에서부터 하나씩 꺼내 전부 꺼낼 때까지 반복한다(참이 아닐때까지 반복한다.)
            해당 구문 반복

        setText(내용) 해당 위젯에 텍스트 내용을 넣는다.
        append(내용) 해당 위젯에 텍스트 내용을 추가한다. 
    '''
    def addbtn_clicked(self):
        text = self.inputTextEdit.text().split()
        if len(text) == 0:
            return
        elif len(text) < 2:
            self.staticLabel.setText("<span style=\" font-size:15pt; font-weight:600; color:#ff0000;\" >'주어'</span>와 <span style=\" font-size:15pt; font-weight:600; color:#800080;\" >'서술어'</span>중에 하나가 없는거같아요. 띄어쓰기가 안되어있다면 해주세요.")
            return
#        elif len(text) >= 4:
#            self.staticLabel.setText("<span style=\" font-size:15pt; font-weight:600; color:#ff0000;\" >'주어'</span>와 <span style=\" font-size:15pt; font-weight:600; color:#800080;\" >'서술어'</span>이외의 단어가 들어가지 않게 해주세요.")
#            return
        self.resultstr = ''
        for word in text:
            self.resultstr += ml.listen(word)

        if ml.CheckPredicate and ml.CheckSubject:    
            self.staticLabel.setText("<span style=\" font-size:15pt; font-weight:600; color:#ff0000;\" >'주어'</span>와 <span style=\" font-size:15pt; font-weight:600; color:#800080;\" >'서술어'</span>가 포함된 '평서문'이되도록 해보세요")      
        else:
            self.staticLabel.setText("<span style=\" font-size:15pt; font-weight:600; color:#ff0000;\" >'주어'</span>와 <span style=\" font-size:15pt; font-weight:600; color:#800080;\" >'서술어'</span>중에 하나가 없는거같아요. 띄어쓰기가 안되어있다면 해주세요.")
#           만약 주어 서술어가 반드시 포함되어야 한다면 아래 주석( # )을 제거해주세요!
#           return

        #문제가 없다면 색이 입혀진 문장을 추가해주고 ( append ), 입력창과 필요변수를 초기화 (빈칸으로) 해줍니다.
        self.resultEdit.append(self.resultstr)
        self.inputTextEdit.setText('')
        ml.CheckSubject = False
        ml.CheckPredicate = False

        #아래 내용을 사용하면 팝업 메세지가 나온다.
        #QMessageBox.about(self, "message", "clicked")
    
    def voiceInputbtn_clicked(self):
        voicedata = mic.listen()
        if voicedata[1] == False:
            self.staticLabel.setText(voicedata[0])
        else:
            self.inputTextEdit.setText(voicedata[0])
            self.addbtn_clicked()


    # 키보드가 눌렸을 때 사용되는 이벤트 처리 함수
    '''
        if 원소 in 리스트:  <-- 리스트에 원소가 포함되어있다면 수행
            해당 구문 수행

        키보드를 e 로 가져와 눌린 키가 엔터키라면 입력하기 버튼을 누른 효과와 같게 하기위해 addbtn_clicked 함수를 요청한다.
    '''
    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.addbtn_clicked()



# 파이썬에서 위 MyWindow 클래스를 사용하기 위해 불러오고 실행하는 코드
'''
    if __name__ == "__main__":

    사실 위 코드를 지워도 수행자체에는 문제가 없다.
    pyqt5_ui.py를 다른곳에서 import 해서 사용할 경우 __main__이 아니게 되어 코드실행이 안되게 뛰어넘는다.

    QApplication 클래스 : 이벤트처리 loop를 위해 (이벤트를 계속 입력받을수 있게 하기위해) 잡아두는 클래스이다.
    exec_() 를 하게되면 이벤트입력을 계속 받을 수 있다.

    MyWindow 클래스를 생성해서 show()를 하여 화면에 띄워주게 된다.
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()


'''
    PyQt에 대해 더 알고싶으신 분은 https://wikidocs.net/5222 이쪽에 정보가 더 자세히 있습니다.
'''