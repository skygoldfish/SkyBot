# -*- coding: utf-8 -*-

import sys, os
import datetime, time
import win32com.client
#import pythoncom
import inspect

import pandas as pd
#from pandas import Panel, DataFrame, Series
from pandas import DataFrame, Series

xarealdata = dict()

class XARealEvents(object):
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def OnReceiveMessage(self, systemError, messageCode, message):
        if self.parent != None:
            self.parent.OnReceiveMessage(systemError, messageCode, message)

    def OnReceiveData(self, szTrCode):
        if self.parent != None:
            self.parent.OnReceiveData(szTrCode)

    def OnReceiveRealData(self, szTrCode):
        if self.parent != None:
            self.parent.OnReceiveRealData(szTrCode)

    def OnReceiveChartRealData(self, szTrCode):
        if self.parent != None:
            self.parent.OnReceiveChartRealData(szTrCode)

    def OnReceiveLinkData(self, szLinkName, szData, szFiller):
        if self.parent != None:
            self.parent.OnReceiveLinkData(szLinkName, szData, szFiller)

class XAReal(object):
    def __init__(self, parent=None, 식별자='식별자'):
        self.parent = parent
        self.식별자 = 식별자
        self.ActiveX = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XARealEvents)
        self.ActiveX.set_parent(parent=self)

        pathname = os.path.dirname(sys.argv[0])
        self.RESDIR = os.path.abspath(pathname)

        self.MYNAME = self.__class__.__name__
        self.INBLOCK = "InBlock"
        self.OUTBLOCK = "OutBlock"
        self.RESFILE = "%s\\Res\\%s.res" % (self.RESDIR, self.MYNAME)

    def OnReceiveMessage(self, systemError, messageCode, message):
        클래스이름 = self.__class__.__name__
        함수이름 = inspect.currentframe().f_code.co_name
        print("%s-%s " % (클래스이름, 함수이름), systemError, messageCode, message)

        if self.parent != None:
            self.parent.OnReceiveMessage(systemError, messageCode, message)

    def AdviseLinkFromHTS(self):
        self.ActiveX.AdviseLinkFromHTS()

    def UnAdviseLinkFromHTS(self):
        self.ActiveX.UnAdviseLinkFromHTS()

    def OnReceiveLinkData(self, szLinkName, szData, szFiller):
        print(szLinkName, szData, szFiller)


# KOSPI호가잔랑
class H1_(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 종목코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "shcode", 종목코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 종목코드):
        self.ActiveX.UnadviseRealDataWithKey(종목코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
        매도호가 = []
        매수호가 = []
        매도호가잔량 = []
        매수호가잔량 = []
        for i in range(1,11):
            매도호가.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho%s" % i))
            매수호가.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho%s" % i))
            매도호가잔량.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem%s" % i))
            매수호가잔량.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem%s" % i))

        result['매도호가'] = 매도호가
        result['매수호가'] = 매수호가
        result['매도호가잔량'] = 매도호가잔량
        result['매수호가잔량'] = 매수호가잔량

        result['총매도호가잔량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totofferrem")
        result['총매수호가잔량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidrem")
        result['동시호가구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "donsigubun")
        result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shcode")
        result['배분적용구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "alloc_gubun")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# KOSDAQ호가잔랑
class HA_(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 종목코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "shcode", 종목코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 종목코드):
        self.ActiveX.UnadviseRealDataWithKey(종목코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
        매도호가 = []
        매수호가 = []
        매도호가잔량 = []
        매수호가잔량 = []
        for i in range(1,11):
            매도호가.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho%s" % i))
            매수호가.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho%s" % i))
            매도호가잔량.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem%s" % i))
            매수호가잔량.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem%s" % i))

        result['매도호가'] = 매도호가
        result['매수호가'] = 매수호가
        result['매도호가잔량'] = 매도호가잔량
        result['매수호가잔량'] = 매수호가잔량

        result['총매도호가잔량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totofferrem")
        result['총매수호가잔량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidrem")
        result['동시호가구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "donsigubun")
        result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shcode")
        result['배분적용구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "alloc_gubun")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# KOSDAQ체결
class K3_(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)
        self.onadvise = dict()

    def AdviseRealData(self, 종목코드):
        if 종목코드 not in list(self.onadvise.keys()):
            self.ActiveX.SetFieldData(self.INBLOCK, "shcode", 종목코드)
            self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 종목코드):
        self.onadvise.pop(종목코드,None)
        self.ActiveX.UnadviseRealDataWithKey(종목코드)

    def UnadviseRealData(self):
        self.onadvise = dict()
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "chetime")
        result['전일대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
        result['전일대비'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
        result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "drate"))
        result['현재가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "price"))
        result['시가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "opentime")
        result['시가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "open"))
        result['고가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hightime")
        result['고가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "high"))
        result['저가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lowtime")
        result['저가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "low"))
        result['체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cgubun")
        result['체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
        result['누적거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
        result['누적거래대금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "value"))
        result['매도누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume"))
        result['매도누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdchecnt"))
        result['매수누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume"))
        result['매수누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mschecnt"))
        result['체결강도'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cpower"))
        result['가중평균가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "w_avrg"))
        result['매도호가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho"))
        result['매수호가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho"))
        result['장정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "status")
        result['전일동시간대거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilvolume"))
        result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shcode")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# KOSPI체결
class S3_(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)
        self.onadvise = dict()

    def AdviseRealData(self, 종목코드):
        if 종목코드 not in list(self.onadvise.keys()):
            self.onadvise[종목코드] = ''
            self.ActiveX.SetFieldData(self.INBLOCK, "shcode", 종목코드)
            self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 종목코드):
        self.onadvise.pop(종목코드, None)
        self.ActiveX.UnadviseRealDataWithKey(종목코드)

    def UnadviseRealData(self):
        self.onadvise = dict()
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "chetime")
        result['전일대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
        result['전일대비'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
        result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "drate"))
        result['현재가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "price"))
        result['시가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "opentime")
        result['시가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "open"))
        result['고가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hightime")
        result['고가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "high"))
        result['저가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lowtime")
        result['저가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "low"))
        result['체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cgubun")
        result['체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
        result['누적거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
        result['누적거래대금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "value"))
        result['매도누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume"))
        result['매도누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdchecnt"))
        result['매수누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume"))
        result['매수누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mschecnt"))
        result['체결강도'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cpower"))
        result['가중평균가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "w_avrg"))
        result['매도호가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho"))
        result['매수호가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho"))
        result['장정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "status")
        result['전일동시간대거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilvolume"))
        result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shcode")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 주식주문접수
class SC0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        # result['라인일련번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "lineseq"))
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno")
        # result['조작자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "user")
        # result['헤더길이'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "len"))
        # result['헤더구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "gubun")
        # result['압축구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compress")
        # result['암호구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "encrypt")
        # result['공통시작지점'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offset"))
        # result['TRCODE'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trcode")
        # result['이용사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "comid")
        # result['사용자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "userid")
        # result['접속매체'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "media")
        # result['IF일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifid")
        # result['전문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "seq")
        # result['TR추적ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trid")
        # result['공인IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pubip")
        # result['사설IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prvip")
        # result['처리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pcbpno")
        # result['지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bpno")
        # result['단말번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "termno")
        # result['언어구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lang")
        # result['AP처리시간'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "proctm"))
        # result['메세지코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msgcode")
        # result['메세지출력구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "outgu")
        # result['압축요청구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compreq")
        # result['기능키'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "funckey")
        # result['요청레코드개수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "reqcnt"))
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler")
        # result['연속구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cont")
        # result['연속키값'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "contkey")
        # result['가변시스템길이'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "varlen"))
        # result['가변해더길이'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "varhdlen"))
        # result['가변메시지길이'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "varmsglen"))
        # result['조회발원지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trsrc")
        # result['IF이벤트ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "eventid")
        # result['IF정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifinfo")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler1")
        # result['주문체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordchegb")
        # result['시장구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "marketgb")
        # result['주문구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordgb")
        # result['원주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordno"))
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno1")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno2")
        # result['비밀번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "passwd")
        # result['종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "expcode")
        # result['단축종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shtcode")
        # result['종목명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hname")
        # result['주문수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordqty"))
        # result['주문가격'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprice"))
        # result['주문조건'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hogagb")
        # result['호가유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "etfhogagb")
        # result['프로그램호가구분'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "pgmtype"))
        # result['공매도호가구분'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "gmhogagb"))
        # result['공매도가능여부'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "gmhogayn"))
        # result['신용구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "singb")
        # result['대출일'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "loandt")
        # result['반대매매주문구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cvrgordtp")
        # result['전략코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "strtgcode")
        # result['그룹ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "groupid")
        # result['주문회차'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordseqno"))
        # result['포트폴리오번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "prtno"))
        # result['바스켓번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "basketno"))
        # result['트렌치번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "trchno"))
        # result['아아템번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "itemno"))
        # result['차입구분'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "brwmgmyn"))
        # result['회원사번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mbrno"))
        # result['처리구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "procgb")
        # result['관리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "admbrchno")
        # result['선물계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futaccno")
        # result['선물상품구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futmarketgb")
        # result['통신매체구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tongsingb")
        # result['유동성공급자구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lpgb")
        # result['DUMMY'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "dummy")
        # result['주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordno"))
        # result['주문시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtm")
        # result['모주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "prntordno"))
        # result['관리사원번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgempno")
        # result['원주문미체결수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordundrqty"))
        # result['원주문정정수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordmdfyqty"))
        # result['원주문취소수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordordcancelqty"))
        # result['비회원사송신번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "nmcpysndno"))
        # result['주문금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordamt"))
        # result['매매구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bnstp")
        # result['예비주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "spareordno"))
        # result['반대매매일련번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvrgseqno"))
        # result['예약주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "rsvordno"))
        # result['복수주문일련번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mtordseqno"))
        # result['예비주문수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "spareordqty"))
        # result['주문사원번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orduserid")
        # result['실물주문수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "spotordqty"))
        # result['재사용주문수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordruseqty"))
        # result['현금주문금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mnyordamt"))
        # result['주문대용금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordsubstamt"))
        # result['재사용주문금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ruseordamt"))
        # result['수수료주문금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordcmsnamt"))
        # result['사용신용담보재사용금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtuseamt"))
        # result['잔고수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqty"))
        # result['실물가능수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "spotordableqty"))
        # result['재사용가능수량_매도'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordableruseqty"))
        # result['변동수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "flctqty"))
        # result['잔고수량_D2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqtyd2"))
        # result['매도주문가능수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "sellableqty"))
        # result['미체결매도주문수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "unercsellordqty"))
        # result['평균매입가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "avrpchsprc"))
        # result['매입금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "pchsamt"))
        # result['예수금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "deposit"))
        # result['대용금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "substamt"))
        # result['위탁증거금현금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnmnymgn"))
        # result['위탁증거금대용'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnsubstmgn"))
        # result['신용담보재사용금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgruseamt"))
        # result['주문가능현금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablemny"))
        # result['주문가능대용'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablesubstamt"))
        # result['재사용가능금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ruseableamt"))
        # result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 주식주문체결
class SC1(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        # result['라인일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lineseq")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno")
        # result['조작자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "user")
        # result['헤더길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "len")
        # result['헤더구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "gubun")
        # result['압축구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compress")
        # result['암호구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "encrypt")
        # result['공통시작지점'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "offset")
        # result['TRCODE'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trcode")
        # result['이용사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "comid")
        # result['사용자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "userid")
        # result['접속매체'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "media")
        # result['IF일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifid")
        # result['전문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "seq")
        # result['TR추적ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trid")
        # result['공인IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pubip")
        # result['사설IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prvip")
        # result['처리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pcbpno")
        # result['지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bpno")
        # result['단말번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "termno")
        # result['언어구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lang")
        # result['AP처리시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "proctm")
        # result['메세지코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msgcode")
        # result['메세지출력구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "outgu")
        # result['압축요청구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compreq")
        # result['기능키'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "funckey")
        # result['요청레코드개수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "reqcnt")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler")
        # result['연속구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cont")
        # result['연속키값'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "contkey")
        # result['가변시스템길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varlen")
        # result['가변해더길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varhdlen")
        # result['가변메시지길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varmsglen")
        # result['조회발원지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trsrc")
        # result['IF이벤트ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "eventid")
        # result['IF정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifinfo")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler1")
        # result['주문체결유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordxctptncode")
        # result['주문시장코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordmktcode")
        # result['주문유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordptncode")
        # result['관리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgmtbrnno")
        # result['계좌번호1'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno1")
        # result['계좌번호2'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno2")
        # result['계좌명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "acntnm")
        # result['종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Isuno")
        result['종목명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Isunm")
        result['주문번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordno")
        # result['원주문번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordno")
        result['체결번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execno")
        result['주문수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordqty")
        result['주문가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprc")
        result['체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execqty")
        result['체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execprc")
        # result['정정확인수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdfycnfqty")
        # result['정정확인가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdfycnfprc")
        # result['취소확인수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "canccnfqty")
        # result['거부수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rjtqty")
        # result['주문처리유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtrxptncode")
        # result['복수주문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mtiordseqno")
        # result['주문조건'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordcndi")
        # result['호가유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprcptncode")
        # result['비저축체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "nsavtrdqty")
        result['단축종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shtnIsuno")
        # result['운용지시번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "opdrtnno")
        # result['반대매매주문구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cvrgordtp")
        # result['미체결수량_주문'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "unercqty")
        # result['원주문미체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordunercqty")
        # result['원주문정정수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordmdfyqty")
        # result['원주문취소수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordcancqty")
        result['주문평균체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordavrexecprc")
        # result['주문금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordamt")
        # result['표준종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "stdIsuno")
        # result['전표준종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bfstdIsuno")
        result['매매구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bnstp")
        # result['주문거래유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtrdptncode")
        # result['신용거래코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgntrncode")
        # result['수수료합산코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "adduptp")
        # result['통신매체코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "commdacode")
        # result['대출일'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Loandt")
        # result['회원_비회원사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mbrnmbrno")
        result['주문계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordacntno")
        # result['집계지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "agrgbrnno")
        # result['관리사원번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgempno")
        # result['선물연계지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsLnkbrnno")
        # result['선물연계계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsLnkacntno")
        # result['선물시장구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsmkttp")
        # result['등록시장코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "regmktcode")
        # result['현금증거금률'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mnymgnrat")
        # result['대용증거금률'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "substmgnrat")
        # result['현금체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mnyexecamt")
        # result['대용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ubstexecamt")
        # result['수수료체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cmsnamtexecamt")
        # result['신용담보체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgexecamt")
        # result['신용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtexecamt")
        # result['전일재사용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prdayruseexecval")
        # result['금일재사용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdayruseexecval")
        # result['실물체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "spotexecqty")
        # result['공매도체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "stslexecqty")
        # result['전략코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "strtgcode")
        # result['그룹Id'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "grpId")
        # result['주문회차'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordseqno")
        # result['포트폴리오번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ptflno")
        # result['바스켓번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bskno")
        # result['트렌치번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trchno")
        # result['아이템번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "itemno")
        # result['주문자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orduserId")
        # result['차입관리여부'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "brwmgmtYn")
        # result['외국인고유번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "frgrunqno")
        # result['거래세징수구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trtzxLevytp")
        # result['유동성공급자구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lptp")
        result['체결시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "exectime")
        # result['거래소수신체결시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rcptexectime")
        # result['잔여대출금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rmndLoanamt")
        # result['잔고수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqty")
        # result['실물가능수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "spotordableqty")
        # result['재사용가능수량_매도'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordableruseqty")
        # result['변동수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "flctqty")
        # result['잔고수량_D2'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqtyd2")
        # result['매도주문가능수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sellableqty")
        # result['미체결매도주문수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "unercsellordqty")
        # result['평균매입가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "avrpchsprc")
        # result['매입금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pchsant")
        # result['예수금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "deposit")
        # result['대용금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "substamt")
        # result['위탁증거금현금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnmnymgn")
        # result['위탁증거금대용'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnsubstmgn")
        # result['신용담보재사용금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgruseamt")
        # result['주문가능현금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablemny")
        # result['주문가능대용'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablesubstamt")
        # result['재사용가능금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ruseableamt")
        # result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 주식주문정정
class SC2(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        # result['라인일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lineseq")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno")
        # result['조작자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "user")
        # result['헤더길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "len")
        # result['헤더구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "gubun")
        # result['압축구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compress")
        # result['암호구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "encrypt")
        # result['공통시작지점'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "offset")
        # result['TRCODE'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trcode")
        # result['이용사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "comid")
        # result['사용자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "userid")
        # result['접속매체'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "media")
        # result['IF일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifid")
        # result['전문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "seq")
        # result['TR추적ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trid")
        # result['공인IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pubip")
        # result['사설IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prvip")
        # result['처리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pcbpno")
        # result['지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bpno")
        # result['단말번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "termno")
        # result['언어구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lang")
        # result['AP처리시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "proctm")
        # result['메세지코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msgcode")
        # result['메세지출력구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "outgu")
        # result['압축요청구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compreq")
        # result['기능키'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "funckey")
        # result['요청레코드개수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "reqcnt")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler")
        # result['연속구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cont")
        # result['연속키값'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "contkey")
        # result['가변시스템길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varlen")
        # result['가변해더길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varhdlen")
        # result['가변메시지길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varmsglen")
        # result['조회발원지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trsrc")
        # result['IF이벤트ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "eventid")
        # result['IF정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifinfo")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler1")
        # result['주문체결유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordxctptncode")
        # result['주문시장코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordmktcode")
        # result['주문유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordptncode")
        # result['관리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgmtbrnno")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno1")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno2")
        # result['계좌명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "acntnm")
        # result['종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Isuno")
        # result['종목명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Isunm")
        # result['주문번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordno")
        # result['원주문번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordno")
        # result['체결번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execno")
        # result['주문수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordqty")
        # result['주문가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprc")
        # result['체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execqty")
        # result['체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execprc")
        # result['정정확인수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdfycnfqty")
        # result['정정확인가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdfycnfprc")
        # result['취소확인수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "canccnfqty")
        # result['거부수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rjtqty")
        # result['주문처리유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtrxptncode")
        # result['복수주문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mtiordseqno")
        # result['주문조건'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordcndi")
        # result['호가유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprcptncode")
        # result['비저축체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "nsavtrdqty")
        # result['단축종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shtnIsuno")
        # result['운용지시번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "opdrtnno")
        # result['반대매매주문구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cvrgordtp")
        # result['미체결수량_주문'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "unercqty")
        # result['원주문미체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordunercqty")
        # result['원주문정정수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordmdfyqty")
        # result['원주문취소수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordcancqty")
        # result['주문평균체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordavrexecprc")
        # result['주문금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordamt")
        # result['표준종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "stdIsuno")
        # result['전표준종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bfstdIsuno")
        # result['매매구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bnstp")
        # result['주문거래유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtrdptncode")
        # result['신용거래코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgntrncode")
        # result['수수료합산코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "adduptp")
        # result['통신매체코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "commdacode")
        # result['대출일'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Loandt")
        # result['회원_비회원사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mbrnmbrno")
        # result['주문계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordacntno")
        # result['집계지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "agrgbrnno")
        # result['관리사원번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgempno")
        # result['선물연계지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsLnkbrnno")
        # result['선물연계계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsLnkacntno")
        # result['선물시장구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsmkttp")
        # result['등록시장코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "regmktcode")
        # result['현금증거금률'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mnymgnrat")
        # result['대용증거금률'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "substmgnrat")
        # result['현금체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mnyexecamt")
        # result['대용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ubstexecamt")
        # result['수수료체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cmsnamtexecamt")
        # result['신용담보체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgexecamt")
        # result['신용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtexecamt")
        # result['전일재사용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prdayruseexecval")
        # result['금일재사용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdayruseexecval")
        # result['실물체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "spotexecqty")
        # result['공매도체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "stslexecqty")
        # result['전략코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "strtgcode")
        # result['그룹Id'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "grpId")
        # result['주문회차'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordseqno")
        # result['포트폴리오번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ptflno")
        # result['바스켓번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bskno")
        # result['트렌치번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trchno")
        # result['아이템번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "itemno")
        # result['주문자Id'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orduserId")
        # result['차입관리여부'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "brwmgmtYn")
        # result['외국인고유번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "frgrunqno")
        # result['거래세징수구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trtzxLevytp")
        # result['유동성공급자구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lptp")
        # result['체결시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "exectime")
        # result['거래소수신체결시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rcptexectime")
        # result['잔여대출금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rmndLoanamt")
        # result['잔고수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqty")
        # result['실물가능수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "spotordableqty")
        # result['재사용가능수량_매도'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordableruseqty")
        # result['변동수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "flctqty")
        # result['잔고수량_d2'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqtyd2")
        # result['매도주문가능수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sellableqty")
        # result['미체결매도주문수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "unercsellordqty")
        # result['평균매입가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "avrpchsprc")
        # result['매입금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pchsant")
        # result['예수금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "deposit")
        # result['대용금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "substamt")
        # result['위탁증거금현금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnmnymgn")
        # result['위탁증거금대용'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnsubstmgn")
        # result['신용담보재사용금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgruseamt")
        # result['주문가능현금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablemny")
        # result['주문가능대용'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablesubstamt")
        # result['재사용가능금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ruseableamt")
        #result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 주식주문취소
class SC3(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        # result['라인일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lineseq")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno")
        # result['조작자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "user")
        # result['헤더길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "len")
        # result['헤더구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "gubun")
        # result['압축구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compress")
        # result['암호구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "encrypt")
        # result['공통시작지점'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "offset")
        # result['TRCODE'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trcode")
        # result['이용사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "comid")
        # result['사용자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "userid")
        # result['접속매체'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "media")
        # result['IF일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifid")
        # result['전문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "seq")
        # result['TR추적ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trid")
        # result['공인IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pubip")
        # result['사설IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prvip")
        # result['처리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pcbpno")
        # result['지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bpno")
        # result['단말번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "termno")
        # result['언어구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lang")
        # result['AP처리시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "proctm")
        # result['메세지코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msgcode")
        # result['메세지출력구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "outgu")
        # result['압축요청구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compreq")
        # result['기능키'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "funckey")
        # result['요청레코드개수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "reqcnt")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler")
        # result['연속구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cont")
        # result['연속키값'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "contkey")
        # result['가변시스템길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varlen")
        # result['가변해더길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varhdlen")
        # result['가변메시지길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varmsglen")
        # result['조회발원지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trsrc")
        # result['IF이벤트ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "eventid")
        # result['IF정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifinfo")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler1")
        # result['주문체결유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordxctptncode")
        # result['주문시장코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordmktcode")
        # result['주문유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordptncode")
        # result['관리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgmtbrnno")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno1")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno2")
        # result['계좌명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "acntnm")
        # result['종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Isuno")
        # result['종목명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Isunm")
        # result['주문번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordno")
        # result['원주문번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordno")
        # result['체결번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execno")
        # result['주문수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordqty")
        # result['주문가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprc")
        # result['체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execqty")
        # result['체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execprc")
        # result['정정확인수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdfycnfqty")
        # result['정정확인가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdfycnfprc")
        # result['취소확인수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "canccnfqty")
        # result['거부수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rjtqty")
        # result['주문처리유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtrxptncode")
        # result['복수주문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mtiordseqno")
        # result['주문조건'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordcndi")
        # result['호가유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprcptncode")
        # result['비저축체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "nsavtrdqty")
        # result['단축종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shtnIsuno")
        # result['운용지시번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "opdrtnno")
        # result['반대매매주문구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cvrgordtp")
        # result['미체결수량_주문'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "unercqty")
        # result['원주문미체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordunercqty")
        # result['원주문정정수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordmdfyqty")
        # result['원주문취소수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordcancqty")
        # result['주문평균체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordavrexecprc")
        # result['주문금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordamt")
        # result['표준종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "stdIsuno")
        # result['전표준종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bfstdIsuno")
        # result['매매구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bnstp")
        # result['주문거래유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtrdptncode")
        # result['신용거래코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgntrncode")
        # result['수수료합산코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "adduptp")
        # result['통신매체코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "commdacode")
        # result['대출일'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Loandt")
        # result['회원_비회원사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mbrnmbrno")
        # result['주문계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordacntno")
        # result['집계지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "agrgbrnno")
        # result['관리사원번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgempno")
        # result['선물연계지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsLnkbrnno")
        # result['선물연계계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsLnkacntno")
        # result['선물시장구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsmkttp")
        # result['등록시장코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "regmktcode")
        # result['현금증거금률'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mnymgnrat")
        # result['대용증거금률'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "substmgnrat")
        # result['현금체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mnyexecamt")
        # result['대용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ubstexecamt")
        # result['수수료체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cmsnamtexecamt")
        # result['신용담보체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgexecamt")
        # result['신용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtexecamt")
        # result['전일재사용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prdayruseexecval")
        # result['금일재사용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdayruseexecval")
        # result['실물체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "spotexecqty")
        # result['공매도체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "stslexecqty")
        # result['전략코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "strtgcode")
        # result['그룹Id'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "grpId")
        # result['주문회차'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordseqno")
        # result['포트폴리오번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ptflno")
        # result['바스켓번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bskno")
        # result['트렌치번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trchno")
        # result['아이템번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "itemno")
        # result['주문자Id'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orduserId")
        # result['차입관리여부'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "brwmgmtYn")
        # result['외국인고유번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "frgrunqno")
        # result['거래세징수구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trtzxLevytp")
        # result['유동성공급자구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lptp")
        # result['체결시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "exectime")
        # result['거래소수신체결시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rcptexectime")
        # result['잔여대출금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rmndLoanamt")
        # result['잔고수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqty")
        # result['실물가능수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "spotordableqty")
        # result['재사용가능수량_매도'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordableruseqty")
        # result['변동수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "flctqty")
        # result['잔고수량_d2'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqtyd2")
        # result['매도주문가능수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sellableqty")
        # result['미체결매도주문수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "unercsellordqty")
        # result['평균매입가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "avrpchsprc")
        # result['매입금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pchsant")
        # result['예수금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "deposit")
        # result['대용금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "substamt")
        # result['위탁증거금현금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnmnymgn")
        # result['위탁증거금대용'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnsubstmgn")
        # result['신용담보재사용금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgruseamt")
        # result['주문가능현금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablemny")
        # result['주문가능대용'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablesubstamt")
        # result['재사용가능금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ruseableamt")
        #result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 주식주문거부
class SC4(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        # result['라인일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lineseq")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno")
        # result['조작자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "user")
        # result['헤더길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "len")
        # result['헤더구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "gubun")
        # result['압축구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compress")
        # result['암호구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "encrypt")
        # result['공통시작지점'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "offset")
        # result['TRCODE'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trcode")
        # result['이용사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "comid")
        # result['사용자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "userid")
        # result['접속매체'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "media")
        # result['IF일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifid")
        # result['전문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "seq")
        # result['TR추적ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trid")
        # result['공인IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pubip")
        # result['사설IP'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prvip")
        # result['처리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pcbpno")
        # result['지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bpno")
        # result['단말번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "termno")
        # result['언어구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lang")
        # result['AP처리시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "proctm")
        # result['메세지코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msgcode")
        # result['메세지출력구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "outgu")
        # result['압축요청구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "compreq")
        # result['기능키'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "funckey")
        # result['요청��코드개수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "reqcnt")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler")
        # result['연속구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cont")
        # result['연속키값'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "contkey")
        # result['가변시스템길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varlen")
        # result['가변해더길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varhdlen")
        # result['가변메시지길이'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "varmsglen")
        # result['조회발원지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trsrc")
        # result['IF이벤트ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "eventid")
        # result['IF정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ifinfo")
        # result['예비영역'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "filler1")
        # result['주문체결유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordxctptncode")
        # result['주문시장코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordmktcode")
        # result['주문유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordptncode")
        # result['관리지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgmtbrnno")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno1")
        # result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "accno2")
        # result['계좌명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "acntnm")
        # result['종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Isuno")
        # result['종목명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Isunm")
        # result['주문번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordno")
        # result['원주문번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordno")
        # result['체결번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execno")
        # result['주문수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordqty")
        # result['주문가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprc")
        # result['체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execqty")
        # result['체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "execprc")
        # result['정정확인수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdfycnfqty")
        # result['정정확인가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdfycnfprc")
        # result['취소확인수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "canccnfqty")
        # result['거부수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rjtqty")
        # result['주문처리유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtrxptncode")
        # result['복수주문일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mtiordseqno")
        # result['주문조건'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordcndi")
        # result['호가유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordprcptncode")
        # result['비저축체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "nsavtrdqty")
        # result['단축종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shtnIsuno")
        # result['운용지시번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "opdrtnno")
        # result['반대매매주문구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cvrgordtp")
        # result['미체결수량_주문'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "unercqty")
        # result['원주문미체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordunercqty")
        # result['원주문정정수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordmdfyqty")
        # result['원주문취소수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orgordcancqty")
        # result['주문평균체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordavrexecprc")
        # result['주문금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordamt")
        # result['표준종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "stdIsuno")
        # result['전표준종목번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bfstdIsuno")
        # result['매매구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bnstp")
        # result['주문거래유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordtrdptncode")
        # result['신용거래코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgntrncode")
        # result['수수료합산코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "adduptp")
        # result['통신매체코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "commdacode")
        # result['대출일'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "Loandt")
        # result['회원_비회원사번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mbrnmbrno")
        # result['주문계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordacntno")
        # result['집계지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "agrgbrnno")
        # result['관리사원번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mgempno")
        # result['선물연계지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsLnkbrnno")
        # result['선물연계계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsLnkacntno")
        # result['선물시장구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futsmkttp")
        # result['등록시장코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "regmktcode")
        # result['현금증거금률'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mnymgnrat")
        # result['대용증거금률'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "substmgnrat")
        # result['현금체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mnyexecamt")
        # result['대용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ubstexecamt")
        # result['수수료체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cmsnamtexecamt")
        # result['신용담보체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgexecamt")
        # result['신용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtexecamt")
        # result['전일재사용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "prdayruseexecval")
        # result['금일재사용체결금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdayruseexecval")
        # result['실물체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "spotexecqty")
        # result['공매도체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "stslexecqty")
        # result['전략코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "strtgcode")
        # result['그룹Id'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "grpId")
        # result['주문회차'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordseqno")
        # result['포트폴리오번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ptflno")
        # result['바스켓번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "bskno")
        # result['트렌치번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trchno")
        # result['아이템번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "itemno")
        # result['주문자Id'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "orduserId")
        # result['차입관리여부'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "brwmgmtYn")
        # result['외국인고유번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "frgrunqno")
        # result['거래세징수구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trtzxLevytp")
        # result['유동성공급자구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lptp")
        # result['체결시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "exectime")
        # result['거래소수신체결시각'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rcptexectime")
        # result['잔여대출금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rmndLoanamt")
        # result['잔고수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqty")
        # result['실물가능수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "spotordableqty")
        # result['재사용가능수량_매도'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordableruseqty")
        # result['변동수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "flctqty")
        # result['잔고수량_d2'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "secbalqtyd2")
        # result['매도주문가능수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sellableqty")
        # result['미체결매도주문수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "unercsellordqty")
        # result['평균매입가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "avrpchsprc")
        # result['매입금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "pchsant")
        # result['예수금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "deposit")
        # result['대용금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "substamt")
        # result['위탁증거금현금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnmnymgn")
        # result['위탁증거금대용'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "csgnsubstmgn")
        # result['신용담보재사용금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crdtpldgruseamt")
        # result['주문가능현금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablemny")
        # result['주문가능대용'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordablesubstamt")
        # result['재사용가능금액'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ruseableamt")
        #result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 실시간 뉴스 제목 패킷(NWS)
class NWS(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 뉴스코드='NWS001'):
        self.ActiveX.SetFieldData(self.INBLOCK, "nwcode", 뉴스코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['날짜'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "date")
        result['시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "time")
        result['뉴스구분자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "id")
        result['키값'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "realkey")
        result['제목'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "title")
        result['단축종목코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "code")
        result['BODY길이'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bodysize"))
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# KOSPI200 선물체결(FC0)
class FC0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 선물코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "futcode", 선물코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 선물코드):
        self.ActiveX.UnadviseRealDataWithKey(선물코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "chetime")
            #result['전일대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
            #result['전일대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
            result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "drate"))
            result['현재가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "price"))
            result['시가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "open"))
            result['고가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "high"))
            result['저가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "low"))
            #result['체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cgubun")
            #result['체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
            #result['누적거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
            #result['누적거래대금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "value"))
            result['매도누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume"))
            #result['매도누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdchecnt"))
            result['매수누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume"))
            #result['매수누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mschecnt"))
            #result['체결강도'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cpower"))
            #result['매도호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho1"))
            #result['매수호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho1"))
            result['미결제약정수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "openyak"))
            result['KOSPI200지수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "k200jisu")
            #result['이론가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "theoryprice"))
            #result['괴리율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "kasis"))
            #result['시장BASIS'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "sbasis"))
            #result['이론BASIS'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "ibasis"))
            result['미결제약정증감'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "openyakcha"))
            #result['장운영정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jgubun")
            #result['전일동시간대거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilvolume"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

# CME연계 KP200지수 선물체결(NC0)
class NC0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 선물코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "futcode", 선물코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 선물코드):
        self.ActiveX.UnadviseRealDataWithKey(선물코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        # 클래스이름 = self.__class__.__name__
        # 함수이름 = inspect.currentframe().f_code.co_name
        # print("ENTER : %s --> %s" %(클래스이름, 함수이름))

        try:
            result = dict()
            result['체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "chetime")
            result['체결시간(36시간)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "chetime1")
            #result['전일대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
            #result['전일대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
            result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "drate"))
            result['현재가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "price")
            result['시가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "open")
            result['고가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "high")
            result['저가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "low")
            #result['체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cgubun")
            #result['체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
            #result['누적거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
            #result['누적거래대금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "value"))
            result['매도누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume"))
            #result['매도누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdchecnt"))
            result['매수누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume"))
            #result['매수누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mschecnt"))
            #result['체결강도'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cpower"))
            #result['매도호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho1"))
            #result['매수호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho1"))
            result['미결제약정수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "openyak"))
            #result['KOSPI200지수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "k200jisu")
            #result['이론가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "theoryprice"))
            #result['괴리율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "kasis"))
            #result['시장BASIS'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "sbasis"))
            #result['이론BASIS'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "ibasis"))
            result['미결제약정증감'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "openyakcha"))
            #result['장운영정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jgubun")
            # result['미사용filler'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilvolume"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# KOSPI200 선물호가(FH0)
class FH0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "futcode", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 단축코드):
        self.ActiveX.UnadviseRealDataWithKey(단축코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
            #result['매도호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho1"))
            #result['매수호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho1"))
            #result['매도호가수량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem1"))
            #result['매수호가수량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem1"))
            #result['매도호가건수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt1"))
            #result['매수호가건수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt1"))
            #result['매도호가2'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho2"))
            #result['매수호가2'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho2"))
            #result['매도호가수량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem2"))
            #result['매수호가수량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem2"))
            #result['매도호가건수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt2"))
            #result['매수호가건수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt2"))
            #result['매도호가3'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho3"))
            #result['매수호가3'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho3"))
            #result['매도호가수량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem3"))
            #result['매수호가수량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem3"))
            #result['매도호가건수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt3"))
            #result['매수호가건수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt3"))
            #result['매도호가4'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho4"))
            #result['매수호가4'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho4"))
            #result['매도호가수량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem4"))
            #result['매수호가수량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem4"))
            #result['매도호가건수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt4"))
            #result['매수호가건수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt4"))
            #result['매도호가5'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho5"))
            #result['매수호가5'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho5"))
            #result['매도호가수량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem5"))
            #result['매수호가수량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem5"))
            #result['매도호가건수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt5"))
            #result['매수호가건수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt5"))
            result['매도호가총수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totofferrem"))
            result['매수호가총수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidrem"))
            result['매도호가총건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totoffercnt"))
            result['매수호가총건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidcnt"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futcode")
            #result['단일가호가여부'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "danhochk")
            #result['배분적용구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "alloc_gubun")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# CME연계 KP200지수선물호가(NH0)
class NH0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "futcode", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 단축코드):
        self.ActiveX.UnadviseRealDataWithKey(단축코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        # 클래스이름 = self.__class__.__name__
        # 함수이름 = inspect.currentframe().f_code.co_name
        # print("ENTER : %s --> %s" %(클래스이름, 함수이름))

        try:
            result = dict()
            result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
            result['호가시간(36시간)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime1")
            #result['매도호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho1"))
            #result['매수호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho1"))
            #result['매도호가수량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem1"))
            #result['매수호가수량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem1"))
            #result['매도호가건수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt1"))
            #result['매수호가건수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt1"))
            #result['매도호가2'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho2"))
            #result['매수호가2'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho2"))
            #result['매도호가수량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem2"))
            #result['매수호가수량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem2"))
            #result['매도호가건수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt2"))
            #result['매수호가건수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt2"))
            #result['매도호가3'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho3"))
            #result['매수호가3'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho3"))
            #result['매도호가수량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem3"))
            #result['매수호가수량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem3"))
            #result['매도호가건수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt3"))
            #result['매수호가건수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt3"))
            #result['매도호가4'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho4"))
            #result['매수호가4'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho4"))
            #result['매도호가수량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem4"))
            #result['매수호가수량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem4"))
            #result['매도호가건수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt4"))
            #result['매수호가건수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt4"))
            #result['매도호가5'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho5"))
            #result['매수호가5'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho5"))
            #result['매도호가수량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem5"))
            #result['매수호가수량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem5"))
            #result['매도호가건수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt5"))
            #result['매수호가건수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt5"))
            result['매도호가총수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totofferrem"))
            result['매수호가총수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidrem"))
            result['매도호가총건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totoffercnt"))
            result['매수호가총건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidcnt"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# 당월물 옵션실시간(OC0)
class OC0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "optcode", 단축코드)
        self.ActiveX.AdviseRealData()
        #print('실시간요청 옵션코드 : %s' %(단축코드))

    def UnadviseRealDataWithKey(self, 단축코드):
        self.ActiveX.UnadviseRealDataWithKey(단축코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "chetime")
            #result['전일대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
            #result['전일대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
            result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "drate"))
            result['현재가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "price"))
            result['시가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "open"))
            result['고가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "high"))
            result['저가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "low"))
            #result['체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cgubun")
            #result['체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
            #result['누적거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
            #result['누적거래대금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "value"))
            result['매도누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume"))
            #result['매도누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdchecnt"))
            result['매수누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume"))
            #result['매수누적체결건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mschecnt"))
            #result['체결강도'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cpower"))
            #result['매도호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho1"))
            #result['매수호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho1"))
            result['미결제약정수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "openyak"))
            #result['KOSPI200지수'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "k200jisu"))
            #result['KOSPI등가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "eqva"))
            #result['이론가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "theoryprice"))
            #result['내재변동성'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "impv"))
            result['미결제약정증감'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "openyakcha"))
            #result['시간가치'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "timevalue"))
            #result['장운영정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jgubun")
            #result['전일동시간대거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilvolume"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "optcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

# KOSPI200 옵션호가(OH0)
class OH0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "optcode", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 단축코드):
        self.ActiveX.UnadviseRealDataWithKey(단축코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
            #result['매도호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho1"))
            #result['매수호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho1"))
            #result['매도호가수량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem1"))
            #result['매수호가수량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem1"))
            #result['매도호가건수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt1"))
            #result['매수호가건수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt1"))
            #result['매도호가2'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho2"))
            #result['매수호가2'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho2"))
            #result['매도호가수량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem2"))
            #result['매수호가수량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem2"))
            #result['매도호가건수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt2"))
            #result['매수호가건수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt2"))
            #result['매도호가3'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho3"))
            #result['매수호가3'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho3"))
            #result['매도호가수량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem3"))
            #result['매수호가수량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem3"))
            #result['매도호가건수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt3"))
            #result['매수호가건수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt3"))
            #result['매도호가4'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho4"))
            #result['매수호가4'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho4"))
            #result['매도호가수량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem4"))
            #result['매수호가수량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem4"))
            #result['매도호가건수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt4"))
            #result['매수호가건수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt4"))
            #result['매도호가5'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho5"))
            #result['매수호가5'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho5"))
            #result['매도호가수량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem5"))
            #result['매수호가수량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem5"))
            #result['매도호가건수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt5"))
            #result['매수호가건수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt5"))
            result['매도호가총수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totofferrem"))
            result['매수호가총수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidrem"))
            result['매도호가총건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totoffercnt"))
            result['매수호가총건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidcnt"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "optcode")
            #result['단일가호가여부'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "danhochk")
            #result['배분적용구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "alloc_gubun")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

# 당월물 야간 옵션실시간(EC0)
class EC0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "optcode", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 단축코드):
        self.ActiveX.UnadviseRealDataWithKey(단축코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "chetime")
            result['체결시간(36시간)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "chetime1")
            #result['정규장종가대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
            #result['정규장종가대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
            result['정규장종가기준등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "drate"))
            result['현재가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "price")
            result['시가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "open")
            result['고가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "high")
            result['저가'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "low")
            #result['체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cgubun")
            #result['체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
            #result['누적거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
            #result['누적거래대금(미제공)'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "value"))
            result['매도누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume"))
            #result['매도누적체결건수(미제공)'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdchecnt"))
            result['매수누적체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume"))
            #result['매수누적체결건수(미제공)'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mschecnt"))
            #result['체결강도'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cpower"))
            #result['매도호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho1"))
            #result['매수호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho1"))
            #result['미결제약정수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "openyak"))
            #result['KOSPI200지수'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "k200jisu"))
            #result['KOSPI등가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "eqva"))
            #result['이론가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "theoryprice"))
            #result['내재변동성'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "impv"))
            #result['미결제약정증감'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "openyakcha"))
            #result['시간가치'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "timevalue"))
            #result['장운영정보'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jgubun")
            #result['전일동시간대거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilvolume"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "optcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

# EUREX연계 KP200지수옵션 선물호가(EH0)
class EH0(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "optcode", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 단축코드):
        self.ActiveX.UnadviseRealDataWithKey(단축코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
            result['호가시간(36시간)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime1")
            #result['매도호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho1"))
            #result['매수호가1'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho1"))
            #result['매도호가수량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem1"))
            #result['매수호가수량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem1"))
            #result['매도호가건수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt1"))
            #result['매수호가건수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt1"))
            #result['매도호가2'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho2"))
            #result['매수호가2'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho2"))
            #result['매도호가수량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem2"))
            #result['매수호가수량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem2"))
            #result['매도호가건수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt2"))
            #result['매수호가건수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt2"))
            #result['매도호가3'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho3"))
            #result['매수호가3'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho3"))
            #result['매도호가수량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem3"))
            #result['매수호가수량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem3"))
            #result['매도호가건수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt3"))
            #result['매수호가건수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt3"))
            #result['매도호가4'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho4"))
            #result['매수호가4'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho4"))
            #result['매도호가수량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem4"))
            #result['매수호가수량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem4"))
            #result['매도호가건수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt4"))
            #result['매수호가건수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt4"))
            #result['매도호가5'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho5"))
            #result['매수호가5'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho5"))
            #result['매도호가수량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem5"))
            #result['매수호가수량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem5"))
            #result['매도호가건수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offercnt5"))
            #result['매수호가건수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidcnt5"))
            result['매도호가총수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totofferrem"))
            result['매수호가총수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidrem"))
            result['매도호가총건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totoffercnt"))
            result['매수호가총건수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidcnt"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "optcode")
            #result['단일가호가여부'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "danhochk")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

# 장운영정보(JIF)
class JIF(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "jangubun", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        #클래스이름 = self.__class__.__name__
        #함수이름 = inspect.currentframe().f_code.co_name
        #print("ENTER : %s --> %s" %(클래스이름, 함수이름))

        try:
            result = dict()
            result['장구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jangubun")
            result['장상태'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jstatus")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# 예상지수(YJ_)
class YJ_(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 업종코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "upcode", 업종코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        #클래스이름 = self.__class__.__name__
        #함수이름 = inspect.currentframe().f_code.co_name
        #print("ENTER : %s --> %s" %(클래스이름, 함수이름))

        try:
            result = dict()
            result['시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "time")
            result['예상지수'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "jisu"))
            result['예상전일대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
            result['예상전일비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
            result['예상등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "drate"))
            result['예상체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
            result['누적거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
            result['예상거래대금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "value"))
            result['업종코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "upcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# 지수선물예상체결(YFC)
class YFC(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "futcode", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        #클래스이름 = self.__class__.__name__
        #함수이름 = inspect.currentframe().f_code.co_name
        #print("ENTER : %s --> %s" %(클래스이름, 함수이름))

        try:
            result = dict()
            result['예상체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ychetime")
            result['예상체결가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "yeprice"))
            result['예상체결가전일종가대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilysign")
            result['예상체결가전일종가대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "preychange"))
            result['예상체결가전일종가등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilydrate"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "futcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# 지수옵션예상체결(YOC)
class YOC(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "optcode", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        #클래스이름 = self.__class__.__name__
        #함수이름 = inspect.currentframe().f_code.co_name
        #print("ENTER : %s --> %s" %(클래스이름, 함수이름))

        try:
            result = dict()
            result['예상체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ychetime")
            result['예상체결가격'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "yeprice")
            result['예상체결가전일종가대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilysign")
            result['예상체결가전일종가대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "preychange"))
            result['예상체결가전일종가등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilydrate"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "optcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# KOSPI예상체결(YS3)
class YS3(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 단축코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "shcode", 단축코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        #클래스이름 = self.__class__.__name__
        #함수이름 = inspect.currentframe().f_code.co_name
        #print("ENTER : %s --> %s" %(클래스이름, 함수이름))

        try:
            result = dict()
            result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
            result['예상체결가격'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "yeprice"))
            result['예상체결수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "yevolume"))
            result['예상체결가전일종가대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilysign")
            result['예상체결가전일종가대비'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "preychange"))
            result['예상체결가전일종가등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "jnilydrate"))
            result['예상매도호가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "yofferho0"))
            result['예상매수호가'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ybidho0"))
            result['예상매도호가수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "yofferrem0"))
            result['예상매수호가수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ybidrem0"))
            result['단축코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "shcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# 지수(IJ_)
class IJ_(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 업종코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "upcode", 업종코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 업종코드):
        self.ActiveX.UnadviseRealDataWithKey(업종코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        #클래스이름 = self.__class__.__name__
        #함수이름 = inspect.currentframe().f_code.co_name
        #print("ENTER : %s --> %s" %(클래스이름, 함수이름))

        try:
            result = dict()
            result['시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "time")
            result['지수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "jisu")
            result['전일대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
            result['전일비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
            result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "drate"))
            result['체결량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
            result['거래량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
            result['거래대금'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "value"))
            result['상한종목수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "upjo"))
            result['상승종목수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "highjo"))
            result['보합종목수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "unchgjo"))
            result['하락종목수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "lowjo"))
            result['하한종목수'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "downjo"))
            result['상승종목비율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "upjrate"))
            result['시가지수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "openjisu")
            result['시가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "opentime")
            result['고가지수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "highjisu")
            result['고가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hightime")
            result['저가지수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lowjisu")
            result['저가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lowtime")
            result['외인순매수수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "frgsvolume"))
            result['기관순매수수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "orgsvolume"))
            result['외인순매수금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "frgsvalue"))
            result['기관순매수금액'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "orgsvalue"))
            result['업종코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "upcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# 업종별 투자자별 매매현황(BM_)
class BM_(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 업종코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "upcode", 업종코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 업종코드):
        self.ActiveX.UnadviseRealDataWithKey(업종코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['투자자코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode")
            result['수신시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjtime")
            #result['매수거래량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume")
            #result['매도거래량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume")
            #result['거래량순매수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol")
            #result['거래량순매수직전대비'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "p_msvol")
            #result['매수거래대금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue")
            #result['매도거래대금'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue")
            result['거래대금순매수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval")
            result['거래대금순매수직전대비'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "p_msval")
            result['업종코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "upcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e, result)

# 시간대별 투자자 매매추이(BMT)
class BMT(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 업종코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "upcode", 업종코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 업종코드):
        self.ActiveX.UnadviseRealDataWithKey(업종코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['수신시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjtime")

            result['투자자코드1(개인)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode1")
            result['매수거래량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume1"))
            result['매도거래량1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume1"))
            result['거래량순매수1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol1"))
            result['매수거래대금1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue1"))
            result['매도거래대금1'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue1"))
            result['거래대금순매수1'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval1")

            result['투자자코드2(외국인)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode2")
            result['매수거래량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume2"))
            result['매도거래량2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume2"))
            result['거래량순매수2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol2"))
            result['매수거래대금2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue2"))
            result['매도거래대금2'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue2"))
            result['거래대금순매수2'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval2")

            result['투자자코드3(기관계)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode3")
            result['매수거래량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume3"))
            result['매도거래량3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume3"))
            result['거래량순매수3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol3"))
            result['매수거래대금3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue3"))
            result['매도거래대금3'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue3"))
            result['거래대금순매수3'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval3")

            result['투자자코드4(증권)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode4")
            result['매수거래량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume4"))
            result['매도거래량4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume4"))
            result['거래량순매수4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol4"))
            result['매수거래대금4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue4"))
            result['매도거래대금4'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue4"))
            result['거래대금순매수4'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval4")

            result['투자자코드5(투신)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode5")
            result['매수거래량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume5"))
            result['매도거래량5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume5"))
            result['거래량순매수5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol5"))
            result['매수거래대금5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue5"))
            result['매도거래대금5'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue5"))
            result['거래대금순매수5'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval5")

            result['투자자코드6(은행)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode6")
            result['매수거래량6'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume6"))
            result['매도거래량6'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume6"))
            result['거래량순매수6'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol6"))
            result['매수거래대금6'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue6"))
            result['매도거래대금6'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue6"))
            result['거래대금순매수6'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval6")

            result['투자자코드7(보험)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode7")
            result['매수거래량7'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume7"))
            result['매도거래량7'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume7"))
            result['거래량순매수7'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol7"))
            result['매수거래대금7'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue7"))
            result['매도거래대금7'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue7"))
            result['거래대금순매수7'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval7")

            result['투자자코드8(종금)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode8")
            result['매수거래량8'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume8"))
            result['매도거래량8'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume8"))
            result['거래량순매수8'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol8"))
            result['매수거래대금8'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue8"))
            result['매도거래대금8'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue8"))
            result['거래대금순매수8'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval8")

            result['투자자코드9(기금)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode9")
            result['매수거래량9'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume9"))
            result['매도거래량9'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume9"))
            result['거래량순매수9'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol9"))
            result['매수거래대금9'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue9"))
            result['매도거래대금9'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue9"))
            result['거래대금순매수9'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval9")

            result['투자자코드10(선물업자)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode10")
            result['매수거래량10'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume10"))
            result['매도거래량10'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume10"))
            result['거래량순매수10'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol10"))
            result['매수거래대금10'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue10"))
            result['매도거래대금10'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue10"))
            result['거래대금순매수10'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval10")

            result['투자자코드11(기타)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode11")
            result['매수거래량11'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume11"))
            result['매도거래량11'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume11"))
            result['거래량순매수11'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol11"))
            result['매수거래대금11'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue11"))
            result['매도거래대금11'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue11"))
            result['거래대금순매수11'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval11")

            result['투자자코드0(사모펀드)'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tjjcode0")
            result['매수거래량0'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume0"))
            result['매도거래량0'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume0"))
            result['거래량순매수0'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvol0"))
            result['매수거래대금0'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "msvalue0"))
            result['매도거래대금0'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvalue0"))
            result['거래대금순매수0'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msval0")

            result['업종코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "upcode")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e, result)

        # print(" EXIT : %s --> %s" % (클래스이름, 함수이름))

# KOSPI프로그램매매전체집계(PM_)
class PM_(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 구분값='0'):
        self.ActiveX.SetFieldData(self.INBLOCK, "gubun", 구분값)
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):

        try:
            result = dict()
            result['수신시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "time")
            #result['전체매도체결금액합계'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tdvalue")
            #result['전체매수체결금액합계'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tsvalue")
            result['전체순매수금액합계'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "tval")
            result['전체순매수금액직전대비'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "p_tvalcha")
            result['구분값'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "gubun")
            result['szTrCode'] = szTrCode

            if self.parent != None:
                self.parent.OnReceiveRealData(result)

        except Exception as e:
            클래스이름 = self.__class__.__name__
            함수이름 = inspect.currentframe().f_code.co_name
            print("%s-%s " % (클래스이름, 함수이름), e)

##----------------------------------------------------------------------------------------------------------------------
# 해외선물

# 해외선물 현재가체결(OVC)
class OVC(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 종목코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "symbol", 종목코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 종목코드):
        self.ActiveX.UnadviseRealDataWithKey(종목코드)
        print('종목코드 =', 종목코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['종목코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "symbol")
        result['체결일자_현지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ovsdate")
        result['체결일자_한국'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "kordate")
        result['체결시간_현지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trdtm")
        result['체결시간_한국'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "kortm")
        result['체결가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "curpr"))
        result['전일대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "ydiffpr"))
        result['전일대비기호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ydiffSign")
        result['시가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "open"))
        result['고가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "high"))
        result['저가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "low"))
        result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "chgrate"))
        result['건별체결수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "trdq"))
        result['누적체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totq")
        result['체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cgubun")
        result['매도누적체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume")
        result['매수누적체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume")
        result['장마감일'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ovsmkend")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 해외선물 호가(OVH)
class OVH(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 종목코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "symbol", 종목코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 종목코드):
        self.ActiveX.UnadviseRealDataWithKey(종목코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['종목코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "symbol")
        result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
        매도호가 = []
        매수호가 = []
        매도호가잔량 = []
        매수호가잔량 = []
        매도호가건수 = []
        매수호가건수 = []
        for i in range(1,6):
            매도호가.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho%s" % i))
            매수호가.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho%s" % i))
            매도호가잔량.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem%s" % i))
            매수호가잔량.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem%s" % i))
            매도호가건수.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerno%s" % i))
            매수호가건수.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidno%s" % i))

        result['매도호가'] = 매도호가
        result['매수호가'] = 매수호가
        result['매도호가잔량'] = 매도호가잔량
        result['매수호가잔량'] = 매수호가잔량
        result['매도호가건수'] = 매도호가건수
        result['매수호가건수'] = 매수호가건수

        result['매도호가총건수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totoffercnt")
        result['매수호가총건수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidcnt")
        result['매도호가총수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totofferrem")
        result['매수호가총수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidrem")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 해외선물주문
class TC1(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['라인일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lineseq")
        result['KEY'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "key")
        result['조작자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "user")
        result['서비스ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "svc_id")
        result['주문일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_dt")
        result['지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "brn_cd")
        result['주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_no"))
        result['원주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "orgn_ordr_no"))
        result['모주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mthr_ordr_no"))
        result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ac_no")
        result['종목코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "is_cd")
        result['매도매수유형'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "s_b_ccd")
        result['정정취소유형'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_ccd")
        result['주문유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_typ_cd")
        result['주문기간코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_typ_prd_ccd")
        result['주문적용시작일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_aplc_strt_dt")
        result['주문적용종료일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_aplc_end_dt")
        result['주문가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_prc"))
        result['주문조건가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cndt_ordr_prc"))
        result['주문수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_q"))
        result['주문시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_tm")
        result['사용자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "userid")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 해외선물응답
class TC2(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['라인일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lineseq")
        result['KEY'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "key")
        result['조작자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "user")
        result['서비스ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "svc_id")
        result['주문일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_dt")
        result['지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "brn_cd")
        result['주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_no"))
        result['원주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "orgn_ordr_no"))
        result['모주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mthr_ordr_no"))
        result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ac_no")
        result['종목코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "is_cd")
        result['매도매수유형'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "s_b_ccd")
        result['정정취소유형'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_ccd")
        result['주문유형코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_typ_cd")
        result['주문기간코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_typ_prd_ccd")
        result['주문적용시작일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_aplc_strt_dt")
        result['주문적용종료일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_aplc_end_dt")
        result['주문가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_prc"))
        result['주문조건가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cndt_ordr_prc"))
        result['주문수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_q"))
        result['주문시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_tm")
        result['호가확인수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "cnfr_q"))
        result['호가거부사유코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "rfsl_cd")
        result['호가거부사유코드명'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "text")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 해외선물체결
class TC3(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['라인일련번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "lineseq")
        result['KEY'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "key")
        result['조작자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "user")
        result['서비스ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "svc_id")
        result['주문일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_dt")
        result['지점번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "brn_cd")
        result['주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_no"))
        result['원주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "orgn_ordr_no"))
        result['모주문번호'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "mthr_ordr_no"))
        result['계좌번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ac_no")
        result['종목코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "is_cd")
        result['매도매수유형'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "s_b_ccd")
        result['정정취소유형'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ordr_ccd")
        result['체결수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "ccls_q"))
        result['체결가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "ccls_prc"))
        result['체결번호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ccls_no")
        result['체결시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ccls_tm")
        result['매입평균단가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "avg_byng_uprc"))
        result['매입금액'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "byug_amt"))
        result['청산손익'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "clr_pl_amt"))
        result['위탁수수료'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "ent_fee"))
        result['FCM수수료'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "fcm_fee"))
        result['사용자ID'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "userid")
        result['현재가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "now_prc"))
        result['통화코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "crncy_cd")
        result['만기일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mtrt_dt")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 해외옵션 현재가체결(WOC)
class WOC(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 종목코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "symbol", 종목코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 종목코드):
        self.ActiveX.UnadviseRealDataWithKey(종목코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['종목코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "symbol")
        result['체결일자_현지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ovsdate")
        result['체결일자_한국'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "kordate")
        result['체결시간_현지'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "trdtm")
        result['체결시간_한국'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "kortm")
        result['체결가격'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "curpr"))
        result['전일대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "ydiffpr"))
        result['전일대비기호'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ydiffSign")
        result['시가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "open"))
        result['고가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "high"))
        result['저가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "low"))
        result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "chgrate"))
        result['건별체결수량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "trdq"))
        result['누적체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totq")
        result['체결구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "cgubun")
        result['매도누적체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "mdvolume")
        result['매수누적체결수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "msvolume")
        result['장마감일'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "ovsmkend")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# 해외옵션 호가(WOH)
class WOH(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 종목코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "symbol", 종목코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 종목코드):
        self.ActiveX.UnadviseRealDataWithKey(종목코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['종목코드'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "symbol")
        result['호가시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "hotime")
        매도호가 = []
        매수호가 = []
        매도호가잔량 = []
        매수호가잔량 = []
        매도호가건수 = []
        매수호가건수 = []
        for i in range(1,6):
            매도호가.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho%s" % i))
            매수호가.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho%s" % i))
            매도호가잔량.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem%s" % i))
            매수호가잔량.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem%s" % i))
            매도호가건수.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerno%s" % i))
            매수호가건수.append(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidno%s" % i))

        result['매도호가'] = 매도호가
        result['매수호가'] = 매수호가
        result['매도호가잔량'] = 매도호가잔량
        result['매수호가잔량'] = 매수호가잔량
        result['매도호가건수'] = 매도호가건수
        result['매수호가건수'] = 매수호가건수

        result['매도호가총건수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totoffercnt")
        result['매수호가총건수'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidcnt")
        result['매도호가총수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totofferrem")
        result['매수호가총수량'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "totbidrem")
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)


# US지수(MK2) : 수급파악 용도로사용
class MK2(XAReal):
    def __init__(self, parent=None, 식별자='식별자'):
        super(__class__,self).__init__(parent=parent,식별자=식별자)
        self.ActiveX.LoadFromResFile(self.RESFILE)

    def AdviseRealData(self, 심볼코드):
        self.ActiveX.SetFieldData(self.INBLOCK, "symbol", 심볼코드)
        self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, 심볼코드):
        self.ActiveX.UnadviseRealDataWithKey(심볼코드)

    def UnadviseRealData(self):
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = dict()
        result['일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "date")
        result['시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "time")
        result['한국일자'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "kodate")
        result['한국시간'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "kotime")
        result['시가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "open"))
        result['고가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "high"))
        result['저가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "low"))
        result['현재가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "price"))
        result['전일대비구분'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "sign")
        result['전일대비'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "change"))
        result['등락율'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "uprate"))
        result['매수호가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidho"))
        result['매수잔량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "bidrem"))
        result['매도호가'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerho"))
        result['매도잔량'] = int(self.ActiveX.GetFieldData(self.OUTBLOCK, "offerrem"))
        result['누적거래량'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "volume"))
        result['심볼'] = self.ActiveX.GetFieldData(self.OUTBLOCK, "xsymbol")
        result['체결거래량'] = float(self.ActiveX.GetFieldData(self.OUTBLOCK, "cvolume"))
        result['szTrCode'] = szTrCode

        if self.parent != None:
            self.parent.OnReceiveRealData(result)
