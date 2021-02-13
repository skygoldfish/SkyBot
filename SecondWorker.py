import sys, os
import datetime, time
import multiprocessing as mp
from multiprocessing import Process, Queue
from configparser import ConfigParser

from XASessions import *
from XAQueries import *
from XAReals import *

# Configuration Parser
parser = ConfigParser()
parser.read('skybot.ini')

# [1]. << Server Type >>
REAL_SERVER = parser.getboolean('Server Type', 'Real Server')

# [2]. << Month Info >>
CURRENT_MONTH = parser.get('Month Info', 'Current Month')

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
class SecondWorker(mp.Process):

    def __init__(self, dataQ):
        super(SecondWorker, self).__init__()

        self.dataQ = dataQ
        self.data = []

        self.connection = None

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
                txt = '실서버 2nd 백그라운드 프로세스 생성 !!!'
                self.data.append(txt)
            else:
                txt = '모의서버 2nd 백그라운드 프로세스 생성 !!!'
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

        self.dataQ.put(result, False)

    def Login(self, url, id, pwd, cert):

        if self.connection is None:
            self.connection = XASession(parent=self)
        
        self.url = url
        self.id = id
        self.pwd = pwd
        self.cert = cert

        self.connection.login(url=self.url, id=self.id, pwd=self.pwd, cert=self.cert)

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
            self.S3.UnadviseRealDataWithKey(code)

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

        print('Second MultiProcess RealTimeWorker Start...')
        
        while not self.exit.is_set():
            pass

        print("Second MultiProcess RealTimeWorker Terminated !!!")

    def disconnect(self):

        print('Second 서버연결 해지...')
        self.connection.disconnect()

    def shutdown(self):

        print("Second MultiProcess Shutdown initiated...")        
        self.exit.set()            