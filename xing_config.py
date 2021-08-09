from datetime import datetime
from configparser import ConfigParser

# Configuration Parser
parser = ConfigParser()
parser.read('.\skybot.ini')

NightTime_PreStart_Hour = parser.getint('Initial Value', 'NightTime Pre-Start Hour')

#RES_FOLDER_PATH = "C:/eBEST/xingAPI/Res"  # xing_tick_crawler Res 파일 폴더 위치
RES_FOLDER_PATH = "./Res"  # xing_tick_crawler Res 파일 폴더 위치
TICKER_DATA_FOLDER_PATH = "."  # tick 데이터 저장할 위치

dt = datetime.now()

# 오전 6시 ~ 7시는 Break Time
if 7 <= dt.hour < NightTime_PreStart_Hour:
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

