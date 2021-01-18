import sys, os
import datetime, time
import pandas as pd
import multiprocessing as mp
from multiprocessing import Process, Queue
from configparser import ConfigParser

from XASessions import *
from XAQueries import *
from XAReals import *

# Configuration Parser
parser = ConfigParser()
parser.read('skybot.ini')

# [0]. << Logging Level >>
Logging_Level = parser.getint('Logging Level', 'Log Level')

# [1]. << Server Type >>
REAL_SERVER = parser.getboolean('Server Type', 'Real Server')

# [2]. << Month Info >>
KSE_START_HOUR = parser.getint('Month Info', 'KSE Start Hour')
CURRENT_MONTH = parser.get('Month Info', 'Current Month')
MONTH_FIRSTDAY = parser.get('Month Info', 'First Day of the Current Month')

# [3]. << Target Month Select : current month = 1, next month = 2 >>
TARGET_MONTH_SELECT = parser.get('Target Month Select', 'Target Month Select')

# [4]. << Window Style >>
DARK_STYLESHEET = parser.getboolean('Window Style', 'Dark Style')

# [5]. << User Switch = 'ON or OFF' >>
MULTIPROCESS = parser.getboolean('User Switch', 'Multiprocess')
TELEGRAM_SERVICE = parser.getboolean('User Switch', 'Telegram service')
MANGI_YAGAN = parser.getboolean('User Switch', 'Mangi Yagan')
AUTO_START = parser.getboolean('User Switch', 'Auto Start')
ResizeRowsToContents = parser.getboolean('User Switch', 'Resize Rows To Contents')
CROSS_HAIR_LINE = parser.getboolean('User Switch', 'Cross Hair Line')
SECOND_PLOT_SYNC = parser.getboolean('User Switch', 'Second Plot Sync')
CSV_FILE = parser.getboolean('User Switch', 'CSV Data File')
TTS = parser.getboolean('User Switch', 'Text To Speach')
SEARCH_MOVING_NODE = parser.getboolean('User Switch', 'Search Moving Node')
UI_HIDE = parser.getboolean('User Switch', 'UI Hide')

# [6]. << Real Time Request Item Switch = 'ON or OFF' >>
CM_FUT_PRICE = parser.getboolean('RealTime Request Item Switch', 'Current Month Futures Price')
CM_FUT_QUOTE = parser.getboolean('RealTime Request Item Switch', 'Current Month Futures Quote')
CM_OPT_PRICE = parser.getboolean('RealTime Request Item Switch', 'Current Month Option Price')
CM_OPT_PRICE1 = parser.getboolean('RealTime Request Item Switch', 'Current Month Option Price1')
CM_OPT_QUOTE = parser.getboolean('RealTime Request Item Switch', 'Current Month Option Quote')
CM_OPT_QUOTE1 = parser.getboolean('RealTime Request Item Switch', 'Current Month Option Quote1')
NM_FUT_PRICE = parser.getboolean('RealTime Request Item Switch', 'Next Month Futures Price')
NM_FUT_QUOTE = parser.getboolean('RealTime Request Item Switch', 'Next Month Futures Quote')
NM_OPT_PRICE = parser.getboolean('RealTime Request Item Switch', 'Next Month Option Price')
NM_OPT_QUOTE = parser.getboolean('RealTime Request Item Switch', 'Next Month Option Quote')
NM_OPT_QUOTE1 = parser.getboolean('RealTime Request Item Switch', 'Next Month Option Quote1')
SUPPLY_DEMAND = parser.getboolean('RealTime Request Item Switch', 'Supply & Demand')
DOW_CHK = parser.getboolean('RealTime Request Item Switch', 'DOW')
SP500_CHK = parser.getboolean('RealTime Request Item Switch', 'S&P 500')
NASDAQ_CHK = parser.getboolean('RealTime Request Item Switch', 'NASDAQ')
WTI_CHK = parser.getboolean('RealTime Request Item Switch', 'WTI OIL')
EUROFX_CHK = parser.getboolean('RealTime Request Item Switch', 'EUROFX')
HANGSENG_CHK = parser.getboolean('RealTime Request Item Switch', 'HANGSENG')
GOLD_CHK = parser.getboolean('RealTime Request Item Switch', 'GOLD')
NEWS_CHK = parser.getboolean('RealTime Request Item Switch', 'NEWS')

# [7]. << Moving Average Type >>
MA_TYPE = parser.getint('Moving Average Type', 'MA Type')

# [8]. << Initial Value >>
CALL_ITM_REQUEST_NUMBER = parser.getint('Initial Value', 'Number of Call ITM Request')
CALL_OTM_REQUEST_NUMBER = parser.getint('Initial Value', 'Number of Call OTM Request')
PUT_ITM_REQUEST_NUMBER = parser.getint('Initial Value', 'Number of Put ITM Request')
PUT_OTM_REQUEST_NUMBER = parser.getint('Initial Value', 'Number of Put OTM Request')
HL_Depth = parser.getint('Initial Value', 'HL List Depth')
NightTime_PreStart_Hour = parser.getint('Initial Value', 'NightTime Pre-Start Hour')
ActvalCount = parser.getint('Initial Value', 'Actval Count of the Option Pairs')
MY_COREVAL = parser.getfloat('Initial Value', 'My Coreval')
ASYM_RATIO = parser.getfloat('Initial Value', 'Asymmetric Market Ratio')
ONEWAY_RATIO = parser.getfloat('Initial Value', 'OneWay Market Ratio')
GOLDEN_RATIO = parser.getfloat('Initial Value', 'Golden Ratio')
CROSS_COLOR_INTERVAL = parser.getint('Initial Value', 'Cross Coloring Interval(minute)')
MAIN_UPDATE_INTERVAL = parser.getfloat('Initial Value', 'Main Update Interval(msec)')
BIGCHART_UPDATE_INTERVAL = parser.getfloat('Initial Value', 'Big Chart Update Interval(msec)')
SCORE_BOARD_UPDATE_INTERVAL = parser.getint('Initial Value', 'Score Board Update Interval(sec)')
SECOND_DISPLAY_X_POSITION = parser.getint('Initial Value', 'X Position of the Second Display')
SECOND_DISPLAY_Y_POSITION = parser.getint('Initial Value', 'Y Position of the Second Display')

# [9]. << Code of the Foreign Futures (H/M/U/Z) >>
SP500 = parser.get('Code of the Foreign Futures', 'S&P 500')
DOW = parser.get('Code of the Foreign Futures', 'DOW')
NASDAQ = parser.get('Code of the Foreign Futures', 'NASDAQ')
WTI = parser.get('Code of the Foreign Futures', 'WTI')
EUROFX = parser.get('Code of the Foreign Futures', 'EUROFX')
HANGSENG = parser.get('Code of the Foreign Futures', 'HANGSENG')
GOLD = parser.get('Code of the Foreign Futures', 'GOLD')

# [10]. << Telegram >>
TELEGRAM_START_TIME = parser.getint('Telegram', 'Telegram polling start time(minute) after service')
TELEGRAM_POLLING_INTERVAL = parser.getint('Telegram', 'Telegram polling interval(second)')
TELEGRAM_SEND_INTERVAL = parser.getint('Telegram', 'Telegram send interval(second)')

# [11]. << Rules >>
ONEWAY_THRESHOLD = parser.getint('Rules', 'Threshold of the institutional party supply & demand')
########################################################################################################################

if int(CURRENT_MONTH[4:6]) == 11:
    NEXT_MONTH = CURRENT_MONTH[0:4] + '12'
    MONTH_AFTER_NEXT = repr(int(CURRENT_MONTH[0:4]) + 1) + '01'
elif int(CURRENT_MONTH[4:6]) == 12:
    NEXT_MONTH = repr(int(CURRENT_MONTH[0:4]) + 1) + '01'
    MONTH_AFTER_NEXT = repr(int(CURRENT_MONTH[0:4]) + 1) + '02'
else:
    NEXT_MONTH = repr(int(CURRENT_MONTH) + 1)
    MONTH_AFTER_NEXT = repr(int(CURRENT_MONTH) + 2)

dt = datetime.datetime.now()        
nowDate = dt.strftime('%Y-%m-%d')
current_str = dt.strftime('%H:%M:%S')

today = datetime.date.today()
now_Month = today.strftime('%Y%m')
today_str = today.strftime('%Y%m%d')
today_title = today.strftime('%Y-%m-%d')

yesterday = today - datetime.timedelta(1)
yesterday_str = yesterday.strftime('%Y%m%d')

current_month = int(CURRENT_MONTH[4:6])
next_month = int(NEXT_MONTH[4:6])
month_after_next = int(MONTH_AFTER_NEXT[4:6])

########################################################################################################################
class CallWorker(mp.Process):

    def __init__(self, dataQ):
        super(CallWorker, self).__init__()

        self.daemon = True

        self.dataQ = dataQ
        self.data = []

        self.connection = None

        self.valid_data_receive = False
        self.oc0_value = None

        # 조회요청 TR 초기화
        self.XQ_t0167 = None # 시간 조회
        self.XQ_t1514 = None # 코스피/코스닥 지수 조회
        self.XQ_t8432 = None # 지수선물 마스터조회 API용
        self.XQ_t8433 = None # 지수옵션 마스터조회 API용
        self.XQ_t2301 = None # 주간 옵션전광판 조회
        self.XQ_t2101 = None # 주간 선물전광판 조회
        self.XQ_t2801 = None # 야간 선물전광판 조회
        self.XQ_t2835 = None # 야간 옵션전광판 조회
        self.XQ_t8415 = None # 선물/옵션 차트(N분) 조회
        self.XQ_t8416 = None # 선물/옵션 차트(일,주,월) 조회

        # 실시간요청 TR 초기화
        self.JIF = None

        self.YJ = None
        self.YFC = None
        self.YS3 = None
        self.YOC = None

        self.FUT_REAL_FC0 = None
        self.FUT_HO_FH0 = None
        self.OPT_REAL_OC0 = None  
        self.OPT_HO_OH0 = None

        self.FUT_REAL_NC0 = None
        self.FUT_HO_NH0 = None
        self.OPT_REAL_EC0 = None  
        self.OPT_HO_EH0 = None  

        self.IJ = None
        self.S3 = None
        self.BM = None
        self.PM = None

        self.OVC = None
        self.OVH = None
        self.NWS = None

        self.exit = mp.Event()

    def OnLogin(self, code, msg):

        self.data = []

        if code == '0000':

            # COM 객체는 초기화시 객체생성하면 pickling error 발생 --> 로그인후 객체생성하면 해결됨(이유?)

            # 조회요청 TR 객체생성
            self.XQ_t0167 = t0167(parent=self) # 시간 조회
            self.XQ_t1514 = t1514(parent=self) # 코스피/코스닥 지수 조회
            self.XQ_t8432 = t8432(parent=self) # 지수선물 마스터조회 API용
            self.XQ_t8433 = t8433(parent=self) # 지수옵션 마스터조회 API용
            self.XQ_t2301 = t2301(parent=self) # 주간 옵션전광판 조회
            self.XQ_t2101 = t2101(parent=self) # 주간 선물전광판 조회
            self.XQ_t2801 = t2801(parent=self) # 야간 선물전광판 조회
            self.XQ_t2835 = t2835(parent=self) # 야간 옵션전광판 조회
            self.XQ_t8415 = t8415(parent=self) # 선물/옵션 차트(N분) 조회
            self.XQ_t8416 = t8416(parent=self) # 선물/옵션 차트(일,주,월) 조회

            # 실시간 TR 객체생성
            self.JIF = JIF(parent=self)

            self.YJ = YJ_(parent=self)
            self.YFC = YFC(parent=self)
            self.YS3 = YS3(parent=self)
            self.YOC = YOC(parent=self)
            
            self.FUT_REAL_FC0 = FC0(parent=self)
            self.FUT_HO_FH0 = FH0(parent=self)
            self.OPT_REAL_OC0 = OC0(parent=self)
            self.OPT_HO_OH0 = OH0(parent=self)

            self.FUT_REAL_NC0 = NC0(parent=self)
            self.FUT_HO_NH0 = NH0(parent=self)
            self.OPT_REAL_EC0 = EC0(parent=self)
            self.OPT_HO_EH0 = EH0(parent=self)

            self.IJ = IJ_(parent=self)
            self.S3 = S3_(parent=self)
            self.BM = BM_(parent=self)
            self.PM = PM_(parent=self)

            self.OVC = OVC(parent=self)
            self.OVH = OVH(parent=self)

            self.NWS = NWS(parent=self)
            
            self.data.append(code)

            if REAL_SERVER:
                txt = '실서버 콜 백그라운드 로그인 성공 !!!'
                self.data.append(txt)
            else:
                txt = '모의서버 콜 백그라운드 로그인 성공 !!!'
                self.data.append(txt)
            
            print(txt)

            self.dataQ.put(self.data, False)
        else:
            txt = '로그인 실패({0})...'.format(code)
            print(txt)
            self.data.append(code)
            self.dataQ.put(self.data, False)

    def Check_Online(self):

        ret = self.connection.IsConnected()
        return ret

    def Set_Valid_Data_Receive(self, state):

        print('콜 수신방식 변경요청 수신 =', state)

        if state:
            self.valid_data_receive = True
        else:
            self.valid_data_receive = False

    def OnReceiveMessage(self, ClassName, systemError, messageCode, message):

        pass
        '''
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        txt = 'ClassName = {0} : systemError = {1}, messageCode = {2}, message = {3}'.format(ClassName, systemError, messageCode, message)
        print(txt)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        '''
            
    # 조회성 TR 수신 콜백함수
    def OnReceiveData(self, result):

        #print('*********************************************************************************************************************************')
        #print(type(result))
        #print(result)
        self.dataQ.put(result, False)
        #print('*********************************************************************************************************************************')

    # 실시간데이타 수신 콜백함수
    def OnReceiveRealData(self, result):

        if self.valid_data_receive:

            szTrCode = result['szTrCode']

            if szTrCode == 'OC0':

                if result['현재가'] != self.oc0_value:
                    self.dataQ.put(result, False)
                    self.oc0_value = result['현재가']
                else:
                    pass
            else:
                pass
        else:
            self.dataQ.put(result, False)

    def Login(self, url, port, svrtype, id, pwd, cert):

        if self.connection is None:
            self.connection = XASession(parent=self)
        
        self.connection.login(url, port, svrtype, id, pwd, cert)

    def RequestTRData(self, type, code='0'):

        if type == 't0167':

            self.XQ_t0167.Query()

        elif type == 't1514':

            self.XQ_t1514.Query(업종코드=code)

        elif type == 't8432':

            self.XQ_t8432.Query()

        elif type == 't8433':

            self.XQ_t8433.Query()

        elif type == 't2301':

            self.XQ_t2301.Query(월물=code)

        elif type == 't2101':

            self.XQ_t2101.Query(종목코드=code)

        elif type == 't2801':

            self.XQ_t2801.Query(종목코드=code)

        elif type == 't2835':

            self.XQ_t2835.Query(월물=code)

        elif type == 't8415':

            if today_str == MONTH_FIRSTDAY:
                self.XQ_t8415.Query(단축코드=code, 시작일자=yesterday_str, 종료일자=today_str)
            else:
                self.XQ_t8415.Query(단축코드=code, 시작일자=MONTH_FIRSTDAY, 종료일자=today_str)

        elif type == 't8416':

            if code[0:3] == '101':

                # 휴일 포함 30일치 과거데이타를 요청한다.
                temp = today - datetime.timedelta(30)
                startday_str = temp.strftime('%Y%m%d')

                self.XQ_t8416.Query(단축코드=code, 시작일자=startday_str, 종료일자=today_str)
            else:
                if today_str == MONTH_FIRSTDAY:
                    self.XQ_t8416.Query(단축코드=code, 시작일자=yesterday_str, 종료일자=today_str)
                else:
                    self.XQ_t8416.Query(단축코드=code, 시작일자=MONTH_FIRSTDAY, 종료일자=today_str)
        else:
            pass

    def RequestRealData(self, type, code='0'):

        if type == 'JIF':
            # 장운영 정보 요청
            self.JIF.AdviseRealData(code)

        elif type == 'YJ':
            # KOSPI 예상체결 요청
            self.YJ.AdviseRealData(code)

        elif type == 'YFC':
            # 지수선물 예상체결 요청
            self.YFC.AdviseRealData(code)

        elif type == 'YS3':
            # KOSPI 주요업체 예상체결 요청
            self.YS3.AdviseRealData(code)

        elif type == 'YOC':
            # 지수옵션 예상체결 요청
            self.YOC.AdviseRealData(code)
        
        elif type == 'FUT_REAL_FC0':
            # 선물 실시간 주간 가격 요청
            self.FUT_REAL_FC0.AdviseRealData(code)

        elif type == 'FUT_HO_FH0':
            # 선물 실시간 주간 호가 요청
            self.FUT_HO_FH0.AdviseRealData(code)

        elif type == 'OPT_REAL_OC0':
            # 옵션 실시간 주간 가격 요청
            self.OPT_REAL_OC0.AdviseRealData(code)

        elif type == 'OPT_HO_OH0':
            # 옵션 실시간 주간 호가 요청
            self.OPT_HO_OH0.AdviseRealData(code)

        elif type == 'FUT_REAL_NC0':
            # 선물 실시간 야간 가격 요청
            self.FUT_REAL_NC0.AdviseRealData(code)

        elif type == 'FUT_HO_NH0':
            # 선물 실시간 야간 호가 요청
            self.FUT_HO_NH0.AdviseRealData(code)

        elif type == 'OPT_REAL_EC0':
            # 옵션 실시간 야간 가격 요청
            self.OPT_REAL_EC0.AdviseRealData(code)

        elif type == 'OPT_HO_EH0':
            # 옵션 실시간 야간 호가 요청
            self.OPT_HO_EH0.AdviseRealData(code)

        elif type == 'IJ':
            # KOSPI/KOSPI200/KOSDAQ 지수요청
            self.IJ.AdviseRealData(code)

        elif type == 'S3':
            # KOSPI 주요업체(SAMSUNG) 체결 요청
            self.S3.AdviseRealData(code)

        elif type == 'BM':
            # 업종별 투자자별 매매현황 요청
            self.BM.AdviseRealData(code)

        elif type == 'PM':
            # 프로그램 매매현황 요청
            self.PM.AdviseRealData()

        elif type == 'OVC':
            # 해외선물 체결가격 실시간 요청
            self.OVC.AdviseRealData(code)

        elif type == 'OVH':
            # 해외선물 호가 실시간 요청
            self.OVH.AdviseRealData(code)

        elif type == 'NWS':
            # 실시간 뉴스요청
            print('실시간 뉴스를 요청합니다.')
            self.NWS.AdviseRealData()
        else:
            pass

    def CancelRealData(self, type, code='0'):

        if type == 'JIF':
            # 장운영 정보 요청취소
            self.JIF.UnadviseRealData()

        elif type == 'YJ':
            # KOSPI 예상체결 요청취소
            self.YJ.UnadviseRealData()

        elif type == 'YFC':
            # 지수선물 예상체결 요청취소
            self.YFC.UnadviseRealData()

        elif type == 'YS3':
            # KOSPI 주요업체 예상체결 요청취소
            self.YS3.UnadviseRealData()

        elif type == 'YOC':
            # 지수옵션 예상체결 요청취소
            self.YOC.UnadviseRealData()
        
        elif type == 'FUT_REAL_FC0':
            # 선물 실시간 가격 요청취소
            self.FUT_REAL_FC0.UnadviseRealDataWithKey(code)

        elif type == 'FUT_HO_FH0':
            # 선물 실시간 호가 요청취소
            self.FUT_HO_FH0.UnadviseRealDataWithKey(code)

        elif type == 'OPT_REAL_OC0':
            # 옵션 실시간 가격 요청취소
            self.OPT_REAL_OC0.UnadviseRealData()

        elif type == 'OPT_HO_OH0':
            # 옵션 실시간 호가 요청취소
            self.OPT_HO_OH0.UnadviseRealData()

        elif type == 'FUT_REAL_NC0':
            # 선물 실시간 가격 요청취소
            self.FUT_REAL_NC0.UnadviseRealDataWithKey(code)

        elif type == 'FUT_HO_NH0':
            # 선물 실시간 호가 요청취소
            self.FUT_HO_NH0.UnadviseRealDataWithKey(code)

        elif type == 'OPT_REAL_EC0':
            # 옵션 실시간 가격 요청취소
            self.OPT_REAL_EC0.UnadviseRealData()

        elif type == 'OPT_HO_EH0':
            # 옵션 실시간 호가 요청취소
            self.OPT_HO_EH0.UnadviseRealData()

        elif type == 'IJ':
            # KOSPI/KOSPI200/KOSDAQ 지수 요청취소
            self.IJ.UnadviseRealDataWithKey(code)

        elif type == 'S3':
            # KOSPI 주요업체(SAMSUNG) 체결 요청취소
            self.S3.UnadviseRealData()

        elif type == 'BM':
            # 업종별 투자자별 매매현황 요청취소
            self.BM.UnadviseRealData()

        elif type == 'PM':
            # 프로그램 매매현황 요청취소
            self.PM.UnadviseRealData()

        elif type == 'OVC':
            # 해외선물 체결가격 실시간 요청취소
            # 개별항목 취소가 안됨!!! --> 좌측정열로 8자리 맞추어야함(ljust함수 사용)
            self.OVC.UnadviseRealDataWithKey(code)

        elif type == 'OVH':
            # 해외선물 호가 실시간 요청취소
            self.OVH.UnadviseRealData()

        elif type == 'NWS':
            # 실시간 뉴스 요청취소
            self.NWS.UnadviseRealData()
        else:
            pass

    def CancelAllRealData(self):

        self.JIF.UnadviseRealData()

        self.YJ.UnadviseRealData()
        self.YFC.UnadviseRealData()
        self.YS3.UnadviseRealData()
        self.YOC.UnadviseRealData()

        self.FUT_REAL_FC0.UnadviseRealData()
        self.FUT_HO_FH0.UnadviseRealData()
        self.OPT_REAL_OC0.UnadviseRealData()
        self.OPT_HO_OH0.UnadviseRealData()

        self.FUT_REAL_NC0.UnadviseRealData()
        self.FUT_HO_NH0.UnadviseRealData()
        self.OPT_REAL_EC0.UnadviseRealData()
        self.OPT_HO_EH0.UnadviseRealData()

        self.IJ.UnadviseRealData()

        self.S3.UnadviseRealData()
        self.BM.UnadviseRealData()
        self.PM.UnadviseRealData()

        self.OVC.UnadviseRealData()
        self.OVH.UnadviseRealData()
        self.NWS.UnadviseRealData()     

    def run(self):

        print('Call MultiProcess RealTimeWorker Start...')
        
        while not self.exit.is_set():
            pass

        print("Call MultiProcess RealTimeWorker Terminated !!!")

    def disconnect(self):

        print('Call 서버연결 해지...')
        self.connection.disconnect()

    def shutdown(self):

        print("Call MultiProcess Shutdown initiated...")        
        self.exit.set()            