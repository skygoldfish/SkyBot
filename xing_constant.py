from enum import Enum

from xing_config import *

class DataType(Enum):

    JIF_TICK = 1
    IJ_TICK = 2

    KOSPI_QUOTE = 3
    KOSPI_TICK = 4

    KOSDAQ_QUOTE = 5
    KOSDAQ_TICK = 6

    INDEX_FUTURES_QUOTE = 7
    INDEX_FUTURES_TICK = 8

    INDEX_OPTION_QUOTE = 9
    INDEX_OPTION_TICK = 10
    
    BM_TICK = 11
    PM_TICK = 12
    OVC_TICK = 13
    NWS_TICK = 14

    YJ_TICK = 15
    YFC_TICK = 16
    YOC_TICK = 17
    S3_TICK = 18

# 장운영정보
JIF_FIELDS = ["jangubun", "jstatus"]
JIF_COLUMNS = ["system_time", "tr_code", *JIF_FIELDS]
JIF_COLUMNS_HEADER = ["system_time", "tr_code", "장구분", "장상태"]

# 지수
IJ_FIELDS = ["time", "jisu", "sign", "change", "drate", "cvolume", 
    "volume", "value", "upjo", "highjo", "unchgjo", "lowjo", "downjo", 
    "upjrate", "openjisu", "opentime", "highjisu", "hightime", "lowjisu",
    "lowtime", "frgsvolume", "orgsvolume", "frgsvalue", "orgsvalue", "upcode"]
IJ_COLUMNS = ["system_time", "tr_code", *IJ_FIELDS]
IJ_COLUMNS_HEADER = ["system_time", "tr_code", "수신시간", "지수", "전일대비구분", "전일비", "등락율", "체결량", 
    "거래량", "거래대금", "상한종목수", "상승종목수", "보합종목수", "하락종목수", "하한종목수", 
    "상승종목비율", "시가지수", "시가시간", "고가지수", "고가시간", "저가지수",
    "저가시간", "외인순매수수량", "기관순매수수량", "외인순매수금액", "기관순매수금액", "업종코드"]

# 체결
TICK_FIELDS = [    
    "chetime",
    "sign",
    "change",
    "drate",
    "price",
    "opentime",
    "open",
    "hightime",
    "high",
    "lowtime",
    "low",
    "cgubun",
    "cvolume",
    "volume",
    "value",
    "mdvolume",
    "mdchecnt",
    "msvolume",
    "mschecnt",
    "cpower",
    "w_avrg",
    "offerho",
    "bidho",
    "status",
    "jnilvolume",
    "shcode",
]
TICK_COLUMNS = [
    "system_time",
    "tr_code",
    *TICK_FIELDS
]
TICK_COLUMNS_HEADER = [
    "system_time",
    "tr_code",    
    "수신시간",
    "전일대비구분",
    "전일대비",
    "등락율",
    "현재가",
    "시가시간",
    "시가",
    "고가시간",
    "고가",
    "저가시간",
    "저가",
    "체결구분",
    "체결량",
    "누적거래량",
    "누적거래대금",
    "매도누적체결량",
    "매도누적체결건수",
    "매수누적체결량",
    "매수누적체결건수",
    "체결강도",
    "가중평균가",
    "매도호가",
    "매수호가",
    "장정보",
    "전일동시간대거래량",
    "단축코드",
]

# 호가
QUOTE_FIELDS = [
    "shcode", "hotime", "donsigubun", "totofferrem", "totbidrem",
    "offerho1", "bidho1", "offerrem1", "bidrem1",
    "offerho2", "bidho2", "offerrem2", "bidrem2",
    "offerho3", "bidho3", "offerrem3", "bidrem3",
    "offerho4", "bidho4", "offerrem4", "bidrem4",
    "offerho5", "bidho5", "offerrem5", "bidrem5",
    "offerho6", "bidho6", "offerrem6", "bidrem6",
    "offerho7", "bidho7", "offerrem7", "bidrem7",
    "offerho8", "bidho8", "offerrem8", "bidrem8",
    "offerho9", "bidho9", "offerrem9", "bidrem9",
    "offerho10", "bidho10", "offerrem10", "bidrem10",
]
QUOTE_COLUMNS = [
    "system_time",
    "tr_code",
    *QUOTE_FIELDS
]
QUOTE_COLUMNS_HEADER = [
    "system_time", "tr_code", "shcode", "hotime", "donsigubun", "totofferrem", "totbidrem",
    "offerho1", "bidho1", "offerrem1", "bidrem1",
    "offerho2", "bidho2", "offerrem2", "bidrem2",
    "offerho3", "bidho3", "offerrem3", "bidrem3",
    "offerho4", "bidho4", "offerrem4", "bidrem4",
    "offerho5", "bidho5", "offerrem5", "bidrem5",
    "offerho6", "bidho6", "offerrem6", "bidrem6",
    "offerho7", "bidho7", "offerrem7", "bidrem7",
    "offerho8", "bidho8", "offerrem8", "bidrem8",
    "offerho9", "bidho9", "offerrem9", "bidrem9",
    "offerho10", "bidho10", "offerrem10", "bidrem10",
]

# 지수선물 체결
INDEX_FUTURES_TICK_FIELDS = [    
    "chetime",       # 체결시간
    "sign",          # 대비기호
    "change",        # 전일대비
    "drate",         # 등락율
    "price",         # 현재가
    "open",          # 시가
    "high",          # 고가
    "low",           # 저가
    "cgubun",        # 체결구분
    "cvolume",       # 체결량
    "volume",        # 누적거래량
    "value",         # 누적거래대금
    "mdvolume",      # 매도누적체결량
    "mdchecnt",      # 매도누적체결건수
    "msvolume",      # 매수누적체결량
    "mschecnt",      # 매수누적체결건수
    "cpower",        # 체결강도
    "offerho1",      # 매도호가1
    "bidho1",        # 매수호가1
    "openyak",       # 미결제약정수량
    "k200jisu",      # KOSPI200지수
    "theoryprice",   # 이론가
    "kasis",         # 괴리율
    "sbasis",        # 시장BASIS
    "ibasis",        # 이론BASIS
    "openyakcha",    # 미결제약정증감
    "jgubun",        # 장운영정보
    "jnilvolume",    # 전일동시간대거래량
    "futcode",       # 단축코드
]
INDEX_FUTURES_TICK_COLUMNS = [
    "system_time",
    "tr_code",
    *INDEX_FUTURES_TICK_FIELDS
]
INDEX_FUTURES_TICK_COLUMNS_HEADER = [ 
    "system_time",
    "tr_code",   
    "수신시간",       # 체결시간
    "대비기호",          # 대비기호
    "전일대비",        # 전일대비
    "등락율",         # 등락율
    "현재가",         # 현재가
    "시가",          # 시가
    "고가",          # 고가
    "저가",           # 저가
    "체결구분",        # 체결구분
    "체결량",       # 체결량
    "누적거래량",        # 누적거래량
    "누적거래대금",         # 누적거래대금
    "매도누적체결량",      # 매도누적체결량
    "매도누적체결건수",      # 매도누적체결건수
    "매수누적체결량",      # 매수누적체결량
    "매수누적체결건수",      # 매수누적체결건수
    "체결강도",        # 체결강도
    "매도호가1",      # 매도호가1
    "매수호가1",        # 매수호가1
    "미결제약정수량",       # 미결제약정수량
    "KOSPI200지수",      # KOSPI200지수
    "이론가",   # 이론가
    "괴리율",         # 괴리율
    "시장BASIS",        # 시장BASIS
    "이론BASIS",        # 이론BASIS
    "미결제약정증감",    # 미결제약정증감
    "장운영정보",        # 장운영정보
    "전일동시간대거래량",    # 전일동시간대거래량
    "단축코드",       # 단축코드
]

# 지수선물 호가
INDEX_FUTURES_QUOTE_FIELDS = [
    
    "hotime",         # 호가시간
    "offerho1",       # 매도호가1
    "bidho1",         # 매수호가1
    "offerrem1",      # 매도호가수량1
    "bidrem1",        # 매수호가수량1
    "offercnt1",      # 매도호가건수1
    "bidcnt1",        # 매수호가건수1
    "offerho2",       # 매도호가2
    "bidho2",         # 매수호가2
    "offerrem2",      # 매도호가수량2
    "bidrem2",        # 매수호가수량2
    "offercnt2",      # 매도호가건수2
    "bidcnt2",        # 매수호가건수2
    "offerho3",       # 매도호가3
    "bidho3",         # 매수호가3
    "offerrem3",      # 매도호가수량3
    "bidrem3",        # 매수호가수량3
    "offercnt3",      # 매도호가건수3
    "bidcnt3",        # 매수호가건수3
    "offerho4",       # 매도호가4
    "bidho4",         # 매수호가4
    "offerrem4",      # 매도호가수량4
    "bidrem4",        # 매수호가수량4
    "offercnt4",      # 매도호가건수4
    "bidcnt4",        # 매수호가건수4
    "offerho5",       # 매도호가5
    "bidho5",         # 매수호가5
    "offerrem5",      # 매도호가수량5
    "bidrem5",        # 매수호가수량5
    "offercnt5",      # 매도호가건수5
    "bidcnt5",        # 매수호가건수5
    "totofferrem",    # 매도호가총수량
    "totbidrem",      # 매수호가총수량
    "totoffercnt",    # 매도호가총건수
    "totbidcnt",      # 매수호가총건수
    "futcode",        # 단축코드
    "danhochk",       # 단일가호가여부
    "alloc_gubun",    # 배분적용구분
]
INDEX_FUTURES_QUOTE_COLUMNS = [
    "system_time",
    "tr_code",
    *INDEX_FUTURES_QUOTE_FIELDS
]
INDEX_FUTURES_QUOTE_COLUMNS_HEADER = [
    "system_time",
    "tr_code",    
    "수신시간",         # 호가시간
    "매도호가1",       # 매도호가1
    "매수호가1",         # 매수호가1
    "매도호가수량1",      # 매도호가수량1
    "매수호가수량1",        # 매수호가수량1
    "매도호가건수1",      # 매도호가건수1
    "매수호가건수1",        # 매수호가건수1
    "매도호가2",       # 매도호가2
    "매수호가2",         # 매수호가2
    "매도호가수량2",      # 매도호가수량2
    "매수호가수량2",        # 매수호가수량2
    "매도호가건수2",      # 매도호가건수2
    "매수호가건수2",        # 매수호가건수2
    "매도호가3",       # 매도호가3
    "매수호가3",         # 매수호가3
    "매도호가수량3",      # 매도호가수량3
    "매수호가수량3",        # 매수호가수량3
    "매도호가건수3",      # 매도호가건수3
    "매수호가건수3",        # 매수호가건수3
    "매도호가4",       # 매도호가4
    "매수호가4",         # 매수호가4
    "매도호가수량4",      # 매도호가수량4
    "매수호가수량4",        # 매수호가수량4
    "매도호가건수4",      # 매도호가건수4
    "매수호가건수4",        # 매수호가건수4
    "매도호가5",       # 매도호가5
    "매수호가5",         # 매수호가5
    "매도호가수량5",      # 매도호가수량5
    "매수호가수량5",        # 매수호가수량5
    "매도호가건수5",      # 매도호가건수5
    "매수호가건수5",        # 매수호가건수5
    "매도호가총수량",    # 매도호가총수량
    "매수호가총수량",      # 매수호가총수량
    "매도호가총건수",    # 매도호가총건수
    "매수호가총건수",      # 매수호가총건수
    "단축코드",        # 단축코드
    "단일가호가여부",       # 단일가호가여부
    "배분적용구분",    # 배분적용구분
]

# 지수옵션 체결
INDEX_OPTION_TICK_FIELDS = [    
    "chetime",       # 체결시간
    "sign",          # 전일대비구분
    "change",        # 전일대비
    "drate",         # 등락율
    "price",         # 현재가
    "open",          # 시가
    "high",          # 고가
    "low",           # 저가
    "cgubun",        # 체결구분
    "cvolume",       # 체결량
    "volume",        # 누적거래량
    "value",         # 누적거래대금
    "mdvolume",      # 매도누적체결량
    "mdchecnt",      # 매도누적체결건수
    "msvolume",      # 매수누적체결량
    "mschecnt",      # 매수누적체결건수
    "cpower",        # 체결강도
    "offerho1",      # 매도호가1
    "bidho1",        # 매수호가1
    "openyak",       # 미결제약정수량
    "k200jisu",      # KOSPI200지수
    "eqva",          # KOSPI등가
    "theoryprice",   # 이론가
    "impv",          # 내재변동성
    "openyakcha",    # 미결제약정증감
    "timevalue",     # 시간가치
    "jgubun",        # 장운영정보
    "jnilvolume",    # 전일동시간대거래량
    "optcode",       # 단축코드
]
INDEX_OPTION_TICK_COLUMNS = [
    "system_time",
    "tr_code",
    *INDEX_OPTION_TICK_FIELDS
]
INDEX_OPTION_TICK_COLUMNS_HEADER = [    
    "system_time",
    "tr_code",
    "수신시간",       # 체결시간
    "전일대비구분",          # 전일대비구분
    "전일대비",        # 전일대비
    "등락율",         # 등락율
    "현재가",         # 현재가
    "시가",          # 시가
    "고가",          # 고가
    "저가",           # 저가
    "체결구분",        # 체결구분
    "체결량",       # 체결량
    "누적거래량",        # 누적거래량
    "누적거래대금",         # 누적거래대금
    "매도누적체결량",      # 매도누적체결량
    "매도누적체결건수",      # 매도누적체결건수
    "매수누적체결량",      # 매수누적체결량
    "매수누적체결건수",      # 매수누적체결건수
    "체결강도",        # 체결강도
    "매도호가1",      # 매도호가1
    "매수호가1",        # 매수호가1
    "미결제약정수량",       # 미결제약정수량
    "KOSPI200지수",      # KOSPI200지수
    "KOSPI등가",          # KOSPI등가
    "이론가",   # 이론가
    "내재변동성",          # 내재변동성
    "미결제약정증감",    # 미결제약정증감
    "시간가치",     # 시간가치
    "장운영정보",        # 장운영정보
    "전일동시간대거래량",    # 전일동시간대거래량
    "단축코드",       # 단축코드
]

# 지수옵션 호가
if NightTime:
    INDEX_OPTION_QUOTE_FIELDS = [    
        "hotime",         # 호가시간(24시간)
        "hotime1",        # 호가시간(36시간)
        "offerho1",       # 매도호가1
        "bidho1",         # 매수호가1
        "offerrem1",      # 매도호가수량1
        "bidrem1",        # 매수호가수량1
        "offercnt1",      # 매도호가건수1
        "bidcnt1",        # 매수호가건수1
        "offerho2",       # 매도호가2
        "bidho2",         # 매수호가2
        "offerrem2",      # 매도호가수량2
        "bidrem2",        # 매수호가수량2
        "offercnt2",      # 매도호가건수2
        "bidcnt2",        # 매수호가건수2
        "offerho3",       # 매도호가3
        "bidho3",         # 매수호가3
        "offerrem3",      # 매도호가수량3
        "bidrem3",        # 매수호가수량3
        "offercnt3",      # 매도호가건수3
        "bidcnt3",        # 매수호가건수3
        "offerho4",       # 매도호가4
        "bidho4",         # 매수호가4
        "offerrem4",      # 매도호가수량4
        "bidrem4",        # 매수호가수량4
        "offercnt4",      # 매도호가건수4
        "bidcnt4",        # 매수호가건수4
        "offerho5",       # 매도호가5
        "bidho5",         # 매수호가5
        "offerrem5",      # 매도호가수량5
        "bidrem5",        # 매수호가수량5
        "offercnt5",      # 매도호가건수5
        "bidcnt5",        # 매수호가건수5
        "totofferrem",    # 매도호가총수량
        "totbidrem",      # 매수호가총수량
        "totoffercnt",    # 매도호가총건수
        "totbidcnt",      # 매수호가총건수
        "optcode",        # 단축코드
        "danhochk",       # 단일가호가여부
    ]
    INDEX_OPTION_QUOTE_COLUMNS_HEADER = [
        "system_time",
        "tr_code",
        "호가시간(24시간)",         # 호가시간(24시간)
        "수신시간",        # 호가시간(36시간)
        "매도호가1",       # 매도호가1
        "매수호가1",         # 매수호가1
        "매도호가수량1",      # 매도호가수량1
        "매수호가수량1",        # 매수호가수량1
        "매도호가건수1",      # 매도호가건수1
        "매수호가건수1",        # 매수호가건수1
        "매도호가2",       # 매도호가2
        "매수호가2",         # 매수호가2
        "매도호가수량2",      # 매도호가수량2
        "매수호가수량2",        # 매수호가수량2
        "매도호가건수2",      # 매도호가건수2
        "매수호가건수2",        # 매수호가건수2
        "매도호가3",       # 매도호가3
        "매수호가3",         # 매수호가3
        "매도호가수량3",      # 매도호가수량3
        "매수호가수량3",        # 매수호가수량3
        "매도호가건수3",      # 매도호가건수3
        "매수호가건수3",        # 매수호가건수3
        "매도호가4",       # 매도호가4
        "매수호가4",         # 매수호가4
        "매도호가수량4",      # 매도호가수량4
        "매수호가수량4",        # 매수호가수량4
        "매도호가건수4",      # 매도호가건수4
        "매수호가건수4",        # 매수호가건수4
        "매도호가5",       # 매도호가5
        "매수호가5",         # 매수호가5
        "매도호가수량5",      # 매도호가수량5
        "매수호가수량5",        # 매수호가수량5
        "매도호가건수5",      # 매도호가건수5
        "매수호가건수5",        # 매수호가건수5
        "매도호가총수량",    # 매도호가총수량
        "매수호가총수량",      # 매수호가총수량
        "매도호가총건수",    # 매도호가총건수
        "매수호가총건수",      # 매수호가총건수
        "단축코드",        # 단축코드
        "단일가호가여부",       # 단일가호가여부
    ]
else:
    INDEX_OPTION_QUOTE_FIELDS = [
    
        "hotime",         # 호가시간
        "offerho1",       # 매도호가1
        "bidho1",         # 매수호가1
        "offerrem1",      # 매도호가수량1
        "bidrem1",        # 매수호가수량1
        "offercnt1",      # 매도호가건수1
        "bidcnt1",        # 매수호가건수1
        "offerho2",       # 매도호가2
        "bidho2",         # 매수호가2
        "offerrem2",      # 매도호가수량2
        "bidrem2",        # 매수호가수량2
        "offercnt2",      # 매도호가건수2
        "bidcnt2",        # 매수호가건수2
        "offerho3",       # 매도호가3
        "bidho3",         # 매수호가3
        "offerrem3",      # 매도호가수량3
        "bidrem3",        # 매수호가수량3
        "offercnt3",      # 매도호가건수3
        "bidcnt3",        # 매수호가건수3
        "offerho4",       # 매도호가4
        "bidho4",         # 매수호가4
        "offerrem4",      # 매도호가수량4
        "bidrem4",        # 매수호가수량4
        "offercnt4",      # 매도호가건수4
        "bidcnt4",        # 매수호가건수4
        "offerho5",       # 매도호가5
        "bidho5",         # 매수호가5
        "offerrem5",      # 매도호가수량5
        "bidrem5",        # 매수호가수량5
        "offercnt5",      # 매도호가건수5
        "bidcnt5",        # 매수호가건수5
        "totofferrem",    # 매도호가총수량
        "totbidrem",      # 매수호가총수량
        "totoffercnt",    # 매도호가총건수
        "totbidcnt",      # 매수호가총건수
        "optcode",        # 단축코드
        "danhochk",       # 단일가호가여부
        "alloc_gubun",    # 배분적용구분
    ]
    INDEX_OPTION_QUOTE_COLUMNS_HEADER = [
        "system_time",
        "tr_code",
        "수신시간",         # 호가시간(24시간)
        "매도호가1",       # 매도호가1
        "매수호가1",         # 매수호가1
        "매도호가수량1",      # 매도호가수량1
        "매수호가수량1",        # 매수호가수량1
        "매도호가건수1",      # 매도호가건수1
        "매수호가건수1",        # 매수호가건수1
        "매도호가2",       # 매도호가2
        "매수호가2",         # 매수호가2
        "매도호가수량2",      # 매도호가수량2
        "매수호가수량2",        # 매수호가수량2
        "매도호가건수2",      # 매도호가건수2
        "매수호가건수2",        # 매수호가건수2
        "매도호가3",       # 매도호가3
        "매수호가3",         # 매수호가3
        "매도호가수량3",      # 매도호가수량3
        "매수호가수량3",        # 매수호가수량3
        "매도호가건수3",      # 매도호가건수3
        "매수호가건수3",        # 매수호가건수3
        "매도호가4",       # 매도호가4
        "매수호가4",         # 매수호가4
        "매도호가수량4",      # 매도호가수량4
        "매수호가수량4",        # 매수호가수량4
        "매도호가건수4",      # 매도호가건수4
        "매수호가건수4",        # 매수호가건수4
        "매도호가5",       # 매도호가5
        "매수호가5",         # 매수호가5
        "매도호가수량5",      # 매도호가수량5
        "매수호가수량5",        # 매수호가수량5
        "매도호가건수5",      # 매도호가건수5
        "매수호가건수5",        # 매수호가건수5
        "매도호가총수량",    # 매도호가총수량
        "매수호가총수량",      # 매수호가총수량
        "매도호가총건수",    # 매도호가총건수
        "매수호가총건수",      # 매수호가총건수
        "단축코드",        # 단축코드
        "단일가호가여부",       # 단일가호가여부
        "배분적용구분",    # 배분적용구분
    ]

INDEX_OPTION_QUOTE_COLUMNS = [
    "system_time",
    "tr_code",
    *INDEX_OPTION_QUOTE_FIELDS
]

# 업종별 투자자별 매매현황
BM_FIELDS = ["tjjcode", "tjjtime", "msvolume", "mdvolume", "msvol", "p_msvol", "msvalue", "mdvalue", "msval", "p_msval", "upcode"]
BM_COLUMNS = ["system_time", "tr_code", *BM_FIELDS]
BM_COLUMNS_HEADER = ["system_time", "tr_code", "투자자코드", "수신시간", "매수거래량", "매도거래량", "거래량순매수", "거래량순매수직전대비", 
    "매수거래대금", "매도거래대금", "거래대금순매수", "거래대금순매수직전대비", "업종코드"]

# KOSPI 프로그램매매 전체집계
PM_FIELDS = ["time", "tdvalue", "tsvalue", "tval", "p_tvalcha", "gubun"]
PM_COLUMNS = ["system_time", "tr_code", *PM_FIELDS]
PM_COLUMNS_HEADER = ["system_time", "tr_code", "수신시간", "전체매도체결금액합계", "전체매수체결금액합계", "전체순매수금액합계", "전체순매수금액직전대비", "구분값"]

# 해외선물 체결
OVC_FIELDS = ["symbol", "ovsdate", "kordate", "trdtm", "kortm", "curpr", "ydiffpr", "ydiffSign", "open", "high", "low", "chgrate", "trdq", "totq", 
    "cgubun", "mdvolume", "msvolume", "ovsmkend"]
OVC_COLUMNS = ["system_time", "tr_code", *OVC_FIELDS]
OVC_COLUMNS_HEADER = ["system_time", "tr_code", "종목코드", "체결일자_현지", "체결일자_한국", "체결시간_현지", "수신시간", "체결가격", 
    "전일대비", "전일대비기호", "시가", "고가", "저가", "등락율", "건별체결수량", "누적체결수량", 
    "체결구분", "매도누적체결수량", "매수누적체결수량", "장마감일"]

# 실시간 뉴스
NWS_FIELDS = ["date", "time", "id", "realkey", "title", "code", "bodysize"]
NWS_COLUMNS = ["system_time", "tr_code", *NWS_FIELDS]
NWS_COLUMNS_HEADER = ["system_time", "tr_code", "날짜", "수신시간", "뉴스구분자", "키값", "제목", "단축종목코드", "BODY길이"]

# 예상지수
YJ_FIELDS = ["time", "jisu", "sign", "change", "drate", "cvolume", "volume", "value", "upcode"]
YJ_COLUMNS = ["system_time", "tr_code", *YJ_FIELDS]
YJ_COLUMNS_HEADER = ["system_time", "tr_code", "수신시간", "예상지수", "예상전일대비구분", "예상전일비", "예상등락율", "예상체결량", "누적거래량", "예상거래대금", "업종코드"]

# 지수선물 예상체결
YFC_FIELDS = ["ychetime", "yeprice", "jnilysign", "preychange", "jnilydrate", "futcode"]
YFC_COLUMNS = ["system_time", "tr_code", *YFC_FIELDS]
YFC_COLUMNS_HEADER = ["system_time", "tr_code", "수신시간", "예상체결가격", "예상체결가전일종가대비구분", "예상체결가전일종가대비", "예상체결가전일종가등락율", "단축코드"]

# 지수옵션 예상체결
YOC_FIELDS = ["ychetime", "yeprice", "jnilysign", "preychange", "jnilydrate", "optcode"]
YOC_COLUMNS = ["system_time", "tr_code", *YOC_FIELDS]
YOC_COLUMNS_HEADER = ["system_time", "tr_code", "수신시간", "예상체결가격", "예상체결가전일종가대비구분", "예상체결가전일종가대비", "예상체결가전일종가등락율", "단축코드"]

# 지수옵션 예상체결

# KOSPI체결
S3_FIELDS = ["chetime", "sign", "change", "drate", "price", "opentime", "open", "hightime", "high", "lowtime", "low", "cgubun", "cvolume", "volume", "value", "mdvolume", \
    "mdchecnt", "msvolume", "mschecnt", "cpower", "w_avrg", "offerho", "bidho", "status", "jnilvolume", "shcode"]
S3_COLUMNS = ["system_time", "tr_code", *S3_FIELDS]
S3_COLUMNS_HEADER = ["system_time", "tr_code", "수신시간", "전일대비구분", "전일대비", "등락율", "현재가", "시가시간", "시가", "고가시간", "고가", "저가시간", "저가", "체결구분", \
    "체결량", "누적거래량", "누적거래대금", "매도누적체결량", "매도누적체결건수", "매수누적체결량", "매수누적체결건수", "체결강도", "가중평균가", "매도호가", "매수호가", "장정보", "전일동시간대거래량", "단축코드"]

