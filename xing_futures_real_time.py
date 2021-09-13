from multiprocessing import Queue
import win32com.client

from xing_config import *
from xing_futures_event_handler import *

class RealTimeAbs:

    def __init__(self, queue: Queue, res_code: str):

        xa_real = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XARealEventHandler)
        xa_real.queue = queue
        xa_real.ResFileName = f"{RES_FOLDER_PATH}/{res_code}.res"
        self.xa_real = xa_real

    def set_code_list(self, code_list: list, field="shcode"):

        for code in code_list:
            self.xa_real.SetFieldData("InBlock", field, code)
            self.xa_real.AdviseRealData()

    def set_jif_code(self, code, field="jangubun"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

    def set_ij_code(self, code, field="upcode"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

    def set_yj_code(self, code, field="upcode"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

    def set_yfc_code(self, code, field="futcode"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

    def set_s3_code(self, code, field="shcode"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

    def set_bm_code(self, code, field="upcode"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

    def set_pm_code(self, code, field="gubun"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

    def set_ovc_code(self, code, field="symbol"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

    def set_nws_code(self, code, field="nwcode"):

        self.xa_real.SetFieldData("InBlock", field, code)
        self.xa_real.AdviseRealData()

class RealTimeJIFTick(RealTimeAbs):
    """
    [JIF] 장운영정보
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "JIF")

class RealTimeNWSTick(RealTimeAbs):
    """
    [NWS] 실시간뉴스
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "NWS")

class RealTimeIJTick(RealTimeAbs):
    """
    [IJ_] 지수
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "IJ_")

class RealTimeYJTick(RealTimeAbs):
    """
    [YJ_] 예상지수
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "YJ_")

class RealTimeYFCTick(RealTimeAbs):
    """
    [YFC] 지수선물 예상체결
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "YFC")

class RealTimeS3Tick(RealTimeAbs):
    """
    [S3_] KOSPI체결, 삼성/현대등 주요업체 체결요청
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "S3_")

class RealTimeBMTick(RealTimeAbs):
    """
    [BM_] 업종별투자자별 매매현황
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "BM_")

class RealTimePMTick(RealTimeAbs):
    """
    [PM_] KOSPI 프로그램매매 전체집계
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "PM_")

class RealTimeOVCTick(RealTimeAbs):
    """
    [OVC] 해외선물 체결
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "OVC")

class RealTimeKospiQuote(RealTimeAbs):
    """
    [H1_] KOSPI호가잔량
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "H1_")

class RealTimeKospiTick(RealTimeAbs):
    """
    [S3_] KOSPI체결
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "S3_")

class RealTimeKosdaqQuote(RealTimeAbs):
    """
    [HA_] KOSDAQ호가잔량
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "HA_")

class RealTimeKosdaqTick(RealTimeAbs):
    """
    [K3_] KOSDAQ체결
    """
    def __init__(self, queue: Queue):
        super().__init__(queue, "K3_")

class RealTimeIndexFuturesQuote(RealTimeAbs):
    """
    [FH0/NH0] 지수선물호가
    """
    def __init__(self, queue: Queue):

        if NightTime:
            super().__init__(queue, "NH0")
        else:
            super().__init__(queue, "FH0")

class RealTimeIndexFuturesTick(RealTimeAbs):
    """
    [FC0/NC0] 지수선물체결
    """
    def __init__(self, queue: Queue):

        if NightTime:
            super().__init__(queue, "NC0")
        else:
            super().__init__(queue, "FC0")

class RealTimeIndexOptionQuote(RealTimeAbs):
    """
    [OH0/EH0] 지수옵션호가
    """
    def __init__(self, queue: Queue):

        if NightTime:
            super().__init__(queue, "EH0")
        else:
            super().__init__(queue, "OH0")

class RealTimeIndexOptionTick(RealTimeAbs):
    """
    [OC0/EC0] 지수옵션체결
    """
    def __init__(self, queue: Queue):

        if NightTime:
            super().__init__(queue, "EC0")
        else:
            super().__init__(queue, "OC0")

