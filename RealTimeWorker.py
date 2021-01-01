import sys, os
import datetime, time
import pandas as pd
import multiprocessing as mp
from multiprocessing import Process, Queue

from XASessions import *
from XAQueries import *
from XAReals import *

class RealTimeWorker(mp.Process):

    def __init__(self, dataQ):
        super(RealTimeWorker, self).__init__()

        self.daemon = True

        self.dataQ = dataQ

        self.result = dict()
        self.connection = None

        # 실시간요청 아이디 초기화
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
        self.WOC = None
        self.NWS = None

        self.exit = mp.Event()

    def OnLogin(self, code, msg):

        if code == '0000':

            # 로그인 이후 객체를 생성해야 됨
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

            print('로그인 성공...')
            
            self.result['szTrCode'] = 'LOGIN'
            self.result['로그인'] = '백그라운드 로그인 성공 !!!'
            self.dataQ.put(self.result, False)

            #self.NWS.AdviseRealData()
        else:
            print('로그인 실패...')

    def OnLogout(self):

        print("로그아웃 되었습니다.")

    def OnDisconnect(self):

        print("연결이 끊겼습니다.")

    def OnReceiveMessage(self, ClassName, systemError, messageCode, message):

        txt = 'ClassName = {0} : systemError = {1}, messageCode = {2}, message = {3}'.format(ClassName, systemError, messageCode, message)
        print(txt)
    
    def OnReceiveData(self, szTrCode, result):

        print(result)

    # 실시간데이타 수신 콜백함수
    def OnReceiveRealData(self, szTrCode, result):

        print(result)
        self.dataQ.put(result, False)
    
    def login(self):

        계좌정보 = pd.read_csv("secret/passwords.csv", converters={'계좌번호': str, '거래비밀번호': str})

        주식계좌정보 = 계좌정보.query("구분 == '모의'")
        print('MP 모의서버에 접속합니다.') 

        self.connection = XASession(parent=self)

        self.url = 주식계좌정보['url'].values[0].strip()
        self.id = 주식계좌정보['사용자ID'].values[0].strip()
        self.pwd = 주식계좌정보['비밀번호'].values[0].strip()
        self.cert = 주식계좌정보['공인인증비밀번호'].values[0].strip()
        
        self.connection.login(url=self.url, id=self.id, pwd=self.pwd, cert=self.cert)

    def RequestRealData(self, type, code):

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
            # 선물 실시간 가격 요청
            self.FUT_REAL_FC0.AdviseRealData(code)

        elif type == 'FUT_HO_FH0':
            # 선물 실시간 호가 요청
            self.FUT_HO_FH0.AdviseRealData(code)

        elif type == 'OPT_REAL_OC0':
            # 옵션 실시간 가격 요청
            self.OPT_REAL_OC0.AdviseRealData(code)

        elif type == 'OPT_HO_OH0':
            # 옵션 실시간 호가 요청
            self.OPT_HO_OH0.AdviseRealData(code)

        elif type == 'FUT_REAL_NC0':
            # 선물 실시간 가격 요청
            self.FUT_REAL_NC0.AdviseRealData(code)

        elif type == 'FUT_HO_NH0':
            # 선물 실시간 호가 요청
            self.FUT_HO_NH0.AdviseRealData(code)

        elif type == 'OPT_REAL_EC0':
            # 옵션 실시간 가격 요청
            self.OPT_REAL_EC0.AdviseRealData(code)

        elif type == 'OPT_HO_EH0':
            # 옵션 실시간 호가 요청
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
            self.OVC.AdviseRealData(code)

        elif type == 'NWS':
            # 실시간 뉴스요청
            print('실시간 뉴스를 요청합니다.')
            self.NWS.AdviseRealData()
        else:
            pass

    def CancelRealData(self, type, code):

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
            self.FUT_REAL_FC0.UnadviseRealData()

        elif type == 'FUT_HO_FH0':
            # 선물 실시간 호가 요청취소
            self.FUT_HO_FH0.UnadviseRealData()

        elif type == 'OPT_REAL_OC0':
            # 옵션 실시간 가격 요청취소
            self.OPT_REAL_OC0.UnadviseRealData()

        elif type == 'OPT_HO_OH0':
            # 옵션 실시간 호가 요청취소
            self.OPT_HO_OH0.UnadviseRealData()

        elif type == 'FUT_REAL_NC0':
            # 선물 실시간 가격 요청취소
            self.FUT_REAL_NC0.UnadviseRealData()

        elif type == 'FUT_HO_NH0':
            # 선물 실시간 호가 요청취소
            self.FUT_HO_NH0.UnadviseRealData()

        elif type == 'OPT_REAL_EC0':
            # 옵션 실시간 가격 요청취소
            self.OPT_REAL_EC0.UnadviseRealData()

        elif type == 'OPT_HO_EH0':
            # 옵션 실시간 호가 요청취소
            self.OPT_HO_EH0.UnadviseRealData()

        elif type == 'IJ':
            # KOSPI/KOSPI200/KOSDAQ 지수 요청취소
            self.IJ.UnadviseRealData()

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
            # 개별항목 취소가 안됨!!!
            #self.OVC.UnadviseRealDataWithKey(code)
            self.OVC.UnadviseRealData()

        elif type == 'OVH':
            # 해외선물 호가 실시간 요청취소
            self.OVH.UnadviseRealData()

        elif type == 'NWS':
            # 실시간 뉴스 요청취소
            self.NWS.UnadviseRealData()
        else:
            pass     

    def run(self):

        print('MultiProcessing RealTimeWorker Start...')

        self.result['szTrCode'] = 'START'
        self.result['MultiProcessing Start'] = '멀티프로세싱 시작...'
        self.dataQ.put(self.result, False)

        while not self.exit.is_set():
            pass

        print("MultiProcessing RealTimeWorker Terminated !!!")

    def shutdown(self):

        print("MultiProcessing Shutdown initiated...")

        self.result['szTrCode'] = 'SHUTDOWN'
        self.result['MultiProcessing Shutdown'] = '멀티프로세싱 종료...'
        self.dataQ.put(self.result, False)
        
        print('실시간요청 취소...')
        self.NWS.UnadviseRealData()

        print('서버연결 해지...')
        self.connection.disconnect()

        self.exit.set()            