from datetime import datetime

REAL_SERVER = False

if REAL_SERVER:
    config = {"id": "goldrune", "password": "sky1037045", "cert_password": "sky@1037045"}
else:
    config = {"id": "goldrune", "password": "sky0000", "cert_password": "0"}

RES_FOLDER_PATH = "C:/eBEST/xingAPI/Res"  # xing_tick_crawler Res 파일 폴더 위치
TICKER_DATA_FOLDER_PATH = "."  # tick 데이터 저장할 위치

dt = datetime.now()

# 오전 6시 ~ 7시는 Break Time
if 7 <= dt.hour < 16:
    # 오전 7시 ~ 오후 3시 59분
    DayTime = True
    NightTime = False
else:
    # 오후 4시 ~ 익일 오전 5시 59분
    DayTime = False
    NightTime = True

BUNDLE_BY_MARKET = True
"""
bundle_by_market: True, 시장별 파일
                  False, 종목별 파일
"""

KOSPI = '001'
KOSPI200 = '101'
KOSDAQ = '301'
FUTURES = '900'

SAMSUNG = '005930'
HYUNDAI = '005380'

SP500 = 'ESH21'
DOW = 'YMH21'
NASDAQ = 'NQH21'
WTI = 'CLH21'
EUROFX = 'UROH21'
HANGSENG = 'HSIZ20'
GOLD = 'GCG21'
