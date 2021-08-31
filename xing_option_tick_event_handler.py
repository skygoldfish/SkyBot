import time
from datetime import datetime

from xing_constant import *

class XASessionEventHandler:

    login_state = False
    login_code = ''
    login_msg = ''

    def OnLogin(self, code, msg):

        XASessionEventHandler.login_state = True

        if code == "0000":       
            XASessionEventHandler.login_code = code
            XASessionEventHandler.login_msg = msg
        else:
            XASessionEventHandler.login_code = code
            XASessionEventHandler.login_msg = msg

class XAQueryEventHandler:

    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandler.query_state = 1

class XARealEventHandler:

    def __init__(self):
        self.queue = None
        '''
        response = ntplib.NTPClient().request(TimeServer, version=3)

        time_str = time.ctime(response.tx_time).split(' ')
        srever_time = time_str[3]

        server_hour = int(srever_time[0:2])
        server_minute = int(srever_time[3:5])
        server_second = int(srever_time[6:8])

        self.timegap = round(-response.offset)

        print('\r')
        print('옵션 시스템 서버간 시간차는 {0}초 입니다...\r', self.timegap)
        print('\r')
        '''
    def handle_jif_tick(self) -> list:
        """
        JIF
        """
        values = []
        for field in JIF_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_ij_tick(self) -> list:
        """
        IJ
        """
        values = []
        for field in IJ_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_quote(self) -> list:
        """
        코스피, 코스닥 호가 데이터
        """
        values = []
        for field in QUOTE_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))
            
        return values

    def handle_tick(self) -> list:
        """
        코스피, 코스닥 체결 데이터
        """
        values = []
        for field in TICK_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_index_futures_quote(self) -> list:
        """
        지수선물 호가 데이터
        """
        values = []
        for field in INDEX_FUTURES_QUOTE_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_index_futures_tick(self) -> list:
        """
        지수선물 체결 데이터
        """
        values = []
        for field in INDEX_FUTURES_TICK_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_index_option_quote(self) -> list:
        """
        지수옵션 호가 데이터
        """
        values = []
        for field in INDEX_OPTION_QUOTE_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_index_option_tick(self) -> list:
        """
        지수옵션 체결 데이터
        """
        values = []
        for field in INDEX_OPTION_TICK_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_index_option_yoc_tick(self) -> list:
        """
        지수옵션 예상체결 데이터
        """
        values = []
        for field in INDEX_OPTION_TICK_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_bm_tick(self) -> list:
        """
        BM
        """
        values = []
        for field in BM_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_pm_tick(self) -> list:
        """
        PM
        """
        values = []
        for field in PM_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values
    
    def handle_ovc_tick(self) -> list:
        """
        OVC
        """
        values = []
        for field in OVC_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_nws_tick(self) -> list:
        """
        NWS
        """
        values = []
        for field in NWS_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_yj_tick(self) -> list:
        """
        YJ_
        """
        values = []
        for field in YJ_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_yfc_tick(self) -> list:
        """
        YFC
        """
        values = []
        for field in YFC_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_s3_tick(self) -> list:
        """
        S3
        """
        values = []
        for field in S3_FIELDS:
            values.append(self.GetFieldData("OutBlock", field))

        return values

    def handle_jif(self, tr_code) -> tuple:
        """
        JIF : 장운영정보
        """
        values = self.handle_jif_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(JIF_COLUMNS_HEADER, values))

        return DataType.JIF_TICK, result

    def handle_ij(self, tr_code) -> tuple:
        """
        IJ : 지수
        """
        values = self.handle_ij_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(IJ_COLUMNS_HEADER, values))

        return DataType.IJ_TICK, result

    def handle_h1(self, tr_code) -> tuple:
        """
        H1_ : 코스피 호가
        """
        values = self.handle_quote()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(QUOTE_COLUMNS_HEADER, values))

        return DataType.KOSPI_QUOTE, result

    def handle_s3(self, tr_code) -> tuple:
        """
        S3_ : 코스피 체결
        """
        values = self.handle_s3_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(S3_COLUMNS_HEADER, values))

        return DataType.S3_TICK, result

    def handle_ha(self, tr_code) -> tuple:
        """
        HA_ : 코스닥 호가
        """
        values = self.handle_quote()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(QUOTE_COLUMNS_HEADER, values))

        return DataType.KOSDAQ_QUOTE, result

    def handle_k3(self, tr_code) -> tuple:
        """
        K3 : 코스닥 체결
        """
        values = self.handle_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(TICK_COLUMNS_HEADER, values))

        return DataType.KOSDAQ_TICK, result

    def handle_fh0(self, tr_code) -> tuple:
        """
        FH0 : 지수선물 호가
        """
        values = self.handle_index_futures_quote()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(INDEX_FUTURES_QUOTE_COLUMNS_HEADER, values))

        return DataType.INDEX_FUTURES_QUOTE, result

    def handle_fc0(self, tr_code) -> tuple:
        """
        FC0 : 지수선물 체결
        """
        values = self.handle_index_futures_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(INDEX_FUTURES_TICK_COLUMNS_HEADER, values))

        return DataType.INDEX_FUTURES_TICK, result

    def handle_oh0_eh0(self, tr_code) -> tuple:
        """
        OH0/EH0 : 지수옵션 호가
        """
        values = self.handle_index_option_quote()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(INDEX_OPTION_QUOTE_COLUMNS_HEADER, values))

        return DataType.INDEX_OPTION_QUOTE, result

    def handle_oc0_ec0(self, tr_code) -> tuple:
        """
        OC0/EC0 : 지수옵션 체결
        """
        values = self.handle_index_option_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(INDEX_OPTION_TICK_COLUMNS_HEADER, values))

        return DataType.INDEX_OPTION_TICK, result

    def handle_yoc(self, tr_code) -> tuple:
        """
        YOC : 지수옵션 예상체결
        """
        values = self.handle_index_option_yoc_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(YOC_COLUMNS_HEADER, values))

        return DataType.YOC_TICK, result
    
    def handle_ovc(self, tr_code) -> tuple:
        """
        OVC : 해외선물 체결
        """
        values = self.handle_ovc_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(OVC_COLUMNS_HEADER, values))

        return DataType.OVC_TICK, result

    def handle_bm(self, tr_code) -> tuple:
        """
        BM : 업종별투자자별 매매현황
        """
        values = self.handle_bm_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(BM_COLUMNS_HEADER, values))

        return DataType.BM_TICK, result

    def handle_pm(self, tr_code) -> tuple:
        """
        PM : KOSPI 프로그램매매 전체집계
        """
        values = self.handle_pm_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(PM_COLUMNS_HEADER, values))

        return DataType.PM_TICK, result

    def handle_nws(self, tr_code) -> tuple:
        """
        NWS : 뉴스
        """
        values = self.handle_nws_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(NWS_COLUMNS_HEADER, values))

        return DataType.NWS_TICK, result

    def handle_yj(self, tr_code) -> tuple:
        """
        YJ_ : 예상지수
        """
        values = self.handle_yj_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(YJ_COLUMNS_HEADER, values))

        return DataType.YJ_TICK, result

    def handle_yfc(self, tr_code) -> tuple:
        """
        YFC : 지수선물 예상체결
        """
        values = self.handle_yfc_tick()
        values.insert(0, datetime.now().strftime('%H%M%S'))
        values.insert(1, tr_code)

        result = dict(zip(YFC_COLUMNS_HEADER, values))

        return DataType.YFC_TICK, result

    def OnReceiveRealData(self, tr_code):

        if tr_code == "JIF":
            # 장운영정보
            self.queue.put(self.handle_jif(tr_code))
        elif tr_code == "YJ_":
            # 예상지수
            self.queue.put(self.handle_yj(tr_code))
        elif tr_code == "YFC":
            # 지수선물 예상체결
            self.queue.put(self.handle_yfc(tr_code))
        elif tr_code == "YOC":
            # 지수옵션 예상체결
            self.queue.put(self.handle_yoc(tr_code))
        elif tr_code == "IJ_":
            # 지수
            self.queue.put(self.handle_ij(tr_code))
        elif tr_code == "H1_":
            # 코스피 호가
            self.queue.put(self.handle_h1(tr_code))
        elif tr_code == "S3_":
            # 코스피 체결
            self.queue.put(self.handle_s3(tr_code))
        elif tr_code == "HA_":
            # 코스닥 호가
            self.queue.put(self.handle_ha(tr_code))
        elif tr_code == "K3_":
            # 코스닥 체결
            self.queue.put(self.handle_k3(tr_code))        
        elif tr_code == "FH0":
            # 지수선물 호가
            self.queue.put(self.handle_fh0(tr_code))
        elif tr_code == "FC0":
            # 지수선물 체결
            self.queue.put(self.handle_fc0(tr_code))
        elif tr_code == "OH0" or  tr_code == "EH0":
            # 지수옵션 호가
            self.queue.put(self.handle_oh0_eh0(tr_code))
        elif tr_code == "OC0" or tr_code == "EC0":
            # 지수옵션 체결
            self.queue.put(self.handle_oc0_ec0(tr_code))
            '''
            values = self.handle_index_option_tick()
            time = datetime.now().strftime('%H%M%S')

            ticktime = int(values[0][0:2]) * 3600 + int(values[0][2:4]) * 60 + int(values[0][4:6])
            systime = int(time[0:2]) * 3600 + int(time[2:4]) * 60 + int(time[4:6])

            time_gap = abs(systime -self.timegap - ticktime)

            # 허용오차 이내의 값만 취한다.
            if time_gap < QUEUE_INPUT_PERMIT_TIME:
                self.queue.put(self.handle_oc0_ec0(tr_code))
            else:
                print('OC0 허용오차 오류!!!\r')
            '''
        elif tr_code == "BM_":
            # 업종별투자자별 매매현황
            self.queue.put(self.handle_bm(tr_code))
        elif tr_code == "PM_":
            # KOSPI 프로그램매매 전체집계
            self.queue.put(self.handle_pm(tr_code))
        elif tr_code == "OVC":
            # 해외선물 체결
            self.queue.put(self.handle_ovc(tr_code))
        elif tr_code == "NWS":
            # 뉴스
            self.queue.put(self.handle_nws(tr_code))
        else:
            raise ValueError(f"Invalid TR code : {tr_code}")
