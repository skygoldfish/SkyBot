# -*- coding: utf-8 -*-

프로그램정보 = [
    ['프로그램명','SkyBot-eBEST'],
    ['Version','1.4'],
    ['개발일','2018-02-28'],
    ['2018-06-04','포트폴리오 더블클릭으로 삭제 기능 추가'],
    ['2018-05-23','시장가매도, query->ActiveX 오류수정'],
    ['2018-07-19','국내선물옵션, 해외선물옵션에 필요한 모듈을 XAQuery, XAReals에 추가'],
    ['2018-07-19','검색식에서 종목이 빠지는 경우, 손절 및 익절이 나가지 않는 부분 추가'],
    ['2018-07-20','체결시간과 종목검색에서 종목이 빠지는 시간차가 있는 경우 주문이 나가지 않는 부분추가'],
    ['2018-07-25','종목검색 중지시 계속 검색된 종목이 들어오는 문제 수정'],
    ['2018-08-01','종목검색, Chartindex에서 식별자를 사용하는 방법 통일'],
    ['2018-08-01','한번에 수량이 다 체결된 경우 포트에 반영되지 않는 것을 수정'],
    ['2018-08-07','조건검색시 다른 조건검색과 섞이는 것을 수정'],
    ['2018-08-07','API메뉴중 백업에 OnReceiveMessage 추가']
]

import sys, os
import datetime, time
import win32com.client
import pythoncom
import inspect
import pickle
import uuid
import base64
import subprocess
import webbrowser
import numpy as np
import pandas as pd
import pandas.io.sql as pdsql
import sqlite3
import ctypes
import logging
import logging.handlers
import timeit
import pyqtgraph as pg
import math
import collections
import win32gui
import copy
import locale

from subprocess import Popen
from PyQt5 import QtCore, QtGui, QtWidgets, QAxContainer, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from numpy import NaN, Inf, arange, isscalar, asarray, array
from pandas import DataFrame, Series
from threading import Timer
from multiprocessing import Pool, Process, Queue
from enum import Enum
from bisect import bisect
from mss import mss
from PIL import Image
from collections import Counter
#from PIL import ImageGrab

from XASessions import *
from XAQueries import *
from XAReals import *
from FileWatcher import *
from Utils import *

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

# 시스템 기본 로케일 사용
locale.setlocale(locale.LC_ALL, '')  

주문지연 = 3000

DATABASE = 'DATA\\mymoneybot.sqlite'
UI_DIR = "UI\\"

np.warnings.filterwarnings('ignore')

# 만기일 야간옵션은 month_info.txt에서 mangi_yagan을 NO -> YES로 변경
with open('month_info.txt', mode='r') as monthfile:

    tmp = monthfile.readline().strip()

    tmp = monthfile.readline().strip()
    temp = tmp.split()
    kse_start_hour = int(temp[4])
    #print('kse_start_hour =', kse_start_hour)

    tmp = monthfile.readline().strip()
    temp = tmp.split()
    CURRENT_MONTH = temp[3]

    if int(CURRENT_MONTH[4:6]) == 11:

        NEXT_MONTH = CURRENT_MONTH[0:4] + '12'
        MONTH_AFTER_NEXT = repr(int(CURRENT_MONTH[0:4]) + 1) + '01'

    elif int(CURRENT_MONTH[4:6]) == 12:

        NEXT_MONTH = repr(int(CURRENT_MONTH[0:4]) + 1) + '01'
        MONTH_AFTER_NEXT = repr(int(CURRENT_MONTH[0:4]) + 1) + '02'

    else:
        NEXT_MONTH = repr(int(CURRENT_MONTH) + 1)
        MONTH_AFTER_NEXT = repr(int(CURRENT_MONTH) + 2)

    #print('NEXT MONTH =', NEXT_MONTH)
    #print('MONTH AFTER NEXT =', MONTH_AFTER_NEXT)

    tmp = monthfile.readline().strip()
    temp = tmp.split()
    MONTH_FIRSTDAY = temp[7]
        
    tmp = monthfile.readline().strip()
    temp = tmp.split()
    MANGI_YAGAN = temp[3]
    #print('MANGI_YAGAN =', MANGI_YAGAN)

    tmp = monthfile.readline().strip()
    tmp = monthfile.readline().strip()
    tmp = monthfile.readline().strip()

    tmp = monthfile.readline().strip()
    temp = tmp.split()
    TARGET_MONTH_SELECT = int(temp[4])
    print('TARGET MONTH SELECT =', TARGET_MONTH_SELECT)

    tmp = monthfile.readline().strip()
    tmp = monthfile.readline().strip()

    tmp = monthfile.readline().strip()
    temp = tmp.split()
    SP500 = temp[3]

    tmp = monthfile.readline().strip()
    temp = tmp.split()
    DOW = temp[2]

    tmp = monthfile.readline().strip()
    temp = tmp.split()
    NASDAQ = temp[2]     

with open('overnight_info.txt', mode='r') as overnight_file:

    tmp = overnight_file.readline().strip()
    
    tmp = overnight_file.readline().strip()
    temp = tmp.split()
    DOW_INDEX = int(temp[4])
    print('DOW_INDEX =', DOW_INDEX)

    tmp = overnight_file.readline().strip()
    temp = tmp.split()
    CME_INDEX = float(temp[5])
    print('CME_INDEX =', CME_INDEX)

    tmp = overnight_file.readline().strip()
    tmp = overnight_file.readline().strip()

    tmp = overnight_file.readline().strip()
    temp = tmp.split()
    SP500_LAST_LOW = float(temp[5])
    print('SP500_LAST_LOW =', SP500_LAST_LOW)

    tmp = overnight_file.readline().strip()
    temp = tmp.split()
    SP500_LAST_HIGH = float(temp[5])
    print('SP500_LAST_HIGH =', SP500_LAST_HIGH)

    tmp = overnight_file.readline().strip()
    temp = tmp.split()
    DOW_LAST_LOW = float(temp[4])
    print('DOW_LAST_LOW =', DOW_LAST_LOW)

    tmp = overnight_file.readline().strip()
    temp = tmp.split()
    DOW_LAST_HIGH = float(temp[4])
    print('DOW_LAST_HIGH =', DOW_LAST_HIGH)

    tmp = overnight_file.readline().strip()
    temp = tmp.split()
    NASDAQ_LAST_LOW = float(temp[4])
    print('NASDAQ_LAST_LOW =', NASDAQ_LAST_LOW)

    tmp = overnight_file.readline().strip()
    temp = tmp.split()
    NASDAQ_LAST_HIGH = float(temp[4])
    print('NASDAQ_LAST_HIGH =', NASDAQ_LAST_HIGH)

with open('UI_Style.txt', mode='r') as uifile:

    tmp = uifile.readline().strip()
    tmp = uifile.readline().strip()
    temp = tmp.split()
    UI_STYLE = temp[2]

with open('rules.txt', mode='r') as initfile:

    tmp = initfile.readline().strip()

    tmp = initfile.readline().strip()
    temp = tmp.split()
    행사가갯수 = temp[7]

    tmp = initfile.readline().strip()
    temp = tmp.split()

    진성맥점 = []

    for i in range(len(temp)):

        if i > 5:
            진성맥점.append(float(temp[i]))
        else:
            pass

    tmp = initfile.readline().strip()
    temp = tmp.split()
    MY_COREVAL = float(temp[3])

    진성맥점.append(MY_COREVAL)
    진성맥점 = list(set(진성맥점))
    진성맥점.sort()
    #print(진성맥점)

    NEW_NODE_VAL1 = 0
    NEW_NODE_VAL2 = 0
    NEW_NODE_VAL3 = 0

    if os.path.exists('HL-List.txt'):

        with open('HL-List.txt', mode='r') as hlfile:

            tmp = hlfile.readline().strip()
            temp = tmp.split()

            HIGH_LOW_LIST = []

            for i in range(len(temp)):
                
                HIGH_LOW_LIST.append(float(temp[i]))

            HIGH_LOW_LIST.sort()
            HIGH_LOW_LIST.reverse()
            print('HIGH_LOW_LIST =', HIGH_LOW_LIST)

            # 첫번재 최대빈도 맥점탐색
            result = list(Counter(HIGH_LOW_LIST).values())
            #print('중복횟수 리스트 =', result)
            #print('1st 동적맥점 빈도수 =', max(result))
            동적맥점_빈도수_1st = max(result)

            if max(result) > 2:

                # 중복횟수 최대값 인덱스 구함
                max_index = result.index(max(result))            
                #print('중복횟수 최대빈도수 인덱스 =', max_index)

                # 최대 중복값 산출
                result = list(Counter(HIGH_LOW_LIST).keys())
                NEW_NODE_VAL1 = result[max_index]
                #print('1st 동적맥점(최대빈도수의 값) =', NEW_NODE_VAL1)
                print('1st 동적맥점 값 = {0}, 1st 동적맥점 빈도수 = {1}'.format(NEW_NODE_VAL1, 동적맥점_빈도수_1st))

                진성맥점.append(NEW_NODE_VAL1)
                진성맥점 = list(set(진성맥점))
                진성맥점.sort()
                #print('진성맥점 리스트 =', 진성맥점)
                
                # 두번재 최대빈도 맥점탐색
                SECOND_LIST = list(filter((NEW_NODE_VAL1).__ne__, HIGH_LOW_LIST))
                #print('2nd 최대빈도 제거된 리스트 =', SECOND_LIST)

                result = list(Counter(SECOND_LIST).values())
                #print('2nd 중복횟수 리스트 =', result)
                #print('2nd 동적맥점 빈도수 =', max(result))
                동적맥점_빈도수_2nd = max(result)

                if max(result) > 2:

                    max_index = result.index(max(result))            
                    #print('2nd 중복횟수 최대빈도수 인덱스 =', max_index)

                    # 최대 중복값 산출
                    result = list(Counter(SECOND_LIST).keys())
                    #print('2nd keys list =', result)
                    NEW_NODE_VAL2 = result[max_index]
                    #print('2nd 동적맥점(최대빈도수의 값) =', NEW_NODE_VAL2)
                    print('2nd 동적맥점 값 = {0}, 2nd 동적맥점 빈도수 = {1}'.format(NEW_NODE_VAL2, 동적맥점_빈도수_2nd))
                    
                    진성맥점.append(NEW_NODE_VAL2)
                    진성맥점 = list(set(진성맥점))
                    진성맥점.sort()
                    #print('진성맥점 리스트 =', 진성맥점)

                    # 세번재 최대빈도 맥점탐색
                    THIRD_LIST = list(filter((NEW_NODE_VAL2).__ne__, SECOND_LIST))
                    #print('3rd 최대빈도 제거된 리스트 =', THIRD_LIST)

                    result = list(Counter(THIRD_LIST).values())
                    #print('3rd 중복횟수 리스트 =', result)
                    #print('3rd 동적맥점 빈도수 =', max(result))
                    동적맥점_빈도수_3rd = max(result)

                    if max(result) > 2:

                        max_index = result.index(max(result))            
                        #print('3rd 중복횟수 최대빈도수 인덱스 =', max_index)

                        # 최대 중복값 산출
                        result = list(Counter(THIRD_LIST).keys())
                        #print('3rd keys list =', result)
                        NEW_NODE_VAL3 = result[max_index]
                        #print('3rd 동적맥점(최대빈도수의 값) =', NEW_NODE_VAL3)
                        print('3rd 동적맥점 값 = {0}, 3rd 동적맥점 빈도수 = {1}'.format(NEW_NODE_VAL3, 동적맥점_빈도수_3rd))

                        진성맥점.append(NEW_NODE_VAL3)
                        진성맥점 = list(set(진성맥점))
                        진성맥점.sort()
                        print('진성맥점 리스트 =', 진성맥점)
                    else:
                        pass
                else:
                    pass                
            else:
                pass
    else:
        pass

    tmp = initfile.readline().strip()
    temp = tmp.split()
    ASYM_RATIO = float(temp[4])
    print('ASYM_RATIO =', ASYM_RATIO)

    tmp = initfile.readline().strip()
    temp = tmp.split()
    ONEWAY_RATIO = float(temp[4])
    print('ONEWAY_RATIO =', ONEWAY_RATIO)
    
    tmp = initfile.readline().strip()
    tmp = initfile.readline().strip()

    tmp = initfile.readline().strip()
    temp = tmp.split()
    TELEGRAM_SERVICE = temp[3]
    #print(TELEGRAM_SERVICE)

    tmp = initfile.readline().strip()
    temp = tmp.split()
    TELEGRAM_START_TIME = int(temp[7])
    #print(TELEGRAM_START_TIME)

    tmp = initfile.readline().strip()
    temp = tmp.split()
    TELEGRAM_POLLING_INTERVAL = int(temp[4])
    #print(TELEGRAM_POLLING_INTERVAL)

    tmp = initfile.readline().strip()
    temp = tmp.split()
    TELEGRAM_SEND_INTERVAL = int(temp[4])
    #print(TELEGRAM_SEND_INTERVAL)

    tmp = initfile.readline().strip()
    tmp = initfile.readline().strip()

    tmp = initfile.readline().strip()
    temp = tmp.split()
    ONEWAY_THRESHOLD = int(temp[9])
    #print(ONEWAY_THRESHOLD)

    tmp = initfile.readline().strip()
    temp = tmp.split()
    COL_OL = int(temp[7])
    COL_OH = int(temp[11])    
    #print(COL_OL, COL_OH)

    tmp = initfile.readline().strip()
    temp = tmp.split()
    COH_OL = int(temp[7])
    COH_OH = int(temp[11])    
    #print(COH_OL, COH_OH)

    tmp = initfile.readline().strip()
    temp = tmp.split()
    POL_OL = int(temp[7])
    POL_OH = int(temp[11])    
    #print(POL_OL, POL_OH)

    tmp = initfile.readline().strip()
    temp = tmp.split()
    POH_OL = int(temp[7])
    POH_OH = int(temp[11])    
    #print(POH_OL, POH_OH)

# 전역변수
########################################################################################################################
모니터번호 = 0
nRowCount = int(행사가갯수)

server_date = ''
server_time = ''
system_server_timegap = 0

telegram_toggle = True

ovc_start_hour = kse_start_hour - 1

시스템시간 = 0
서버시간 = 0
시스템_서버_시간차 = 0

day_timespan = 395 + 10
overnight_timespan = 660 + 60 + 10

flag_offline = False

# 업종코드
KOSPI = '001'
KOSPI200 = '101'
KOSDAQ = '301'
OPT_CALL = '700'
OPT_PUT = '800'
FUTURES = '900'
CME = '950'

SAMSUNG = '005930'
HYUNDAI = '005380'
Celltrion = '068270'
MOBIS = '012330'
NAVER = '035420'

STOCK = "0001"
BOHEOM = "0002"
TOOSIN = "0003"
BANK = "0004"
JONGGEUM = "0005"
GIGEUM = "0006"
GITA = "0007"
RETAIL = "0008"
FOREIGNER = "0017"
INSTITUTIONAL = "0018"

if UI_STYLE == 'Vertical_view.ui':

    # Plot3 관련 전역변수    
    plot3_time_line = None
    plot3_time_line_start = None
    plot3_time_line_yagan_start = None

    plot3_ovc_jl_line = None
    plot3_ovc_jh_line = None
    plot3_ovc_close_line = None
    plot3_ovc_open_line = None
    plot3_ovc_pivot_line = None
    
    plot3_ovc_low_line = None
    plot3_ovc_high_line = None

    plot3_curve = None

    # Plot4 관련 전역변수    
    plot4_time_line = None    
    plot4_time_line_start = None    
    plot4_time_line_yagan_start = None
        
    plot4_fv_plus_curve = None
    plot4_fv_minus_curve = None

    plot4_fut_jl_line = None
    plot4_fut_jh_line = None
    plot4_fut_close_line = None
    plot4_fut_open_line = None    
    plot4_fut_pivot_line = None

    plot4_fut_low_line = None
    plot4_fut_high_line = None    
    
    plot4_price_curve = None
    plot4_kp200_curve = None
else:
    pass

today = datetime.date.today()
now_Month = today.strftime('%Y%m')
today_str = today.strftime('%Y%m%d')
today_str_title = today.strftime('%Y-%m-%d')

now = datetime.datetime.now()        
nowDate = now.strftime('%Y-%m-%d')

yesterday = today - datetime.timedelta(1)
yesterday_str = yesterday.strftime('%Y%m%d')

current_month = 0
next_month = 0
month_after_next = 0

t2301_month_info = ''
t2835_month_info = ''

dongsi_hoga = False
flag_kp200_start_set = False

flag_telegram_send_worker = False
flag_telegram_listen_worker = False

telegram_command = '/start'
telegram_send_worker_on_time = 0
flag_telegram_on = True

telegram_send_message = 'None'

MONTH_1 = False
MONTH_2 = False
MONTH_3 = False
FLAG_OLOH = False

n_oloh_str = ''

call_low_touch = False
call_high_touch = False
put_low_touch = False
put_high_touch = False

oneway_first_touch = False
oneway_str = ''

콜시가갭합 = 0
풋시가갭합 = 0
콜시가갭합_퍼센트 = 0
풋시가갭합_퍼센트 = 0

콜시가갭합_단위평균 = 0
풋시가갭합_단위평균 = 0

콜대비합 = 0
풋대비합 = 0
콜대비합_퍼센트 = 0
풋대비합_퍼센트 = 0

콜대비합_단위평균 = 0
풋대비합_단위평균 = 0

비대칭장 = ''

call_open_count = 0
put_open_count = 0

call_low_node_count = 0
call_high_node_count = 0
put_low_node_count = 0
put_high_node_count = 0

call_low_node_list = []
call_high_node_list = []
put_low_node_list = []
put_high_node_list = []

call_low_node_str = ''
call_high_node_str = ''
put_low_node_str = ''
put_high_node_str = ''

call_low_coreval_str = ''
call_high_coreval_str = ''
put_low_coreval_str = ''
put_high_coreval_str = ''

kp200_low_node_str = ''
kp200_high_node_str = ''

opt_search_start_value = 0.0
opt_coreval_search_start_value = 0.5
opt_search_end_value = 10

저가_고가_갱신_탐색치1 = 0.09
저가_고가_갱신_탐색치2 = 10.0
탐색폭 = 0.2

start_time_str = ''
end_time_str = ''

콜_체결_초 = 0
풋_체결_초 = 0

call_ol_count = 0
call_oh_count = 0
put_ol_count = 0
put_oh_count = 0

coloring_done_time = 0
coloring_interval = 1
node_coloring = False

first_refresh = True
fut_first_arrive = 0

flag_kp200_low_node = False
flag_kp200_high_node = False
kp200_low_node_time = 0
kp200_high_node_time = 0

service_terminate = False
jugan_service_terminate = False
yagan_service_terminate = False

call_ms_oneway = False
put_ms_oneway = False

call_ms_asymmetric = False
put_ms_asymmetric = False
call_md_asymmetric = False
put_md_asymmetric = False

call_md_all_dying = False
put_md_all_dying = False

call_oneway_level1 = False
call_oneway_level2 = False
call_oneway_level3 = False
call_oneway_level4 = False
call_oneway_level5 = False

put_oneway_level1 = False
put_oneway_level2 = False
put_oneway_level3 = False
put_oneway_level4 = False
put_oneway_level5 = False

flag_fut_low = False
flag_fut_high = False

flag_kp200_low = False
flag_kp200_high = False

kp200_종가 = 0

옵션잔존일 = 0

OVC_체결시간 = '000000'
호가시간 = '000000'

night_time = 0

야간선물_기준시간 = 17

선물_전저 = 0
선물_전고 = 0
선물_종가 = 0
선물_피봇 = 0

선물_시가 = 0
선물_현재가 = 0
선물_저가 = 0
선물_고가 = 0

선물_누적거래량 = 0

oloh_cutoff = 0.10
nodelist_low_cutoff = 0.09
nodelist_high_cutoff = 20.0

centerval_threshold = 0.60

콜매수 = ''
콜매도 = ''
풋매수 = ''
풋매도 = ''
손절 = ''
익절 = '' 

basis = 0

time_delta = 0
START_ON = False

Option_column = Enum('Option_column', '행사가 OLOH 기준가 월저 월고 전저 전고 종가 피봇 시가 시가갭 저가 현재가 고가 대비 진폭 VP OI OID')
Futures_column = Enum('Futures_column', 'OLOH 매수건수 매도건수 매수잔량 매도잔량 건수비 잔량비 전저 전고 종가 피봇 시가 시가갭 저가 현재가 고가 대비 진폭 거래량 FR OI OID')
Option_volume_column = Enum('Option_volume_column', '매도누적체결량 매도누적체결건수 매수누적체결량 매수누적체결건수')
Supply_column = Enum('Supply_column', '외인선옵 개인선옵 기관선옵 외인현물 프로그램')
Quote_column = Enum('Quote_column', 'C-MSCC C-MDCC C-MSCR C-MDCR P-MSCC P-MDCC P-MSCR P-MDCR 콜건수비 콜잔량비 풋건수비 풋잔량비 호가종합 미결종합')
option_pairs_count = 0

call_result = dict()
put_result = dict()

call_oi_init_value = 0
put_oi_init_value = 0

call_volume_total = 0
put_volume_total = 0

opt_x_idx = 0
opt_x_idx_old = 0

ovc_x_idx = 0

call_below_atm_count = 0
put_above_atm_count = 0

every_2sec = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58]
every_5sec = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

every_10sec_a = [0, 10, 20, 30, 40, 50]
every_10sec_b = [5, 15, 25, 35, 45, 55]
every_20sec = [0, 20, 40]
every_30sec = [0, 30]
only_30sec = [30]
every_0sec = [0]

every_5min = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

# 국내선물과 해외선물간 시간차
선물장간_시간차 = 60

receive_real_ovc = False
receive_quote = False

cm_option_title = ''

FUT_FOREIGNER_거래대금순매수 = 0
FUT_RETAIL_거래대금순매수 = 0
FUT_INSTITUTIONAL_거래대금순매수 = 0
FUT_STOCK_거래대금순매수 = 0
FUT_BOHEOM_거래대금순매수 = 0
FUT_TOOSIN_거래대금순매수 = 0
FUT_BANK_거래대금순매수 = 0
FUT_JONGGEUM_거래대금순매수 = 0
FUT_GIGEUM_거래대금순매수 = 0
FUT_GITA_거래대금순매수 = 0

FUT_FOREIGNER_거래대금순매수_직전대비 = 0
FUT_RETAIL_거래대금순매수_직전대비 = 0
FUT_INSTITUTIONAL_거래대금순매수_직전대비 = 0
FUT_STOCK_거래대금순매수_직전대비 = 0
FUT_BOHEOM_거래대금순매수_직전대비 = 0
FUT_TOOSIN_거래대금순매수_직전대비 = 0
FUT_BANK_거래대금순매수_직전대비 = 0
FUT_JONGGEUM_거래대금순매수_직전대비 = 0
FUT_GIGEUM_거래대금순매수_직전대비 = 0
FUT_GITA_거래대금순매수_직전대비 = 0

KOSPI_FOREIGNER_거래대금순매수 = 0
KOSPI_RETAIL_거래대금순매수 = 0
KOSPI_INSTITUTIONAL_거래대금순매수 = 0
KOSPI_STOCK_거래대금순매수 = 0
KOSPI_BOHEOM_거래대금순매수 = 0
KOSPI_TOOSIN_거래대금순매수 = 0
KOSPI_BANK_거래대금순매수 = 0
KOSPI_JONGGEUM_거래대금순매수 = 0
KOSPI_GIGEUM_거래대금순매수 = 0
KOSPI_GITA_거래대금순매수 = 0

프로그램_전체순매수금액 = 0
프로그램_전체순매수금액직전대비 = 0

KOSPI_FOREIGNER_거래대금순매수_직전대비 = 0
KOSPI_RETAIL_거래대금순매수_직전대비 = 0
KOSPI_INSTITUTIONAL_거래대금순매수_직전대비 = 0
KOSPI_STOCK_거래대금순매수_직전대비 = 0
KOSPI_BOHEOM_거래대금순매수_직전대비 = 0
KOSPI_TOOSIN_거래대금순매수_직전대비 = 0
KOSPI_BANK_거래대금순매수_직전대비 = 0
KOSPI_JONGGEUM_거래대금순매수_직전대비 = 0
KOSPI_GIGEUM_거래대금순매수_직전대비 = 0
KOSPI_GITA_거래대금순매수_직전대비 = 0

선물_거래대금순매수 = 0
현물_거래대금순매수 = 0

FUT_FOREIGNER_직전대비 = collections.deque([0, 0, 0], 3)
FUT_RETAIL_직전대비 = collections.deque([0, 0, 0], 3)
FUT_INSTITUTIONAL_직전대비 = collections.deque([0, 0, 0], 3)
KOSPI_FOREIGNER_직전대비 = collections.deque([0, 0, 0], 3)
PROGRAM_직전대비 = collections.deque([0, 0, 0], 3)
수정미결_직전대비 = collections.deque([0, 0, 0], 3)
콜순매수_직전대비 = collections.deque([0, 0, 0], 3)
풋순매수_직전대비 = collections.deque([0, 0, 0], 3)

sp500_직전대비 = collections.deque([0, 0, 0], 5)
dow_직전대비 = collections.deque([0, 0, 0], 5)
nasdaq_직전대비 = collections.deque([0, 0, 0], 5)

opt_total_list = []
call_open_list = []
put_open_list = []

actval_increased = False

flag_call_low_coreval = False
flag_call_high_coreval = False
flag_put_low_coreval = False
flag_put_high_coreval = False

fut_code = ''
gmshcode = ''
cmshcode = ''
ccmshcode = ''

call_atm_value = 0
put_atm_value = 0

kp200_realdata = dict()
fut_realdata = dict()
cme_realdata = dict()

fut_tick_list = []
fut_value_list = []
df_fut_ohlc = pd.DataFrame()

call_code = []
put_code = []
opt_actval = []

view_actval = []

call_t8415_count = 0
put_t8415_count = 0
call_t8416_count = 0
put_t8416_count = 0

df_fut = pd.DataFrame()
df_call = pd.DataFrame()
df_put = pd.DataFrame()
df_call_hoga = pd.DataFrame()
df_put_hoga = pd.DataFrame()
df_call_volume = pd.DataFrame()
df_put_volume = pd.DataFrame()

df_plotdata_call = pd.DataFrame()
df_plotdata_put = pd.DataFrame()

df_plotdata_call_volume = pd.DataFrame()
df_plotdata_put_volume = pd.DataFrame()
df_plotdata_volume_cha = pd.DataFrame()

df_plotdata_call_oi = pd.DataFrame()
df_plotdata_put_oi = pd.DataFrame()

df_plotdata_two_sum = pd.DataFrame()
df_plotdata_two_cha = pd.DataFrame()

df_plotdata_fut = pd.DataFrame()
df_plotdata_fut_volume = pd.DataFrame()
df_plotdata_kp200 = pd.DataFrame()

df_plotdata_sp500 = pd.DataFrame()
df_plotdata_dow = pd.DataFrame()
df_plotdata_nasdaq = pd.DataFrame()

call_quote = pd.Series()
put_quote = pd.Series()

call_volume = pd.Series()
put_volume = pd.Series()

call_ckbox = []
put_ckbox = []
call_cell_widget = []
put_cell_widget = []

atm_str = ''
atm_val = 0
atm_index = 0
atm_index_old = 0
atm_index_yj = 0
jgubun = ''

start_time = 0
start_time1 = 0

global_blink = True

coreval = []
kp200_coreval = []

call_행사가 = []
call_기준가 = []
call_월저 = []
call_월고 = []
call_전저 = []
call_전고 = []
call_종가 = []
call_피봇 = []
call_시가 = []
call_저가 = []
call_고가 = []
call_진폭 = []

콜_순미결합 = 0
콜_수정미결합 = 0
콜_순미결퍼센트 = 0
콜_수정미결퍼센트 = 0

call_기준가_node_list = []
call_월저_node_list = []
call_월고_node_list = []
call_전저_node_list = []
call_전고_node_list = []
call_종가_node_list = []
call_피봇_node_list = []
call_시가_node_list = []
call_저가_node_list = []
call_고가_node_list = []

put_행사가 = []
put_기준가 = []
put_월저 = []
put_월고 = []
put_전저 = []
put_전고 = []
put_종가 = []
put_피봇 = []
put_시가 = []
put_저가 = []
put_고가 = []
put_진폭 = []

풋_순미결합 = 0
풋_순미결퍼센트 = 0
풋_수정미결합 = 0
풋_수정미결퍼센트 = 0

put_기준가_node_list = []
put_월저_node_list = []
put_월고_node_list = []
put_전저_node_list = []
put_전고_node_list = []
put_종가_node_list = []
put_피봇_node_list = []
put_시가_node_list = []
put_저가_node_list = []
put_고가_node_list = []

overnight = False

call_scroll_begin_position = 0
call_scroll_end_position = 0
put_scroll_begin_position = 0
put_scroll_end_position = 0

x_idx = 0

pre_start = False
market_service = False

new_actval_up_count = 0
new_actval_down_count = 0

selected_call = []
selected_put = []

call_node_state = dict()
put_node_state = dict()

yoc_call_gap_percent = [NaN] * nRowCount
yoc_put_gap_percent = [NaN] * nRowCount

call_open = [False] * nRowCount
call_ol = [False] * nRowCount
call_oh = [False] * nRowCount
call_gap_percent = [NaN] * nRowCount
call_db_percent = [NaN] * nRowCount

put_open = [False] * nRowCount
put_ol = [False] * nRowCount
put_oh = [False] * nRowCount
put_gap_percent = [NaN] * nRowCount
put_db_percent = [NaN] * nRowCount

opt_callreal_update_counter = 0
opt_putreal_update_counter = 0
opt_call_ho_update_counter = 0
opt_put_ho_update_counter = 0

refresh_flag = False

oi_delta = 0
oi_delta_old = 0

volume_delta = 0
volume_delta_old = 0

sp500_delta = 0
sp500_delta_old = 0

dow_delta = 0
dow_delta_old = 0

nasdaq_delta = 0
nasdaq_delta_old = 0

comboindex1 = 0
comboindex2 = 0
comboindex3 = 0
comboindex4 = 0

콜현재가 = ''
풋현재가 = ''
선물현재가 = 0

콜시가리스트 = None
콜저가리스트 = None
콜고가리스트 = None

풋시가리스트 = None
풋저가리스트 = None
풋고가리스트 = None

콜_순매수_체결량 = 0
풋_순매수_체결량 = 0

# 컬러정의
blueviolet = QColor(138, 43, 226)
darkviolet = QColor(0x94, 0x00, 0xD3)
lightyellow = QColor(255, 255, 153)
aqua = QColor(0x00, 0xFF, 0xFF)
deepskyblue = QColor(0, 191, 255)
orange = QColor(0xFF, 0xA5, 0x00)
orangered = QColor(255, 69, 0)
magenta = QColor(255, 0, 255)
cyan = QColor(0, 255, 255)
lime = QColor(0, 255, 0)
lavender = QColor(230, 230, 250)
mistyrose = QColor(255, 228, 225)
chocolate = QColor(0xD2, 0x69, 0x1E)
indianred = QColor(0xCD, 0x5C, 0x5C)

greenyellow = QColor(0xAD, 0xFF, 0x2F)
lawngreen = QColor(0x7C, 0xFC, 0x00)
greenyellow = QColor(0xAD, 0xFF, 0x2F)
gold = QColor(0xFF, 0xD7, 0x00)
goldenrod = QColor(0xDA, 0xA5, 0x20)
skyblue = QColor(0x87, 0xCE, 0xEB)
steelblue = QColor(0x46, 0x82, 0xB4)

darkorange = QColor(0xFF, 0x8C, 0x00)
brown = QColor(0xA5, 0x2A, 0x2A)
crimson = QColor(0xDC, 0x14, 0x3C)
indigo = QColor(0x4B, 0x00, 0x82)
royalblue = QColor(0x41, 0x69, 0xE1)
dodgerblue = QColor(0x1E, 0x90, 0xFF)
darkturquoise = QColor(0x00, 0xCE, 0xD1)
darkslateblue = QColor(0x48, 0x3D, 0x8B)
purple = QColor(0x80, 0x00, 0x80)
gainsboro = QColor(0xDC, 0xDC, 0xDC)
slategray = QColor(0x70, 0x80, 0x90)
gray = QColor(0x80, 0x80, 0x80) 
pink = QColor(0xFF, 0xC0, 0xCB)
lightskyblue = QColor(0x87, 0xCE, 0xFA)

흰색 = Qt.white
검정색 = Qt.black
옅은회색 = gainsboro
회색 = gray
적색 = Qt.red
청색 = Qt.blue
녹색 = Qt.green
라임 = lime
노란색 = Qt.yellow

선물색 = Qt.magenta

콜기준가색 = orange
콜월저색 = indianred
콜월고색 = darkorange
콜전저색 = goldenrod
콜전고색 = gold
콜종가색 = chocolate
콜피봇색 = magenta
콜시가색 = 적색

풋기준가색 = royalblue
풋월저색 = darkslateblue
풋월고색 = dodgerblue
풋전저색 = steelblue
풋전고색 = skyblue
풋종가색 = darkturquoise
풋피봇색 = cyan
풋시가색 = 청색

대맥점색 = lawngreen

futpen = pg.mkPen('r', width=2, style=QtCore.Qt.SolidLine)
rpen = pg.mkPen('r', width=2, style=QtCore.Qt.SolidLine)
bpen = pg.mkPen('b', width=2, style=QtCore.Qt.SolidLine)
gpen = pg.mkPen('g', width=2, style=QtCore.Qt.SolidLine)
ypen1 = pg.mkPen('y', width=2, style=QtCore.Qt.DotLine)
ypen = pg.mkPen('y', width=2, style=QtCore.Qt.SolidLine)
mvpen = pg.mkPen('g', width=1, style=QtCore.Qt.DotLine)
tpen = pg.mkPen(lightyellow, width=1, style=QtCore.Qt.DotLine)
tpen1 = pg.mkPen('w', width=1, style=QtCore.Qt.DotLine)

fut_jl_pen = pg.mkPen(aqua, width=2, style=QtCore.Qt.DotLine)
fut_jh_pen = pg.mkPen(orangered, width=2, style=QtCore.Qt.DotLine)
fut_pvt_pen = pg.mkPen(magenta, width=2, style=QtCore.Qt.DotLine)
fut_hc_pen = pg.mkPen(lawngreen, width=1, style=QtCore.Qt.DashLine)
opt_hc_pen = pg.mkPen(lawngreen, width=1, style=QtCore.Qt.DashLine)

atm_upper_pen = pg.mkPen(lawngreen, width=1, style=QtCore.Qt.DashLine)
atm_lower_pen = pg.mkPen(lawngreen, width=1, style=QtCore.Qt.DashLine)

aqua_pen = pg.mkPen(aqua, width=2, style=QtCore.Qt.DotLine)
aqua_pen1 = pg.mkPen(aqua, width=2, style=QtCore.Qt.SolidLine)
magenta_pen = pg.mkPen(magenta, width=2, style=QtCore.Qt.DotLine)
magenta_pen1 = pg.mkPen(magenta, width=2, style=QtCore.Qt.SolidLine)
green_pen = pg.mkPen('g', width=2, style=QtCore.Qt.DotLine)
yellow_pen = pg.mkPen('y', width=2, style=QtCore.Qt.DotLine)
orange_pen = pg.mkPen(orange, width=1, style=QtCore.Qt.DashLine)
skyblue_pen = pg.mkPen(skyblue, width=1, style=QtCore.Qt.DashLine)
goldenrod_pen = pg.mkPen(goldenrod, width=2, style=QtCore.Qt.DotLine)
gold_pen = pg.mkPen(gold, width=2, style=QtCore.Qt.DotLine)

# Plot1
plot1_time_line = None
plot1_time_line_start = None
plot1_time_line_yagan_start = None

plot1_fut_price_curve = None

plot1_fut_volume_curve = None
plot1_fut_volume_plus_curve = None
plot1_fut_volume_minus_curve = None

plot1_fut_pivot_line = None
plot1_fut_jl_line = None
plot1_fut_jh_line = None
plot1_kp200_curve = None

plot1_ovc_open_line = None

plot1_hc_high_line = None
plot1_hc_low_line = None

plot1_atm_high_line = None
plot1_atm_low_line = None

plot1_call_volume_curve = None
plot1_put_volume_curve = None
plot1_volume_cha_curve = None

plot1_call_oi_curve = None
plot1_put_oi_curve = None

plot1_two_sum_curve = None
plot1_two_cha_curve = None

plot1_sp500_curve = None
plot1_dow_curve = None
plot1_nasdaq_curve = None

# Plot2
plot2_time_line = None
plot2_time_line_start = None
plot2_time_line_yagan_start = None

plot2_ovc_open_line = None

plot2_fut_volume_curve = None
plot2_fut_volume_plus_curve = None
plot2_fut_volume_minus_curve = None
plot2_call_volume_curve = None
plot2_put_volume_curve = None
plot2_volume_cha_curve = None

plot2_hc_high_line = None
plot2_hc_low_line = None

plot2_call_oi_curve = None
plot2_put_oi_curve = None

plot2_two_sum_curve = None
plot2_two_cha_curve = None

plot2_sp500_curve = None
plot2_dow_curve = None
plot2_nasdaq_curve = None

mv_curve = []
mv_line = []

call_curve = []
put_curve = []

yoc_stop = False

kospi_price = 0.0
kosdaq_price = 0.0
samsung_price = 0.0
sp500_price = 0.0
dow_price = 0.0
nasdaq_price = 0.0

cme_close = 0.0
dow_close = 0.0

kospi_text_color = ''
kosdaq_text_color = ''
samsung_text_color = ''
sp500_text_color = ''
dow_text_color = ''
nasdaq_text_color = ''

sp500_전일종가 = 0.0
dow_전일종가 = 0.0  
nasdaq_전일종가 = 0.0

sp500_시가 = 0.0
dow_시가 = 0.0  
nasdaq_시가 = 0.0

sp500_피봇 = 0.0
dow_피봇 = 0.0  
nasdaq_피봇 = 0.0

sp500_저가 = 0.0
dow_저가 = 0.0  
nasdaq_저가 = 0.0

sp500_고가 = 0.0
dow_고가 = 0.0  
nasdaq_고가 = 0.0

call_max_actval = False
put_max_actval = False

flag_fut_ol = False
flag_fut_oh = False

콜_인덱스 = 0
콜_시가 = ''
콜_현재가 = ''
콜_저가 = ''
콜_고가 = ''

풋_인덱스 = 0
풋_시가 = ''
풋_현재가 = ''
풋_저가 = ''
풋_고가 = ''

########################################################################################################################

def sqliteconn():
    conn = sqlite3.connect(DATABASE)
    return conn

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        if data is None:
            self._data = DataFrame()

    def rowCount(self, parent=None):
        return len(self._data.index)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, column, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._data.columns[column]
        return int(column + 1)

    def update(self, data):
        self._data = data
        self.reset()

    def reset(self):
        self.beginResetModel()
        self.endResetModel()

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled


class RealDataTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.realdata = {}
        self.headers = ['종목코드', '현재가', '전일대비', '등락률', '매도호가', '매수호가', '누적거래량', '시가', '고가', '저가', '거래회전율', '시가총액']

    def rowCount(self, index=QModelIndex()):
        return len(self.realdata)

    def columnCount(self, index=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or not (0 <= index.row() < len(self.realdata))):
            return None

        if role == Qt.DisplayRole:
            rows = []
            for k in self.realdata.keys():
                rows.append(k)
            one_row = rows[index.row()]
            selected_row = self.realdata[one_row]

            return selected_row[index.column()]

        return None

    def headerData(self, column, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.headers[column]
        return int(column + 1)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def reset(self):
        self.beginResetModel()
        self.endResetModel()


class CPluginManager:
    plugins = None
    @classmethod
    def plugin_loader(cls):
        path = "plugins/"
        result = {}

        # Load plugins
        sys.path.insert(0, path)
        for f in os.listdir(path):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                mod = __import__(fname)
                robot = mod.robot_loader()
                if robot is not None:
                    result[robot.Name] = robot
        sys.path.pop(0)

        CPluginManager.plugins = result

        return result


Ui_계좌정보조회, QtBaseClass_계좌정보조회 = uic.loadUiType(UI_DIR+"계좌정보조회.ui")


class 화면_계좌정보(QDialog, Ui_계좌정보조회):
    def __init__(self, parent=None):
        super(화면_계좌정보, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.parent = parent
        self.model1 = PandasModel()
        self.tableView_1.setModel(self.model1)
        self.model2 = PandasModel()
        self.tableView_2.setModel(self.model2)

        self.result = []
        self.connection = self.parent.connection

        # 계좌정보 불러오기
        nCount = self.connection.ActiveX.GetAccountListCount()
        for i in range(nCount):
            self.comboBox.addItem(self.connection.ActiveX.GetAccountList(i))

        self.XQ_t0424 = t0424(parent=self)

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't0424':
            self.df1, self.df2 = result

            self.model1.update(self.df1)
            for i in range(len(self.df1.columns)):
                self.tableView_1.resizeColumnToContents(i)

            self.model2.update(self.df2)
            for i in range(len(self.df2.columns)):
                self.tableView_2.resizeColumnToContents(i)

            CTS_종목번호 = self.df1['CTS_종목번호'].values[0].strip()
            if CTS_종목번호 != '':
                self.XQ_t0424.Query(계좌번호=self.계좌번호, 비밀번호=self.비밀번호, 단가구분='1', 체결구분='0', 단일가구분='0', 제비용포함여부='1', CTS_종목번호=CTS_종목번호)

    def inquiry(self):
        self.계좌번호 = self.comboBox.currentText().strip()
        self.비밀번호 = self.lineEdit.text().strip()

        self.XQ_t0424.Query(계좌번호=self.계좌번호, 비밀번호=self.비밀번호, 단가구분='1', 체결구분='0', 단일가구분='0', 제비용포함여부='1', CTS_종목번호='')

        QTimer().singleShot(3*1000, self.inquiry)


Ui_일별가격정보백업, QtBaseClass_일별가격정보백업 = uic.loadUiType(UI_DIR+"일별가격정보백업.ui")
class 화면_일별가격정보백업(QDialog, Ui_일별가격정보백업):
    def __init__(self, parent=None):
        super(화면_일별가격정보백업, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('가격 정보 백업')
        self.parent = parent
        self.result = []

        d = datetime.date.today()
        self.lineEdit_date.setText(str(d))

        XQ_t8436 = t8436(parent=self)
        XQ_t8436.Query(구분='0')

        self.조회건수 = 10
        self.XQ_t1305 = t1305(parent=self)

    def OnReceiveMessage(self, systemError, messageCode, message):
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = ">> " + self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

        if szTrCode == 't1305':
            CNT, 날짜, IDX, df = result
            # print(self.단축코드, CNT, 날짜, IDX)
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                query = "insert or replace into 일별주가( 날짜, 시가, 고가, 저가, 종가, 전일대비구분, 전일대비, 등락율, 누적거래량, 거래증가율, 체결강도, 소진율, 회전율, 외인순매수, 기관순매수, 종목코드, 누적거래대금, 개인순매수, 시가대비구분, 시가대비, 시가기준등락율, 고가대비구분, 고가대비, 고가기준등락율, 저가대비구분, 저가대비, 저가기준등락율, 시가총액) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.executemany(query, df.values.tolist())
                conn.commit()

            try:
                if int(CNT) == int(self.조회건수) and self.radioButton_all.isChecked() == True:
                    QTimer.singleShot(주문지연, lambda: self.Request(result=result))
                else:
                    self.백업한종목수 += 1
                    if len(self.백업할종목코드) > 0:
                        self.단축코드 = self.백업할종목코드.pop(0)
                        self.result = []

                        self.progressBar.setValue(int(self.백업한종목수 / (len(self.종목코드테이블.index) - self.comboBox.currentIndex()) * 100))
                        S = '%s %s' % (self.단축코드[0], self.단축코드[1])
                        self.label_codename.setText(S)

                        QTimer.singleShot(주문지연, lambda : self.Request([]))
                    else:
                        QMessageBox.about(self, "백업완료","백업을 완료하였습니다..")
            except Exception as e:
                print('Handling run-time error : ', e)

    def Request(self, result=[]):
        if len(result) > 0:
            CNT, 날짜, IDX, df = result
            self.XQ_t1305.Query(단축코드=self.단축코드[0], 일주월구분='1', 날짜=날짜, IDX=IDX, 건수=self.조회건수, 연속조회=True)
        else:
            try:
                # print('%s %s' % (self.단축코드[0], self.단축코드[1]))
                self.XQ_t1305.Query(단축코드=self.단축코드[0], 일주월구분='1', 날짜='', IDX='', 건수=self.조회건수, 연속조회=False)
            except Exception as e:
                print('Handling run-time error : ', e)

    def Backup_One(self):
        idx = self.comboBox.currentIndex()

        self.백업한종목수 = 1
        self.백업할종목코드 = []
        self.단축코드 = self.종목코드테이블[idx:idx + 1][['단축코드','종목명']].values[0]
        self.기준일자 = self.lineEdit_date.text().strip().replace('-','')
        self.result = []
        self.Request(result=[])

    def Backup_All(self):
        idx = self.comboBox.currentIndex()
        self.백업한종목수 = 1
        self.백업할종목코드 = list(self.종목코드테이블[idx:][['단축코드','종목명']].values)
        self.단축코드 = self.백업할종목코드.pop(0)
        self.기준일자 = self.lineEdit_date.text().strip().replace('-','')

        self.progressBar.setValue(int(self.백업한종목수 / (len(self.종목코드테이블.index) - self.comboBox.currentIndex()) * 100))
        S = '%s %s' % (self.단축코드[0], self.단축코드[1])
        self.label_codename.setText(S)

        self.result = []
        self.Request(result=[])


Ui_일별업종정보백업, QtBaseClass_일별업종정보백업 = uic.loadUiType(UI_DIR+"일별업종정보백업.ui")


class 화면_일별업종정보백업(QDialog, Ui_일별업종정보백업):
    def __init__(self, parent=None):
        super(화면_일별업종정보백업, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('업종 정보 백업')
        self.parent = parent

        self.columns = ['현재가', '거래량', '일자', '시가', '고가', '저가','거래대금', '대업종구분', '소업종구분', '종목정보', '종목정보', '수정주가이벤트', '전일종가']

        self.result = []

        d = datetime.date.today()
        self.lineEdit_date.setText(str(d))

        XQ = t8424(parent=self)
        XQ.Query()

        self.조회건수 = 10
        self.XQ_t1514 = t1514(parent=self)

    def OnReceiveMessage(self, systemError, messageCode, message):
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8424':
            df = result[0]
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                query = "insert or replace into 업종코드(업종명, 업종코드) values(?, ?)"
                cursor.executemany(query, df.values.tolist())
                conn.commit()

            self.업종코드테이블 = result[0]
            self.업종코드테이블['컬럼'] = ">> " + self.업종코드테이블['업종코드'] + " : " + self.업종코드테이블['업종명']
            self.업종코드테이블 = self.업종코드테이블.sort_values(['업종코드', '업종명'], ascending=[True, True])
            self.comboBox.addItems(self.업종코드테이블['컬럼'].values)

        if szTrCode == 't1514':
            CTS일자, df = result
            # print(CTS일자)
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                query = "insert or replace into 업종정보(일자, 지수, 전일대비구분, 전일대비, 등락율, 거래량, 거래증가율, 거래대금1, 상승, 보합, 하락, 상승종목비율, 외인순매수, 시가, 고가, 저가, 거래대금2, 상한, 하한, 종목수, 기관순매수, 업종코드, 거래비중, 업종배당수익률) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.executemany(query, df.values.tolist())
                conn.commit()

            try:
                if len(df) == int(self.조회건수) and self.radioButton_all.isChecked() == True:
                    QTimer.singleShot(주문지연, lambda: self.Request(result=result))
                else:
                    self.백업한종목수 += 1
                    if len(self.백업할업종코드) > 0:
                        self.업종코드 = self.백업할업종코드.pop(0)
                        self.result = []

                        self.progressBar.setValue(int(self.백업한종목수 / (len(self.업종코드테이블.index) - self.comboBox.currentIndex()) * 100))
                        S = '%s %s' % (self.업종코드[0], self.업종코드[1])
                        self.label_codename.setText(S)

                        QTimer.singleShot(주문지연, lambda : self.Request([]))
                    else:
                        QMessageBox.about(self, "백업완료","백업을 완료하였습니다..")
            except Exception as e:
                pass

    def Request(self, result=[]):
        if len(result) > 0:
            CTS일자, df = result
            self.XQ_t1514.Query(업종코드=self.업종코드[0],구분1='',구분2='1',CTS일자=CTS일자, 조회건수=self.조회건수,비중구분='', 연속조회=True)
        else:
            # print('%s %s' % (self.업종코드[0], self.업종코드[1]))
            self.XQ_t1514.Query(업종코드=self.업종코드[0], 구분1='', 구분2='1', CTS일자='', 조회건수=self.조회건수, 비중구분='', 연속조회=False)

    def Backup_One(self):
        idx = self.comboBox.currentIndex()

        self.백업한종목수 = 1
        self.백업할업종코드 = []
        self.업종코드 = self.업종코드테이블[idx:idx + 1][['업종코드','업종명']].values[0]
        self.기준일자 = self.lineEdit_date.text().strip().replace('-','')
        self.result = []
        self.Request(result=[])

    def Backup_All(self):
        idx = self.comboBox.currentIndex()
        self.백업한종목수 = 1
        self.백업할업종코드 = list(self.업종코드테이블[idx:][['업종코드','업종명']].values)
        self.업종코드 = self.백업할업종코드.pop(0)
        self.기준일자 = self.lineEdit_date.text().strip().replace('-','')

        self.progressBar.setValue(int(self.백업한종목수 / (len(self.업종코드테이블.index) - self.comboBox.currentIndex()) * 100))
        S = '%s %s' % (self.업종코드[0], self.업종코드[1])
        self.label_codename.setText(S)

        self.result = []
        self.Request(result=[])


Ui_분별가격정보백업, QtBaseClass_분별가격정보백업 = uic.loadUiType(UI_DIR+"분별가격정보백업.ui")
class 화면_분별가격정보백업(QDialog, Ui_분별가격정보백업):
    def __init__(self, parent=None):
        super(화면_분별가격정보백업, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('가격 정보 백업')
        self.parent = parent

        self.columns = ['체결시간', '현재가', '시가', '고가', '저가', '거래량']

        self.result = []

        XQ_t8436 = t8436(parent=self)
        XQ_t8436.Query(구분='0')

        self.조회건수 = 10
        self.XQ_t1302 = t1302(parent=self)

    def OnReceiveMessage(self, systemError, messageCode, message):
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = ">> " + self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

        if szTrCode == 't1302':
            시간CTS, df = result
            df['단축코드'] = self.단축코드[0]
            # print(시간CTS)
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                query = "insert or replace into 분별주가(시간, 종가, 전일대비구분, 전일대비, 등락율, 체결강도, 매도체결수량, 매수체결수량, 순매수체결량, 매도체결건수, 매수체결건수, 순체결건수, 거래량, 시가, 고가, 저가, 체결량, 매도체결건수시간, 매수체결건수시간, 매도잔량, 매수잔량, 시간별매도체결량, 시간별매수체결량,단축코드) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.executemany(query, df.values.tolist())
                conn.commit()

            try:
                if len(df) == int(self.조회건수) and self.radioButton_all.isChecked() == True:
                    QTimer.singleShot(주문지연, lambda: self.Request(result=result))
                else:
                    self.백업한종목수 += 1
                    if len(self.백업할종목코드) > 0:
                        self.단축코드 = self.백업할종목코드.pop(0)
                        self.result = []

                        self.progressBar.setValue(int(self.백업한종목수 / (len(self.종목코드테이블.index) - self.comboBox.currentIndex()) * 100))
                        S = '%s %s' % (self.단축코드[0], self.단축코드[1])
                        self.label_codename.setText(S)

                        QTimer.singleShot(주문지연, lambda : self.Request([]))
                    else:
                        QMessageBox.about(self, "백업완료","백업을 완료하였습니다..")
            except Exception as e:
                pass

    def Request(self, result=[]):
        if len(result) > 0:
            시간CTS, df = result
            self.XQ_t1302.Query(단축코드=self.단축코드[0], 작업구분=self.틱범위, 시간=시간CTS, 건수=self.조회건수, 연속조회=True)
        else:
            # print('%s %s' % (self.단축코드[0], self.단축코드[1]))
            self.XQ_t1302.Query(단축코드=self.단축코드[0], 작업구분=self.틱범위, 시간='', 건수=self.조회건수, 연속조회=False)

    def Backup_One(self):
        idx = self.comboBox.currentIndex()

        self.백업한종목수 = 1
        self.백업할종목코드 = []
        self.단축코드 = self.종목코드테이블[idx:idx + 1][['단축코드','종목명']].values[0]
        self.틱범위 = self.comboBox_min.currentText()[0:1].strip()
        if self.틱범위[0] == '0':
            self.틱범위 = self.틱범위[1:]
        self.result = []
        self.Request(result=[])

    def Backup_All(self):
        idx = self.comboBox.currentIndex()
        self.백업한종목수 = 1
        self.백업할종목코드 = list(self.종목코드테이블[idx:][['단축코드','종목명']].values)
        self.단축코드 = self.백업할종목코드.pop(0)
        self.틱범위 = self.comboBox_min.currentText()[0:1].strip()
        if self.틱범위[0] == '0':
            self.틱범위 = self.틱범위[1:]

        self.progressBar.setValue(int(self.백업한종목수 / (len(self.종목코드테이블.index) - self.comboBox.currentIndex()) * 100))
        S = '%s %s' % (self.단축코드[0], self.단축코드[1])
        self.label_codename.setText(S)

        self.result = []
        self.Request(result=[])


Ui_종목별투자자정보백업, QtBaseClass_종목별투자자정보백업 = uic.loadUiType(UI_DIR+"종목별투자자정보백업.ui")
class 화면_종목별투자자정보백업(QDialog, Ui_종목별투자자정보백업):
    def __init__(self, parent=None):
        super(화면_종목별투자자정보백업, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('종목별 투자자 정보 백업')
        self.parent = parent

        self.columns = ['일자', '현재가', '전일대비', '누적거래대금', '개인투자자', '외국인투자자','기관계','금융투자','보험','투신','기타금융','은행','연기금등','국가','내외국인','사모펀드','기타법인']

        d = datetime.date.today()
        self.lineEdit_date.setText(str(d))

        XQ_t8436 = t8436(parent=self)
        XQ_t8436.Query(구분='0')

        self.조회건수 = 10
        self.XQ_t1702 = t1702(parent=self)

    def OnReceiveMessage(self, systemError, messageCode, message):
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = ">> " + self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

        if szTrCode == 't1702':
            CTSIDX, CTSDATE, df = result
            df['단축코드'] = self.단축코드[0]
            # print(CTSIDX, CTSDATE)
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                query = "insert or replace into 종목별투자자(일자, 종가, 전일대비구분, 전일대비, 등락율, 누적거래량, 사모펀드, 증권, 보험, 투신, 은행, 종금, 기금, 기타법인, 개인, 등록외국인, 미등록외국인, 국가외, 기관, 외인계, 기타계, 단축코드) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.executemany(query, df.values.tolist())
                conn.commit()

            try:
                if len(df) == int(self.조회건수) and self.radioButton_all.isChecked() == True:
                    QTimer.singleShot(주문지연, lambda: self.Request(result=result))
                else:
                    self.백업한종목수 += 1
                    if len(self.백업할종목코드) > 0:
                        self.단축코드 = self.백업할종목코드.pop(0)
                        self.result = []

                        self.progressBar.setValue(int(self.백업한종목수 / (len(self.종목코드테이블.index) - self.comboBox.currentIndex()) * 100))
                        S = '%s %s' % (self.단축코드[0], self.단축코드[1])
                        self.label_codename.setText(S)

                        QTimer.singleShot(주문지연, lambda : self.Request([]))
                    else:
                        QMessageBox.about(self, "백업완료","백업을 완료하였습니다..")
            except Exception as e:
                pass

    def Request(self, result=[]):
        if len(result) > 0:
            CTSIDX, CTSDATE, df = result
            self.XQ_t1702.Query(종목코드=self.단축코드[0], 종료일자='', 금액수량구분='0', 매수매도구분='0', 누적구분='0', CTSDATE=CTSDATE, CTSIDX=CTSIDX)
        else:
            # print('%s %s' % (self.단축코드[0], self.단축코드[1]))
            self.XQ_t1702.Query(종목코드=self.단축코드[0], 종료일자='', 금액수량구분='0', 매수매도구분='0', 누적구분='0', CTSDATE='', CTSIDX='')

    def Backup_One(self):
        idx = self.comboBox.currentIndex()

        self.백업한종목수 = 1
        self.백업할종목코드 = []
        self.단축코드 = self.종목코드테이블[idx:idx + 1][['단축코드','종목명']].values[0]
        self.기준일자 = self.lineEdit_date.text().strip().replace('-','')
        self.result = []
        self.Request(result=[])

    def Backup_All(self):
        idx = self.comboBox.currentIndex()
        self.백업한종목수 = 1
        self.백업할종목코드 = list(self.종목코드테이블[idx:][['단축코드','종목명']].values)
        self.단축코드 = self.백업할종목코드.pop(0)
        self.기준일자 = self.lineEdit_date.text().strip().replace('-','')

        self.progressBar.setValue(int(self.백업한종목수 / (len(self.종목코드테이블.index) - self.comboBox.currentIndex()) * 100))
        S = '%s %s' % (self.단축코드[0], self.단축코드[1])
        self.label_codename.setText(S)

        self.result = []
        self.Request(result=[])

## ---------------------------------------------------------------------------------------------------------------------
Ui_종목코드, QtBaseClass_종목코드 = uic.loadUiType(UI_DIR+"종목코드조회.ui")
class 화면_종목코드(QDialog, Ui_종목코드):
    def __init__(self, parent=None):
        super(화면_종목코드, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.df = DataFrame()
        self.XQ_t8436 = t8436(parent=self)
        self.XQ_t8436.Query(구분='0')

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.df = result[0]
            self.model.update(self.df)
            for i in range(len(self.df.columns)):
                self.tableView.resizeColumnToContents(i)

    def SaveCode(self):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            query = "insert or replace into 종목코드(종목명,단축코드,확장코드,ETF구분,상한가,하한가,전일가,주문수량단위,기준가,구분,증권그룹,기업인수목적회사여부) values(?,?,?,?,?,?,?,?,?,?,?,?)"
            cursor.executemany(query, self.df.values.tolist())
            conn.commit()

        QMessageBox.about(self, "종목코드 생성", " %s 항목의 종목코드를 생성하였습니다." % (len(self.df)))


Ui_업종정보, QtBaseClass_업종정보 = uic.loadUiType(UI_DIR+"업종정보조회.ui")
class 화면_업종정보(QDialog, Ui_업종정보):
    def __init__(self, parent=None):
        super(화면_업종정보, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.setWindowTitle('업종정보 조회')

        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.columns = ['일자', '지수', '전일대비구분', '전일대비', '등락율', '거래량', '거래증가율', '거래대금1', '상승', '보합', '하락', '상승종목비율', '외인순매수',
                   '시가', '고가', '저가', '거래대금2', '상한', '하한', '종목수', '기관순매수', '업종코드', '거래비중', '업종배당수익률']

        self.result = []

        d = datetime.date.today()

        XQ = t8424(parent=self)
        XQ.Query()

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8424':
            df = result[0]
            df['컬럼'] = df['업종코드'] + " : " + df['업종명']
            df = df.sort_values(['업종코드', '업종명'], ascending=[True, True])
            self.comboBox.addItems(df['컬럼'].values)

        if szTrCode == 't1514':
            CTS일자, df = result
            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)

    def inquiry(self):
        업종코드 = self.comboBox.currentText()[:3]
        조회건수 = self.lineEdit_date.text().strip().replace('-', '')

        XQ = t1514(parent=self)
        XQ.Query(업종코드=업종코드,구분1='',구분2='1',CTS일자='',조회건수=조회건수,비중구분='', 연속조회=False)


Ui_테마정보, QtBaseClass_테마정보 = uic.loadUiType(UI_DIR+"테마정보조회.ui")
class 화면_테마정보(QDialog, Ui_테마정보):
    def __init__(self, parent=None):
        super(화면_테마정보, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.setWindowTitle('테마정보 조회')

        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.columns = ['일자', '지수', '전일대비구분', '전일대비', '등락율', '거래량', '거래증가율', '거래대금1', '상승', '보합', '하락', '상승종목비율', '외인순매수',
                   '시가', '고가', '저가', '거래대금2', '상한', '하한', '종목수', '기관순매수', '업종코드', '거래비중', '업종배당수익률']

        self.result = []

        d = datetime.date.today()

        XQ = t8425(parent=self)
        XQ.Query()

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8425':
            df = result[0]
            df['컬럼'] = df['테마코드'] + " : " + df['테마명']
            df = df.sort_values(['테마코드', '테마명'], ascending=[True, True])
            self.comboBox.addItems(df['컬럼'].values)

        if szTrCode == 't1537':
            df0, df = result
            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)

    def inquiry(self):
        테마코드 = self.comboBox.currentText()[:4]

        XQ = t1537(parent=self)
        XQ.Query(테마코드=테마코드, 연속조회=False)


Ui_분별주가조회, QtBaseClass_분별주가조회 = uic.loadUiType(UI_DIR+"분별주가조회.ui")
class 화면_분별주가(QDialog, Ui_분별주가조회):
    def __init__(self, parent=None):
        super(화면_분별주가, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('분별 주가 조회')
        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.columns = []

        self.result = []

        XQ = t8436(parent=self)
        XQ.Query(구분='0')

        self.XQ_t1302 = t1302(parent=self)

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = ">> " + self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

        if szTrCode == 't1302':
            시간CTS, df = result
            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)

    def inquiry(self):
        단축코드 = self.comboBox.currentText().strip()[3:9]
        조회건수 = self.lineEdit_cnt.text().strip().replace('-', '')

        self.XQ_t1302.Query(단축코드=단축코드,작업구분='1',시간='',건수=조회건수, 연속조회=False)


Ui_일자별주가조회, QtBaseClass_일자별주가조회 = uic.loadUiType(UI_DIR+"일자별주가조회.ui")
class 화면_일별주가(QDialog, Ui_일자별주가조회):
    def __init__(self, parent=None):
        super(화면_일별주가, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.setWindowTitle('일자별 주가 조회')

        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.columns = ['날짜', '시가', '고가', '저가', '종가', '전일대비구분', '전일대비', '등락율', '누적거래량', '거래증가율', '체결강도', '소진율', '회전율',
                   '외인순매수', '기관순매수', '종목코드', '누적거래대금', '개인순매수', '시가대비구분', '시가대비', '시가기준등락율', '고가대비구분', '고가대비',
                   '고가기준등락율', '저가대비구분', '저가대비', '저가기준등락율', '시가총액']

        self.result = []

        d = datetime.date.today()

        XQ = t8436(parent=self)
        XQ.Query(구분='0')

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = ">> " + self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

        if szTrCode == 't1305':
            CNT, 날짜, IDX, df = result
            # print(CNT, 날짜, IDX)

            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)

            if int(CNT) == int(self.조회건수):
                QTimer.singleShot(주문지연, lambda: self.inquiry_repeatly(result=result))
            else:
                # print("===END===")
                pass

    def inquiry_repeatly(self, result):
        CNT, 날짜, IDX, df = result
        self.XQ.Query(단축코드=self.단축코드, 일주월구분='1', 날짜=날짜, IDX=IDX, 건수=self.조회건수, 연속조회=True)

    def inquiry(self):
        self.단축코드 = self.comboBox.currentText()[3:9]
        self.조회건수 = self.lineEdit_date.text().strip().replace('-', '')

        self.XQ = t1305(parent=self)
        self.XQ.Query(단축코드=self.단축코드,일주월구분='1',날짜='',IDX='',건수=self.조회건수, 연속조회=False)


Ui_종목별투자자조회, QtBaseClass_종목별투자자조회 = uic.loadUiType(UI_DIR+"종목별투자자조회.ui")
class 화면_종목별투자자(QDialog, Ui_종목별투자자조회):
    def __init__(self, parent=None):
        super(화면_종목별투자자, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('종목별 투자자 조회')
        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.columns = ['일자', '종가', '전일대비구분', '전일대비', '등락율', '누적거래량', '사모펀드', '증권', '보험', '투신', '은행', '종금', '기금', '기타법인',
                       '개인', '등록외국인', '미등록외국인', '국가외', '기관', '외인계', '기타계']

        self.result = []

        d = datetime.date.today()
        self.lineEdit_date.setText(str(d))

        XQ = t8436(parent=self)
        XQ.Query(구분='0')

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = ">> " + self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

        if szTrCode == 't1702':
            CTSIDX, CTSDATE, df = result
            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)

    def Request(self, _repeat=0):
        종목코드 = self.lineEdit_code.text().strip()
        기준일자 = self.lineEdit_date.text().strip().replace('-','')

    def inquiry(self):
        단축코드 = self.comboBox.currentText()[3:9]
        조회건수 = self.lineEdit_date.text().strip().replace('-', '')

        XQ = t1702(parent=self)
        XQ.Query(종목코드=단축코드, 종료일자='', 금액수량구분='0', 매수매도구분='0', 누적구분='0', CTSDATE='', CTSIDX='')


class 화면_종목별투자자2(QDialog, Ui_종목별투자자조회):
    def __init__(self, parent=None):
        super(화면_종목별투자자2, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('종목별 투자자 조회')
        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.columns = []

        self.result = []

        d = datetime.date.today()
        self.lineEdit_date.setText(str(d))

        XQ = t8436(parent=self)
        XQ.Query(구분='0')

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = ">> " + self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

        if szTrCode == 't1717':
            df = result[0]
            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)

    def Request(self, _repeat=0):
        종목코드 = self.lineEdit_code.text().strip()
        기준일자 = self.lineEdit_date.text().strip().replace('-','')

    def inquiry(self):
        단축코드 = self.comboBox.currentText()[3:9]
        조회건수 = self.lineEdit_date.text().strip().replace('-', '')

        XQ = t1717(parent=self)
        XQ.Query(종목코드=단축코드,구분='0',시작일자='20170101',종료일자='20172131')


Ui_차트인덱스, QtBaseClass_차트인덱스 = uic.loadUiType(UI_DIR+"차트인덱스.ui")
class 화면_차트인덱스(QDialog, Ui_차트인덱스):
    def __init__(self, parent=None):
        super(화면_차트인덱스, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.parent = parent

        self.columns = ['일자', '시간', '시가', '고가', '저가', '종가', '거래량', '지표값1', '지표값2', '지표값3', '지표값4', '지표값5', '위치']

        self.XQ_ChartIndex = ChartIndex(parent=self)
        XQ = t8436(parent=self)
        XQ.Query(구분='0')

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = ">> " + self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

        if szTrCode == 'CHARTINDEX':
            식별자, 지표ID, 레코드갯수, 유효데이터컬럼갯수, self.df = result

            self.model.update(self.df)
            for i in range(len(self.df.columns)):
                self.tableView.resizeColumnToContents(i)

    def OnReceiveChartRealData(self, szTrCode, lst):
        if szTrCode == 'CHARTINDEX':
            식별자, result = lst
            지표ID, 레코드갯수, 유효데이터컬럼갯수, d = result
            lst = [[d['일자'],d['시간'],d['시가'],d['고가'],d['저가'],d['종가'],d['거래량'],d['지표값1'],d['지표값2'],d['지표값3'],d['지표값4'],d['지표값5'],d['위치']]]
            self.df = self.df.append(pd.DataFrame(lst, columns=self.columns), ignore_index=True)

            try:
                self.model.update(self.df)
                for i in range(len(self.df.columns)):
                    self.tableView.resizeColumnToContents(i)
            except Exception as e:
                pass

    def inquiry(self):
        지표명 = self.lineEdit_name.text()
        단축코드 =  self.comboBox.currentText()[3:9]
        요청건수 = self.lineEdit_cnt.text()
        실시간 = '1' if self.checkBox.isChecked() == True else '0'

        self.XQ_ChartIndex.Query(지표ID='', 지표명=지표명, 지표조건설정='', 시장구분='1', 주기구분='0', 단축코드=단축코드, 요청건수=요청건수, 단위='3', 시작일자='',
                 종료일자='', 수정주가반영여부='1', 갭보정여부='1', 실시간데이터수신자동등록여부=실시간)


Ui_종목검색, QtBaseClass_종목검색 = uic.loadUiType(UI_DIR+"종목검색.ui")
class 화면_종목검색(QDialog, Ui_종목검색):
    def __init__(self, parent=None):
        super(화면_종목검색, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.parent = parent

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't1833':
            종목검색수, df = result
            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)

    def fileselect(self):
        pathname = os.path.dirname(sys.argv[0])
        RESDIR = "%s\\ADF\\" % os.path.abspath(pathname)

        fname = QFileDialog.getOpenFileName(self, 'Open file',RESDIR, "조검검색(*.adf)")
        self.lineEdit.setText(fname[0])

    def inquiry(self):
        filename = self.lineEdit.text()
        XQ = t1833(parent=self)
        XQ.Query(종목검색파일=filename)


Ui_e종목검색, QtBaseClass_e종목검색 = uic.loadUiType(UI_DIR+"e종목검색.ui")
class 화면_e종목검색(QDialog, Ui_e종목검색):
    def __init__(self, parent=None):
        super(화면_e종목검색, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.parent = parent

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't1857':
            검색종목수, 포착시간, 실시간키, df = result
            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)

    def OnReceiveSearchRealData(self, szTrCode, result):
        if szTrCode == 't1857':
            print(result)

    def fileselect(self):
        pathname = os.path.dirname(sys.argv[0])
        RESDIR = "%s\\ACF\\" % os.path.abspath(pathname)

        fname = QFileDialog.getOpenFileName(self, 'Open file',RESDIR, "조검검색(*.acf)")
        self.lineEdit.setText(fname[0])

    def inquiry(self):
        filename = self.lineEdit.text()
        XQ = t1857(parent=self)
        XQ.Query(실시간구분='0',종목검색구분='F',종목검색입력값=filename)


Ui_호가창정보, QtBaseClass_호가창정보 = uic.loadUiType(UI_DIR+"실시간호가.ui")
class 화면_호가창정보(QDialog, Ui_호가창정보):
    def __init__(self, parent=None):
        super(화면_호가창정보, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.parent = parent

        self.매도호가컨트롤 = [
            self.label_offerho1, self.label_offerho2, self.label_offerho3, self.label_offerho4, self.label_offerho5,
            self.label_offerho6, self.label_offerho7, self.label_offerho8, self.label_offerho9, self.label_offerho10
        ]

        self.매수호가컨트롤 = [
            self.label_bidho1, self.label_bidho2, self.label_bidho3, self.label_bidho4, self.label_bidho5,
            self.label_bidho6, self.label_bidho7, self.label_bidho8, self.label_bidho9, self.label_bidho10
        ]

        self.매도호가잔량컨트롤 = [
            self.label_offerrem1, self.label_offerrem2, self.label_offerrem3, self.label_offerrem4,
            self.label_offerrem5,
            self.label_offerrem6, self.label_offerrem7, self.label_offerrem8, self.label_offerrem9,
            self.label_offerrem10
        ]

        self.매수호가잔량컨트롤 = [
            self.label_bidrem1, self.label_bidrem2, self.label_bidrem3, self.label_bidrem4, self.label_bidrem5,
            self.label_bidrem6, self.label_bidrem7, self.label_bidrem8, self.label_bidrem9, self.label_bidrem10
        ]

        with sqlite3.connect(DATABASE) as conn:
            query = 'select 단축코드,종��명,ETF구분,구분 from 종목코드'
            df = pdsql.read_sql_query(query, con=conn)

        self.kospi_codes = df.query("구분=='1'")['단축코드'].values.tolist()
        self.kosdaq_codes = df.query("구분=='2'")['단축코드'].values.tolist()

        XQ = t8436(parent=self)
        XQ.Query(구분='0')

        self.kospi_askbid = H1_(parent=self)
        self.kosdaq_askbid = HA_(parent=self)

    def OnReceiveMessage(self, systemError, messageCode, message):
        # print(systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 't8436':
            self.종목코드테이블 = result[0]
            self.종목코드테이블['컬럼'] = self.종목코드테이블['단축코드'] + " : " + self.종목코드테이블['종목명']
            self.종목코드테이블 = self.종목코드테이블.sort_values(['단축코드', '종목명'], ascending=[True, True])
            self.comboBox.addItems(self.종목코드테이블['컬럼'].values)

    def OnReceiveRealData(self, szTrCode, result):
        try:
            s = "%s:%s:%s" % (result['호가시간'][0:2],result['호가시간'][2:4],result['호가시간'][4:6])
            self.label_hotime.setText(s)

            for i in range(0,10):
                self.매도호가컨트롤[i].setText(result['매도호가'][i])
                self.매수호가컨트롤[i].setText(result['매수호가'][i])
                self.매도호가잔량컨트롤[i].setText(result['매도호가잔량'][i])
                self.매수호가잔량컨트롤[i].setText(result['매수호가잔량'][i])

            self.label_offerremALL.setText(result['총매도호가잔량'])
            self.label_bidremALL.setText(result['총매수호가잔량'])
            self.label_donsigubun.setText(result['동시호가구분'])
            self.label_alloc_gubun.setText(result['배분적용구분'])
        except Exception as e:
            pass

    def AddCode(self):
        종목코드 = self.comboBox.currentText().strip()[0:6]

        self.kospi_askbid.UnadviseRealData()
        self.kosdaq_askbid.UnadviseRealData()

        if 종목코드 in self.kospi_codes:
            self.kospi_askbid.AdviseRealData(종목코드=종목코드)
        if 종목코드 in self.kosdaq_codes:
            self.kosdaq_askbid.AdviseRealData(종목코드=종목코드)


Ui_실시간정보, QtBaseClass_실시간정보 = uic.loadUiType(UI_DIR+"실시간주가.ui")
class 화면_실시간정보(QDialog, Ui_실시간정보):
    def __init__(self, parent=None):
        super(화면_실시간정보, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.parent = parent

        self.kospi_real = S3_(parent=self)

    def OnReceiveRealData(self, szTrCode, result):
        try:
            str = '{}:{} - {}--{}\r'.format(result['체결시간'], result['단축코드'], result['현재가'], result['체결량'])
            self.textBrowser.append(str)
        except Exception as e:
            pass

    def AddCode(self):
        종목코드 = self.comboBox.currentText().strip()
        self.comboBox.addItems([종목코드])
        self.kospi_real.AdviseRealData(종목코드=종목코드)

    def RemoveCode(self):
        종목코드 = self.comboBox.currentText().strip()
        self.kospi_real.UnadviseRealDataWithKey(종목코드=종목코드)


Ui_뉴스, QtBaseClass_뉴스 = uic.loadUiType(UI_DIR+"뉴스.ui")
class 화면_뉴스(QDialog, Ui_뉴스):
    def __init__(self, parent=None):
        super(화면_뉴스, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.parent = parent

        self.news = NWS(parent=self)

    def OnReceiveRealData(self, szTrCode, result):
        str = '{}:{} - {}\r'.format(result['날짜'], result['시간'], result['제목'])
        try:
            self.textBrowser.append(str)
        except Exception as e:
            pass

    def AddCode(self):
        self.news.AdviseRealData()

    def RemoveCode(self):
        self.news.UnadviseRealData()


Ui_주문테스트, QtBaseClass_주문테스트 = uic.loadUiType(UI_DIR+"주문테스트.ui")
class 화면_주문테스트(QDialog, Ui_주문테스트):
    def __init__(self, parent=None):
        super(화면_주문테스트, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.parent = parent

        self.connection = self.parent.connection

        # 계좌정보 불러오기
        nCount = self.connection.ActiveX.GetAccountListCount()
        for i in range(nCount):
            self.comboBox.addItem(self.connection.ActiveX.GetAccountList(i))

        self.QA_CSPAT00600 = CSPAT00600(parent=self)

        self.setup()

    def setup(self):
        self.XR_SC1 = SC1(parent=self)
        self.XR_SC1.AdviseRealData()
        self.주문번호리스트 = []

    def OnReceiveMessage(self, systemError, messageCode, message):
        self.textEdit.insertPlainText("systemError:[%s] messageCode:[%s] message:[%s]\r" % (systemError, messageCode, message))

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 'CSPAT00600':
            df, df1 = result
            주문번호 = df1['주문번호'].values[0]
            self.textEdit.insertPlainText("주문번호 : %s\r" % 주문번호)
            if 주문번호 != '0':
                # 주문번호처리
                self.주문번호리스트.append(str(주문번호))

    def OnReceiveRealData(self, szTrCode, result):
        try:
            self.textEdit.insertPlainText(szTrCode+'\r')
            self.textEdit.insertPlainText(str(result)+'\r')
        except Exception as e:
            pass

        if szTrCode == 'SC1':
            체결시각 = result['체결시각']
            단축종목번호 = result['단축종목번호'].strip().replace('A','')
            종목명 = result['종목명']
            매매구분 = result['매매구분']
            주문번호 = result['주문번호']
            체결번호 = result['체결번호']
            주문수량 = result['주문수량']
            주문가격 = result['주문가격']
            체결수량 = result['체결수량']
            체결가격 = result['체결가격']
            주문평균체결가격 = result['주문평균체결가격']
            주문계좌번호 = result['주문계좌번호']

            # 내가 주문한 것이 맞을 경우 처리
            if 주문번호 in self.주문번호리스트:
                s = "[%s] %s %s %s %s %s %s %s %s %s %s %s" % (szTrCode,체결시각,단축종목번호,매매구분,주문번호,체결번호,주문수량,주문가격,체결수량,체결가격,주문평균체결가격,주문계좌번호)
                try:
                    self.textEdit.insertPlainText(s + '\r')
                except Exception as e:
                    pass

                일자 = "{:%Y-%m-%d}".format(datetime.datetime.now())
                with sqlite3.connect(DATABASE) as conn:
                    query = 'insert into 거래결과(로봇명, UUID, 일자, 체결시각, 단축종목번호, 종목명, 매매구분, 주문번호, 체결번호, 주문수량, 주문가격, 체결수량, 체결가격, 주문평균체결가격) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                    data = ['주문테스트', '주문테스트-UUID', 일자, 체결시각, 단축종목번호, 종목명, 매매구분, 주문번호, 체결번호, 주문수량, 주문가격, 체결수량, 체결가격, 주문평균체결가격]
                    cursor = conn.cursor()
                    cursor.execute(query, data)
                    conn.commit()

    def Order(self):
        계좌번호 = self.comboBox.currentText().strip()
        비밀번호 = self.lineEdit_pwd.text().strip()
        종목코드 = self.lineEdit_code.text().strip()
        주문가 = self.lineEdit_price.text().strip()
        주문수량 = self.lineEdit_amt.text().strip()
        매매구분 = self.lineEdit_bs.text().strip()
        호가유형 = self.lineEdit_hoga.text().strip()
        신용거래 = self.lineEdit_sin.text().strip()
        주문조건 = self.lineEdit_jogun.text().strip()

        self.QA_CSPAT00600.Query(계좌번호=계좌번호, 입력비밀번호=비밀번호, 종목번호=종목코드, 주문수량=주문수량, 주문가=주문가, 매매구분=매매구분, 호가유형코드=호가유형, 신용거래코드=신용거래, 주문조건구분=주문조건)


Ui_외부신호2eBEST, QtBaseClass_외부신호2eBEST = uic.loadUiType(UI_DIR+"외부신호2eBEST.ui")
class 화면_외부신호2eBEST(QDialog, Ui_외부신호2eBEST):
    def __init__(self, parent=None):
        super(화면_외부신호2eBEST, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.parent = parent

        self.pathname = os.path.dirname(sys.argv[0])
        self.file = "%s\\" % os.path.abspath(self.pathname)

        self.매도 = 1
        self.매수 = 2
        self.매수방법 = '00'
        self.매도방법 = '00'
        self.조건없음 = 0
        self.조건IOC = 1
        self.조건FOK = 2

        self.신용거래코드 = '000'

        self.주문번호리스트 = []
        self.QA_CSPAT00600 = CSPAT00600(parent=self)
        self.XR_SC1 = SC1(parent=self)
        self.XR_SC1.AdviseRealData()

        self.connection = self.parent.connection

        # 계좌정보 불러오기
        nCount = self.connection.ActiveX.GetAccountListCount()
        for i in range(nCount):
            self.comboBox.addItem(self.connection.ActiveX.GetAccountList(i))

    def OnReceiveMessage(self, systemError, messageCode, message):
        s = "\r%s %s %s\r" % (systemError, messageCode, message)
        try:
            self.plainTextEdit.insertPlainText(s)
        except Exception as e:
            pass

    def OnReceiveData(self, szTrCode, result):
        if szTrCode == 'CSPAT00600':
            df, df1 = result
            주문번호 = df1['주문번호'].values[0]
            if 주문번호 != '0':
                self.주문번호리스트.append(str(주문번호))
                s = "주문번호 : %s\r" % 주문번호
                try:
                    self.plainTextEdit.insertPlainText(s)
                except Exception as e:
                    pass

    def OnReceiveRealData(self, szTrCode, result):
        if szTrCode == 'SC1':
            체결시각 = result['체결시각']
            단축종목번호 = result['단축종목번호'].strip().replace('A','')
            종목명 = result['종목명']
            매매구분 = result['매매구분']
            주문번호 = result['주문번호']
            체결번호 = result['체결번호']
            주문수량 = result['주문수량']
            주문가격 = result['주문가격']
            체결수량 = result['체결수량']
            체결가격 = result['체결가격']
            주문평균체결가격 = result['주문평균체결가격']
            주문계좌번호 = result['주문계좌번호']

            # 내가 주문한 것이 체결된 경우 처리
            if 주문번호 in self.주문번호리스트:
                s = "\r주문체결[%s] : %s %s %s %s %s %s %s %s %s %s %s\r" % (szTrCode,체결시각,단축종목번호,매매구분,주문번호,체결번호,주문수량,주문가격,체결수량,체결가격,주문평균체결가격,주문계좌번호)
                try:
                    self.plainTextEdit.insertPlainText(s)
                except Exception as e:
                    pass

                일자 = "{:%Y-%m-%d}".format(datetime.datetime.now())
                with sqlite3.connect(DATABASE) as conn:
                    query = 'insert into 거래결과(로봇명, UUID, 일자, 체결시각, 단축종목번호, 종목명, 매매구분, 주문번호, 체결번호, 주문수량, 주문가격, 체결수량, 체결가격, 주문평균체결가격) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                    data = ['툴박스2EBEST', '툴박스2EBEST-UUID', 일자, 체결시각, 단축종목번호, 종목명, 매매구분, 주문번호, 체결번호, 주문수량, 주문가격, 체결수량, 체결가격, 주문평균체결가격]
                    cursor = conn.cursor()
                    cursor.execute(query, data)
                    conn.commit()


    def OnReadFile(self, line):
        try:
            self.plainTextEdit.insertPlainText("\r>> " +line.strip() + '\r')
        except Exception as e:
            pass

        lst = line.strip().split(',')

        try:
            시각, 종류, 단축코드, 가격, 수량 = lst
            가격 = int(가격)
            수량 = int(수량)

            if 종류 == '매수':
                self.QA_CSPAT00600.Query(계좌번호=self.계좌번호, 입력비밀번호=self.비밀번호, 종목번호=단축코드, 주문수량=수량, 주문가=가격, 매매구분=self.매수, 호가유형코드=self.매수방법, 신용거래코드=self.신용거래코드, 주문조건구분=self.조건없음)
            if 종류 == '매도':
                self.QA_CSPAT00600.Query(계좌번호=self.계좌번호, 입력비밀번호=self.비밀번호, 종목번호=단축코드, 주문수량=수량, 주문가=가격, 매매구분=self.매도, 호가유형코드=self.매도방법, 신용거래코드=self.신용거래코드, 주문조건구분=self.조건없음)
        except Exception as e:
            pass

    def fileselect(self):
        ret = QFileDialog.getOpenFileName(self, 'Open file',self.file, "CSV,TXT(*.csv;*.txt)")
        self.file = ret[0]
        self.lineEdit.setText(self.file)

    def StartWatcher(self):
        self.계좌번호 = self.comboBox.currentText().strip()
        self.비밀번호 = self.lineEdit_pwd.text().strip()

        self.fw = FileWatcher(filename=self.file, callback=self.OnReadFile, encoding='utf-8')
        self.fw.start()


Ui_거래결과, QtBaseClass_거래결과 = uic.loadUiType(UI_DIR+"거래결과.ui")
class 화면_거래결과(QDialog, Ui_거래결과):
    def __init__(self, parent=None):
        super(화면_거래결과, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('거래결과 조회')
        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        self.columns = []

        with sqlite3.connect(DATABASE) as conn:
            query = "select distinct 로봇명 from 거래결과 order by 로봇명"
            df = pdsql.read_sql_query(query, con=conn)
            for name in df['로봇명'].values.tolist():
                self.comboBox.addItem(name)

    def inquiry(self):
        로봇명 = self.comboBox.currentText().strip()
        with sqlite3.connect(DATABASE) as conn:
            query = """
                select 로봇명, UUID, 일자, 체결시각, 단축종목번호, 종목명, 매매구분, 주문번호, 체결번호, 주문수량, 주문가격, 체결수량, 체결가격, 주문평균체결가격 
                from 거래결과
                where  로봇명='%s'
                order by 일자, 체결시각
            """ % 로봇명
            df = pdsql.read_sql_query(query, con=conn)

            self.model.update(df)
            for i in range(len(df.columns)):
                self.tableView.resizeColumnToContents(i)


Ui_버전, QtBaseClass_버전 = uic.loadUiType(UI_DIR+"버전.ui")
class 화면_버전(QDialog, Ui_버전):
    def __init__(self, parent=None):
        super(화면_버전, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.setWindowTitle('버전')
        self.parent = parent

        self.model = PandasModel()
        self.tableView.setModel(self.model)

        df = DataFrame(data=프로그램정보,columns=['A','B'])

        self.model.update(df)
        for i in range(len(df.columns)):
            self.tableView.resizeColumnToContents(i)

########################################################################################################################
# sky work !!!
########################################################################################################################
class screen_update_worker(QThread):

    finished = pyqtSignal(dict)
    
    def run(self):
        
        while True:

            data = {}

            # atm index 중심으로 위,아래 15개 요청(총 31개)
            for actval in opt_actval[atm_index - 15:atm_index + 16]:
            #for actval in opt_actval:

                data[actval] = self.get_data_infos(actval)

            # dummy 요청(안하면 screen update로 못들어감 ?)
            for actval in opt_actval[option_pairs_count - 1:option_pairs_count]:

                data[actval] = self.get_data_infos(actval)
            
            self.finished.emit(data)  
            self.msleep(500)

    def get_data_infos(self, actval):

        try:
            index = opt_actval.index(actval)

            call_curve_data = df_plotdata_call.iloc[index].values.tolist()
            put_curve_data = df_plotdata_put.iloc[index].values.tolist()

            # COMBO 1
            if comboindex1 == 0:

                curve1_data = df_plotdata_fut_volume.iloc[0].values.tolist()
                curve2_data = None
                curve3_data = None

            elif comboindex1 == 1:                             
                
                curve1_data = df_plotdata_call_volume.iloc[0].values.tolist()
                curve2_data = df_plotdata_put_volume.iloc[0].values.tolist()
                curve3_data = df_plotdata_volume_cha.iloc[0].values.tolist()

            elif comboindex1 == 2:
                
                curve1_data = df_plotdata_call_oi.iloc[0].values.tolist()
                curve2_data = df_plotdata_put_oi.iloc[0].values.tolist() 
                curve3_data = None 

            elif comboindex1 == 3:

                curve1_data = df_plotdata_two_sum.iloc[0].values.tolist()
                curve2_data = df_plotdata_two_cha.iloc[0].values.tolist()
                curve3_data = None  

            elif comboindex1 == 4:     

                curve1_data = df_plotdata_kp200.iloc[0].values.tolist()
                curve2_data = df_plotdata_fut.iloc[0].values.tolist()
                curve3_data = None

            elif comboindex1 == 5: 

                curve1_data = df_plotdata_sp500.iloc[0].values.tolist()
                curve2_data = None
                curve3_data = None

            elif comboindex1 == 6: 

                curve1_data = df_plotdata_dow.iloc[0].values.tolist()
                curve2_data = None
                curve3_data = None

            elif comboindex1 == 7: 

                curve1_data = df_plotdata_nasdaq.iloc[0].values.tolist()
                curve2_data = None
                curve3_data = None
            else:
                pass

            # COMBO 2
            if comboindex2 == 0:
                
                curve4_data = df_plotdata_call_volume.iloc[0].values.tolist()
                curve5_data = df_plotdata_put_volume.iloc[0].values.tolist()
                curve6_data = df_plotdata_volume_cha.iloc[0].values.tolist()
            
            elif comboindex2 == 1:                
                
                curve4_data = df_plotdata_call_oi.iloc[0].values.tolist()
                curve5_data = df_plotdata_put_oi.iloc[0].values.tolist()
                curve6_data = None 
            
            elif comboindex2 == 2:

                curve4_data = df_plotdata_fut_volume.iloc[0].values.tolist()
                curve5_data = None
                curve6_data = None  

            elif comboindex2 == 3:

                curve4_data = df_plotdata_two_sum.iloc[0].values.tolist()
                curve5_data = df_plotdata_two_cha.iloc[0].values.tolist()
                curve6_data = None 

            elif comboindex2 == 4:

                curve4_data = None
                curve5_data = None
                curve6_data = None

            elif comboindex2 == 5:

                curve4_data = df_plotdata_sp500.iloc[0].values.tolist()
                curve5_data = None
                curve6_data = None 

            elif comboindex2 == 6:

                curve4_data = df_plotdata_dow.iloc[0].values.tolist()
                curve5_data = None
                curve6_data = None 

            elif comboindex2 == 7:

                curve4_data = df_plotdata_nasdaq.iloc[0].values.tolist()
                curve5_data = None
                curve6_data = None 
            else:
                pass
            
            if UI_STYLE == 'Vertical_view.ui':

                # COMBO 3
                if comboindex3 == 0:

                    plot3_data = df_plotdata_dow.iloc[0].values.tolist()

                elif comboindex3 == 1:                             

                    plot3_data = df_plotdata_sp500.iloc[0].values.tolist()

                elif comboindex3 == 2:

                    plot3_data = df_plotdata_nasdaq.iloc[0].values.tolist()
                else:
                    pass

                # COMBO 4
                if comboindex4 == 0:

                    plot4_1_data = df_plotdata_fut.iloc[0].values.tolist()
                    plot4_2_data = df_plotdata_kp200.iloc[0].values.tolist()

                elif comboindex4 == 1:                             

                    plot4_1_data = df_plotdata_fut_volume.iloc[0].values.tolist()
                    plot4_2_data = None
                else:
                    pass  
            else:
                pass
            
            if UI_STYLE == 'Vertical_view.ui':

                return call_curve_data, put_curve_data, curve1_data, curve2_data, curve3_data, curve4_data, \
                    curve5_data, curve6_data, plot3_data, plot4_1_data, plot4_2_data
            else:
                return call_curve_data, put_curve_data, curve1_data, curve2_data, curve3_data, curve4_data, \
                    curve5_data, curve6_data

        except:

            if UI_STYLE == 'Vertical_view.ui':
                return None, None, None, None, None, None, None, None, None, None, None 
            else:
                return None, None, None, None, None, None, None, None

########################################################################################################################

########################################################################################################################
class t8415_Call_Worker(QThread):

    finished = pyqtSignal(int)

    def run(self):
        
        while True:

            self.finished.emit(call_t8415_count)
            self.msleep(1100)
########################################################################################################################

########################################################################################################################
class t8415_Put_Worker(QThread):

    finished = pyqtSignal(int)

    def run(self):

        while True:

            self.finished.emit(put_t8415_count)
            self.msleep(1100)
########################################################################################################################

########################################################################################################################
class t8416_Call_Worker(QThread):

    finished = pyqtSignal(int)

    def run(self):

        while True:

            self.finished.emit(call_t8416_count)
            self.msleep(1100)
########################################################################################################################

########################################################################################################################
class t8416_Put_Worker(QThread):

    finished = pyqtSignal(int)

    def run(self):

        while True:

            self.finished.emit(put_t8416_count)
            self.msleep(1100)
########################################################################################################################

########################################################################################################################
# 텔레그램 송수신시 약 1.2초 정도 전달지연 시간 발생함
class telegram_send_worker(QThread):

    finished = pyqtSignal(str)

    def run(self):

        while True:
            
            dt = datetime.datetime.now()
            
            global telegram_toggle, MONTH_1, MONTH_2, MONTH_3, FLAG_OLOH 

            telegram_toggle = not telegram_toggle

            str = 'None'
            
            # 텔레그램 명령어 파싱
            element = telegram_command.split()
            
            command_count = len(element)
            
            command = []

            for i in range(command_count):

                command.append(element[i])   

            if command_count == 1 and command[0] == 'Stop':

                MONTH_1 = False
                MONTH_2 = False
                MONTH_3 = False
                FLAG_OLOH = False

            elif command_count == 1 and command[0] == '/start':

                MONTH_1 = True
                MONTH_2 = True
                MONTH_3 = True
                FLAG_OLOH = True

            elif command_count == 2 and command[0] == 'Go':

                if command[1] == '1':

                    MONTH_1 = True
                    MONTH_2 = False
                    MONTH_3 = False
                    FLAG_OLOH = False

                elif command[1] == '2':

                    MONTH_1 = False
                    MONTH_2 = True
                    MONTH_3 = False
                    FLAG_OLOH = False

                elif command[1] == '3':

                    MONTH_1 = False
                    MONTH_2 = False
                    MONTH_3 = True
                    FLAG_OLOH = False

                elif command[1] == '12':

                    MONTH_1 = True
                    MONTH_2 = True
                    MONTH_3 = False
                    FLAG_OLOH = False

                elif command[1] == '123':

                    MONTH_1 = True
                    MONTH_2 = True
                    MONTH_3 = True
                    FLAG_OLOH = False
                
                elif command[1] == '1234':

                    MONTH_1 = True
                    MONTH_2 = True
                    MONTH_3 = True
                    FLAG_OLOH = True
                else:
                    pass
            else:
                pass           

            if TELEGRAM_SERVICE == 'ON' and flag_telegram_on and (command[0] == 'Go' or command[0] == '/start'):

                if telegram_toggle:

                    # 선물 OL/OH 알람(NM, MAN인 경우만)
                    if n_oloh_str != '' and FLAG_OLOH:

                        str = n_oloh_str
                        ToTelegram(str)
                    else:
                        pass

                    # 옵션맥점 발생 알람
                    if call_low_node_str != '' and (MONTH_1 or MONTH_2 or MONTH_3):

                        str = call_low_node_str
                        ToTelegram(str)
                    else:
                        pass

                    if call_high_node_str != '' and (MONTH_1 or MONTH_2 or MONTH_3):

                        str = call_high_node_str
                        ToTelegram(str)
                    else:
                        pass

                    if put_low_node_str != '' and (MONTH_1 or MONTH_2 or MONTH_3):

                        str = put_low_node_str
                        ToTelegram(str)
                    else:
                        pass

                    if put_high_node_str != '' and (MONTH_1 or MONTH_2 or MONTH_3):

                        str = put_high_node_str
                        ToTelegram(str)
                    else:
                        pass

                    '''
                    # 콜 원웨이 알람 --> 비대칭장으로 대체
                    if call_oneway_level3:

                        str = oneway_str
                        ToTelegram(str)

                    elif call_oneway_level4:

                        str = oneway_str
                        ToTelegram(str)

                    elif call_oneway_level5:

                        str = oneway_str
                        ToTelegram(str)
                    else:
                        pass

                    # 풋 원웨이 알람
                    if put_oneway_level3:

                        str = oneway_str
                        ToTelegram(str)

                    elif put_oneway_level4:

                        str = oneway_str
                        ToTelegram(str)

                    elif put_oneway_level5:

                        str = oneway_str
                        ToTelegram(str)
                    else:
                        pass
                    '''

                    # 비대칭장(장의 형태) 알람
                    if (비대칭장 != '' and FLAG_OLOH) and (MONTH_1 or MONTH_2 or MONTH_3):

                        str = 비대칭장
                        ToTelegram(str)
                    else:
                        pass
                else:
                    pass                
                
                # kp200 맥점 알람
                if kp200_low_node_str != '':

                    str = kp200_low_node_str
                    ToTelegram(str)
                else:
                    pass

                if kp200_high_node_str != '':

                    str = kp200_high_node_str
                    ToTelegram(str)
                else:
                    pass
            else:
                pass

            self.finished.emit(str)
            self.msleep(1000 * TELEGRAM_SEND_INTERVAL)

        return

########################################################################################################################

########################################################################################################################
class telegram_listen_worker(QThread):

    finished = pyqtSignal(str)

    def run(self):

        while True:

            if TELEGRAM_SERVICE == 'ON' and flag_telegram_on:

                # 텔레그램 메시지 수신
                str = FromTelegram()
            else:
                str = 'Stopped by Tool...'

            self.finished.emit(str)
            self.msleep(1000 * TELEGRAM_POLLING_INTERVAL)
            
########################################################################################################################
# 당월물 옵션전광판 class
########################################################################################################################
#Ui_당월물옵션전광판, QtBaseClass_당월물옵션전광판 = uic.loadUiType(UI_DIR+"당월물옵션전광판.ui")

Ui_당월물옵션전광판, QtBaseClass_당월물옵션전광판 = uic.loadUiType(UI_DIR + UI_STYLE)

class 화면_당월물옵션전광판(QDialog, Ui_당월물옵션전광판):

    def __init__(self, parent=None):
        super(화면_당월물옵션전광판, self).\
            __init__(parent, flags=Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.parent = parent

        global 모니터번호
        
        global MANGI_YAGAN, current_month, next_month, month_after_next, TARGET_MONTH_SELECT, MONTH_FIRSTDAY
        global cm_option_title, CURRENT_MONTH, NEXT_MONTH, MONTH_AFTER_NEXT, SP500, DOW, NASDAQ, fut_code
        global overnight, kse_start_hour, ovc_start_hour
        
        self.상태그림 = ['▼', '▲']
        self.상태문자 = ['매도', '대기', '매수']
        self.특수문자 = \
        ['☆', '★', '※', '○', '●', '◎', '√', '↗', '⬈', '↘', '⬊', '↑', '⬆', '↓', '⬇', '↕', '♣', '♠', '♥', '◆', 'Δ', '【', '】', '🕘', '✔', '⬍', '⌛', '⬀ ⬁ ⬂ ⬃']

        self.특수문자_숫자 = ['⑴ ⑵ ⑶ ⑷ ⑸ ⑹ ⑺ ⑻ ⑼ ⑽ ⓵ ⓶ ⓷ ⓸ ⓹ ⓺ ⓻ ⓼ ⓽ ⓾']
        
        # 다중모니터와 WQHD 해상도에서 초기화면 표시를 위한 Setting
        모니터번호 = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        screen = QtGui.QDesktopWidget().screenGeometry(모니터번호)

        print('모니터화면 번호 = ', 모니터번호)
        
        print('current month = %s, month firstday = %s, next month = %s, month after next = %s, next month select = %s, SP500 = %s, DOW = %s, NASDAQ = %s' \
            % (CURRENT_MONTH, MONTH_FIRSTDAY, NEXT_MONTH, MONTH_AFTER_NEXT, TARGET_MONTH_SELECT, SP500, DOW, NASDAQ))

        left = screen.left()
        top = screen.top()

        if screen.width() > 1920:

            width = 1920
        else:
            width = screen.width()

        if screen.height() > 1080:

            height = 1080
        else:
            height = screen.height()

        self.setGeometry(left, top + 30, width, height - 60)

        self.showMaximized()

        dt = datetime.datetime.now()
        
        nowDate = now.strftime('%Y-%m-%d')
        current_str = dt.strftime('%H:%M:%S')

        current_month = int(CURRENT_MONTH[4:6])
        next_month = int(NEXT_MONTH[4:6])
        month_after_next = int(MONTH_AFTER_NEXT[4:6])

        if 4 < int(current_str[0:2]) < 야간선물_기준시간:

            if TARGET_MONTH_SELECT == 1:

                if os.path.exists('SkyBot_CM.exe'):

                    buildtime = time.ctime(os.path.getmtime('SkyBot_CM.exe'))
                else:
                    buildtime = time.ctime(os.path.getmtime(__file__))

            elif TARGET_MONTH_SELECT == 2:

                if os.path.exists('SkyBot_NM.exe'):

                    buildtime = time.ctime(os.path.getmtime('SkyBot_NM.exe'))
                else:
                    buildtime = time.ctime(os.path.getmtime(__file__))

            else:
                if os.path.exists('SkyBot_MAN.exe'):

                    buildtime = time.ctime(os.path.getmtime('SkyBot_MAN.exe'))
                else:
                    buildtime = time.ctime(os.path.getmtime(__file__))
        else:

            if TARGET_MONTH_SELECT == 1:

                if os.path.exists('SkyBot_CM.exe'):

                    buildtime = time.ctime(os.path.getmtime('SkyBot_CM.exe'))
                else:
                    buildtime = time.ctime(os.path.getmtime(__file__))

            elif TARGET_MONTH_SELECT == 2:

                if os.path.exists('SkyBot_NM.exe'):

                    buildtime = time.ctime(os.path.getmtime('SkyBot_NM.exe'))
                else:
                    buildtime = time.ctime(os.path.getmtime(__file__))

            else:
                if os.path.exists('SkyBot_MAN.exe'):

                    buildtime = time.ctime(os.path.getmtime('SkyBot_MAN.exe'))
                else:
                    buildtime = time.ctime(os.path.getmtime(__file__))
        
        #self.telegram_flag = True
        self.pushButton_remove.setStyleSheet("background-color: lightGray")

        if 4 < int(current_str[0:2]) < 야간선물_기준시간:

            if TARGET_MONTH_SELECT == 1:

                cm_option_title = repr(current_month) + '월물 주간 선물옵션 전광판' + '(' + today_str_title + ')' + ' build : ' + buildtime
                ToTelegram("{0}월물 주간 선물옵션 SkyBot이 실행되었습니다.".format(repr(current_month)))

            elif TARGET_MONTH_SELECT == 2:

                cm_option_title = repr(next_month) + '월물 주간 선물옵션 전광판' + '(' + today_str_title + ')' + ' build : ' + buildtime
                ToTelegram("{0}월물 주간 선물옵션 SkyBot이 실행되었습니다.".format(repr(next_month)))

            else:
                cm_option_title = repr(month_after_next) + '월물 주간 선물옵션 전광판' + '(' + today_str_title + ')' + ' build : ' + buildtime
                ToTelegram("{0}월물 주간 선물옵션 SkyBot이 실행되었습니다.".format(repr(month_after_next)))
        else:
            overnight = True

            kse_start_hour = 18            

            if MANGI_YAGAN == 'YES':

                if TARGET_MONTH_SELECT == 1:

                    cm_option_title = repr(next_month) + '월물 야간 선물옵션 전광판' + '(' + today_str_title + ')' + ' build : ' + buildtime
                    ToTelegram("{0}월물 야간 선물옵션 SkyBot이 실행되었습니다.".format(repr(next_month)))

                    print('next_month =', next_month)

                elif TARGET_MONTH_SELECT == 2:

                    cm_option_title = repr(month_after_next) + '월물 야간 선물옵션 전광판' + '(' + today_str_title + ')' + ' build : ' + buildtime
                    ToTelegram("{0}월물 야간 선물옵션 SkyBot이 실행되었습니다.".format(repr(month_after_next)))
                else:
                    pass
            else:
                if TARGET_MONTH_SELECT == 1:

                    cm_option_title = repr(current_month) + '월물 야간 선물옵션 전광판' + '(' + today_str_title + ')' + ' build : ' + buildtime
                    ToTelegram("{0}월물 야간 선물옵션 SkyBot이 실행되었습니다.".format(repr(current_month)))

                elif TARGET_MONTH_SELECT == 2:

                    cm_option_title = repr(next_month) + '월물 야간 선물옵션 전광판' + '(' + today_str_title + ')' + ' build : ' + buildtime
                    ToTelegram("{0}월물 야간 선물옵션 SkyBot이 실행되었습니다.".format(repr(next_month)))

                else:
                    cm_option_title = repr(month_after_next) + '월물 야간 선물옵션 전광판' + '(' + today_str_title + ')' + ' build : ' + buildtime
                    ToTelegram("{0}월물 야간 선물옵션 SkyBot이 실행되었습니다.".format(repr(month_after_next)))

        ovc_start_hour = kse_start_hour - 1 

        print('장시작 준비시간 =', ovc_start_hour)

        self.setWindowTitle(cm_option_title)
        
        # 사용할 쓰레드 등록
        # 쓰레드 시작은 start(), 종료는 terminate()
        self.t8416_callworker = t8416_Call_Worker()
        self.t8416_callworker.finished.connect(self.t8416_call_request)

        self.t8416_putworker = t8416_Put_Worker()
        self.t8416_putworker.finished.connect(self.t8416_put_request)

        self.screen_update_worker = screen_update_worker()
        self.screen_update_worker.finished.connect(self.update_screen)

        self.telegram_send_worker = telegram_send_worker()
        self.telegram_send_worker.finished.connect(self.send_telegram_message)

        self.telegram_listen_worker = telegram_listen_worker()
        self.telegram_listen_worker.finished.connect(self.listen_telegram_message)

        # 위젯 선언 및 초기화
        self.comboBox1.setStyleSheet("background-color: white")
        self.comboBox2.setStyleSheet("background-color: white")

        if UI_STYLE == 'Vertical_view.ui':

            self.comboBox3.setStyleSheet("background-color: white")
            self.comboBox4.setStyleSheet("background-color: white")
        else:
            pass
        
        self.pushButton_add.setStyleSheet("background-color: lightGray")
        
        self.label_msg.setText("🕘")
        self.label_msg.setStyleSheet('background-color: lawngreen; color: blue')
        #self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))

        self.label_atm.setText("Basis(양합:양차)")
        self.label_atm.setStyleSheet('background-color: yellow; color: black')
        #self.label_atm.setFont(QFont("Consolas", 9, QFont.Bold))
        
        self.label_kospi.setText("KOSPI: 가격 (전일대비, 등락율)")
        self.label_kospi.setStyleSheet('background-color: black ; color: yellow')
        self.label_kosdaq.setText("KOSDAQ: 가격 (전일대비, 등락율)")
        self.label_kosdaq.setStyleSheet('background-color: black ; color: yellow')
        self.label_samsung.setText("SAMSUNG: 가격 (전일대비, 등락율)")
        self.label_samsung.setStyleSheet('background-color: black ; color: yellow')

        self.label_1st.setText("S&P 500: 가격 (전일대비, 등락율)")
        self.label_1st.setStyleSheet('background-color: black ; color: yellow')
        self.label_2nd.setText("DOW: 가격 (전일대비, 등락율, 진폭)")
        self.label_2nd.setStyleSheet('background-color: black ; color: yellow')
        self.label_3rd.setText("NASDAQ: 가격 (전일대비, 등락율)")
        self.label_3rd.setStyleSheet('background-color: black ; color: yellow')

        stylesheet = "::section{Background-color: lightGray}"

        # call tablewidget 초기화
        self.tableWidget_call.setRowCount(nRowCount)
        self.tableWidget_call.setColumnCount(Option_column.OID.value + 1)
        
        self.tableWidget_call.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget_call.horizontalHeader().setFont(QFont("Consolas", 9, QFont.Bold))

        self.tableWidget_call.setHorizontalHeaderLabels(['C', '행사가', '▲:▼', '기준가', '월저', '월고', '전저', '전고', 
        '종가\n✓', '피봇\n✓', '시가\n✓', '시가갭\n(%)', '저가', '현재가', '고가', '대비\n(%)', '진폭', '∑PVP', '∑OI', 'OI↕'])
        self.tableWidget_call.verticalHeader().setVisible(False)

        cell_widget = []

        for i in range(nRowCount):
            
            cell_widget.append(QWidget())            
            lay_out = QHBoxLayout(cell_widget[i])
            lay_out.addWidget(QCheckBox())
            lay_out.setAlignment(Qt.AlignCenter)          
            cell_widget[i].setLayout(lay_out)         
            self.tableWidget_call.setCellWidget(i, 0, cell_widget[i])
            
        self.tableWidget_call.resizeColumnsToContents()

        # put tablewidget 초기화
        self.tableWidget_put.setRowCount(nRowCount)
        self.tableWidget_put.setColumnCount(Option_column.OID.value + 1)

        self.tableWidget_put.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget_put.horizontalHeader().setFont(QFont("Consolas", 9, QFont.Bold))

        self.tableWidget_put.setHorizontalHeaderLabels(['P', '행사가', '▲:▼', '기준가', '월저', '월고', '전저', '전고', 
        '종가\n✓', '피봇\n✓', '시가\n✓', '시가갭\n(%)', '저가', '현재가', '고가', '대비\n(%)', '진폭', '∑PVP', '∑OI', 'OI↕'])
        self.tableWidget_put.verticalHeader().setVisible(False)

        cell_widget = []

        for i in range(nRowCount):

            cell_widget.append(QWidget())            
            lay_out = QHBoxLayout(cell_widget[i])
            lay_out.addWidget(QCheckBox())
            lay_out.setAlignment(Qt.AlignCenter)           
            cell_widget[i].setLayout(lay_out)
            self.tableWidget_put.setCellWidget(i, 0, cell_widget[i])

        self.tableWidget_put.resizeColumnsToContents()
        
        # 선물 tablewidget 초기화
        self.tableWidget_fut.setRowCount(3)
        self.tableWidget_fut.setColumnCount(Futures_column.OID.value + 1)

        self.tableWidget_fut.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget_fut.horizontalHeader().setFont(QFont("Consolas", 9, QFont.Bold))

        self.tableWidget_fut.setHorizontalHeaderLabels(
            ['F', '▲▼', 'MSC', 'MDC', 'MSR', 'MDR', 'CR', 'RR', '전저', '전고', '종가', '피봇', '시가', '시가갭', '저가',
             '현재가', '고가', '대비', '진폭', 'PVP', 'FR', 'OI', 'OI↕'])
        self.tableWidget_fut.verticalHeader().setVisible(False)

        item = QTableWidgetItem("{0}".format('CME'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(0, 0, item)

        item = QTableWidgetItem("{0}".format('KSE'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(1, 0, item)

        item = QTableWidgetItem("{0}".format('KP200'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(녹색))
        self.tableWidget_fut.setItem(2, 0, item)
        
        self.tableWidget_fut.resizeColumnsToContents()

        # Quote tablewidget 초기화
        self.tableWidget_quote.setRowCount(1)
        self.tableWidget_quote.setColumnCount(Quote_column.미결종합.value)

        self.tableWidget_quote.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget_quote.horizontalHeader().setFont(QFont("Consolas", 9, QFont.Bold))

        self.tableWidget_quote.setHorizontalHeaderLabels(['C-MSCC', 'C-MDCC', 'C-MSCR', 'C-MDCR',
                                                          'P-MSCC', 'P-MDCC', 'P-MSCR', 'P-MDCR', '콜건수비', '콜잔량비',
                                                          '풋건수비', '풋잔량비', '∑CRΔ/∑RRΔ', '∑COI:∑POI'])
        self.tableWidget_quote.verticalHeader().setVisible(False)

        header = self.tableWidget_quote.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(12, QHeaderView.Stretch)
        self.tableWidget_quote.verticalHeader().setStretchLastSection(True)
        self.tableWidget_quote.clearContents()

        # 수급 tablewidget 초기화
        self.tableWidget_supply.setRowCount(1)
        self.tableWidget_supply.setColumnCount(Supply_column.프로그램.value + 1)

        self.tableWidget_supply.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget_supply.horizontalHeader().setFont(QFont("Consolas", 9, QFont.Bold))

        self.tableWidget_supply.setHorizontalHeaderLabels(['외인선물', '프로그램', '외인현물', '개인선물', '기관선물', '∑선물/∑현물'])
        self.tableWidget_supply.verticalHeader().setVisible(False)

        header = self.tableWidget_supply.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        self.tableWidget_supply.verticalHeader().setStretchLastSection(True)
        self.tableWidget_supply.clearContents()

        if overnight:

            self.comboBox1.addItems(['1. FV-Plot', '2. OV-Plot', '3. None', '4. HC-Plot', '5. FP-Plot', '6. S&P 500', '7. DOW', '8. NASDAQ'])
            self.comboBox1.currentIndexChanged.connect(self.cb1_selectionChanged)
            
            self.comboBox2.addItems(['1. OV-Plot', '2. None', '3. FV-Plot', '4. HC-Plot', '5. OP-Plot', '6. S&P 500', '7. DOW', '8. NASDAQ'])
            self.comboBox2.currentIndexChanged.connect(self.cb2_selectionChanged)
             
        else:
            self.comboBox1.addItems(['1. FV-Plot', '2. OV-Plot', '3. OO-Plot', '4. HC-Plot', '5. FP-Plot', '6. S&P 500', '7. DOW', '8. NASDAQ'])
            self.comboBox1.currentIndexChanged.connect(self.cb1_selectionChanged)
            
            self.comboBox2.addItems(['1. OV-Plot', '2. OO-Plot', '3. FV-Plot', '4. HC-Plot', '5. OP-Plot', '6. S&P 500', '7. DOW', '8. NASDAQ'])
            self.comboBox2.currentIndexChanged.connect(self.cb2_selectionChanged)

        if UI_STYLE == 'Vertical_view.ui':

            self.comboBox3.addItems(['1. DOW', '2. S&P 500', '3. NASDAQ'])
            self.comboBox3.currentIndexChanged.connect(self.cb3_selectionChanged)

            self.comboBox4.addItems(['1. FP-Plot', '2. FV-Plot'])
            self.comboBox4.currentIndexChanged.connect(self.cb4_selectionChanged) 
        else:
            pass  

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.Plot1.enableAutoRange('y', True)
        self.Plot1.plotItem.showGrid(True, True, 0.5)
        self.Plot1.setRange(xRange=[0, 선물장간_시간차 + day_timespan], padding=0)        

        self.Plot2.enableAutoRange('y', True)
        self.Plot2.plotItem.showGrid(True, True, 0.5)
        self.Plot2.setRange(xRange=[0, 선물장간_시간차 + day_timespan], padding=0)
        self.Plot2.setXLink(self.Plot1) 

        if UI_STYLE == 'Vertical_view.ui':

            self.Plot3.enableAutoRange('y', True)
            self.Plot3.plotItem.showGrid(True, True, 0.5)
            self.Plot3.setRange(xRange=[0, 선물장간_시간차 + day_timespan], padding=0)
            self.Plot3.setXLink(self.Plot1)

            self.Plot4.enableAutoRange('y', True)
            self.Plot4.plotItem.showGrid(True, True, 0.5)
            self.Plot4.setRange(xRange=[0, 선물장간_시간차 + day_timespan], padding=0)
            self.Plot4.setXLink(self.Plot1)
        else:
            pass

        global plot1_time_line_start, plot1_time_line_yagan_start, plot1_time_line, plot1_fut_price_curve, plot1_kp200_curve
        global plot1_fut_jl_line, plot1_fut_jh_line, plot1_fut_pivot_line, plot1_ovc_open_line        
        global plot1_fut_volume_curve, plot1_fut_volume_plus_curve, plot1_fut_volume_minus_curve
        global plot1_call_oi_curve, plot1_put_oi_curve
        global plot1_call_volume_curve, plot1_put_volume_curve, plot1_volume_cha_curve
        global plot1_two_sum_curve, plot1_two_cha_curve
        global plot1_sp500_curve, plot1_dow_curve, plot1_nasdaq_curve
        global plot1_hc_high_line, plot1_hc_low_line
        global plot1_atm_high_line, plot1_atm_low_line

        global plot2_fut_volume_curve, plot2_fut_volume_plus_curve, plot2_fut_volume_minus_curve        
        global plot2_call_oi_curve, plot2_put_oi_curve        
        global plot2_call_volume_curve, plot2_put_volume_curve, plot2_volume_cha_curve        
        global plot2_two_sum_curve, plot2_two_cha_curve
        global plot2_sp500_curve, plot2_dow_curve, plot2_nasdaq_curve        
        global plot2_time_line_start, plot2_time_line_yagan_start, plot2_time_line, plot2_ovc_open_line
        global plot2_hc_high_line, plot2_hc_low_line
        global mv_line, call_curve, put_curve
        
        # Plot1
        plot1_time_line_start = self.Plot1.addLine(x=0, y=None, pen=tpen)
        plot1_time_line_yagan_start = self.Plot1.addLine(x=0, y=None, pen=tpen)
        plot1_time_line = self.Plot1.addLine(x=0, y=None, pen=tpen1)
        
        plot1_fut_jl_line = self.Plot1.addLine(x=None, pen=goldenrod_pen)
        plot1_fut_jh_line = self.Plot1.addLine(x=None, pen=gold_pen)        
        plot1_fut_pivot_line = self.Plot1.addLine(x=None, pen=fut_pvt_pen)

        plot1_ovc_open_line = self.Plot1.addLine(x=None, pen=ypen1)      
        
        plot1_two_sum_curve = self.Plot1.plot(pen=ypen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
        plot1_two_cha_curve = self.Plot1.plot(pen=gpen, symbolBrush=magenta, symbolPen='w', symbol='h', symbolSize=3)  

        plot1_hc_high_line = self.Plot1.addLine(x=None, pen=magenta_pen)
        plot1_hc_low_line = self.Plot1.addLine(x=None, pen=aqua_pen)
        
        plot1_atm_high_line = self.Plot1.addLine(x=None, pen=yellow_pen)
        plot1_atm_low_line = self.Plot1.addLine(x=None, pen=yellow_pen)
                
        plot1_fut_volume_curve = self.Plot1.plot(pen=magenta_pen1, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)
        plot1_fut_volume_plus_curve = self.Plot1.plot(pen=magenta_pen1, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)
        plot1_fut_volume_minus_curve = self.Plot1.plot(pen=aqua_pen1, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)

        plot1_call_volume_curve = self.Plot1.plot(pen=rpen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
        plot1_put_volume_curve = self.Plot1.plot(pen=bpen, symbolBrush=gold, symbolPen='w', symbol='h', symbolSize=3)
        plot1_volume_cha_curve = self.Plot1.plot(pen=gpen, symbolBrush=magenta, symbolPen='w', symbol='o', symbolSize=3)

        plot1_call_oi_curve = self.Plot1.plot(pen=rpen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
        plot1_put_oi_curve = self.Plot1.plot(pen=bpen, symbolBrush=gold, symbolPen='w', symbol='h', symbolSize=3)
        
        plot1_fut_price_curve = self.Plot1.plot(pen=rpen, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)
        plot1_kp200_curve = self.Plot1.plot(pen=gpen, symbolBrush=magenta, symbolPen='w', symbol='h', symbolSize=3)
        
        plot1_sp500_curve = self.Plot1.plot(pen=futpen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
        plot1_dow_curve = self.Plot1.plot(pen=futpen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
        plot1_nasdaq_curve = self.Plot1.plot(pen=futpen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)   
        
        # Plot2
        plot2_time_line_start = self.Plot2.addLine(x=0, y=None, pen=tpen)
        plot2_time_line_yagan_start = self.Plot2.addLine(x=0, y=None, pen=tpen)
        plot2_time_line = self.Plot2.addLine(x=0, y=None, pen=tpen1)

        plot2_ovc_open_line = self.Plot2.addLine(x=None, pen=yellow_pen)
        
        plot2_two_sum_curve = self.Plot2.plot(pen=ypen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
        plot2_two_cha_curve = self.Plot2.plot(pen=gpen, symbolBrush=magenta, symbolPen='w', symbol='h', symbolSize=3) 

        plot2_hc_high_line = self.Plot2.addLine(x=None, pen=magenta_pen)
        plot2_hc_low_line = self.Plot2.addLine(x=None, pen=aqua_pen)
        
        plot2_call_oi_curve = self.Plot2.plot(pen=rpen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
        plot2_put_oi_curve = self.Plot2.plot(pen=bpen, symbolBrush=gold, symbolPen='w', symbol='h', symbolSize=3)

        plot2_call_volume_curve = self.Plot2.plot(pen=rpen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
        plot2_put_volume_curve = self.Plot2.plot(pen=bpen, symbolBrush=gold, symbolPen='w', symbol='h', symbolSize=3)
        plot2_volume_cha_curve = self.Plot2.plot(pen=gpen, symbolBrush=magenta, symbolPen='w', symbol='o', symbolSize=3)

        plot2_fut_volume_curve = self.Plot2.plot(pen=magenta_pen1, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3) 
        plot2_fut_volume_plus_curve = self.Plot2.plot(pen=magenta_pen1, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3) 
        plot2_fut_volume_minus_curve = self.Plot2.plot(pen=aqua_pen1, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3) 

        plot2_sp500_curve = self.Plot2.plot(pen=futpen, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)
        plot2_dow_curve = self.Plot2.plot(pen=futpen, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)
        plot2_nasdaq_curve = self.Plot2.plot(pen=futpen, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)
        
        for i in range(9):
            mv_line.append(self.Plot2.addLine(x=None, pen=mvpen)) 

        for i in range(29):
            call_curve.append(self.Plot2.plot(pen=rpen, symbolBrush='r', symbolPen='w', symbol='o', symbolSize=3))
            put_curve.append(self.Plot2.plot(pen=bpen, symbolBrush='b', symbolPen='w', symbol='o', symbolSize=3))

        # Plot 3, 4 관련 설정
        if UI_STYLE == 'Vertical_view.ui':

            global plot3_time_line, plot3_time_line_start, plot3_time_line_yagan_start 
            global plot3_ovc_close_line, plot3_ovc_open_line, plot3_ovc_high_line, plot3_ovc_low_line, plot3_curve
            global plot3_ovc_jl_line, plot3_ovc_jh_line, plot3_ovc_pivot_line 

            global plot4_time_line, plot4_time_line_start, plot4_time_line_yagan_start 
            global plot4_fut_open_line, plot4_fut_close_line, plot4_fut_pivot_line, plot4_fut_jl_line, plot4_fut_jh_line
            global plot4_fv_plus_curve, plot4_fv_minus_curve, plot4_price_curve, plot4_kp200_curve
            global plot4_fut_low_line, plot4_fut_high_line            
            
            plot3_time_line = self.Plot3.addLine(x=0, y=None, pen=tpen1)
            plot3_time_line_start = self.Plot3.addLine(x=0, y=None, pen=tpen)
            plot3_time_line_yagan_start = self.Plot3.addLine(x=0, y=None, pen=tpen)

            plot3_ovc_jl_line = self.Plot3.addLine(x=None, pen=goldenrod_pen)
            plot3_ovc_jh_line = self.Plot3.addLine(x=None, pen=gold_pen)  
            plot3_ovc_close_line = self.Plot3.addLine(x=None, pen=green_pen)
            plot3_ovc_open_line = self.Plot3.addLine(x=None, pen=yellow_pen)
            plot3_ovc_pivot_line = self.Plot3.addLine(x=None, pen=fut_pvt_pen)

            plot3_ovc_low_line = self.Plot3.addLine(x=None, pen=skyblue_pen)
            plot3_ovc_high_line = self.Plot3.addLine(x=None, pen=orange_pen)
            
            plot3_curve = self.Plot3.plot(pen=futpen, symbolBrush=cyan, symbolPen='w', symbol='o', symbolSize=3)
            
            plot4_time_line = self.Plot4.addLine(x=0, y=None, pen=tpen1)  
            plot4_time_line_start = self.Plot4.addLine(x=0, y=None, pen=tpen)
            plot4_time_line_yagan_start = self.Plot4.addLine(x=0, y=None, pen=tpen)
            
            plot4_fut_jl_line = self.Plot4.addLine(x=None, pen=goldenrod_pen)
            plot4_fut_jh_line = self.Plot4.addLine(x=None, pen=gold_pen)  
            plot4_fut_open_line = self.Plot4.addLine(x=None, pen=yellow_pen)
            plot4_fut_close_line = self.Plot4.addLine(x=None, pen=green_pen)
            plot4_fut_pivot_line = self.Plot4.addLine(x=None, pen=fut_pvt_pen)   

            plot4_fut_low_line = self.Plot4.addLine(x=None, pen=skyblue_pen)
            plot4_fut_high_line = self.Plot4.addLine(x=None, pen=orange_pen)               

            plot4_fv_plus_curve = self.Plot4.plot(pen=magenta_pen1, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3) 
            plot4_fv_minus_curve = self.Plot4.plot(pen=aqua_pen1, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)

            plot4_price_curve = self.Plot4.plot(pen=rpen, symbolBrush='g', symbolPen='w', symbol='o', symbolSize=3)             
            plot4_kp200_curve = self.Plot4.plot(pen=gpen, symbolBrush=magenta, symbolPen='w', symbol='h', symbolSize=3)
        else:
            pass

        # init value & clear color
        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.매수건수.value, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.매수건수.value, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.매도건수.value, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.매도건수.value, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.매수잔량.value, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.매수잔량.value, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.매도잔량.value, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.매도잔량.value, item)

        item = QTableWidgetItem('0.00')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.건수비.value, item)

        item = QTableWidgetItem('0.00')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.건수비.value, item)

        item = QTableWidgetItem('0.00')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.잔량비.value, item)

        item = QTableWidgetItem('0.00')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.잔량비.value, item)

        item = QTableWidgetItem('0.0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.FR.value, item)

        item = QTableWidgetItem('0.0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.FR.value, item)        

        item = QTableWidgetItem("{0}".format(0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.거래량.value, item)

        item = QTableWidgetItem("{0}".format(0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.거래량.value, item)

        item = QTableWidgetItem("{0}".format('T'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(2, Futures_column.OLOH.value, item)

        item = QTableWidgetItem("{0}".format('콜매수'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(2, Futures_column.매수건수.value, item)

        item = QTableWidgetItem("{0}".format('콜매도'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(2, Futures_column.매도건수.value, item)

        item = QTableWidgetItem("{0}".format('풋매수'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(2, Futures_column.매수잔량.value, item)

        item = QTableWidgetItem("{0}".format('풋매도'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(2, Futures_column.매도잔량.value, item)

        item = QTableWidgetItem("{0}".format('손절'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(2, Futures_column.건수비.value, item)

        item = QTableWidgetItem("{0}".format('익절'))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(검정색))
        item.setForeground(QBrush(흰색))
        self.tableWidget_fut.setItem(2, Futures_column.잔량비.value, item)
        
        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.전저.value, item)
        
        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.전저.value, item)

        item = QTableWidgetItem("{0}".format('-'))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(2, Futures_column.전저.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.전고.value, item)
        
        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.전고.value, item)

        item = QTableWidgetItem("{0}".format('-'))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(2, Futures_column.전고.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.피봇.value, item)
        
        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.피봇.value, item)

        item = QTableWidgetItem("{0}".format('-'))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(2, Futures_column.피봇.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.종가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.종가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(2, Futures_column.종가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(0, Futures_column.시가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(1, Futures_column.시가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_fut.setItem(2, Futures_column.시가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(0, Futures_column.저가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(1, Futures_column.저가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(2, Futures_column.저가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        #item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(0, Futures_column.현재가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        #item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(1, Futures_column.현재가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        #item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(2, Futures_column.현재가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(0, Futures_column.고가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(1, Futures_column.고가.value, item)

        item = QTableWidgetItem("{0:0.2f}".format(0.0))
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QBrush(옅은회색))
        self.tableWidget_fut.setItem(2, Futures_column.고가.value, item)

        self.tableWidget_fut.resizeColumnsToContents()

        for i in range(nRowCount):

            item = QTableWidgetItem("{0}".format(''))
            self.tableWidget_call.setItem(i, 0, item)
            self.tableWidget_call.item(i, 0).setBackground(QBrush(검정색))

        for i in range(nRowCount):

            item = QTableWidgetItem("{0}".format(''))
            self.tableWidget_put.setItem(i, 0, item)
            self.tableWidget_put.item(i, 0).setBackground(QBrush(검정색))

        for i in range(nRowCount):
            for j in range(self.tableWidget_call.columnCount() - 1):

                item = QTableWidgetItem("{0}".format(''))
                self.tableWidget_call.setItem(i, j + 1, item)
                self.tableWidget_call.item(i, j + 1).setBackground(QBrush(검정색))

        for i in range(nRowCount):
            for j in range(self.tableWidget_put.columnCount() - 1):

                item = QTableWidgetItem("{0}".format(''))
                self.tableWidget_put.setItem(i, j + 1, item)
                self.tableWidget_put.item(i, j + 1).setBackground(QBrush(검정색))

        kp200_realdata['KP200'] = 0.0
        kp200_realdata['전저'] = 0.0
        kp200_realdata['전고'] = 0.0
        kp200_realdata['종가'] = 0.0
        kp200_realdata['피봇'] = 0.0
        kp200_realdata['시가'] = 0.0
        kp200_realdata['시가갭'] = 0.0
        kp200_realdata['저가'] = 0.0
        kp200_realdata['현재가'] = 0.0
        kp200_realdata['고가'] = 0.0
        kp200_realdata['대비'] = 0
        kp200_realdata['진폭'] = 0.0
        kp200_realdata['거래량'] = 0
        kp200_realdata['미결'] = 0
        kp200_realdata['미결증감'] = 0

        fut_realdata['KP200'] = 0.0
        fut_realdata['전저'] = 0.0
        fut_realdata['전고'] = 0.0
        fut_realdata['종가'] = 0.0
        fut_realdata['피봇'] = 0.0
        fut_realdata['시가'] = 0.0
        fut_realdata['시가갭'] = 0.0
        fut_realdata['저가'] = 0.0
        fut_realdata['현재가'] = 0.0
        fut_realdata['고가'] = 0.0
        fut_realdata['대비'] = 0
        fut_realdata['등락율'] = 0.0
        fut_realdata['진폭'] = 0.0
        fut_realdata['거래량'] = 0
        fut_realdata['미결'] = 0
        fut_realdata['미결증감'] = 0

        cme_realdata['KP200'] = 0.0
        cme_realdata['전저'] = 0.0
        cme_realdata['전고'] = 0.0
        cme_realdata['종가'] = 0.0
        cme_realdata['피봇'] = 0.0
        cme_realdata['시가'] = 0.0
        cme_realdata['시가갭'] = 0.0
        cme_realdata['저가'] = 0.0
        cme_realdata['현재가'] = 0.0
        cme_realdata['고가'] = 0.0
        cme_realdata['대비'] = 0
        cme_realdata['진폭'] = 0.0
        cme_realdata['거래량'] = 0
        cme_realdata['미결'] = 0
        cme_realdata['미결증감'] = 0              

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 0, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 1, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 2, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 3, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 4, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 5, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 6, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 7, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 8, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 9, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 10, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 11, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, 12, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_quote.setItem(0, Quote_column.미결종합.value - 1, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_supply.setItem(0, Supply_column.외인선옵.value - 1, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_supply.setItem(0, Supply_column.개인선옵.value - 1, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_supply.setItem(0, Supply_column.기관선옵.value - 1, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_supply.setItem(0, Supply_column.외인현물.value - 1, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_supply.setItem(0, Supply_column.프로그램.value - 1, item)

        item = QTableWidgetItem('0')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_supply.setItem(0, Supply_column.프로그램.value, item)

        self.color_flag = True
        self.alternate_flag = True
        self.centerval_flag = True

        global call_node_state, put_node_state

        call_node_state = {'기준가': False, '월저': False, '월고': False, '전저': False, '전고': False, '종가': True, '피봇': True, '시가': True, '대비': False, '미결': False, '미결증감': False}
        put_node_state = {'기준가': False, '월저': False, '월고': False, '전저': False, '전고': False, '종가': True, '피봇': True, '시가': True, '대비': False, '미결': False, '미결증감': False}

        global coreval

        list_low1 = []
        list_low2 = []
        list_low3 = []
        list_low4 = []
        list_low5 = []

        list_high1 = []
        list_high2 = []
        list_high3 = []
        list_high4 = []
        list_high5 = []

        for i in range(len(진성맥점)):

            list_low5.append(round(진성맥점[i] - 0.05, 2))
            list_low4.append(round(진성맥점[i] - 0.04, 2))
            list_low3.append(round(진성맥점[i] - 0.03, 2))
            list_low2.append(round(진성맥점[i] - 0.02, 2))
            list_low1.append(round(진성맥점[i] - 0.01, 2))

            list_high1.append(round(진성맥점[i] + 0.01, 2))
            list_high2.append(round(진성맥점[i] + 0.02, 2))
            list_high3.append(round(진성맥점[i] + 0.03, 2))
            list_high4.append(round(진성맥점[i] + 0.04, 2))
            list_high5.append(round(진성맥점[i] + 0.05, 2))

        coreval = 진성맥점 + list_low1 + list_low2 + list_low3 + list_low4 + list_low5 + list_high1 + list_high2 + list_high3 + list_high4 + list_high5
        coreval.sort()

        # 컬럼 헤더 click시 Event 처리용.
        call_h_header = self.tableWidget_call.horizontalHeader()
        call_h_header.sectionClicked.connect(self._call_horizontal_header_clicked)

        put_h_header = self.tableWidget_put.horizontalHeader()
        put_h_header.sectionClicked.connect(self._put_horizontal_header_clicked)

        fut_h_header = self.tableWidget_fut.horizontalHeader()
        fut_h_header.sectionClicked.connect(self._fut_horizontal_header_clicked)

        supply_h_header = self.tableWidget_supply.horizontalHeader()
        supply_h_header.sectionClicked.connect(self._supply_horizontal_header_clicked)

        quote_h_header = self.tableWidget_quote.horizontalHeader()
        quote_h_header.sectionClicked.connect(self._quote_horizontal_header_clicked)

        '''
        call_v_header = self.tableWidget_call.verticalHeader()
        call_v_header.sectionClicked.connect(self._call_vertical_header_clicked)

        put_v_header = self.tableWidget_put.verticalHeader()
        put_v_header.sectionClicked.connect(self._put_vertical_header_clicked)
        '''

        self.tableWidget_call.cellClicked.connect(self._calltable_cell_clicked)
        self.tableWidget_put.cellClicked.connect(self._puttable_cell_clicked)
        self.tableWidget_fut.cellClicked.connect(self._futtable_cell_clicked)

        self.tableWidget_supply.cellClicked.connect(self._supplytable_cell_clicked)
        self.tableWidget_quote.cellClicked.connect(self._quotetable_cell_clicked)
        
        self.tableWidget_call.verticalScrollBar().valueChanged.connect(self._calltable_vertical_scroll_position)
        self.tableWidget_put.verticalScrollBar().valueChanged.connect(self._puttable_vertical_scroll_position)

        if overnight:

            # 시작시간 X축 표시(index 0는 종가, index 1은 시가)
            plot1_time_line_start.setValue(선물장간_시간차 + 1)
            plot2_time_line_start.setValue(선물장간_시간차 + 1)
            plot1_time_line_yagan_start.setValue(선물장간_시간차 + 4 * 선물장간_시간차 + 30)
            plot2_time_line_yagan_start.setValue(선물장간_시간차 + 4 * 선물장간_시간차 + 30)

            if UI_STYLE == 'Vertical_view.ui':

                plot3_time_line_start.setValue(선물장간_시간차 + 1)
                plot4_time_line_start.setValue(선물장간_시간차 + 1)
                plot3_time_line_yagan_start.setValue(선물장간_시간차 + 4 * 선물장간_시간차 + 30)
                plot4_time_line_yagan_start.setValue(선물장간_시간차 + 4 * 선물장간_시간차 + 30)
            else:
                pass
        else:
            # 시작시간 X축 표시(index 60은 시가)
            plot1_time_line_start.setValue(선물장간_시간차)
            plot2_time_line_start.setValue(선물장간_시간차)

            if UI_STYLE == 'Vertical_view.ui':

                plot3_time_line_start.setValue(선물장간_시간차)
                plot4_time_line_start.setValue(선물장간_시간차)
            else:
                pass
        
        self.JIF = JIF(parent=self)

        self.YJ = YJ_(parent=self)
        self.YFC = YFC(parent=self)
        self.YS3 = YS3(parent=self)
        self.YOC = YOC(parent=self)

        self.IJ = IJ_(parent=self)
        self.S3 = S3_(parent=self)
        self.BM = BM_(parent=self)
        self.PM = PM_(parent=self)

        self.OVC = OVC(parent=self)

        self.OPT_REAL = OC0(parent=self)
        self.OPT_HO = OH0(parent=self)
        self.FUT_REAL = FC0(parent=self)
        self.FUT_HO = FH0(parent=self)

        if int(current_str[0:2]) < 12:
            str = '[{0:02d}:{1:02d}:{2:02d}] ♣♣♣ Good Morning! Have a Good Day ♣♣♣\r'.format(dt.hour, dt.minute, dt.second)
        else:
            str = '[{0:02d}:{1:02d}:{2:02d}] ♣♣♣ Good Afternoon! Have a Good Day ♣♣♣\r'.format(dt.hour, dt.minute, dt.second)
        self.textBrowser.append(str)

        self.XingAdminCheck()        
            
    # Xing 관리자모드 실행 체크함수
    def XingAdminCheck(self):

        # 프로세스가 관리자 권한으로 실행 여부
        dt = datetime.datetime.now()

        if ctypes.windll.shell32.IsUserAnAdmin():
            print('관리자권한으로 실행된 프로세스입니다.')
            str = '[{0:02d}:{1:02d}:{2:02d}] 관리자권한으로 실행된 프로세스입니다.\r'.format(dt.hour, dt.minute, dt.second)
            self.textBrowser.append(str)
            return True
        else:
            '''
            print('일반권한으로 실행된 프로세스입니다.')
            str = '[{0:02d}:{1:02d}:{2:02d}] 일반권한으로 실행된 프로세스입니다.\r'.format(dt.hour, dt.minute, dt.second)
            self.textBrowser.append(str)
            '''
            return False

    # 다중모니터 스크린샷 함수
    def capture_screenshot(self):

        # Capture entire screen
        with mss() as sct:
            '''
            monitor = sct.monitors[2]
            sct_img = sct.grab(monitor)
            # Convert to PIL/Pillow Image
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
            '''
            now = time.localtime()
            times = "%04d-%02d-%02d-%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

            for num, monitor in enumerate(sct.monitors[1:], 1):

                # Get raw pixels from the screen
                sct_img = sct.grab(monitor)

                # Create the Image
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

                # The same, but less efficient:
                # img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
                # saveas = "Screenshot {}{}".format(times, '.png')
                # And save it!
                # output = "monitor-{}.png".format(num)

                output = "Monitor{} {}.png".format(num, times)
                img.save(output)

                str = '[{0:02d}:{1:02d}:{2:02d}] {3}번째 화면을 캡처했습니다.\r'.format(now.tm_hour, now.tm_min, now.tm_sec, num)
                self.textBrowser.append(str)
                print(str)

    def cb1_selectionChanged(self):

        global comboindex1
        global plot1_fut_price_curve, plot1_kp200_curve, plot1_fut_volume_curve, plot1_fut_volume_plus_curve, plot1_fut_volume_minus_curve
        global plot1_call_volume_curve, plot1_put_volume_curve
        global plot1_call_oi_curve, plot1_put_oi_curve
        global plot1_two_sum_curve, plot1_two_cha_curve

        txt = self.comboBox1.currentText()
        comboindex1 = self.comboBox1.currentIndex()        

        if comboindex1 == 0:

            plot1_call_oi_curve.clear()
            plot1_put_oi_curve.clear()

            plot1_call_volume_curve.clear()
            plot1_put_volume_curve.clear()
            plot1_volume_cha_curve.clear() 

            plot1_two_sum_curve.clear()
            plot1_two_cha_curve.clear()           
            
            plot1_kp200_curve.clear()
            plot1_fut_price_curve.clear()
            
            plot1_sp500_curve.clear()
            plot1_dow_curve.clear()
            plot1_nasdaq_curve.clear()
            
            plot1_atm_high_line.setValue(0)
            plot1_atm_low_line.setValue(0)            

            plot1_ovc_open_line.setValue(0)

            plot1_hc_high_line.setValue(0)
            plot1_hc_low_line.setValue(0)

            plot1_fut_jl_line.setValue(0)
            plot1_fut_jh_line.setValue(0)
            plot1_fut_pivot_line.setValue(0)

        elif comboindex1 == 1:            
            
            plot1_fut_volume_plus_curve.clear()
            plot1_fut_volume_minus_curve.clear()

            plot1_call_oi_curve.clear()
            plot1_put_oi_curve.clear()

            plot1_two_sum_curve.clear()
            plot1_two_cha_curve.clear() 

            plot1_kp200_curve.clear()
            plot1_fut_price_curve.clear()
            
            plot1_sp500_curve.clear()
            plot1_dow_curve.clear()
            plot1_nasdaq_curve.clear()     
            
            plot1_atm_high_line.setValue(0)
            plot1_atm_low_line.setValue(0)
            
            plot1_ovc_open_line.setValue(0)

            plot1_hc_high_line.setValue(0)
            plot1_hc_low_line.setValue(0)
            
            plot1_fut_jl_line.setValue(0)
            plot1_fut_jh_line.setValue(0)
            plot1_fut_pivot_line.setValue(0) 

        elif comboindex1 == 2:
            
            plot1_fut_volume_plus_curve.clear()
            plot1_fut_volume_minus_curve.clear()

            plot1_call_volume_curve.clear()
            plot1_put_volume_curve.clear()
            plot1_volume_cha_curve.clear()

            plot1_two_sum_curve.clear()
            plot1_two_cha_curve.clear()

            plot1_kp200_curve.clear()
            plot1_fut_price_curve.clear()
            
            plot1_sp500_curve.clear()
            plot1_dow_curve.clear()
            plot1_nasdaq_curve.clear()   

            plot1_atm_high_line.setValue(0)
            plot1_atm_low_line.setValue(0)
            
            plot1_ovc_open_line.setValue(0)

            plot1_hc_high_line.setValue(0)
            plot1_hc_low_line.setValue(0)
            
            plot1_fut_jl_line.setValue(0)
            plot1_fut_jh_line.setValue(0)
            plot1_fut_pivot_line.setValue(0)     
        
        elif comboindex1 == 3:

            plot1_fut_volume_plus_curve.clear()
            plot1_fut_volume_minus_curve.clear()

            plot1_call_volume_curve.clear()
            plot1_put_volume_curve.clear()
            plot1_volume_cha_curve.clear()

            plot1_call_oi_curve.clear()
            plot1_put_oi_curve.clear()

            plot1_kp200_curve.clear()
            plot1_fut_price_curve.clear() 
            
            plot1_sp500_curve.clear()
            plot1_dow_curve.clear()
            plot1_nasdaq_curve.clear()
            
            plot1_atm_high_line.setValue(0)
            plot1_atm_low_line.setValue(0) 

            plot1_ovc_open_line.setValue(0)
            
            plot1_fut_jl_line.setValue(0)
            plot1_fut_jh_line.setValue(0)
            plot1_fut_pivot_line.setValue(0)            

            plot1_hc_high_line.setValue(1.5)
            plot1_hc_low_line.setValue(-1.5)

        elif comboindex1 == 4:
            
            plot1_fut_volume_plus_curve.clear()
            plot1_fut_volume_minus_curve.clear()

            plot1_call_oi_curve.clear()
            plot1_put_oi_curve.clear()

            plot1_call_volume_curve.clear()
            plot1_put_volume_curve.clear()
            plot1_volume_cha_curve.clear()

            plot1_two_sum_curve.clear()
            plot1_two_cha_curve.clear()
            
            plot1_sp500_curve.clear()
            plot1_dow_curve.clear()
            plot1_nasdaq_curve.clear()

            plot1_ovc_open_line.setValue(선물_전저)
            plot1_hc_high_line.setValue(선물_전저)
            plot1_hc_low_line.setValue(선물_전저)

            plot1_fut_jl_line.setValue(선물_전저)
            plot1_fut_jh_line.setValue(선물_전고)
            plot1_fut_pivot_line.setValue(선물_피봇)

            plot1_atm_high_line.setValue(atm_val + 1.25)
            plot1_atm_low_line.setValue(atm_val - 1.25)

        elif comboindex1 == 5:

            plot1_fut_volume_plus_curve.clear()
            plot1_fut_volume_minus_curve.clear()

            plot1_call_oi_curve.clear()
            plot1_put_oi_curve.clear()

            plot1_call_volume_curve.clear()
            plot1_put_volume_curve.clear()
            plot1_volume_cha_curve.clear()

            plot1_two_sum_curve.clear()
            plot1_two_cha_curve.clear()

            plot1_kp200_curve.clear()
            plot1_fut_price_curve.clear()  
            
            plot1_dow_curve.clear()
            plot1_nasdaq_curve.clear()

            if sp500_전일종가 > 0:

                plot1_atm_high_line.setValue(sp500_전일종가)
                plot1_atm_low_line.setValue(sp500_전일종가)
                
                plot1_fut_jl_line.setValue(sp500_전일종가)
                plot1_fut_jh_line.setValue(sp500_전일종가)
                plot1_fut_pivot_line.setValue(sp500_전일종가)

                plot1_hc_high_line.setValue(sp500_고가)
                plot1_hc_low_line.setValue(sp500_저가)
                
                plot1_ovc_open_line.setValue(sp500_시가)                
            else:
                pass

        elif comboindex1 == 6:

            plot1_fut_volume_plus_curve.clear()
            plot1_fut_volume_minus_curve.clear()

            plot1_call_oi_curve.clear()
            plot1_put_oi_curve.clear()

            plot1_call_volume_curve.clear()
            plot1_put_volume_curve.clear()
            plot1_volume_cha_curve.clear()

            plot1_two_sum_curve.clear()
            plot1_two_cha_curve.clear()

            plot1_kp200_curve.clear()
            plot1_fut_price_curve.clear()
            
            plot1_sp500_curve.clear()
            plot1_nasdaq_curve.clear()  

            if dow_전일종가 > 0:

                plot1_atm_high_line.setValue(dow_전일종가)
                plot1_atm_low_line.setValue(dow_전일종가)
                
                plot1_fut_jl_line.setValue(dow_전일종가)
                plot1_fut_jh_line.setValue(dow_전일종가)
                plot1_fut_pivot_line.setValue(dow_전일종가)

                plot1_hc_high_line.setValue(dow_고가)
                plot1_hc_low_line.setValue(dow_저가)
                
                plot1_ovc_open_line.setValue(dow_시가) 
            else:
                pass             

        elif comboindex1 == 7:

            plot1_fut_volume_plus_curve.clear()
            plot1_fut_volume_minus_curve.clear()

            plot1_call_oi_curve.clear()
            plot1_put_oi_curve.clear()

            plot1_call_volume_curve.clear()
            plot1_put_volume_curve.clear()
            plot1_volume_cha_curve.clear()

            plot1_two_sum_curve.clear()
            plot1_two_cha_curve.clear()

            plot1_kp200_curve.clear()
            plot1_fut_price_curve.clear()
            
            plot1_sp500_curve.clear()
            plot1_dow_curve.clear()  

            if nasdaq_전일종가 > 0:

                plot1_atm_high_line.setValue(nasdaq_전일종가)
                plot1_atm_low_line.setValue(nasdaq_전일종가)
                
                plot1_fut_jl_line.setValue(nasdaq_전일종가)
                plot1_fut_jh_line.setValue(nasdaq_전일종가)
                plot1_fut_pivot_line.setValue(nasdaq_전일종가)

                plot1_hc_high_line.setValue(nasdaq_고가)
                plot1_hc_low_line.setValue(nasdaq_저가)
                
                plot1_ovc_open_line.setValue(nasdaq_시가) 
            else:
                pass
        else:
            pass

    def cb2_selectionChanged(self):

        global comboindex2
        global call_curve, put_curve, plot2_fut_volume_curve, plot2_fut_volume_plus_curve, plot2_fut_volume_minus_curve
        global plot2_call_volume_curve, plot2_put_volume_curve
        global plot2_call_oi_curve, plot2_put_oi_curve
        global plot2_two_sum_curve, plot2_two_cha_curve

        txt = self.comboBox2.currentText()
        comboindex2 = self.comboBox2.currentIndex()

        if comboindex2 == 0:
            
            plot2_call_oi_curve.clear()
            plot2_put_oi_curve.clear()

            plot2_fut_volume_plus_curve.clear()
            plot2_fut_volume_minus_curve.clear()

            plot2_two_sum_curve.clear()
            plot2_two_cha_curve.clear()
                        
            for i in range(29):
                call_curve[i].clear()
                put_curve[i].clear()
            
            plot2_sp500_curve.clear()
            plot2_dow_curve.clear()
            plot2_nasdaq_curve.clear()

            for i in range(9):
                mv_line[i].setValue(0)

            plot2_ovc_open_line.setValue(0)

            plot2_hc_high_line.setValue(0)
            plot2_hc_low_line.setValue(0)

        elif comboindex2 == 1:
                        
            if not overnight:

                plot2_call_volume_curve.clear()
                plot2_put_volume_curve.clear()
                plot2_volume_cha_curve.clear()

                plot2_fut_volume_plus_curve.clear()
                plot2_fut_volume_minus_curve.clear()

                plot2_two_sum_curve.clear()
                plot2_two_cha_curve.clear()

                for i in range(29):
                    call_curve[i].clear()
                    put_curve[i].clear() 

                plot2_sp500_curve.clear()
                plot2_dow_curve.clear()
                plot2_nasdaq_curve.clear()

                for i in range(9):
                    mv_line[i].setValue(0)

                plot2_ovc_open_line.setValue(0)

                plot2_hc_high_line.setValue(0)
                plot2_hc_low_line.setValue(0)
            else:
                pass            

        elif comboindex2 == 2:

            plot2_call_oi_curve.clear()
            plot2_put_oi_curve.clear()

            plot2_call_volume_curve.clear()
            plot2_put_volume_curve.clear()
            plot2_volume_cha_curve.clear()

            plot2_two_sum_curve.clear()
            plot2_two_cha_curve.clear()
            
            for i in range(29):
                call_curve[i].clear()
                put_curve[i].clear()

            plot2_sp500_curve.clear()
            plot2_dow_curve.clear()
            plot2_nasdaq_curve.clear() 

            for i in range(9):
                mv_line[i].setValue(0)

            plot2_ovc_open_line.setValue(0)

            plot2_hc_high_line.setValue(0)
            plot2_hc_low_line.setValue(0)
        
        elif comboindex2 == 3:

            plot2_call_oi_curve.clear()
            plot2_put_oi_curve.clear()   

            plot2_call_volume_curve.clear()
            plot2_put_volume_curve.clear()
            plot2_volume_cha_curve.clear()

            plot2_fut_volume_plus_curve.clear()
            plot2_fut_volume_minus_curve.clear()
            
            for i in range(29):
                call_curve[i].clear()
                put_curve[i].clear() 

            plot2_sp500_curve.clear()
            plot2_dow_curve.clear()
            plot2_nasdaq_curve.clear()

            for i in range(9):
                mv_line[i].setValue(0)

            plot2_ovc_open_line.setValue(0)

            plot2_hc_high_line.setValue(1.5)
            plot2_hc_low_line.setValue(-1.5)

        elif comboindex2 == 4:

            plot2_call_oi_curve.clear()
            plot2_put_oi_curve.clear()   

            plot2_call_volume_curve.clear()
            plot2_put_volume_curve.clear()
            plot2_volume_cha_curve.clear()

            plot2_fut_volume_plus_curve.clear()
            plot2_fut_volume_minus_curve.clear()

            plot2_two_sum_curve.clear()
            plot2_two_cha_curve.clear()
            
            plot2_sp500_curve.clear()
            plot2_dow_curve.clear()
            plot2_nasdaq_curve.clear()

            plot2_hc_high_line.setValue(0)
            plot2_hc_low_line.setValue(0)

            # 대맥점 표시
            mv_line[0].setValue(1.2)
            mv_line[1].setValue(2.5)
            mv_line[2].setValue(3.5)
            mv_line[3].setValue(4.85)
            mv_line[4].setValue(5.1)
            mv_line[5].setValue(5.5)

        elif comboindex2 == 5:

            plot2_call_oi_curve.clear()
            plot2_put_oi_curve.clear()   

            plot2_call_volume_curve.clear()
            plot2_put_volume_curve.clear()
            plot2_volume_cha_curve.clear()

            plot2_fut_volume_plus_curve.clear()
            plot2_fut_volume_minus_curve.clear()

            plot2_two_sum_curve.clear()
            plot2_two_cha_curve.clear()
            
            for i in range(29):
                call_curve[i].clear()
                put_curve[i].clear() 

            plot2_dow_curve.clear()
            plot2_nasdaq_curve.clear()

            if sp500_전일종가 > 0:

                for i in range(9):
                    mv_line[i].setValue(sp500_전일종가)

                plot2_hc_high_line.setValue(sp500_고가)
                plot2_hc_low_line.setValue(sp500_저가)
                
                plot2_ovc_open_line.setValue(sp500_시가)
            else:
                pass            

        elif comboindex2 == 6:

            plot2_call_oi_curve.clear()
            plot2_put_oi_curve.clear()   

            plot2_call_volume_curve.clear()
            plot2_put_volume_curve.clear()
            plot2_volume_cha_curve.clear()

            plot2_fut_volume_plus_curve.clear()
            plot2_fut_volume_minus_curve.clear()

            plot2_two_sum_curve.clear()
            plot2_two_cha_curve.clear()
            
            for i in range(29):
                call_curve[i].clear()
                put_curve[i].clear()

            plot2_sp500_curve.clear()
            plot2_nasdaq_curve.clear()

            if dow_전일종가 > 0:

                for i in range(9):
                    mv_line[i].setValue(dow_전일종가)

                plot2_hc_high_line.setValue(dow_고가)
                plot2_hc_low_line.setValue(dow_저가)
                
                plot2_ovc_open_line.setValue(dow_시가)
            else:
                pass

        elif comboindex2 == 7:

            plot2_call_oi_curve.clear()
            plot2_put_oi_curve.clear()   

            plot2_call_volume_curve.clear()
            plot2_put_volume_curve.clear()
            plot2_volume_cha_curve.clear()

            plot2_fut_volume_plus_curve.clear()
            plot2_fut_volume_minus_curve.clear()

            plot2_two_sum_curve.clear()
            plot2_two_cha_curve.clear()
            
            for i in range(29):
                call_curve[i].clear()
                put_curve[i].clear()
                
            plot2_sp500_curve.clear()
            plot2_dow_curve.clear() 

            if nasdaq_전일종가 > 0:

                for i in range(9):
                    mv_line[i].setValue(nasdaq_전일종가)

                plot2_hc_high_line.setValue(nasdaq_고가)
                plot2_hc_low_line.setValue(nasdaq_저가)
                
                plot2_ovc_open_line.setValue(nasdaq_시가)
            else:
                pass
        else:
            pass

    if UI_STYLE == 'Vertical_view.ui':

        def cb3_selectionChanged(self):

            global comboindex3

            comboindex3 = self.comboBox3.currentIndex()

            if comboindex3 == 0:

                plot3_curve.clear()

                if dow_전일종가 > 0:
                    plot3_ovc_close_line.setValue(dow_전일종가)
                else:
                    pass

                if dow_시가 > 0:
                    plot3_ovc_open_line.setValue(dow_시가)
                else:
                    pass

                if DOW_LAST_LOW > 0:
                    plot3_ovc_jl_line.setValue(DOW_LAST_LOW)
                else:
                    pass

                if DOW_LAST_HIGH > 0:
                    plot3_ovc_jh_line.setValue(DOW_LAST_HIGH)
                else:
                    pass

                if dow_피봇 > 0:
                    plot3_ovc_pivot_line.setValue(dow_피봇)
                else:
                    pass

                if dow_저가 > 0:
                    plot3_ovc_low_line.setValue(dow_저가)
                else:
                    pass

                if dow_고가 > 0:
                    plot3_ovc_high_line.setValue(dow_고가)
                else:
                    pass

            elif comboindex3 == 1:

                plot3_curve.clear()

                if sp500_전일종가 > 0:                    
                    plot3_ovc_close_line.setValue(sp500_전일종가)
                else:
                    pass

                if sp500_시가 > 0:    
                    plot3_ovc_open_line.setValue(sp500_시가)
                else:
                    pass

                if SP500_LAST_LOW > 0:
                    plot3_ovc_jl_line.setValue(SP500_LAST_LOW)
                else:
                    pass

                if SP500_LAST_HIGH > 0:
                    plot3_ovc_jh_line.setValue(SP500_LAST_HIGH)
                else:
                    pass

                if sp500_피봇 > 0:
                    plot3_ovc_pivot_line.setValue(sp500_피봇)
                else:
                    pass

                if sp500_저가 > 0:
                    plot3_ovc_low_line.setValue(sp500_저가)
                else:
                    pass

                if sp500_고가 > 0:
                    plot3_ovc_high_line.setValue(sp500_고가)
                else:
                    pass

            elif comboindex3 == 2:

                plot3_curve.clear()

                if nasdaq_전일종가 > 0:                    
                    plot3_ovc_close_line.setValue(nasdaq_전일종가)
                else:
                    pass

                if nasdaq_시가 > 0: 
                    plot3_ovc_open_line.setValue(nasdaq_시가)
                else:
                    pass

                if NASDAQ_LAST_LOW > 0:
                    plot3_ovc_jl_line.setValue(NASDAQ_LAST_LOW)
                else:
                    pass

                if NASDAQ_LAST_HIGH > 0:
                    plot3_ovc_jh_line.setValue(NASDAQ_LAST_HIGH)
                else:
                    pass

                if nasdaq_피봇 > 0:
                    plot3_ovc_pivot_line.setValue(nasdaq_피봇)
                else:
                    pass

                if nasdaq_저가 > 0:
                    plot3_ovc_low_line.setValue(nasdaq_저가)
                else:
                    pass

                if nasdaq_고가 > 0:
                    plot3_ovc_high_line.setValue(nasdaq_고가)
                else:
                    pass
            else:
                pass

            return

        def cb4_selectionChanged(self):

            global comboindex4

            comboindex4 = self.comboBox4.currentIndex()

            if comboindex4 == 0:

                plot4_fv_plus_curve.clear()
                plot4_fv_minus_curve.clear()

                if 선물_전저 > 0:
                    plot4_fut_jl_line.setValue(선물_전저)
                else:
                    pass

                if 선물_전고 > 0:
                    plot4_fut_jh_line.setValue(선물_전고)
                else:
                    pass

                if 선물_종가 > 0:
                    plot4_fut_close_line.setValue(선물_종가)
                else:
                    pass

                if 선물_피봇 > 0:                
                    plot4_fut_pivot_line.setValue(선물_피봇)
                else:
                    pass

                if 선물_시가 > 0:
                    plot4_fut_open_line.setValue(선물_시가)
                else:
                    pass

                if 선물_저가 > 0:
                    plot4_fut_low_line.setValue(선물_저가)
                else:
                    pass

                if 선물_고가 > 0:
                    plot4_fut_high_line.setValue(선물_고가)
                else:
                    pass

                print('선물_전저 =', 선물_전저)
                print('선물_전고 =', 선물_전고)
                print('선물_종가 =', 선물_종가)
                print('선물_피봇 =', 선물_피봇)
                print('선물_시가 =', 선물_시가)
                print('선물_저가 =', 선물_저가)
                print('선물_고가 =', 선물_고가)

            elif comboindex4 == 1:
                
                plot4_price_curve.clear()
                plot4_kp200_curve.clear()

                plot4_fut_jl_line.setValue(0)
                plot4_fut_jh_line.setValue(0)
                plot4_fut_pivot_line.setValue(0)
                plot4_fut_close_line.setValue(0)
                plot4_fut_open_line.setValue(0)
            else:
                pass

            return
    else:
        pass

    def timeout(self):
        dt = datetime.datetime.now()
        str = '{0:02d}:{1:02d}:{2:02d}'.format(dt.hour, dt.minute, dt.second)
        self.label_msg.setText(str)

    def label_blink(self, widget, color1, color2, blink_set):

        if blink_set:
            if self.color_flag:
                stylesheet = "background-color: {0}; color: {1}".format(color1, color2)
                widget.setStyleSheet(stylesheet)
            else:
                stylesheet = "background-color: {0}; color: {1}".format(color2, color1)
                widget.setStyleSheet(stylesheet)
            self.color_flag = not self.color_flag
        else:
            stylesheet = "background-color: {0}; color: {1}".format(color1, color2)
            widget.setStyleSheet(stylesheet)

    @pyqtSlot(int)
    def _call_horizontal_header_clicked(self, idx):

        global call_node_state

        if idx == Option_column.기준가.value or idx == Option_column.월저.value or idx == Option_column.월고.value or \
            idx == Option_column.전저.value or idx == Option_column.전고.value or idx == Option_column.종가.value or \
                idx == Option_column.피봇.value or idx == Option_column.시가.value:

            col_text = self.tableWidget_call.horizontalHeaderItem(idx).text()

            if col_text.find('✓') == -1:
                item = QTableWidgetItem(col_text + '\n✓')
                self.tableWidget_call.setHorizontalHeaderItem(idx, item)
                print("call header column.. ", idx, col_text)

                if idx == Option_column.기준가.value:
                    call_node_state['기준가'] = True
                elif idx == Option_column.월저.value:
                    call_node_state['월저'] = True
                elif idx == Option_column.월고.value:
                    call_node_state['월고'] = True
                elif idx == Option_column.전저.value:
                    call_node_state['전저'] = True
                elif idx == Option_column.전고.value:
                    call_node_state['전고'] = True
                elif idx == Option_column.종가.value:
                    call_node_state['종가'] = True
                elif idx == Option_column.피봇.value:
                    call_node_state['피봇'] = True
                elif idx == Option_column.시가.value:
                    call_node_state['시가'] = True
                else:
                    pass
            else:
                item = QTableWidgetItem(col_text.replace('\n✓', ''))
                self.tableWidget_call.setHorizontalHeaderItem(idx, item)
                print("call header column.. ", idx, col_text)

                global call_scroll_end_position

                if call_scroll_end_position > option_pairs_count:

                    call_scroll_end_position = option_pairs_count
                else:
                    pass

                if idx == Option_column.기준가.value:

                    call_node_state['기준가'] = False

                    for i in range(call_scroll_begin_position, call_scroll_end_position):

                        self.tableWidget_call.item(i, Option_column.기준가.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.기준가.value).setForeground(QBrush(검정색))

                elif idx == Option_column.월저.value:

                    call_node_state['월저'] = False

                    for i in range(call_scroll_begin_position, call_scroll_end_position):

                        self.tableWidget_call.item(i, Option_column.월저.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.월저.value).setForeground(QBrush(검정색))

                elif idx == Option_column.월고.value:

                    call_node_state['월고'] = False

                    for i in range(call_scroll_begin_position, call_scroll_end_position):

                        self.tableWidget_call.item(i, Option_column.월고.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.월고.value).setForeground(QBrush(검정색))

                elif idx == Option_column.전저.value:

                    call_node_state['전저'] = False

                    for i in range(call_scroll_begin_position, call_scroll_end_position):

                        self.tableWidget_call.item(i, Option_column.전저.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.전저.value).setForeground(QBrush(검정색))

                elif idx == Option_column.전고.value:

                    call_node_state['전고'] = False

                    for i in range(call_scroll_begin_position, call_scroll_end_position):

                        self.tableWidget_call.item(i, Option_column.전고.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.전고.value).setForeground(QBrush(검정색))

                elif idx == Option_column.종가.value:

                    call_node_state['종가'] = False

                    for i in range(call_scroll_begin_position, call_scroll_end_position):

                        self.tableWidget_call.item(i, Option_column.종가.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.종가.value).setForeground(QBrush(검정색))

                elif idx == Option_column.피봇.value:

                    call_node_state['피봇'] = False

                    for i in range(call_scroll_begin_position, call_scroll_end_position):

                        self.tableWidget_call.item(i, Option_column.피봇.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))

                elif idx == Option_column.시가.value:

                    call_node_state['시가'] = False

                    for i in range(call_scroll_begin_position, call_scroll_end_position):

                        self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
            
            # cell focus 이동
            self.tableWidget_call.setCurrentCell(100, Option_column.OID.value)
            self.opt_call_node_coloring()

        else:
            pass

        self.tableWidget_call.resizeColumnsToContents()
        
        return

    @pyqtSlot(int)
    def _put_horizontal_header_clicked(self, idx):

        global put_node_state

        if idx == Option_column.기준가.value or idx == Option_column.월저.value or idx == Option_column.월고.value or \
            idx == Option_column.전저.value or idx == Option_column.전고.value or idx == Option_column.종가.value or \
                idx == Option_column.피봇.value or idx == Option_column.시가.value:

            col_text = self.tableWidget_put.horizontalHeaderItem(idx).text()

            if col_text.find('✓') == -1:
                item = QTableWidgetItem(col_text + '\n✓')
                self.tableWidget_put.setHorizontalHeaderItem(idx, item)
                print("put header column.. ", idx, col_text)

                if idx == Option_column.기준가.value:
                    put_node_state['기준가'] = True
                elif idx == Option_column.월저.value:
                    put_node_state['월저'] = True
                elif idx == Option_column.월고.value:
                    put_node_state['월고'] = True
                elif idx == Option_column.전저.value:
                    put_node_state['전저'] = True
                elif idx == Option_column.전고.value:
                    put_node_state['전고'] = True
                elif idx == Option_column.종가.value:
                    put_node_state['종가'] = True
                elif idx == Option_column.피봇.value:
                    put_node_state['피봇'] = True
                elif idx == Option_column.시가.value:
                    put_node_state['시가'] = True
                else:
                    pass
            else:
                item = QTableWidgetItem(col_text.replace('\n✓', ''))
                self.tableWidget_put.setHorizontalHeaderItem(idx, item)
                print("put header column.. ", idx, col_text)

                global put_scroll_end_position

                if put_scroll_end_position > option_pairs_count:

                    put_scroll_end_position = option_pairs_count
                else:
                    pass

                if idx == Option_column.기준가.value:

                    put_node_state['기준가'] = False

                    for i in range(put_scroll_begin_position, put_scroll_end_position):

                        self.tableWidget_put.item(i, Option_column.기준가.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.기준가.value).setForeground(QBrush(검정색))

                elif idx == Option_column.월저.value:

                    put_node_state['월저'] = False

                    for i in range(put_scroll_begin_position, put_scroll_end_position):

                        self.tableWidget_put.item(i, Option_column.월저.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.월저.value).setForeground(QBrush(검정색))

                elif idx == Option_column.월고.value:

                    put_node_state['월고'] = False

                    for i in range(put_scroll_begin_position, put_scroll_end_position):

                        self.tableWidget_put.item(i, Option_column.월고.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.월고.value).setForeground(QBrush(검정색))

                elif idx == Option_column.전저.value:

                    put_node_state['전저'] = False

                    for i in range(put_scroll_begin_position, put_scroll_end_position):

                        self.tableWidget_put.item(i, Option_column.전저.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.전저.value).setForeground(QBrush(검정색))

                elif idx == Option_column.전고.value:

                    put_node_state['전고'] = False

                    for i in range(put_scroll_begin_position, put_scroll_end_position):

                        self.tableWidget_put.item(i, Option_column.전고.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.전고.value).setForeground(QBrush(검정색))

                elif idx == Option_column.종가.value:

                    put_node_state['종가'] = False

                    for i in range(put_scroll_begin_position, put_scroll_end_position):

                        self.tableWidget_put.item(i, Option_column.종가.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.종가.value).setForeground(QBrush(검정색))

                elif idx == Option_column.피봇.value:

                    put_node_state['피봇'] = False

                    for i in range(put_scroll_begin_position, put_scroll_end_position):

                        self.tableWidget_put.item(i, Option_column.피봇.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))

                elif idx == Option_column.시가.value:

                    put_node_state['시가'] = False

                    for i in range(put_scroll_begin_position, put_scroll_end_position):

                        self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
            
            # cell focus 이동
            self.tableWidget_put.setCurrentCell(100, Option_column.OID.value)
            self.opt_put_node_coloring()
        else:
            pass

        self.tableWidget_put.resizeColumnsToContents()
        
        return

    @pyqtSlot(int)
    def _fut_horizontal_header_clicked(self, idx):

        # cell focus 이동
        self.tableWidget_fut.setCurrentCell(3, Futures_column.OID.value)

        return

    @pyqtSlot(int)
    def _supply_horizontal_header_clicked(self, idx):

        # cell focus 이동
        self.tableWidget_supply.setCurrentCell(1, 5)

        return

    @pyqtSlot(int)
    def _quote_horizontal_header_clicked(self, idx):

        # cell focus 이동
        self.tableWidget_quote.setCurrentCell(1, Quote_column.미결종합.value - 1)

        return

    def all_node_set(self):

        global call_node_state, put_node_state

        for idx in range(Option_column.기준가.value, Option_column.시가갭.value):

            col_text = self.tableWidget_call.horizontalHeaderItem(idx).text()

            if col_text.find('✓') == -1:
            
                item = QTableWidgetItem(col_text + '\n✓')
                self.tableWidget_call.setHorizontalHeaderItem(idx, item)

                if idx == Option_column.기준가.value:
                    call_node_state['기준가'] = True
                elif idx == Option_column.월저.value:
                    call_node_state['월저'] = True
                elif idx == Option_column.월고.value:
                    call_node_state['월고'] = True
                elif idx == Option_column.전저.value:
                    call_node_state['전저'] = True
                elif idx == Option_column.전고.value:
                    call_node_state['전고'] = True
                elif idx == Option_column.종가.value:
                    call_node_state['종가'] = True
                elif idx == Option_column.피봇.value:
                    call_node_state['피봇'] = True
                elif idx == Option_column.시가.value:
                    call_node_state['시가'] = True
                else:
                    pass
            else:
            	pass

            col_text = self.tableWidget_put.horizontalHeaderItem(idx).text()

            if col_text.find('✓') == -1:

                item = QTableWidgetItem(col_text + '\n✓')
                self.tableWidget_put.setHorizontalHeaderItem(idx, item)

                if idx == Option_column.기준가.value:
                    put_node_state['기준가'] = True
                elif idx == Option_column.월저.value:
                    put_node_state['월저'] = True
                elif idx == Option_column.월고.value:
                    put_node_state['월고'] = True
                elif idx == Option_column.전저.value:
                    put_node_state['전저'] = True
                elif idx == Option_column.전고.value:
                    put_node_state['전고'] = True
                elif idx == Option_column.종가.value:
                    put_node_state['종가'] = True
                elif idx == Option_column.피봇.value:
                    put_node_state['피봇'] = True
                elif idx == Option_column.시가.value:
                    put_node_state['시가'] = True
                else:
                    pass
            else:
                pass
        return

    '''
    @pyqtSlot(int)
    def _call_vertical_header_clicked(self, idx):

        row_text = self.tableWidget_call.item(idx, Option_column.행사가.value).text()

        if row_text.find('✓') == -1:
            item = QTableWidgetItem(row_text + '✓')
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setItem(idx, Option_column.행사가.value, item)
        else:
            item = QTableWidgetItem(row_text.replace('✓', ''))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setItem(idx, Option_column.행사가.value, item)

        self.tableWidget_call.resizeColumnsToContents()

        return

    @pyqtSlot(int)
    def _put_vertical_header_clicked(self, idx):

        row_text = self.tableWidget_put.item(idx, Option_column.행사가.value).text()

        if row_text.find('✓') == -1:
            item = QTableWidgetItem(row_text + '✓')
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setItem(idx, Option_column.행사가.value, item)
        else:
            item = QTableWidgetItem(row_text.replace('✓', ''))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setItem(idx, Option_column.행사가.value, item)

        self.tableWidget_put.resizeColumnsToContents()

        return
    '''
    @pyqtSlot(int, int)
    def _calltable_cell_clicked(self, row, col):

        cell = self.tableWidget_call.item(row, col)

        if cell is not None:

            txt = "call table cell clicked = ({0},{1}) ==>{2}<==".format(row, col, cell.text())

            if atm_str != '':

                if row < atm_index:
                    call_positionCell = self.tableWidget_call.item(atm_index + 3, 1)
                else:
                    call_positionCell = self.tableWidget_call.item(atm_index - 4, 1)

                self.tableWidget_call.scrollToItem(call_positionCell)

            else:
                pass

            # cell focus 이동
            self.tableWidget_call.setCurrentCell(100, Option_column.OID.value)
        else:
            txt = "call table cell clicked = ({0},{1}) ==>None type<==".format(row, col)

        print(txt)

        return

    @pyqtSlot(int, int)
    def _puttable_cell_clicked(self, row, col):

        cell = self.tableWidget_put.item(row, col)

        if cell is not None:

            txt = "put table cell clicked = ({0},{1}) ==>{2}<==".format(row, col, cell.text())

            if atm_str != '':

                if row < atm_index:
                    put_positionCell = self.tableWidget_put.item(atm_index + 3, 1)
                else:
                    put_positionCell = self.tableWidget_put.item(atm_index - 4, 1)

                self.tableWidget_put.scrollToItem(put_positionCell)
            else:
                pass

            # cell focus 이동
            self.tableWidget_put.setCurrentCell(100, Option_column.OID.value)
        else:
            txt = "put table cell clicked = ({0},{1}) ==>None type<==".format(row, col)

        print(txt)

        return

    @pyqtSlot(int, int)
    def _futtable_cell_clicked(self, row, col):
        
        cell = self.tableWidget_fut.currentItem()
        
        if cell is not None:

            global 콜매수, 콜매도, 풋매수, 풋매도, 손절, 익절 

            fut_txt = cell.text()

            if row == 2 and col == Futures_column.OLOH.value:

                if self.telegram_flag:

                    콜매수 = self.tableWidget_fut.item(2, Futures_column.매수건수.value).text()
                    콜매도 = self.tableWidget_fut.item(2, Futures_column.매도건수.value).text()
                    풋매수 = self.tableWidget_fut.item(2, Futures_column.매수잔량.value).text()
                    풋매도 = self.tableWidget_fut.item(2, Futures_column.매도잔량.value).text()
                    손절 = self.tableWidget_fut.item(2, Futures_column.건수비.value).text()
                    익절 = self.tableWidget_fut.item(2, Futures_column.잔량비.value).text()

                    if 콜매수 != '콜매수':

                        str = '[{0:02d}:{1:02d}:{2:02d}] 콜매수 {3} 진입...\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]), 콜매수)
                        self.textBrowser.append(str)
                    else:
                        pass

                    if 콜매도 != '콜매도':

                        str = '[{0:02d}:{1:02d}:{2:02d}] 콜매도 {3} 진입...\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]), 콜매도)
                        self.textBrowser.append(str)
                    else:
                        pass

                    if 풋매수 != '풋매수':

                        str = '[{0:02d}:{1:02d}:{2:02d}] 풋매수 {3} 진입...\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]), 풋매수)
                        self.textBrowser.append(str)
                    else:
                        pass

                    if 풋매도 != '풋매도':

                        str = '[{0:02d}:{1:02d}:{2:02d}] 풋매도 {3} 진입...\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]), 풋매도)
                        self.textBrowser.append(str)
                    else:
                        pass

                    if 손절 != '손절':

                        str = '[{0:02d}:{1:02d}:{2:02d}] 손절 {3}틱 설정됨\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]), 손절)
                        self.textBrowser.append(str)
                    else:
                        pass

                    if 익절 != '익절':

                        str = '[{0:02d}:{1:02d}:{2:02d}] 익절 {3}틱 설정됨\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]), 익절)
                        self.textBrowser.append(str)
                    else:
                        pass

                    item = QTableWidgetItem("{0}".format('R'))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_fut.setItem(2, Futures_column.OLOH.value, item)

                    str = '[{0:02d}:{1:02d}:{2:02d}] 텔레그램 전송이 예약되었습니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    #self.telegram_flag = not self.telegram_flag
                else:
                    item = QTableWidgetItem("{0}".format('T'))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(검정색))
                    item.setForeground(QBrush(흰색))
                    self.tableWidget_fut.setItem(2, Futures_column.OLOH.value, item)

                    item = QTableWidgetItem("{0}".format('콜매수'))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(검정색))
                    item.setForeground(QBrush(흰색))
                    self.tableWidget_fut.setItem(2, Futures_column.매수건수.value, item)

                    item = QTableWidgetItem("{0}".format('콜매도'))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(검정색))
                    item.setForeground(QBrush(흰색))
                    self.tableWidget_fut.setItem(2, Futures_column.매도건수.value, item)

                    item = QTableWidgetItem("{0}".format('풋매수'))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(검정색))
                    item.setForeground(QBrush(흰색))
                    self.tableWidget_fut.setItem(2, Futures_column.매수잔량.value, item)

                    item = QTableWidgetItem("{0}".format('풋매도'))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(검정색))
                    item.setForeground(QBrush(흰색))
                    self.tableWidget_fut.setItem(2, Futures_column.매도잔량.value, item)

                    item = QTableWidgetItem("{0}".format('손절'))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(검정색))
                    item.setForeground(QBrush(흰색))
                    self.tableWidget_fut.setItem(2, Futures_column.건수비.value, item)

                    item = QTableWidgetItem("{0}".format('익절'))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(검정색))
                    item.setForeground(QBrush(흰색))
                    self.tableWidget_fut.setItem(2, Futures_column.잔량비.value, item)

                    str = '[{0:02d}:{1:02d}:{2:02d}] 텔레그램 전송예약이 취소되었습니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    #self.telegram_flag = not self.telegram_flag
            else:
                pass             
        else:
            pass  
            
        self.tableWidget_fut.resizeColumnsToContents()      

        return

    @pyqtSlot(int, int)
    def _supplytable_cell_clicked(self, row, col):

        cell = self.tableWidget_supply.currentItem()

        if cell is not None:

            print(cell.text())

            # cell focus 이동
            self.tableWidget_supply.setCurrentCell(1, 5)

        else:
            pass  

        return

    @pyqtSlot(int, int)
    def _quotetable_cell_clicked(self, row, col):

        cell = self.tableWidget_quote.currentItem()

        if cell is not None:

            print(cell.text())

            # cell focus 이동
            self.tableWidget_quote.setCurrentCell(1, Quote_column.미결종합.value - 1)

        else:
            pass

        return
    
    @pyqtSlot(int)
    def _calltable_vertical_scroll_position(self, row):

        global call_scroll_begin_position, call_scroll_end_position

        call_scroll_begin_position = row

        if call_scroll_begin_position <= option_pairs_count:

            call_scroll_end_position = call_scroll_begin_position + 9

            print('call scroll position -----> from %d to %d' % (call_scroll_begin_position, call_scroll_end_position))

            self.opt_call_node_coloring()

        elif call_scroll_begin_position > option_pairs_count:
            pass

        self.tableWidget_call.resizeColumnsToContents()

        return

    @pyqtSlot(int)
    def _puttable_vertical_scroll_position(self, row):

        global put_scroll_begin_position, put_scroll_end_position

        put_scroll_begin_position = row

        if put_scroll_begin_position <= option_pairs_count:

            put_scroll_end_position = put_scroll_begin_position + 9

            print('put scroll position -----> from %d to %d' % (put_scroll_begin_position, put_scroll_end_position))

            self.opt_put_node_coloring()

        elif put_scroll_begin_position > option_pairs_count:
            pass

        self.tableWidget_put.resizeColumnsToContents()

        return

    @pyqtSlot(int)
    def t8415_call_request(self, index):
        try:
            XQ = t8415(parent=self)

            if today_str == MONTH_FIRSTDAY:
                XQ.Query(단축코드=call_code[index], 시작일자=yesterday_str, 종료일자=today_str)
            else:
                XQ.Query(단축코드=call_code[index], 시작일자=MONTH_FIRSTDAY, 종료일자=today_str)

        except:
            pass

    @pyqtSlot(int)
    def t8415_put_request(self, index):
        try:
            XQ = t8415(parent=self)

            if today_str == MONTH_FIRSTDAY:
                XQ.Query(단축코드=put_code[index], 시작일자=yesterday_str, 종료일자=today_str)
            else:
                XQ.Query(단축코드=put_code[index], 시작일자=MONTH_FIRSTDAY, 종료일자=today_str)

        except:
            pass

    @pyqtSlot(int)
    def t8416_call_request(self, index):
        try:
            XQ = t8416(parent=self)

            if today_str == MONTH_FIRSTDAY:
                XQ.Query(단축코드=call_code[index], 시작일자=yesterday_str, 종료일자=today_str)
            else:
                XQ.Query(단축코드=call_code[index], 시작일자=MONTH_FIRSTDAY, 종료일자=today_str)
        except:
            pass

    @pyqtSlot(int)
    def t8416_put_request(self, index):
        try:
            XQ = t8416(parent=self)

            if today_str == MONTH_FIRSTDAY:
                XQ.Query(단축코드=put_code[index], 시작일자=yesterday_str, 종료일자=today_str)
            else:
                XQ.Query(단축코드=put_code[index], 시작일자=MONTH_FIRSTDAY, 종료일자=today_str)
        except:
            pass

    def plot_data(self):

        pass 

    @pyqtSlot(str)
    def send_telegram_message(self, str):

        try:
            dt = datetime.datetime.now()

            if market_service:

                str = '[{0:02d}:{1:02d}:{2:02d}] Telegram Send Message = {3}\r'.format(dt.hour, dt.minute, dt.second, str)
                print(str)
            else:
                pass
        except:
            pass

    @pyqtSlot(str)
    def listen_telegram_message(self, str):

        try:
            dt = datetime.datetime.now()

            global telegram_command

            telegram_command = str

            if market_service:

                str = '[{0:02d}:{1:02d}:{2:02d}] Telegram Listen Command = {3}\r'.format(dt.hour, dt.minute, dt.second, telegram_command)
                print(str)
            else:
                pass
        except:
            pass

    @pyqtSlot(dict)
    def update_screen(self, data):

        try:
            start_time = timeit.default_timer()            
            dt = datetime.datetime.now()
            current_str = dt.strftime('%H:%M:%S')

            global flag_fut_low, flag_fut_high
            global flag_kp200_low, flag_kp200_high
            global flag_offline, receive_real_ovc
            global 시스템시간

            시스템시간 = dt.hour * 3600 + dt.minute * 60 + dt.second
            
            self.alternate_flag = not self.alternate_flag

            # 장의 유형을 시간과 함께 표시
            self.market_type_display(self.alternate_flag)
                                    
            if receive_real_ovc or market_service:
                
                self.label_clear(self.alternate_flag) 

                # 그래프 그리기

                # Plot 1 x축 타임라인
                if comboindex1 == 0 or comboindex1 == 4:

                    plot1_time_line.setValue(x_idx)
                else:
                    plot1_time_line.setValue(opt_x_idx)

                # Plot 2 x축 타임라인
                plot2_time_line.setValue(opt_x_idx)

                if UI_STYLE == 'Vertical_view.ui':

                    # Plot 3 x축 타임라인
                    plot3_time_line.setValue(ovc_x_idx)

                    # Plot 4 x축 타임라인
                    plot4_time_line.setValue(x_idx)
                else:
                    pass

                # 옵션그래프 초기화
                if comboindex2 == 4:

                    for i in range(29):
                        call_curve[i].clear()
                        put_curve[i].clear()

                    # 옵션 Y축 최대값 구하기
                    axY = self.Plot2.getAxis('left')
                    #print('옵션 y axis range: {}'.format(axY.range[1]))

                    if 6.0 <= axY.range[1] < 7.1:
                        mv_line[6].setValue(6.85)
                        mv_line[7].setValue(0)
                        mv_line[8].setValue(0)
                    elif 7.1 <= axY.range[1] < 8.1:
                        mv_line[6].setValue(6.85)
                        mv_line[7].setValue(7.1)
                        mv_line[8].setValue(0)
                    elif axY.range[1] >= 8.1:
                        mv_line[6].setValue(6.85)
                        mv_line[7].setValue(7.1)
                        mv_line[8].setValue(8.1)
                    else:
                        pass

                    # 4종의 그래프데이타를 받아옴
                    global selected_call, selected_put

                    call_idx = []
                    put_idx = []

                    # atm index 중심으로 위,아래 15개 만 탐색
                    #for i in range(option_pairs_count):
                    for i in range(atm_index - 15, atm_index + 16):

                        if self.tableWidget_call.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                            call_idx.append(i)
                        else:
                            pass

                        if self.tableWidget_put.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                            put_idx.append(i)
                        else:
                            pass                

                    selected_call = call_idx
                    selected_put = put_idx            
                else:
                    pass            

                for actval, infos in data.items():

                    index = opt_actval.index(actval)

                    if comboindex2 == 4:

                        for i in range(len(call_idx)):

                            if index == call_idx[i]:
                                call_curve[i].setData(infos[0])
                            else:
                                pass                    

                        for i in range(len(put_idx)):

                            if index == put_idx[i]:
                                put_curve[i].setData(infos[1])
                            else:
                                pass
                    else:
                        pass           

                    if index == option_pairs_count - 1:

                        curve1_data = infos[2]
                        curve2_data = infos[3] 
                        curve3_data = infos[4]
                        curve4_data = infos[5]
                        curve5_data = infos[6]
                        curve6_data = infos[7]

                        if UI_STYLE == 'Vertical_view.ui':

                            plot3_data = infos[8]
                            plot4_1_data = infos[9]
                            plot4_2_data = infos[10]
                        else:
                            pass
                    else:
                        pass
                
                # Plot 3, Plot4 그리기
                if UI_STYLE == 'Vertical_view.ui':

                    if comboindex3 == 0:
                        
                        if DOW_LAST_LOW > 0:
                            plot3_ovc_jl_line.setValue(DOW_LAST_LOW)
                        else:
                            pass 
                        
                        if DOW_LAST_HIGH > 0:
                            plot3_ovc_jh_line.setValue(DOW_LAST_HIGH)
                        else:
                            pass
                        
                        if dow_전일종가 > 0:
                            plot3_ovc_close_line.setValue(dow_전일종가)
                        else:
                            pass
                        
                        if dow_시가 > 0:
                            plot3_ovc_open_line.setValue(dow_시가)
                        else:
                            pass
                        
                        if dow_피봇 > 0:
                            plot3_ovc_pivot_line.setValue(dow_피봇)
                        else:
                            pass
                        
                        if dow_저가 > 0:
                            plot3_ovc_low_line.setValue(dow_저가)
                        else:
                            pass

                        if dow_고가 > 0:
                            plot3_ovc_high_line.setValue(dow_고가)
                        else:
                            pass                       
                        
                        plot3_curve.setData(plot3_data)

                    elif comboindex3 == 1:
                        
                        if SP500_LAST_LOW > 0:
                            plot3_ovc_jl_line.setValue(SP500_LAST_LOW)
                        else:
                            pass 

                        if SP500_LAST_HIGH > 0:
                            plot3_ovc_jh_line.setValue(SP500_LAST_HIGH)
                        else:
                            pass

                        if sp500_전일종가 > 0:
                            plot3_ovc_close_line.setValue(sp500_전일종가)
                        else:
                            pass 
                        
                        if sp500_시가 > 0:
                            plot3_ovc_open_line.setValue(sp500_시가)
                        else:
                            pass

                        if sp500_피봇 > 0:
                            plot3_ovc_pivot_line.setValue(sp500_피봇)
                        else:
                            pass

                        if sp500_저가 > 0:
                            plot3_ovc_low_line.setValue(sp500_저가)
                        else:
                            pass

                        if sp500_고가 > 0:
                            plot3_ovc_high_line.setValue(sp500_고가)
                        else:
                            pass
                        
                        plot3_curve.setData(plot3_data)

                    elif comboindex3 == 2:
                        
                        if NASDAQ_LAST_LOW > 0:
                            plot3_ovc_jl_line.setValue(NASDAQ_LAST_LOW)
                        else:
                            pass 

                        if NASDAQ_LAST_HIGH > 0:
                            plot3_ovc_jh_line.setValue(NASDAQ_LAST_HIGH)
                        else:
                            pass

                        if nasdaq_전일종가 > 0:
                            plot3_ovc_close_line.setValue(nasdaq_전일종가)
                        else:
                            pass
                        
                        if nasdaq_시가 > 0:
                            plot3_ovc_open_line.setValue(nasdaq_시가)
                        else:
                            pass   

                        if nasdaq_피봇 > 0:
                            plot3_ovc_pivot_line.setValue(nasdaq_피봇)
                        else:
                            pass

                        if nasdaq_저가 > 0:
                            plot3_ovc_low_line.setValue(nasdaq_저가)
                        else:
                            pass

                        if nasdaq_고가 > 0:
                            plot3_ovc_high_line.setValue(nasdaq_고가)
                        else:
                            pass
                        
                        plot3_curve.setData(plot3_data)
                    else:
                        pass
                    
                    if comboindex4 == 0:
                        
                        if 선물_전저 > 0:
                            plot4_fut_jl_line.setValue(선물_전저)
                        else:
                            pass

                        if 선물_전고 > 0:
                            plot4_fut_jh_line.setValue(선물_전고)
                        else:
                            pass

                        if 선물_종가 > 0:
                            plot4_fut_close_line.setValue(선물_종가)
                        else:
                            pass
                        
                        if 선물_시가 > 0:
                            plot4_fut_open_line.setValue(선물_시가)
                        else:
                            pass

                        if 선물_피봇 > 0:
                            plot4_fut_pivot_line.setValue(선물_피봇)
                        else:
                            pass

                        if 선물_저가 > 0:
                            plot4_fut_low_line.setValue(선물_저가)
                        else:
                            pass

                        if 선물_고가 > 0:
                            plot4_fut_high_line.setValue(선물_고가)
                        else:
                            pass
                        
                        plot4_price_curve.setData(plot4_1_data)
                        plot4_kp200_curve.setData(plot4_2_data)
                        
                    elif comboindex4 == 1:                        
                        
                        if 선물_누적거래량 > 0:

                            plot4_fv_plus_curve.setData(plot4_1_data)
                        else:
                            plot4_fv_minus_curve.setData(plot4_1_data)
                    else:
                        pass                    
                else:
                    pass

                # 선택된 plot1 그래프 그리기
                if comboindex1 == 0:

                    if 선물_누적거래량 > 0:
                        plot1_fut_volume_plus_curve.setData(curve1_data)
                    else:
                        plot1_fut_volume_minus_curve.setData(curve1_data)

                elif comboindex1 == 1:                      
                    
                    plot1_call_volume_curve.setData(curve1_data)
                    plot1_put_volume_curve.setData(curve2_data)
                    plot1_volume_cha_curve.setData(curve3_data)

                elif comboindex1 == 2:
                                       
                    if not overnight:
                        plot1_call_oi_curve.setData(curve1_data)
                        plot1_put_oi_curve.setData(curve2_data)
                    else:
                        pass

                elif comboindex1 == 3:

                    plot1_two_sum_curve.setData(curve1_data)
                    plot1_two_cha_curve.setData(curve2_data)

                elif comboindex1 == 4:
                
                    plot1_kp200_curve.setData(curve1_data)
                    plot1_fut_price_curve.setData(curve2_data)

                elif comboindex1 == 5:

                    plot1_sp500_curve.setData(curve1_data)

                    plot1_hc_high_line.setValue(sp500_고가)
                    plot1_hc_low_line.setValue(sp500_저가)

                elif comboindex1 == 6:

                    plot1_dow_curve.setData(curve1_data)

                    plot1_hc_high_line.setValue(dow_고가)
                    plot1_hc_low_line.setValue(dow_저가)

                elif comboindex1 == 7:

                    plot1_nasdaq_curve.setData(curve1_data)

                    plot1_hc_high_line.setValue(nasdaq_고가)
                    plot1_hc_low_line.setValue(nasdaq_저가)
                else:
                    pass   

                # 선택된 plot2 그래프 그리기
                if comboindex2 == 0:
                                        
                    plot2_call_volume_curve.setData(curve4_data)
                    plot2_put_volume_curve.setData(curve5_data)  
                    plot2_volume_cha_curve.setData(curve6_data) 

                elif comboindex2 == 1:
                                        
                    if not overnight:
                        plot2_call_oi_curve.setData(curve4_data)
                        plot2_put_oi_curve.setData(curve5_data)
                    else:
                        pass         

                elif comboindex2 == 2:

                    if 선물_누적거래량 > 0:
                        plot2_fut_volume_plus_curve.setData(curve4_data)
                    else:
                        plot2_fut_volume_minus_curve.setData(curve4_data)

                elif comboindex2 == 3:

                    plot2_two_sum_curve.setData(curve4_data)
                    plot2_two_cha_curve.setData(curve5_data)

                elif comboindex2 == 4:

                    pass

                elif comboindex2 == 5:

                    plot2_sp500_curve.setData(curve4_data) 

                    plot2_hc_high_line.setValue(sp500_고가)
                    plot2_hc_low_line.setValue(sp500_저가)

                elif comboindex2 == 6: 

                    plot2_dow_curve.setData(curve4_data) 

                    plot2_hc_high_line.setValue(dow_고가)
                    plot2_hc_low_line.setValue(dow_저가)

                elif comboindex2 == 7: 

                    plot2_nasdaq_curve.setData(curve4_data)

                    plot2_hc_high_line.setValue(nasdaq_고가)
                    plot2_hc_low_line.setValue(nasdaq_저가)
                else:
                    pass          

                # 호가 갱신
                if receive_quote:

                    if self.alternate_flag:

                        self.quote_display()
                    else:
                        pass
                else:
                    pass

                if market_service:                                      
                    
                    # 시작과 동시에 컬러링 갱신
                    if opt_x_idx > 선물장간_시간차:

                        # 선물, 콜, 풋 현재가 클리어
                        #self.cv_color_clear()
                        self.price_color_clear()
                        
                        if self.alternate_flag:

                            # 콜 테이블 데이타 갱신
                            self.call_oi_update()                  
                            self.call_volume_power_update()

                            #self.call_state_update() 
                            self.call_db_update()

                            if not overnight:

                                self.label_atm_display()
                            else:
                                pass                                                               
                        else:
                            # 풋 테이블 데이타 갱신
                            self.put_oi_update()
                            self.put_volume_power_update()

                            #self.put_state_update()
                            self.put_db_update()

                            if not overnight:

                                self.oi_sum_display()
                            else:
                                pass
                            
                            # 옵션 저가, 고가 갱신시 방향화살표 OFF
                            global call_low_touch, call_high_touch, put_low_touch, put_high_touch 

                            if call_low_touch:
                                
                                item = QTableWidgetItem('저가')
                                self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)
                                #self.tableWidget_call.resizeColumnsToContents() 

                                call_low_touch = False
                            else:
                                pass

                            if call_high_touch:

                                item = QTableWidgetItem('고가')
                                self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)
                                #self.tableWidget_call.resizeColumnsToContents()

                                call_high_touch = False
                            else:
                                pass

                            if put_low_touch:

                                item = QTableWidgetItem('저가')
                                self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)
                                #self.tableWidget_put.resizeColumnsToContents() 

                                put_low_touch = False
                            else:
                                pass

                            if put_high_touch:

                                item = QTableWidgetItem('고가')
                                self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)
                                #self.tableWidget_put.resizeColumnsToContents()

                                put_high_touch = False
                            else:
                                pass

                        if not dongsi_hoga:
                        
                            # 진성 의미가인 경우 blinking(매우 중요 !!!)      

                            global call_low_coreval_str, call_high_coreval_str, put_low_coreval_str, put_high_coreval_str
                            global call_low_node_count, call_high_node_count, put_low_node_count, put_high_node_count
                            global call_low_node_list, call_high_node_list, put_low_node_list, put_high_node_list
                            global call_low_node_str, call_high_node_str, put_low_node_str, put_high_node_str

                            if flag_call_low_coreval:
                                self.call_low_coreval_color_blink(self.alternate_flag)
                            else:                        
                                call_low_coreval_str = ''
                                call_low_node_count = 0
                                call_low_node_list = []
                                call_low_node_str = ''

                            if flag_call_high_coreval:
                                self.call_high_coreval_color_blink(self.alternate_flag)
                            else:
                                call_high_coreval_str = ''
                                call_high_node_count = 0
                                call_high_node_list = []
                                call_high_node_str = ''

                            if flag_put_low_coreval:
                                self.put_low_coreval_color_blink(self.alternate_flag)
                            else:
                                put_low_coreval_str = ''
                                put_low_node_count = 0
                                put_low_node_list = []
                                put_low_node_str = ''

                            if flag_put_high_coreval:
                                self.put_high_coreval_color_blink(self.alternate_flag)                        
                            else:
                                put_high_coreval_str = '' 
                                put_high_node_count = 0
                                put_high_node_list = []
                                put_high_node_str = ''

                            global kp200_low_node_str, kp200_high_node_str                            

                            if flag_kp200_low_node:

                                self.kp200_low_color_blink(self.alternate_flag)
                            else:
                                kp200_low_node_str = ''

                            if flag_kp200_high_node:

                                self.kp200_high_color_blink(self.alternate_flag)
                            else:
                                kp200_high_node_str = ''
                        else:
                            pass                                               
                    else:
                        pass

                    # 비대칭장 탐색
                    if not dongsi_hoga and abs(콜대비합_단위평균) > 0 and abs(풋대비합_단위평균) > 0:

                        self.asym_detect(self.alternate_flag)
                    else:
                        pass                    
                    
                    # 원웨이장 표시(주간만) --> 비대칭장으로 파악(CM + NM + MAN)
                    if not overnight and not dongsi_hoga:

                        if TARGET_MONTH_SELECT == 1:

                            #self.check_oneway(self.alternate_flag)
                            self.display_centerval()

                        else:
                            pass
                    else:
                        pass
                                                    
                else:
                    pass          
            else:
                pass

            # 오전 7시 10분경 증권사 서버초기화전에 프로그램을 미리 오프라인으로 전환하여야 Crash 발생안함
            if overnight:

                보정된시간 = 시스템시간 - 시스템_서버_시간차

                if 보정된시간 == 6 * 3600 + 1 * 60:

                    str = '[{0:02d}:{1:02d}:{2:02d}] 시스템 서버간 시간차 = {3}초... \r'.format(dt.hour, dt.minute, dt.second, 시스템_서버_시간차)
                    self.textBrowser.append(str)
                    print(str)

                    # 해외선물 지수요청 취소                    
                    self.OVC.UnadviseRealData()

                    str = '[{0:02d}:{1:02d}:{2:02d}] 해외선물 지수요청을 취소(서버시간) 합니다. \r'.format \
                        (int(OVC_체결시간[0:2]), 
                        int(OVC_체결시간[2:4]), 
                        int(OVC_체결시간[4:6]))
                    self.textBrowser.append(str)
                    print(str)
                else:
                    pass

                if dt.hour == 7 and dt.minute == 0:

                    if self.parent.connection.IsConnected() and not flag_offline:

                        # 다음날 해외선물 피봇계산을 위해 종료시(5시 59분 57초 ?) 마지막 값 저장
                        str = '[{0:02d}:{1:02d}:{2:02d}] CME 종가 = {3:0.2f}, DOW 종가 = {4:0.2f}\r'.format \
                            (int(OVC_체결시간[0:2]), 
                            int(OVC_체결시간[2:4]), 
                            int(OVC_체결시간[4:6]),
                            cme_close, dow_close)
                        self.textBrowser.append(str)
                        print(str)

                        str = '[{0:02d}:{1:02d}:{2:02d}] SP500 Low = {3:0.2f}, SP500 High = {4:0.2f}, SP500 Close = {5:0.2f}\r'.format \
                            (int(OVC_체결시간[0:2]), 
                            int(OVC_체결시간[2:4]), 
                            int(OVC_체결시간[4:6]),
                            sp500_저가, sp500_고가, sp500_price)
                        self.textBrowser.append(str)
                        print(str)

                        str = '[{0:02d}:{1:02d}:{2:02d}] DOW Low = {3:0.1f}, DOW High = {4:0.1f}, DOW Close = {5:0.1f}\r'.format \
                            (int(OVC_체결시간[0:2]), 
                            int(OVC_체결시간[2:4]), 
                            int(OVC_체결시간[4:6]),
                            dow_저가, dow_고가, dow_price)
                        self.textBrowser.append(str)
                        print(str)

                        str = '[{0:02d}:{1:02d}:{2:02d}] NASDAQ Low = {3:0.2f}, NASDAQ High = {4:0.2f}, NASDAQ Close = {5:0.2f}\r'.format \
                            (int(OVC_체결시간[0:2]), 
                            int(OVC_체결시간[2:4]), 
                            int(OVC_체결시간[4:6]),
                            nasdaq_저가, nasdaq_고가, nasdaq_price)
                        self.textBrowser.append(str)
                        print(str)

                        str = '[{0:02d}:{1:02d}:{2:02d}] 야간장 주요정보를 저징합니다...\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)
                        print(str)
                        
                        # 야간장의 주요정보를 저장
                        with open('overnight_info.txt', mode='w') as overnight_file:

                            file_str = '################# < Futures Index of the Last Night > ###################\n'
                            overnight_file.write(file_str)
                            file_str = 'Overnight DOW Close = {0}\n'.format(dow_close)
                            overnight_file.write(file_str)
                            file_str = 'Overnight CME FUT Close = {0}\n'.format(cme_close)
                            overnight_file.write(file_str)
                            file_str = '\n'
                            overnight_file.write(file_str)
                            file_str = '##################### < US Index of the Last Night > ####################\n'
                            overnight_file.write(file_str)
                            file_str = 'S&P 500 Last Low = {0}\n'.format(sp500_저가)
                            overnight_file.write(file_str)
                            file_str = 'S&P 500 Last High = {0}\n'.format(sp500_고가)
                            overnight_file.write(file_str)
                            file_str = 'DOW Last Low = {0}\n'.format(dow_저가)
                            overnight_file.write(file_str)
                            file_str = 'DOW Last High = {0}\n'.format(dow_고가)
                            overnight_file.write(file_str)
                            file_str = 'NASDAQ Last Low = {0}\n'.format(nasdaq_저가)
                            overnight_file.write(file_str)
                            file_str = 'NASDAQ Last High = {0}\n'.format(nasdaq_고가)
                            overnight_file.write(file_str)
                            overnight_file.close()

                        str = '[{0:02d}:{1:02d}:{2:02d}] 서버 연결을 해제합니다...\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)
                        print(str)

                        flag_offline = True  

                        self.parent.connection.disconnect()
                    else:
                        self.parent.statusbar.showMessage("오프라인")
                else:
                    pass
            else:
                pass    
            
            if not flag_offline:

                str = '[{0:02d}:{1:02d}:{2:02d}] Screen Update Time : {3:0.2f} ms...\r'.format(\
                    dt.hour, dt.minute, dt.second, (timeit.default_timer() - start_time) * 1000)
                print(str)
            else:
                pass
            
        except:
            pass

    def market_type_display(self, blink):

        dt = datetime.datetime.now()

        # 해외선물 한국시간 표시
        if OVC_체결시간 == '000000':

            str = 'ⓜ {0:02d}:{1:02d}:{2:02d}'.format(dt.hour, dt.minute, dt.second)
        else:
            str = 'ⓢ {0:02d}:{1:02d}:{2:02d}'.format(int(OVC_체결시간[0:2]), int(OVC_체결시간[2:4]), int(OVC_체결시간[4:6]))
            
        self.label_msg.setText(str)
        
        # 콜 매수 OneWay장
        if call_ms_oneway:

            if blink:
                self.label_msg.setStyleSheet('background-color: red; color: white')
            else:
                self.label_msg.setStyleSheet('background-color: white; color: red')

        # 콜 매수 비대칭장
        elif call_ms_asymmetric:

            self.label_msg.setStyleSheet('background-color: red; color: white')

        # 콜 매도 비대칭장
        elif call_md_asymmetric:

            self.label_msg.setStyleSheet('background-color: black; color: pink')

        # 콜 매도 양꽝장
        elif call_md_all_dying:

            self.label_msg.setStyleSheet('background-color: black; color: magenta')

        # 풋 매수 OneWay장
        elif put_ms_oneway:

            if blink:
                self.label_msg.setStyleSheet('background-color: blue; color: white')
            else:
                self.label_msg.setStyleSheet('background-color: white; color: blue')

        # 풋 매수 비대칭장
        elif put_ms_asymmetric:

            self.label_msg.setStyleSheet('background-color: blue; color: white')

        # 풋 매도 비대칭장
        elif put_md_asymmetric:

            self.label_msg.setStyleSheet('background-color: black; color: lightskyblue')

        # 풋 매도 양꽝장
        elif put_md_all_dying:

            self.label_msg.setStyleSheet('background-color: black; color: cyan')
        else:
            # 대칭장
            self.label_msg.setStyleSheet('background-color: lawngreen; color: black')
        
        self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))

        return
    
    def opt_call_node_coloring(self):

        global coloring_done_time
        global node_coloring

        dt = datetime.datetime.now()
        start_time = timeit.default_timer()

        if market_service:

            node_coloring = True

            self.call_node_color_clear()        
            self.call_open_check()        
            self.call_crossval_color_update()        
            self.call_node_color_update()

            self.call_coreval_color_update()

            node_coloring = False

            process_time = (timeit.default_timer() - start_time) * 1000

            str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Call Node Color Check Time : {3:0.2f} ms\r'.format(\
                int(call_result['체결시간'][0:2]), int(call_result['체결시간'][2:4]), int(call_result['체결시간'][4:6]), process_time)
            self.textBrowser.append(str)

        else:
            node_coloring = True

            self.call_node_color_clear()        
            self.call_open_check()        
            self.call_crossval_color_update()        
            self.call_node_color_update()
            self.call_coreval_color_update()

            node_coloring = False

            process_time = (timeit.default_timer() - start_time) * 1000

            str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Call Node Color Check Time : {3:0.2f} ms\r'.format(dt.hour, dt.minute, dt.second, process_time)
            self.textBrowser.append(str)

        return

    def opt_call_low_node_coloring(self):

        global coloring_done_time
        global node_coloring
        global 콜_체결_초

        dt = datetime.datetime.now()

        if int(call_result['체결시간'][4:6]) == 콜_체결_초:
            
            # 진성맥점 발생여부는 저,고 갱신시 반드시 수행
            self.call_low_coreval_color_update()
            '''
            str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Call Low Coreval Color Check !!!\r'.format(\
                int(call_result['체결시간'][0:2]), int(call_result['체결시간'][2:4]), int(call_result['체결시간'][4:6]))
            #self.textBrowser.append(str)
            print(str) 
            '''   
        else:

            start_time = timeit.default_timer()

            node_coloring = True

            self.call_node_color_clear()        
            self.call_open_check()        
            self.call_crossval_color_update()        
            self.call_node_color_update()

            self.call_low_coreval_color_update()

            node_coloring = False

            process_time = (timeit.default_timer() - start_time) * 1000

            콜_체결_초 = int(call_result['체결시간'][4:6])

            str = '[{0:02d}:{1:02d}:{2:02d}] Call Low Node Color Check Time : {3:0.2f} ms\r'.format(\
                int(call_result['체결시간'][0:2]), int(call_result['체결시간'][2:4]), int(call_result['체결시간'][4:6]), process_time)
            self.textBrowser.append(str)

        return        

    def opt_call_high_node_coloring(self):

        global coloring_done_time
        global node_coloring
        global 콜_체결_초

        dt = datetime.datetime.now()

        if int(call_result['체결시간'][4:6]) == 콜_체결_초:
            
            # 진성맥점 발생여부는 저,고 갱신시 반드시 수행
            self.call_high_coreval_color_update()
            '''
            str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Call High Coreval Color Check !!!\r'.format(\
                int(call_result['체결시간'][0:2]), int(call_result['체결시간'][2:4]), int(call_result['체결시간'][4:6]))
            #self.textBrowser.append(str)
            print(str)
            '''    
        else:

            start_time = timeit.default_timer()

            node_coloring = True

            self.call_node_color_clear()        
            self.call_open_check()        
            self.call_crossval_color_update()        
            self.call_node_color_update()

            self.call_high_coreval_color_update()

            node_coloring = False

            process_time = (timeit.default_timer() - start_time) * 1000

            콜_체결_초 = int(call_result['체결시간'][4:6])

            str = '[{0:02d}:{1:02d}:{2:02d}] Call High Node Color Check Time : {3:0.2f} ms\r'.format(\
                int(call_result['체결시간'][0:2]), int(call_result['체결시간'][2:4]), int(call_result['체결시간'][4:6]), process_time)
            self.textBrowser.append(str)

        return                
    
    def opt_put_node_coloring(self):

        global coloring_done_time
        global node_coloring

        dt = datetime.datetime.now()
        start_time = timeit.default_timer()

        if market_service:

            node_coloring = True

            self.put_node_color_clear()        
            self.put_open_check()        
            self.put_crossval_color_update()        
            self.put_node_color_update()

            self.put_coreval_color_update()

            node_coloring = False

            process_time = (timeit.default_timer() - start_time) * 1000

            str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Put Node Color Check Time : {3:0.2f} ms\r'.format(\
                int(put_result['체결시간'][0:2]), int(put_result['체결시간'][2:4]), int(put_result['체결시간'][4:6]), process_time)
            self.textBrowser.append(str)
                                 
        else:
            node_coloring = True

            self.put_node_color_clear()        
            self.put_open_check()        
            self.put_crossval_color_update()        
            self.put_node_color_update()
            self.put_coreval_color_update()

            node_coloring = False

            process_time = (timeit.default_timer() - start_time) * 1000

            str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Put Node Color Check Time : {3:0.2f} ms\r'.format(dt.hour, dt.minute, dt.second, process_time)
            self.textBrowser.append(str)

        return

    def opt_put_low_node_coloring(self):

        global coloring_done_time
        global node_coloring
        global 풋_체결_초

        dt = datetime.datetime.now()

        if int(put_result['체결시간'][4:6]) == 풋_체결_초:

            # 진성맥점 발생여부는 저,고 갱신시 반드시 수행
            self.put_low_coreval_color_update()
            '''
            str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Put Low Coreval Color Check !!!\r'.format(\
                int(put_result['체결시간'][0:2]), int(put_result['체결시간'][2:4]), int(put_result['체결시간'][4:6]))
            #self.textBrowser.append(str)
            print(str)
            '''
        else:

            start_time = timeit.default_timer()

            node_coloring = True

            self.put_node_color_clear()        
            self.put_open_check()        
            self.put_crossval_color_update()        
            self.put_node_color_update()

            self.put_low_coreval_color_update()

            node_coloring = False

            process_time = (timeit.default_timer() - start_time) * 1000

            풋_체결_초 = int(put_result['체결시간'][4:6])

            str = '[{0:02d}:{1:02d}:{2:02d}] Put Low Node Color Check Time : {3:0.2f} ms\r'.format(\
                int(put_result['체결시간'][0:2]), int(put_result['체결시간'][2:4]), int(put_result['체결시간'][4:6]), process_time)
            self.textBrowser.append(str)

        return

    def opt_put_high_node_coloring(self):

        global coloring_done_time
        global node_coloring
        global 풋_체결_초

        dt = datetime.datetime.now()

        if int(put_result['체결시간'][4:6]) == 풋_체결_초:

            # 진성맥점 발생여부는 저,고 갱신시 반드시 수행
            self.put_high_coreval_color_update()
            '''
            str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Put High Coreval Color Check !!!\r'.format(\
                int(put_result['체결시간'][0:2]), int(put_result['체결시간'][2:4]), int(put_result['체결시간'][4:6]))
            #self.textBrowser.append(str)
            print(str)
            '''
        else:

            start_time = timeit.default_timer()

            node_coloring = True

            self.put_node_color_clear()        
            self.put_open_check()        
            self.put_crossval_color_update()        
            self.put_node_color_update()

            self.put_high_coreval_color_update()

            node_coloring = False

            process_time = (timeit.default_timer() - start_time) * 1000

            풋_체결_초 = int(put_result['체결시간'][4:6])

            str = '[{0:02d}:{1:02d}:{2:02d}] Put High Node Color Check Time : {3:0.2f} ms\r'.format(\
                int(put_result['체결시간'][0:2]), int(put_result['체결시간'][2:4]), int(put_result['체결시간'][4:6]), process_time)
            self.textBrowser.append(str) 

        return

    # 탐색순서가 중요 !!!
    def opt_node_coloring(self):

        global coloring_done_time
        global node_coloring

        dt = datetime.datetime.now()

        start_time = timeit.default_timer()

        node_coloring = True

        self.call_node_color_clear()
        self.call_open_check()
        self.call_crossval_color_update()
        self.call_node_color_update()
        self.call_coreval_color_update()

        self.put_node_color_clear()
        self.put_open_check()
        self.put_crossval_color_update()
        self.put_node_color_update()
        self.put_coreval_color_update()

        node_coloring = False
        '''
        current_str = dt.strftime('%H:%M:%S')
        coloring_done_time = int(current_str[0:2]) * 3600 + int(current_str[3:5]) * 60 + int(current_str[6:8])

        str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Color Update Done {3}...\r'.format(dt.hour, dt.minute, dt.second, coloring_done_time)
        self.textBrowser.append(str)
        '''
        process_time = (timeit.default_timer() - start_time) * 1000

        str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 Node Color Check Time : {3:0.2f} ms\r'.format(dt.hour, dt.minute, dt.second, process_time)
        self.textBrowser.append(str)

        return        

    def label_atm_display(self):

        global df_plotdata_two_sum, df_plotdata_two_cha, basis
        global atm_str, atm_val, atm_index, atm_index_old
        
        df_plotdata_two_sum[opt_x_idx] = call_atm_value + put_atm_value
        df_plotdata_two_cha[opt_x_idx] = call_atm_value - put_atm_value
        
        # 등가 check & coloring
        atm_str = self.find_ATM(fut_realdata['KP200'])
        atm_index = opt_actval.index(atm_str)

        if atm_str[-1] == '2' or atm_str[-1] == '7':

            atm_val = float(atm_str) + 0.5
        else:
            atm_val = float(atm_str)

        if atm_index != atm_index_old:

            self.tableWidget_call.item(atm_index, Option_column.행사가.value).setBackground(
                QBrush(노란색))
            self.tableWidget_call.item(atm_index_old, Option_column.행사가.value).setBackground(
                QBrush(라임))

            self.tableWidget_put.item(atm_index, Option_column.행사가.value).setBackground(
                QBrush(노란색))
            self.tableWidget_put.item(atm_index_old, Option_column.행사가.value).setBackground(
                QBrush(라임))

            atm_index_old = atm_index
        else:
            pass

        basis = fut_realdata['현재가'] - fut_realdata['KP200']

        if basis < 0:

            self.label_atm.setStyleSheet('background-color: black; color: yellow')
            self.label_atm.setFont(QFont("Consolas", 9, QFont.Bold))
        else:
            self.label_atm.setStyleSheet('background-color: yellow; color: black')
            self.label_atm.setFont(QFont("Consolas", 9, QFont.Bold))

        str = '{0:0.2f}({1:0.2f}:{2:0.2f})'.format(basis, call_atm_value + put_atm_value,
            abs(call_atm_value - put_atm_value))

        self.label_atm.setText(str)

        return

    def set_call_atm_row_color(self, rowIndex, brush):

        for j in range(self.tableWidget_call.columnCount() - 1):
            self.tableWidget_call.item(rowIndex, j + 1).setBackground(brush)

    def set_put_atm_row_color(self, rowIndex, brush):

        for j in range(self.tableWidget_put.columnCount() - 1):
            self.tableWidget_put.item(rowIndex, j + 1).setBackground(brush)

    def within_n_tick(self, source, target, n):

        if round((target - 0.01*n), 2) <= source <= round((target + 0.01*n), 2):
            return True
        else:
            return False

    def calc_pivot(self, jl, jh, jc, do):

        if jl > 0 and jh > 0 and jc > 0 and do > 0:
            tmp = (jl + jh + jc)/3 + (do - jc)
            pivot = round(tmp, 2)

            return pivot
        else:
            return 0

    def make_node_list(self, input_list):

        list_low = []
        list_zero = []
        list_high = []

        if 0 in input_list:
            input_list.remove(0)
        else:
            pass

        if 0.01 in input_list:
            input_list.remove(0.01)
        else:
            pass

        temp = list(set(input_list))
        temp.sort()

        # 컬러링 탐색구간 설정(0.1 ~ 20)
        index1 = bisect(temp, nodelist_low_cutoff)
        index2 = bisect(temp, nodelist_high_cutoff)

        list_singleval = temp[index1:index2]

        for i in range(len(list_singleval)):
            list_low.append(round(list_singleval[i] - 0.01, 2))
            list_zero.append(round(list_singleval[i] + 0.0, 2))
            list_high.append(round(list_singleval[i] + 0.01, 2))

        output_list = list_low + list_zero + list_high
        output_list.sort()

        return output_list

    def find_ATM(self, kp200):

        temp = math.floor(round(kp200 / 2.5, 0) * 2.5)
        str_atm = '{0:0.0f}'.format(temp)

        return str_atm

    '''
    def image_grab(self):
        
        now = time.localtime()
        times = "%04d-%02d-%02d-%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        
        hwnd = win32gui.FindWindow(None, cm_option_title)
        win32gui.SetForegroundWindow(hwnd)
        dimensions = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(dimensions)

        print('ImageGrab dimensions = ', dimensions)
        
        #img = self.capture_screenshot()

        #saveas = "Screenshot {}{}".format(times, '.png')
        #img.save(saveas)

        #str = '[{0:02d}:{1:02d}:{2:02d}] 화면을 캡처했습니다.\r'.format(now.tm_hour, now.tm_min, now.tm_sec)
        #self.textBrowser.append(str)
        
        return
    '''

    # 현재가 클리어
    def cv_color_clear(self):

        if overnight:
            self.tableWidget_fut.item(0, Futures_column.현재가.value).setBackground(QBrush(옅은회색))
        else:
            self.tableWidget_fut.item(1, Futures_column.현재가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_fut.item(2, Futures_column.현재가.value).setBackground(QBrush(옅은회색))

        global call_scroll_end_position

        if call_scroll_end_position > option_pairs_count:

            call_scroll_end_position = option_pairs_count
        else:
            pass

        for i in range(call_scroll_begin_position, call_scroll_end_position):

            self.tableWidget_call.item(i, Option_column.현재가.value).setBackground(QBrush(옅은회색))

        global put_scroll_end_position

        if put_scroll_end_position > option_pairs_count:

            put_scroll_end_position = option_pairs_count
        else:
            pass

        for i in range(put_scroll_begin_position, put_scroll_end_position):

            self.tableWidget_put.item(i, Option_column.현재가.value).setBackground(QBrush(옅은회색))

        return

    # 저가, 현재가, 고가 클리어
    def price_color_clear(self):

        # 선물
        if overnight:
            self.tableWidget_fut.item(0, Futures_column.현재가.value).setBackground(QBrush(흰색))
        else:
            self.tableWidget_fut.item(1, Futures_column.현재가.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(2, Futures_column.현재가.value).setBackground(QBrush(흰색))

        global call_scroll_end_position

        if call_scroll_end_position > option_pairs_count:

            call_scroll_end_position = option_pairs_count
        else:
            pass

        # 콜
        for i in range(call_scroll_begin_position, call_scroll_end_position):

            self.tableWidget_call.item(i, Option_column.현재가.value).setBackground(QBrush(흰색))

        global put_scroll_end_position

        if put_scroll_end_position > option_pairs_count:

            put_scroll_end_position = option_pairs_count
        else:
            pass

        # 풋
        for i in range(put_scroll_begin_position, put_scroll_end_position):

            self.tableWidget_put.item(i, Option_column.현재가.value).setBackground(QBrush(흰색))

        return

    '''
    # 선물 현재가 클리어
    def fut_cv_color_clear(self):

        if overnight:
            self.tableWidget_fut.item(0, Futures_column.현재가.value).setBackground(QBrush(옅은회색))
        else:
            self.tableWidget_fut.item(1, Futures_column.현재가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_fut.item(2, Futures_column.현재가.value).setBackground(QBrush(옅은회색))

        return

    # Call 컬러처리
    def call_cv_color_clear(self):

        if call_scroll_end_position <= option_pairs_count:

            for i in range(call_scroll_begin_position, call_scroll_end_position):

                self.tableWidget_call.item(i, Option_column.현재가.value).setBackground(QBrush(옅은회색))
        else:
            pass

        return
    
    # Put 컬러처리
    def put_cv_color_clear(self):

        if put_scroll_end_position <= option_pairs_count:

            for i in range(put_scroll_begin_position, put_scroll_end_position):

                self.tableWidget_put.item(i, Option_column.현재가.value).setBackground(QBrush(옅은회색))
        else:
            pass

        return
    '''

    def check_oneway(self, blink):

        dt = datetime.datetime.now()
        current_str = dt.strftime('%H:%M:%S')

        global call_ms_oneway, put_ms_oneway
        global call_oneway_level1, call_oneway_level2, call_oneway_level3, call_oneway_level4, call_oneway_level5
        global put_oneway_level1, put_oneway_level2, put_oneway_level3, put_oneway_level4, put_oneway_level5
        global oneway_first_touch, oneway_str

        if overnight:

            pass
        else:
            # oneway check
            if (풋대비합 > 0 and 콜대비합 < 0) and (FUT_INSTITUTIONAL_거래대금순매수 > ONEWAY_THRESHOLD or FUT_RETAIL_거래대금순매수 > ONEWAY_THRESHOLD):

                if 선물_거래대금순매수 > 0 and 현물_거래대금순매수 < 0 \
                    and FUT_FOREIGNER_거래대금순매수 < 0 and 프로그램_전체순매수금액 < 0 and KOSPI_FOREIGNER_거래대금순매수 < 0 and fut_realdata['거래량'] < 0:

                    if blink:
                        self.label_msg.setStyleSheet('background-color: blue; color: white')
                        self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))
                    else:
                        self.label_msg.setStyleSheet('background-color: white; color: blue')
                        self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))

                    put_ms_oneway = True

                    # 시가갭 & 퍼센트로 oneway 판단
                    if 풋시가갭합 > 0 and 풋시가갭합_퍼센트 < 0:
                        
                        put_oneway_level3 = False
                        put_oneway_level4 = False
                        put_oneway_level5 = True

                        if blink:
                            self.label_msg.setStyleSheet('background-color: blue; color: white')
                            self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))                            

                            if dt.second % 10 == 0:
                                str = '[{0:02d}:{1:02d}:{2:02d}] 풋 OneWay 가능성 매우 높음(★★★★★)\r'.format(dt.hour, dt.minute, dt.second)
                                self.textBrowser.append(str)
                            else:
                                pass

                            if not oneway_first_touch:

                                oneway_str = '[{0:02d}:{1:02d}:{2:02d}] 풋 OneWay 가능성 매우 높음 !!!\r'.format(dt.hour, dt.minute, dt.second)
                                oneway_first_touch = True
                            else:
                                pass
                        else:
                            self.label_msg.setStyleSheet('background-color: white; color: blue')
                            self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))                        
                    else:
                        
                        put_oneway_level3 = False
                        put_oneway_level4 = True
                        put_oneway_level5 = False

                        if blink:                            

                            if dt.second % 10 == 0:
                                str = '[{0:02d}:{1:02d}:{2:02d}] 풋 OneWay 가능성 높음(★★★★)\r'.format(dt.hour, dt.minute, dt.second)
                                self.textBrowser.append(str)
                            else:
                                pass

                            if not oneway_first_touch:

                                oneway_str = '[{0:02d}:{1:02d}:{2:02d}] 풋 OneWay 가능성 높음 !!\r'.format(dt.hour, dt.minute, dt.second)
                                oneway_first_touch = True
                            else:
                                pass                 
                        else:
                            pass                 

                elif 선물_거래대금순매수 > 0 and 현물_거래대금순매수 < 0 \
                    and FUT_FOREIGNER_거래대금순매수 < 0 and 프로그램_전체순매수금액 < 0 and KOSPI_FOREIGNER_거래대금순매수 > 0 and fut_realdata['거래량'] < 0:

                    self.label_msg.setStyleSheet('background-color: blue; color: white')
                    self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))

                    put_ms_oneway = True

                    put_oneway_level3 = True
                    put_oneway_level4 = False
                    put_oneway_level5 = False                    

                    if dt.second % 10 == 0:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 풋 OneWay 가능성(★★★)\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)
                    else:
                        pass

                    if not oneway_first_touch:

                        oneway_str = '[{0:02d}:{1:02d}:{2:02d}] 풋 OneWay 가능성 !\r'.format(dt.hour, dt.minute, dt.second)
                        oneway_first_touch = True
                    else:
                        pass

                elif 선물_거래대금순매수 > 0 and 현물_거래대금순매수 < 0 \
                    and FUT_FOREIGNER_거래대금순매수 < 0 and 프로그램_전체순매수금액 > 0 and KOSPI_FOREIGNER_거래대금순매수 < 0 and fut_realdata['거래량'] < 0:

                    self.label_msg.setStyleSheet('background-color: blue; color: white')
                    self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))

                    put_ms_oneway = True
                    oneway_str = ''                    

                    if dt.second % 10 == 0:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 풋 OneWay 가능성(★★)\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)
                    else:
                        pass                   
                else:
                    pass     

            elif (풋대비합 < 0 and 콜대비합 > 0) and (FUT_INSTITUTIONAL_거래대금순매수 < -ONEWAY_THRESHOLD or FUT_RETAIL_거래대금순매수 < -ONEWAY_THRESHOLD):

                if 선물_거래대금순매수 < 0 and 현물_거래대금순매수 > 0 \
                    and FUT_FOREIGNER_거래대금순매수 > 0 and 프로그램_전체순매수금액 > 0 and KOSPI_FOREIGNER_거래대금순매수 > 0 and fut_realdata['거래량'] > 0:

                    if blink:
                        self.label_msg.setStyleSheet('background-color: red; color: white')
                        self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))
                    else:
                        self.label_msg.setStyleSheet('background-color: white; color: red')
                        self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))

                    call_ms_oneway = True

                    # 시가갭 & 퍼센트로 oneway 판단
                    if 콜시가갭합 > 0 and 콜시가갭합_퍼센트 < 0:
                        
                        call_oneway_level3 = False
                        call_oneway_level4 = False
                        call_oneway_level5 = True

                        if blink:
                            self.label_msg.setStyleSheet('background-color: red; color: white')
                            self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))                            

                            if dt.second % 10 == 0:
                                str = '[{0:02d}:{1:02d}:{2:02d}] 콜 OneWay 가능성 매우 높음(★★★★★)\r'.format(dt.hour, dt.minute, dt.second)
                                self.textBrowser.append(str)
                            else:
                                pass

                            if not oneway_first_touch:

                                oneway_str = '[{0:02d}:{1:02d}:{2:02d}] 콜 OneWay 가능성 매우 높음 !!!\r'.format(dt.hour, dt.minute, dt.second)
                                oneway_first_touch = True
                            else:
                                pass
                        else:
                            self.label_msg.setStyleSheet('background-color: white; color: red')
                            self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))                        
                    else:
                        
                        call_oneway_level3 = False
                        call_oneway_level4 = True
                        call_oneway_level5 = False

                        if blink:                            

                            if dt.second % 10 == 0:
                                str = '[{0:02d}:{1:02d}:{2:02d}] 콜 OneWay 가능성 높음(★★★★)\r'.format(dt.hour, dt.minute, dt.second)
                                self.textBrowser.append(str)
                            else:
                                pass

                            if not oneway_first_touch:

                                oneway_str = '[{0:02d}:{1:02d}:{2:02d}] 콜 OneWay 가능성 높음 !!\r'.format(dt.hour, dt.minute, dt.second)
                                oneway_first_touch = True
                            else:
                                pass
                        else:
                            pass                 

                elif 선물_거래대금순매수 < 0 and 현물_거래대금순매수 > 0 \
                    and FUT_FOREIGNER_거래대금순매수 > 0 and 프로그램_전체순매수금액 > 0 and KOSPI_FOREIGNER_거래대금순매수 < 0 and fut_realdata['거래량'] > 0:

                    self.label_msg.setStyleSheet('background-color: red; color: white')
                    self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))

                    call_ms_oneway = True

                    call_oneway_level3 = True
                    call_oneway_level4 = False
                    call_oneway_level5 = False                    

                    if dt.second % 10 == 0:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 콜 OneWay 가능성(★★★)\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)
                    else:
                        pass

                    if not oneway_first_touch:

                        oneway_str = '[{0:02d}:{1:02d}:{2:02d}] 콜 OneWay 가능성 !\r'.format(dt.hour, dt.minute, dt.second)
                        oneway_first_touch = True
                    else:
                        pass

                elif 선물_거래대금순매수 < 0 and 현물_거래대금순매수 > 0 \
                    and FUT_FOREIGNER_거래대금순매수 > 0 and 프로그램_전체순매수금액 < 0 and KOSPI_FOREIGNER_거래대금순매수 > 0 and fut_realdata['거래량'] > 0:

                    self.label_msg.setStyleSheet('background-color: red; color: white')
                    self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))

                    call_ms_oneway = True
                    oneway_str = ''                    

                    if dt.second % 10 == 0:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 콜 OneWay 가능성(★★)\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)
                    else:
                        pass
                else:
                    pass
            else:
                oneway_str = ''

                put_oneway_level3 = False
                put_oneway_level4 = False
                put_oneway_level5 = False

                call_oneway_level3 = False
                call_oneway_level4 = False
                call_oneway_level5 = False            
            
            if not call_ms_oneway and not put_ms_oneway:
                self.label_msg.setStyleSheet('background-color: lawngreen; color: blue')
                self.label_msg.setFont(QFont("Consolas", 9, QFont.Bold))
            else:
                pass
        return

    def display_centerval(self):

        # 예상 중심가 표시
        if call_atm_value > put_atm_value:

            center = put_atm_value + (call_atm_value - put_atm_value) / 2

        elif put_atm_value > call_atm_value:

            center = call_atm_value + (put_atm_value - call_atm_value) / 2

        else:
            center = call_atm_value
        
        if abs(call_atm_value - put_atm_value) <= 0.02:

            str = '[{0:02d}:{1:02d}:{2:02d}] 등가 {3}에서 교차 중심가 {4} 발생 !!!\r'.format(dt.hour, dt.minute, dt.second, atm_str, call_atm_value)
            self.textBrowser.append(str)            
        else:
            pass

        item = QTableWidgetItem("{0:0.2f}".format(center))
        item.setTextAlignment(Qt.AlignCenter)

        if call_atm_value == put_atm_value:

            item.setBackground(QBrush(검정색))
            item.setForeground(QBrush(대맥점색))
        else:
            item.setBackground(QBrush(대맥점색))
            item.setForeground(QBrush(검정색))

        self.tableWidget_fut.setItem(2, Futures_column.거래량.value, item)

        if abs(call_atm_value - put_atm_value) <= centerval_threshold:
                        
            if self.centerval_flag:

                self.tableWidget_call.item(atm_index, Option_column.행사가.value).setForeground(QBrush(적색))
                self.tableWidget_put.item(atm_index, Option_column.행사가.value).setForeground(QBrush(적색))
            else:
                self.tableWidget_call.item(atm_index, Option_column.행사가.value).setForeground(QBrush(검정색))
                self.tableWidget_put.item(atm_index, Option_column.행사가.value).setForeground(QBrush(검정색))

            self.centerval_flag = not self.centerval_flag                        
        else:
            pass  

        return

    def asym_detect(self, blink):
        
        global 비대칭장
        global call_ms_oneway, put_ms_oneway, call_md_all_dying, put_md_all_dying 
        global call_ms_asymmetric, put_ms_asymmetric, call_md_asymmetric, put_md_asymmetric

        dt = datetime.datetime.now()

        if abs(콜대비합_단위평균/풋대비합_단위평균) >= ASYM_RATIO:

            if 풋대비합 < 0 and 콜대비합 > 0:

                if abs(콜대비합_단위평균/풋대비합_단위평균) >= ONEWAY_RATIO:
                    
                    call_ms_oneway = True
                    call_ms_asymmetric = False
                    call_md_asymmetric = False
                    call_md_all_dying = False
                    put_ms_oneway = False 
                    put_ms_asymmetric = False
                    put_md_asymmetric = False
                    put_md_all_dying = False

                    if TARGET_MONTH_SELECT == 1:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] CM 콜 매수({3:0.2f}:{4:0.2f}) OneWay장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                    elif TARGET_MONTH_SELECT == 2:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] NM 콜 매수({3:0.2f}:{4:0.2f}) OneWay장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                    elif TARGET_MONTH_SELECT == 3:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] MAN 콜 매수({3:0.2f}:{4:0.2f}) OneWay장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)
                    else:
                        pass
                else:
                    call_ms_oneway = False
                    call_ms_asymmetric = True
                    call_md_asymmetric = False
                    call_md_all_dying = False
                    put_ms_oneway = False 
                    put_ms_asymmetric = False
                    put_md_asymmetric = False
                    put_md_all_dying = False

                    if TARGET_MONTH_SELECT == 1:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] CM 콜 매수({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                    elif TARGET_MONTH_SELECT == 2:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] NM 콜 매수({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                    elif TARGET_MONTH_SELECT == 3:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] MAN 콜 매수({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)
                    else:
                        pass                

                if dt.second % 10 == 0 and not blink:

                    self.textBrowser.append(비대칭장)
                    str = '[{0:02d}:{1:02d}:{2:02d}] 시가갭 = {3:0.2f}:{4:0.2f}\r'.format(dt.hour, dt.minute, dt.second, 콜시가갭합, 풋시가갭합)
                    self.textBrowser.append(str)
                else:
                    pass

            elif 풋대비합 > 0 and 콜대비합 < 0:

                call_ms_oneway = False
                call_ms_asymmetric = False
                call_md_asymmetric = True
                call_md_all_dying = False
                put_ms_oneway = False 
                put_ms_asymmetric = False
                put_md_asymmetric = False
                put_md_all_dying = False             

                if TARGET_MONTH_SELECT == 1:

                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] CM 콜 매도({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)                    

                elif TARGET_MONTH_SELECT == 2:

                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] NM 콜 매도({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                elif TARGET_MONTH_SELECT == 3:
                    
                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] MAN 콜 매도({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                else:
                    pass

                if dt.second % 10 == 0 and not blink:
                    self.textBrowser.append(비대칭장)
                else:
                    pass

            elif 풋대비합 < 0 and 콜대비합 < 0:

                call_ms_oneway = False
                call_ms_asymmetric = False
                call_md_asymmetric = False
                call_md_all_dying = True
                put_ms_oneway = False 
                put_ms_asymmetric = False
                put_md_asymmetric = False
                put_md_all_dying = False      

                if TARGET_MONTH_SELECT == 1:

                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] CM 콜 매도({3:0.2f}:{4:0.2f}) 양꽝장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                elif TARGET_MONTH_SELECT == 2:

                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] NM 콜 매도({3:0.2f}:{4:0.2f}) 양꽝장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                elif TARGET_MONTH_SELECT == 3:
                    
                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] MAN 콜 매도({3:0.2f}:{4:0.2f}) 양꽝장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                else:
                    pass

                if dt.second % 10 == 0 and not blink:
                    self.textBrowser.append(비대칭장)
                else:
                    pass
            else:
                pass

        elif abs(풋대비합_단위평균/콜대비합_단위평균) >= ASYM_RATIO:

            if 풋대비합 > 0 and 콜대비합 < 0:

                if abs(풋대비합_단위평균/콜대비합_단위평균) >= ONEWAY_RATIO:  

                    call_ms_oneway = False
                    call_ms_asymmetric = False
                    call_md_asymmetric = False
                    call_md_all_dying = False
                    put_ms_oneway = True 
                    put_ms_asymmetric = False
                    put_md_asymmetric = False
                    put_md_all_dying = False

                    if TARGET_MONTH_SELECT == 1:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] CM 풋 매수({3:0.2f}:{4:0.2f}) OneWay장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                    elif TARGET_MONTH_SELECT == 2:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] NM 풋 매수({3:0.2f}:{4:0.2f}) OneWay장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                    elif TARGET_MONTH_SELECT == 3:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] MAN 풋 매수({3:0.2f}:{4:0.2f}) OneWay장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)
                    else:
                        pass
                else:
                    call_ms_oneway = False
                    call_ms_asymmetric = False
                    call_md_asymmetric = False
                    call_md_all_dying = False
                    put_ms_oneway = False 
                    put_ms_asymmetric = True
                    put_md_asymmetric = False
                    put_md_all_dying = False

                    if TARGET_MONTH_SELECT == 1:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] CM 풋 매수({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                    elif TARGET_MONTH_SELECT == 2:

                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] NM 풋 매수({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                    elif TARGET_MONTH_SELECT == 3:
                        
                        비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] MAN 풋 매수({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                            (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)
                    else:
                        pass                

                if dt.second % 10 == 0 and not blink:

                    self.textBrowser.append(비대칭장)
                    str = '[{0:02d}:{1:02d}:{2:02d}] 시가갭 = {3:0.2f}:{4:0.2f}\r'.format(dt.hour, dt.minute, dt.second, 콜시가갭합, 풋시가갭합)
                    self.textBrowser.append(str)
                else:
                    pass

            elif 풋대비합 < 0 and 콜대비합 > 0: 

                call_ms_oneway = False
                call_ms_asymmetric = False
                call_md_asymmetric = False
                call_md_all_dying = False
                put_ms_oneway = False 
                put_ms_asymmetric = False
                put_md_asymmetric = True
                put_md_all_dying = False            

                if TARGET_MONTH_SELECT == 1:

                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] CM 풋 매도({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                elif TARGET_MONTH_SELECT == 2:

                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] NM 풋 매도({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                elif TARGET_MONTH_SELECT == 3:
                    
                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] MAN 풋 매도({3:0.2f}:{4:0.2f}) 비대칭장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                else:
                    pass

                if dt.second % 10 == 0 and not blink:
                    self.textBrowser.append(비대칭장)
                else:
                    pass

            elif 풋대비합 < 0 and 콜대비합 < 0:

                call_ms_oneway = False
                call_ms_asymmetric = False
                call_md_asymmetric = False
                call_md_all_dying = False
                put_ms_oneway = False 
                put_ms_asymmetric = False
                put_md_asymmetric = False
                put_md_all_dying = True        

                if TARGET_MONTH_SELECT == 1:

                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] CM 풋 매도({3:0.2f}:{4:0.2f}) 양꽝장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                elif TARGET_MONTH_SELECT == 2:

                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] NM 풋 매도({3:0.2f}:{4:0.2f}) 양꽝장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                elif TARGET_MONTH_SELECT == 3:
                    
                    비대칭장 = '[{0:02d}:{1:02d}:{2:02d}] MAN 풋 매도({3:0.2f}:{4:0.2f}) 양꽝장\r'.format \
                        (dt.hour, dt.minute, dt.second, 콜대비합_단위평균, 풋대비합_단위평균)

                else:
                    pass

                if dt.second % 10 == 0 and not blink:
                    self.textBrowser.append(비대칭장)
                else:
                    pass
            else:
                pass
        else:
            비대칭장 = ''

            call_ms_oneway = False
            call_ms_asymmetric = False
            call_md_asymmetric = False
            call_md_all_dying = False
            put_ms_oneway = False 
            put_ms_asymmetric = False
            put_md_asymmetric = False
            put_md_all_dying = False 

        return

    def label_clear(self, toggle):

        dt = datetime.datetime.now()

        if kospi_text_color != '':

            if kospi_text_color == 'red':
                self.label_kospi.setStyleSheet('background-color: white; color: red')
            elif kospi_text_color == 'blue':
                self.label_kospi.setStyleSheet('background-color: white; color: blue')
            else:
                self.label_kospi.setStyleSheet('background-color: white; color: black')
        else:
            pass        

        if kosdaq_text_color != '':

            if kosdaq_text_color == 'red':
                self.label_kosdaq.setStyleSheet('background-color: white; color: red')
            elif kosdaq_text_color == 'blue':
                self.label_kosdaq.setStyleSheet('background-color: white; color: blue')
            else:
                self.label_kosdaq.setStyleSheet('background-color: white; color: black')
        else:
            pass 

        if samsung_text_color != '':

            if samsung_text_color == 'red':
                self.label_samsung.setStyleSheet('background-color: white; color: red')
            elif samsung_text_color == 'blue':
                self.label_samsung.setStyleSheet('background-color: white; color: blue')
            else:
                self.label_samsung.setStyleSheet('background-color: white; color: black')
        else:
            pass            

        if sp500_text_color != '':

            if sp500_text_color == 'red':
                self.label_1st.setStyleSheet('background-color: white; color: red')
            elif sp500_text_color == 'blue':
                self.label_1st.setStyleSheet('background-color: white; color: blue')
            else:
                self.label_1st.setStyleSheet('background-color: white; color: black')
        else:
            pass        

        if dow_text_color != '':

            if dow_text_color == 'red':
                self.label_2nd.setStyleSheet('background-color: white; color: red')
            elif dow_text_color == 'blue':
                self.label_2nd.setStyleSheet('background-color: white; color: blue')
            else:
                self.label_2nd.setStyleSheet('background-color: white; color: black')
        else:
            pass        

        if nasdaq_text_color != '':

            if nasdaq_text_color == 'red':
                self.label_3rd.setStyleSheet('background-color: white; color: red')
            elif nasdaq_text_color == 'blue':
                self.label_3rd.setStyleSheet('background-color: white; color: blue')
            else:
                self.label_3rd.setStyleSheet('background-color: white; color: black')
        else:
            pass

        if dt.second % 30 == 0 and toggle:
            
            if kospi_text_color != kosdaq_text_color:

                str = '[{0:02d}:{1:02d}:{2:02d}] KOSPI, KOSDAQ의 극성이 상이합니다... \r'.format(dt.hour, dt.minute, dt.second)
                self.textBrowser.append(str)
            else:
                pass
            
            if dow_text_color != nasdaq_text_color:

                str = '[{0:02d}:{1:02d}:{2:02d}] DOW, NASDAQ의 극성이 상이합니다... \r'.format(dt.hour, dt.minute, dt.second)
                self.textBrowser.append(str)
            else:
                pass                
        else:
            pass        

        return

    def call_low_color_clear(self, index):

        self.tableWidget_call.item(index, Option_column.저가.value).setBackground(QBrush(옅은회색))
        self.tableWidget_call.item(index, Option_column.저가.value).setForeground(QBrush(검정색))            

        return

    def call_high_color_clear(self, index):

        self.tableWidget_call.item(index, Option_column.고가.value).setBackground(QBrush(옅은회색))
        self.tableWidget_call.item(index, Option_column.고가.value).setForeground(QBrush(검정색))            

        return

    def call_node_color_clear(self):

        global call_scroll_end_position

        if call_scroll_end_position > option_pairs_count:

            call_scroll_end_position = option_pairs_count
        else:
            pass

        for i in range(call_scroll_begin_position, call_scroll_end_position):
            
            oloh_str = ''                           
            item = QTableWidgetItem(oloh_str)
            item.setBackground(QBrush(흰색))
            item.setForeground(QBrush(검정색))
            self.tableWidget_call.setItem(i, Option_column.OLOH.value, item)
            
            if call_node_state['기준가']:
                self.tableWidget_call.item(i, Option_column.기준가.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.기준가.value).setForeground(QBrush(검정색))
            else:
                pass

            if call_node_state['월저']:
                self.tableWidget_call.item(i, Option_column.월저.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.월저.value).setForeground(QBrush(검정색))
            else:
                pass

            if call_node_state['월고']:
                self.tableWidget_call.item(i, Option_column.월고.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.월고.value).setForeground(QBrush(검정색))
            else:
                pass

            if call_node_state['전저']:
                self.tableWidget_call.item(i, Option_column.전저.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.전저.value).setForeground(QBrush(검정색))
            else:
                pass

            if call_node_state['전고']:
                self.tableWidget_call.item(i, Option_column.전고.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
            else:
                pass
           
            if call_node_state['종가']:
                self.tableWidget_call.item(i, Option_column.종가.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
            else:
                pass

            if call_node_state['피봇']:
                self.tableWidget_call.item(i, Option_column.피봇.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
            else:
                pass

            if call_node_state['시가']:

                self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(흰색))

                if df_call.iloc[i]['시가'] > df_call.iloc[i]['종가']:
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(적색))
                elif df_call.iloc[i]['시가'] < df_call.iloc[i]['종가']:
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(청색))
                else:
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
            else:
                pass

            self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))

            self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))

        return

    def call_crossval_color_update(self):

        global call_scroll_end_position

        if call_scroll_end_position > option_pairs_count:

            call_scroll_end_position = option_pairs_count
        else:
            pass

        for i in range(call_scroll_begin_position, call_scroll_end_position):

            if df_call.iloc[i]['저가'] in put_저가_node_list:

                self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
            else:
                pass

            if df_call.iloc[i]['저가'] in put_고가_node_list:

                self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
            else:
                pass
            
            if df_call.iloc[i]['저가'] in call_고가_node_list:

                self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))                  
            else:
                pass

            if df_call.iloc[i]['고가'] in put_저가_node_list:

                self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
            else:
                pass

            if df_call.iloc[i]['고가'] in put_고가_node_list:

                self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
            else:
                pass
            
            if df_call.iloc[i]['고가'] in call_저가_node_list:

                self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))   
            else:
                pass

        return

    def kp200_low_color_blink(self, blink):

        if blink:

            self.tableWidget_fut.item(2, Futures_column.저가.value).setBackground(QBrush(대맥점색))
            self.tableWidget_fut.item(2, Futures_column.저가.value).setForeground(QBrush(검정색))
        else:
            self.tableWidget_fut.item(2, Futures_column.저가.value).setBackground(QBrush(검정색))
            self.tableWidget_fut.item(2, Futures_column.저가.value).setForeground(QBrush(대맥점색))

        return

    def kp200_high_color_blink(self, blink):

        if blink:

            self.tableWidget_fut.item(2, Futures_column.고가.value).setBackground(QBrush(대맥점색))
            self.tableWidget_fut.item(2, Futures_column.고가.value).setForeground(QBrush(검정색))
        else:
            self.tableWidget_fut.item(2, Futures_column.고가.value).setBackground(QBrush(검정색))
            self.tableWidget_fut.item(2, Futures_column.고가.value).setForeground(QBrush(대맥점색))

        return

    def call_low_coreval_color_blink(self, blink):

        global call_low_node_count, call_low_node_list, call_low_node_str

        dt = datetime.datetime.now()
        
        if call_open_list:

            loop_list = call_open_list
        else:
            loop_list = opt_total_list

        count = 0
        call_low_node_list = []            

        for i in loop_list:

            if df_call.iloc[i]['저가'] in 진성맥점:

                count += 1
                call_low_node_list.append(df_call.iloc[i]['저가'])

                if blink:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))                    
                else:
                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(대맥점색))
            else:
                pass

        if call_low_node_list and call_low_node_str == '':

            if TARGET_MONTH_SELECT == 1:

                call_low_node_str = "[{0:02d}:{1:02d}:{2:02d}] CM 콜저가 맥점 {3} 발생 C ▲".format(dt.hour, dt.minute, dt.second, call_low_node_list)

            elif TARGET_MONTH_SELECT == 2:

                call_low_node_str = "[{0:02d}:{1:02d}:{2:02d}] NM 콜저가 맥점 {3} 발생 C ▲".format(dt.hour, dt.minute, dt.second, call_low_node_list)

            elif TARGET_MONTH_SELECT == 3:

                call_low_node_str = "[{0:02d}:{1:02d}:{2:02d}] MAN 콜저가 맥점 {3} 발생 C ▲".format(dt.hour, dt.minute, dt.second, call_low_node_list)
            else:
                pass                        
        else:
            call_low_node_str == ''

        call_low_node_count = count

        if count == 1:
            
            if self.tableWidget_call.horizontalHeaderItem(Option_column.저가.value).text() != '★':
            
                item = QTableWidgetItem('★')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass

        elif count == 2:

            if self.tableWidget_call.horizontalHeaderItem(Option_column.저가.value).text() != '★ 2':
            
                item = QTableWidgetItem('★ 2')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass

        elif count == 3: 

            if self.tableWidget_call.horizontalHeaderItem(Option_column.저가.value).text() != '★ 3':
            
                item = QTableWidgetItem('★ 3')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass

        else:

            if self.tableWidget_call.horizontalHeaderItem(Option_column.저가.value).text() != '★ +':
            
                item = QTableWidgetItem('★ +')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass

        return

    def call_high_coreval_color_blink(self, blink):

        global call_high_node_count, call_high_node_list, call_high_node_str

        dt = datetime.datetime.now()
        
        if call_open_list:

            loop_list = call_open_list
        else:
            loop_list = opt_total_list 

        count = 0
        call_high_node_list = []            

        for i in loop_list:

            if df_call.iloc[i]['고가'] in 진성맥점:

                count += 1
                call_high_node_list.append(df_call.iloc[i]['고가'])
                    
                if blink:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))                    
                else:
                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(대맥점색))
            else:
                pass

        if call_high_node_list and call_high_node_str == '':

            if TARGET_MONTH_SELECT == 1:

                call_high_node_str = "[{0:02d}:{1:02d}:{2:02d}] CM 콜고가 맥점 {3} 발생 C ▼".format(dt.hour, dt.minute, dt.second, call_high_node_list)

            elif TARGET_MONTH_SELECT == 2:

                call_high_node_str = "[{0:02d}:{1:02d}:{2:02d}] NM 콜고가 맥점 {3} 발생 C ▼".format(dt.hour, dt.minute, dt.second, call_high_node_list)

            elif TARGET_MONTH_SELECT == 3:

                call_high_node_str = "[{0:02d}:{1:02d}:{2:02d}] MAN 콜고가 맥점 {3} 발생 C ▼".format(dt.hour, dt.minute, dt.second, call_high_node_list)
            else:
                pass
        else:
            call_high_node_str == ''

        call_high_node_count = count    

        if count == 1:
            
            if self.tableWidget_call.horizontalHeaderItem(Option_column.고가.value).text() != '★':
            
                item = QTableWidgetItem('★')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass

        elif count == 2:

            if self.tableWidget_call.horizontalHeaderItem(Option_column.고가.value).text() != '★ 2':
            
                item = QTableWidgetItem('★ 2')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass

        elif count == 3: 

            if self.tableWidget_call.horizontalHeaderItem(Option_column.고가.value).text() != '★ 3':
            
                item = QTableWidgetItem('★ 3')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass

        else:

            if self.tableWidget_call.horizontalHeaderItem(Option_column.고가.value).text() != '★ +':
            
                item = QTableWidgetItem('★ +')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass

        return    

    def call_coreval_color_update(self):

        global flag_call_low_coreval, flag_call_high_coreval
        global call_low_node_count, call_high_node_count
        global call_low_node_list, call_high_node_list

        flag_call_low_coreval = False
        flag_call_high_coreval = False

        call_low_node_list = []
        call_high_node_list = []

        item = QTableWidgetItem('저가')
        self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)

        item = QTableWidgetItem('고가')
        self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)

        if call_open_list:

            loop_list = call_open_list
        else:
            loop_list = opt_total_list

        count_low = 0
        count_high = 0

        for i in loop_list:

            if opt_coreval_search_start_value < df_call.iloc[i]['시가'] < opt_search_end_value:

                if df_call.iloc[i]['시가'] in 진성맥점:

                    self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['저가'] in coreval:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))

                    if df_call.iloc[i]['저가'] in 진성맥점:

                        self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                        self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(대맥점색))

                        flag_call_low_coreval = True

                        count_low += 1

                        '''
                        if fut_code == cmshcode:

                            txt = '차월물 콜 저까 가 {} 입니다'.format(df_call.iloc[i]['저가'])
                        else:
                            txt = '콜 저까 가 {} 입니다'.format(df_call.iloc[i]['저가'])

                        Speak(txt)
                        '''
                    else:
                        pass
                else:
                    pass

                if df_call.iloc[i]['고가'] in coreval:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))

                    if df_call.iloc[i]['고가'] in 진성맥점:

                        self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                        self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(대맥점색))

                        flag_call_high_coreval = True

                        count_high += 1

                        '''                        
                        if fut_code == cmshcode:

                            txt = '차월물 콜 고까 가 {} 입니다'.format(df_call.iloc[i]['고가'])
                        else:
                            txt = '콜 고까 가 {} 입니다'.format(df_call.iloc[i]['고가'])

                        Speak(txt)
                        '''
                    else:
                        pass
                else:
                    pass
            else:
                pass

        call_low_node_count = count_low

        if count_low == 0:

            pass  

        elif count_low == 1:            

            item = QTableWidgetItem('★')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)

        elif count_low == 2:

            item = QTableWidgetItem('★ 2')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)

        elif count_low == 3:

            item = QTableWidgetItem('★ 3')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)
        else:
            item = QTableWidgetItem('★ +')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)

        call_high_node_count = count_high

        if count_high == 0:

            pass  

        elif count_high == 1:            

            item = QTableWidgetItem('★')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)

        elif count_high == 2:

            item = QTableWidgetItem('★ 2')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)

        elif count_high == 3:

            item = QTableWidgetItem('★ 3')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)
        else:
            item = QTableWidgetItem('★ +')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)

        self.tableWidget_call.resizeColumnsToContents()

        return

    def call_low_coreval_color_update(self):

        global flag_call_low_coreval, call_low_coreval_str
        global call_low_node_list

        dt = datetime.datetime.now()

        flag_call_low_coreval = False
        call_low_node_list = []        

        if call_open_list:

            loop_list = call_open_list
        else:
            loop_list = opt_total_list

        for i in loop_list:

            if opt_coreval_search_start_value < df_call.iloc[i]['시가'] < opt_search_end_value:

                if df_call.iloc[i]['시가'] in 진성맥점:

                    self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['저가'] in coreval:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))

                    if df_call.iloc[i]['저가'] in 진성맥점:

                        flag_call_low_coreval = True                        

                        '''
                        if fut_code == cmshcode:

                            txt = '차월물 콜 저까 가 {} 입니다'.format(df_call.iloc[i]['저가'])
                        else:
                            txt = '콜 저까 가 {} 입니다'.format(df_call.iloc[i]['저가'])

                        Speak(txt)
                        '''
                    else:
                        pass
                else:
                    pass                
            else:
                pass

        return

    def call_high_coreval_color_update(self):

        global flag_call_high_coreval, call_high_coreval_str
        global call_high_node_list

        dt = datetime.datetime.now()

        flag_call_high_coreval = False
        call_high_node_list = []

        if call_open_list:

            loop_list = call_open_list
        else:
            loop_list = opt_total_list

        for i in loop_list:

            if opt_coreval_search_start_value < df_call.iloc[i]['시가'] < opt_search_end_value:

                if df_call.iloc[i]['시가'] in 진성맥점:

                    self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass                

                if df_call.iloc[i]['고가'] in coreval:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))

                    if df_call.iloc[i]['고가'] in 진성맥점:

                        flag_call_high_coreval = True                                

                        '''
                        if fut_code == cmshcode:

                            txt = '차월물 콜 고까 가 {} 입니다'.format(df_call.iloc[i]['고가'])
                        else:
                            txt = '콜 고까 가 {} 입니다'.format(df_call.iloc[i]['고가'])

                        Speak(txt)
                        '''
                    else:
                        pass
                else:
                    pass
            else:
                pass        

        return
    
    def call_node_color_update(self):

        start_time = timeit.default_timer()

        dt = datetime.datetime.now()

        global call_scroll_end_position

        if call_scroll_end_position > option_pairs_count:

            call_scroll_end_position = option_pairs_count
        else:
            pass

        for i in range(call_scroll_begin_position, call_scroll_end_position):
            
            # 콜 저가,고가를 풋 node와 비교후 컬러링                            
            if put_node_state['시가']:

                if df_call.iloc[i]['저가'] in put_시가_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(풋시가색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in put_시가_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(풋시가색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                   
            else:
                pass

            if put_node_state['기준가']:

                if df_call.iloc[i]['저가'] in put_기준가_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in put_기준가_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['월저']:

                if df_call.iloc[i]['저가'] in put_월저_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(풋월저색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in put_월저_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(풋월저색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['월고']:

                if df_call.iloc[i]['저가'] in put_월고_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(풋월고색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in put_월고_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(풋월고색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['전저']:

                if df_call.iloc[i]['저가'] in put_전저_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(풋전저색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in put_전저_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(풋전저색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['전고']:

                if df_call.iloc[i]['저가'] in put_전고_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(풋전고색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in put_전고_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(풋전고색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['종가']:

                if df_call.iloc[i]['저가'] in put_종가_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(풋종가색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in put_종가_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(풋종가색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['피봇']:

                if df_call.iloc[i]['저가'] in put_피봇_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(풋피봇색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in put_피봇_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(풋피봇색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                   
            else:
                pass
            
            # 콜 저가,고가를 콜 node와 비교후 컬러링            
            if call_node_state['시가']:

                if df_call.iloc[i]['저가'] in call_시가_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(콜시가색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in call_시가_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(콜시가색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                   
            else:
                pass

            if call_node_state['기준가']:

                if df_call.iloc[i]['저가'] in call_기준가_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in call_기준가_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                   
            else:
                pass

            if call_node_state['월저']:

                if df_call.iloc[i]['저가'] in call_월저_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(콜월저색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in call_월저_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(콜월저색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['월고']:

                if df_call.iloc[i]['저가'] in call_월고_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(콜월고색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in call_월고_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(콜월고색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['전저']:

                if df_call.iloc[i]['저가'] in call_전저_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(콜전저색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in call_전저_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(콜전저색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['전고']:

                if df_call.iloc[i]['저가'] in call_전고_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(콜전고색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in call_전고_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(콜전고색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['종가']:

                if df_call.iloc[i]['저가'] in call_종가_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(콜종가색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in call_종가_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(콜종가색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['피봇']:

                if df_call.iloc[i]['저가'] in call_피봇_node_list:

                    self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['고가'] in call_피봇_node_list:

                    self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            # 콜 맥점을 콜,풋의 저가,고가와 비교후 컬러링
            if call_node_state['기준가']:                    

                if df_call.iloc[i]['기준가'] in put_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.기준가.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_call.item(i, Option_column.기준가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['기준가'] in put_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.기준가.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_call.item(i, Option_column.기준가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['기준가'] in call_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.기준가.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_call.item(i, Option_column.기준가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['기준가'] in call_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.기준가.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_call.item(i, Option_column.기준가.value).setForeground(QBrush(검정색))
                else:
                    pass              
            else:
                pass

            if call_node_state['월저']:

                if df_call.iloc[i]['월저'] in put_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.월저.value).setBackground(QBrush(콜월저색))
                    self.tableWidget_call.item(i, Option_column.월저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['월저'] in put_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.월저.value).setBackground(QBrush(콜월저색))
                    self.tableWidget_call.item(i, Option_column.월저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['월저'] in call_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.월저.value).setBackground(QBrush(콜월저색))
                    self.tableWidget_call.item(i, Option_column.월저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_call.iloc[i]['월저'] in call_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.월저.value).setBackground(QBrush(콜월저색))
                    self.tableWidget_call.item(i, Option_column.월저.value).setForeground(QBrush(흰색))
                else:
                    pass              
            else:
                pass

            if call_node_state['월고']:

                if df_call.iloc[i]['월고'] in put_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.월고.value).setBackground(QBrush(콜월고색))
                    self.tableWidget_call.item(i, Option_column.월고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['월고'] in put_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.월고.value).setBackground(QBrush(콜월고색))
                    self.tableWidget_call.item(i, Option_column.월고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['월고'] in call_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.월고.value).setBackground(QBrush(콜월고색))
                    self.tableWidget_call.item(i, Option_column.월고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['월고'] in call_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.월고.value).setBackground(QBrush(콜월고색))
                    self.tableWidget_call.item(i, Option_column.월고.value).setForeground(QBrush(검정색))
                else:
                    pass           
            else:
                pass

            if call_node_state['전저']:

                if df_call.iloc[i]['전저'] in put_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.전저.value).setBackground(QBrush(콜전저색))
                    self.tableWidget_call.item(i, Option_column.전저.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['전저'] in put_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.전저.value).setBackground(QBrush(콜전저색))
                    self.tableWidget_call.item(i, Option_column.전저.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['전저'] in call_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.전저.value).setBackground(QBrush(콜전저색))
                    self.tableWidget_call.item(i, Option_column.전저.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['전저'] in call_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.전저.value).setBackground(QBrush(콜전저색))
                    self.tableWidget_call.item(i, Option_column.전저.value).setForeground(QBrush(검정색))
                else:
                    pass          
            else:
                pass

            if call_node_state['전고']:

                if df_call.iloc[i]['전고'] in put_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.전고.value).setBackground(QBrush(콜전고색))
                    self.tableWidget_call.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['전고'] in put_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.전고.value).setBackground(QBrush(콜전고색))
                    self.tableWidget_call.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['전고'] in call_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.전고.value).setBackground(QBrush(콜전고색))
                    self.tableWidget_call.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['전고'] in call_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.전고.value).setBackground(QBrush(콜전고색))
                    self.tableWidget_call.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
                else:
                    pass          
            else:
                pass

            if call_node_state['종가']:

                if df_call.iloc[i]['종가'] in put_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.종가.value).setBackground(QBrush(콜종가색))
                    self.tableWidget_call.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['종가'] in put_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.종가.value).setBackground(QBrush(콜종가색))
                    self.tableWidget_call.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['종가'] in call_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.종가.value).setBackground(QBrush(콜종가색))
                    self.tableWidget_call.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['종가'] in call_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.종가.value).setBackground(QBrush(콜종가색))
                    self.tableWidget_call.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
                else:
                    pass         
            else:
                pass

            if call_node_state['피봇']:

                if df_call.iloc[i]['피봇'] in put_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.피봇.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_call.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['피봇'] in put_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.피봇.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_call.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['피봇'] in call_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.피봇.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_call.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['피봇'] in call_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.피봇.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_call.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                else:
                    pass          
            else:
                pass

            if call_node_state['시가']:

                if df_call.iloc[i]['시가'] in put_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(콜시가색))
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['시가'] in put_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(콜시가색))
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['시가'] in call_저가_node_list:

                    self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(콜시가색))
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_call.iloc[i]['시가'] in call_고가_node_list:

                    self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(콜시가색))
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass     
            else:
                pass           

            # 저가, 고가가 같은 경우는 컬러 무효화
            if df_call.iloc[i]['저가'] == df_call.iloc[i]['고가']:
                '''
                self.tableWidget_call.item(i, Option_column.종가.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.종가.value).setForeground(QBrush(검정색))

                self.tableWidget_call.item(i, Option_column.피봇.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                '''
                self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(흰색))
                self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                
                self.tableWidget_call.item(i, Option_column.저가.value).setBackground(QBrush(옅은회색))
                self.tableWidget_call.item(i, Option_column.저가.value).setForeground(QBrush(검정색))

                self.tableWidget_call.item(i, Option_column.고가.value).setBackground(QBrush(옅은회색))
                self.tableWidget_call.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
            else:
                pass

            if call_node_state['시가']:

                if df_call.iloc[i]['시가'] in 진성맥점:

                    self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass          
            else:
                pass                
        '''
        process_time = (timeit.default_timer() - start_time) * 1000
        
        if market_service:

            str = '[{0:02d}:{1:02d}:{2:02d}] Call Node Color Check Time : {3:0.2f} ms\r'.format(\
                int(call_result['체결시간'][0:2]), int(call_result['체결시간'][2:4]), int(call_result['체결시간'][4:6]), process_time)
            self.textBrowser.append(str)
        else:
            str = '[{0:02d}:{1:02d}:{2:02d}] Call Node Color Check Time : {3:0.2f} ms\r'.format(dt.hour, dt.minute, dt.second, process_time)
            self.textBrowser.append(str)        
        '''
        return
    
    def put_node_color_update(self):
	
        start_time = timeit.default_timer()

        dt = datetime.datetime.now()

        global put_scroll_end_position

        if put_scroll_end_position > option_pairs_count:

            put_scroll_end_position = option_pairs_count
        else:
            pass
        
        for i in range(put_scroll_begin_position, put_scroll_end_position):
            
            # 풋 저가,고가를 콜 node와 비교후 컬러링            
            if call_node_state['시가']:

                if df_put.iloc[i]['저가'] in call_시가_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(콜시가색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in call_시가_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(콜시가색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['기준가']:

                if df_put.iloc[i]['저가'] in call_기준가_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in call_기준가_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['월저']:

                if df_put.iloc[i]['저가'] in call_월저_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(콜월저색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in call_월저_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(콜월저색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['월고']:

                if df_put.iloc[i]['저가'] in call_월고_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(콜월고색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in call_월고_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(콜월고색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['전저']:

                if df_put.iloc[i]['저가'] in call_전저_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(콜전저색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in call_전저_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(콜전저색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                   
            else:
                pass

            if call_node_state['전고']:

                if df_put.iloc[i]['저가'] in call_전고_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(콜전고색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in call_전고_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(콜전고색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['종가']:

                if df_put.iloc[i]['저가'] in call_종가_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(콜종가색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in call_종가_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(콜종가색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if call_node_state['피봇']:

                if df_put.iloc[i]['저가'] in call_피봇_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in call_피봇_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            # 풋 저가,고가를 풋 node와 비교후 컬러링            
            if put_node_state['시가']:

                if df_put.iloc[i]['저가'] in put_시가_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(풋시가색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in put_시가_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(풋시가색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass         

            if put_node_state['기준가']:

                if df_put.iloc[i]['저가'] in put_기준가_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in put_기준가_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['월저']:

                if df_put.iloc[i]['저가'] in put_월저_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(풋월저색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in put_월저_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(풋월저색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                   
            else:
                pass

            if put_node_state['월고']:

                if df_put.iloc[i]['저가'] in put_월고_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(풋월고색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in put_월고_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(풋월고색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['전저']:

                if df_put.iloc[i]['저가'] in put_전저_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(풋전저색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in put_전저_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(풋전저색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['전고']:

                if df_put.iloc[i]['저가'] in put_전고_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(풋전고색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in put_전고_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(풋전고색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['종가']:

                if df_put.iloc[i]['저가'] in put_종가_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(풋종가색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in put_종가_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(풋종가색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass

            if put_node_state['피봇']:

                if df_put.iloc[i]['저가'] in put_피봇_node_list:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(풋피봇색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['고가'] in put_피봇_node_list:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(풋피봇색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
                else:
                    pass                    
            else:
                pass                  

            # 풋 맥점을 콜,풋의 저가,고가와 비교후 컬러링
            if put_node_state['기준가']:

                if df_put.iloc[i]['기준가'] in call_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.기준가.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_put.item(i, Option_column.기준가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['기준가'] in call_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.기준가.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_put.item(i, Option_column.기준가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['기준가'] in put_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.기준가.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_put.item(i, Option_column.기준가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['기준가'] in put_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.기준가.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_put.item(i, Option_column.기준가.value).setForeground(QBrush(흰색))
                else:
                    pass           
            else:
                pass

            if put_node_state['월저']:

                if df_put.iloc[i]['월저'] in call_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.월저.value).setBackground(QBrush(풋월저색))
                    self.tableWidget_put.item(i, Option_column.월저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['월저'] in call_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.월저.value).setBackground(QBrush(풋월저색))
                    self.tableWidget_put.item(i, Option_column.월저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['월저'] in put_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.월저.value).setBackground(QBrush(풋월저색))
                    self.tableWidget_put.item(i, Option_column.월저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['월저'] in put_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.월저.value).setBackground(QBrush(풋월저색))
                    self.tableWidget_put.item(i, Option_column.월저.value).setForeground(QBrush(흰색))
                else:
                    pass           
            else:
                pass

            if put_node_state['월고']:

                if df_put.iloc[i]['월고'] in call_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.월고.value).setBackground(QBrush(풋월고색))
                    self.tableWidget_put.item(i, Option_column.월고.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['월고'] in call_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.월고.value).setBackground(QBrush(풋월고색))
                    self.tableWidget_put.item(i, Option_column.월고.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['월고'] in put_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.월고.value).setBackground(QBrush(풋월고색))
                    self.tableWidget_put.item(i, Option_column.월고.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['월고'] in put_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.월고.value).setBackground(QBrush(풋월고색))
                    self.tableWidget_put.item(i, Option_column.월고.value).setForeground(QBrush(흰색))
                else:
                    pass         
            else:
                pass

            if put_node_state['전저']:

                if df_put.iloc[i]['전저'] in call_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.전저.value).setBackground(QBrush(풋전저색))
                    self.tableWidget_put.item(i, Option_column.전저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['전저'] in call_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.전저.value).setBackground(QBrush(풋전저색))
                    self.tableWidget_put.item(i, Option_column.전저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['전저'] in put_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.전저.value).setBackground(QBrush(풋전저색))
                    self.tableWidget_put.item(i, Option_column.전저.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['전저'] in put_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.전저.value).setBackground(QBrush(풋전저색))
                    self.tableWidget_put.item(i, Option_column.전저.value).setForeground(QBrush(흰색))
                else:
                    pass        
            else:
                pass

            if put_node_state['전고']:

                if df_put.iloc[i]['전고'] in call_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.전고.value).setBackground(QBrush(풋전고색))
                    self.tableWidget_put.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['전고'] in call_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.전고.value).setBackground(QBrush(풋전고색))
                    self.tableWidget_put.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['전고'] in put_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.전고.value).setBackground(QBrush(풋전고색))
                    self.tableWidget_put.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['전고'] in put_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.전고.value).setBackground(QBrush(풋전고색))
                    self.tableWidget_put.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
                else:
                    pass       
            else:
                pass

            if put_node_state['종가']:

                if df_put.iloc[i]['종가'] in call_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.종가.value).setBackground(QBrush(풋종가색))
                    self.tableWidget_put.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['종가'] in call_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.종가.value).setBackground(QBrush(풋종가색))
                    self.tableWidget_put.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['종가'] in put_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.종가.value).setBackground(QBrush(풋종가색))
                    self.tableWidget_put.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['종가'] in put_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.종가.value).setBackground(QBrush(풋종가색))
                    self.tableWidget_put.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
                else:
                    pass    
            else:
                pass

            if put_node_state['피봇']:

                if df_put.iloc[i]['피봇'] in call_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.피봇.value).setBackground(QBrush(풋피봇색))
                    self.tableWidget_put.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['피봇'] in call_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.피봇.value).setBackground(QBrush(풋피봇색))
                    self.tableWidget_put.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['피봇'] in put_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.피봇.value).setBackground(QBrush(풋피봇색))
                    self.tableWidget_put.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['피봇'] in put_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.피봇.value).setBackground(QBrush(풋피봇색))
                    self.tableWidget_put.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                else:
                    pass           
            else:
                pass

            if put_node_state['시가']:

                if df_put.iloc[i]['시가'] in call_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(풋시가색))
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['시가'] in call_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(풋시가색))
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['시가'] in put_저가_node_list:

                    self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(풋시가색))
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(흰색))
                else:
                    pass

                if df_put.iloc[i]['시가'] in put_고가_node_list:

                    self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(풋시가색))
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(흰색))
                else:
                    pass       
            else:
                pass               

            # 저가, 고가가 같은 경우는 컬러 무효화
            if df_put.iloc[i]['저가'] == df_put.iloc[i]['고가']:
                '''
                self.tableWidget_put.item(i, Option_column.종가.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.종가.value).setForeground(QBrush(검정색))

                self.tableWidget_put.item(i, Option_column.피봇.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
                '''
                self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                
                self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(옅은회색))
                self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))

                self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(옅은회색))
                self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))
            else:
                pass

            if put_node_state['시가']:

                if df_put.iloc[i]['시가'] in 진성맥점:

                    self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass            
            else:
                pass             
        '''
        process_time = (timeit.default_timer() - start_time) * 1000
        
        if market_service:

            str = '[{0:02d}:{1:02d}:{2:02d}] Put Node Color Check Time : {3:0.2f} ms\r'.format(\
                int(put_result['체결시간'][0:2]), int(put_result['체결시간'][2:4]), int(put_result['체결시간'][4:6]), process_time)
            self.textBrowser.append(str)
        else:
            str = '[{0:02d}:{1:02d}:{2:02d}] Put Node Color Check Time : {3:0.2f} ms\r'.format(dt.hour, dt.minute, dt.second, process_time)
            self.textBrowser.append(str)
        '''
        return

    def put_low_color_clear(self, index):

        self.tableWidget_put.item(index, Option_column.저가.value).setBackground(QBrush(옅은회색))
        self.tableWidget_put.item(index, Option_column.저가.value).setForeground(QBrush(검정색))

        return

    def put_high_color_clear(self, index):

        self.tableWidget_put.item(index, Option_column.고가.value).setBackground(QBrush(옅은회색))
        self.tableWidget_put.item(index, Option_column.고가.value).setForeground(QBrush(검정색))

        return

    def put_node_color_clear(self):

        global put_scroll_end_position

        if put_scroll_end_position > option_pairs_count:

            put_scroll_end_position = option_pairs_count
        else:
            pass

        for i in range(put_scroll_begin_position, put_scroll_end_position):
            
            oloh_str = ''                           
            item = QTableWidgetItem(oloh_str)
            item.setBackground(QBrush(흰색))
            item.setForeground(QBrush(검정색))
            self.tableWidget_put.setItem(i, Option_column.OLOH.value, item)
            
            if put_node_state['기준가']:
                self.tableWidget_put.item(i, Option_column.기준가.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.기준가.value).setForeground(QBrush(검정색))
            else:
                pass

            if put_node_state['월저']:
                self.tableWidget_put.item(i, Option_column.월저.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.월저.value).setForeground(QBrush(검정색))
            else:
                pass

            if put_node_state['월고']:
                self.tableWidget_put.item(i, Option_column.월고.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.월고.value).setForeground(QBrush(검정색))
            else:
                pass

            if put_node_state['전저']:
                self.tableWidget_put.item(i, Option_column.전저.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.전저.value).setForeground(QBrush(검정색))
            else:
                pass

            if put_node_state['전고']:
                self.tableWidget_put.item(i, Option_column.전고.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.전고.value).setForeground(QBrush(검정색))
            else:
                pass

            if put_node_state['종가']:
                self.tableWidget_put.item(i, Option_column.종가.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.종가.value).setForeground(QBrush(검정색))
            else:
                pass

            if put_node_state['피봇']:
                self.tableWidget_put.item(i, Option_column.피봇.value).setBackground(QBrush(흰색))
                self.tableWidget_put.item(i, Option_column.피봇.value).setForeground(QBrush(검정색))
            else:
                pass

            if put_node_state['시가']:

                self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(흰색))

                if df_put.iloc[i]['시가'] > df_put.iloc[i]['종가']:
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(적색))
                elif df_put.iloc[i]['시가'] < df_put.iloc[i]['종가']:
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(청색))
                else:
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
            else:
                pass

            self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))

            self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))

        return

    def put_crossval_color_update(self):

        global put_scroll_end_position

        if put_scroll_end_position > option_pairs_count:

            put_scroll_end_position = option_pairs_count
        else:
            pass

        for i in range(put_scroll_begin_position, put_scroll_end_position):

            if df_put.iloc[i]['저가'] in call_저가_node_list:

                self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
            else:
                pass

            if df_put.iloc[i]['저가'] in call_고가_node_list:

                self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))
            else:
                pass
            
            if df_put.iloc[i]['저가'] in put_고가_node_list:

                self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(흰색))                 
            else:
                pass

            if df_put.iloc[i]['고가'] in call_저가_node_list:

                self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
            else:
                pass

            if df_put.iloc[i]['고가'] in call_고가_node_list:

                self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))
            else:
                pass
            
            if df_put.iloc[i]['고가'] in put_저가_node_list:

                self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(흰색))                  
            else:
                pass

        return

    def put_low_coreval_color_blink(self, blink):

        global put_low_node_count, put_low_node_list, put_low_node_str

        dt = datetime.datetime.now()
        
        if put_open_list:

            loop_list = put_open_list
        else:
            loop_list = opt_total_list

        count = 0
        put_low_node_list = []       

        for i in loop_list:

            if df_put.iloc[i]['저가'] in 진성맥점:

                count += 1
                put_low_node_list.append(df_put.iloc[i]['저가'])

                if blink:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))                                                                     
                else:
                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(대맥점색))
            else:
                pass

        if put_low_node_list and put_low_node_str == '':

            if TARGET_MONTH_SELECT == 1:

                put_low_node_str = "[{0:02d}:{1:02d}:{2:02d}] CM 풋저가 맥점 {3} 발생 P ▲".format(dt.hour, dt.minute, dt.second, put_low_node_list)

            elif TARGET_MONTH_SELECT == 2:

                put_low_node_str = "[{0:02d}:{1:02d}:{2:02d}] NM 풋저가 맥점 {3} 발생 P ▲".format(dt.hour, dt.minute, dt.second, put_low_node_list)

            elif TARGET_MONTH_SELECT == 3:

                put_low_node_str = "[{0:02d}:{1:02d}:{2:02d}] MAN 풋저가 맥점 {3} 발생 P ▲".format(dt.hour, dt.minute, dt.second, put_low_node_list)
            else:
                pass
        else:
            put_low_node_str == ''    

        put_low_node_count = count

        if count == 1:
            
            if self.tableWidget_put.horizontalHeaderItem(Option_column.저가.value).text() != '★':
            
                item = QTableWidgetItem('★')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass

        elif count == 2:

            if self.tableWidget_put.horizontalHeaderItem(Option_column.저가.value).text() != '★ 2':
            
                item = QTableWidgetItem('★ 2')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass

        elif count == 3: 

            if self.tableWidget_put.horizontalHeaderItem(Option_column.저가.value).text() != '★ 3':
            
                item = QTableWidgetItem('★ 3')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass

        else:

            if self.tableWidget_put.horizontalHeaderItem(Option_column.저가.value).text() != '★ +':
            
                item = QTableWidgetItem('★ +')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass 

        return

    def put_high_coreval_color_blink(self, blink):

        global put_high_node_count, put_high_node_list, put_high_node_str

        dt = datetime.datetime.now()

        if put_open_list:

            loop_list = put_open_list
        else:
            loop_list = opt_total_list

        count = 0
        put_high_node_list = []              

        for i in loop_list:

            if df_put.iloc[i]['고가'] in 진성맥점:

                count += 1
                put_high_node_list.append(df_put.iloc[i]['고가'])

                if blink:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))                    
                else:
                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(대맥점색))                 
            else:
                pass

        if put_high_node_list and put_high_node_str == '':

            if TARGET_MONTH_SELECT == 1: 

                put_high_node_str = "[{0:02d}:{1:02d}:{2:02d}] CM 풋고가 맥점 {3} 발생 P ▼".format(dt.hour, dt.minute, dt.second, put_high_node_list)

            elif TARGET_MONTH_SELECT == 2:

                put_high_node_str = "[{0:02d}:{1:02d}:{2:02d}] NM 풋고가 맥점 {3} 발생 P ▼".format(dt.hour, dt.minute, dt.second, put_high_node_list)

            elif TARGET_MONTH_SELECT == 3:

                put_high_node_str = "[{0:02d}:{1:02d}:{2:02d}] MAN 풋고가 맥점 {3} 발생 P ▼".format(dt.hour, dt.minute, dt.second, put_high_node_list)
            else:
                pass
        else:
            put_high_node_str == ''

        put_high_node_count = count

        if count == 1:
            
            if self.tableWidget_put.horizontalHeaderItem(Option_column.고가.value).text() != '★':
            
                item = QTableWidgetItem('★')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass

        elif count == 2:

            if self.tableWidget_put.horizontalHeaderItem(Option_column.고가.value).text() != '★ 2':
            
                item = QTableWidgetItem('★ 2')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass

        elif count == 3: 

            if self.tableWidget_put.horizontalHeaderItem(Option_column.고가.value).text() != '★ 3':
            
                item = QTableWidgetItem('★ 3')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass

        else:

            if self.tableWidget_put.horizontalHeaderItem(Option_column.고가.value).text() != '★ +':
            
                item = QTableWidgetItem('★ +')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass   

        return           
    
    def put_coreval_color_update(self):

        global flag_put_low_coreval, flag_put_high_coreval
        global put_low_node_count, put_high_node_count
        global put_low_node_list, put_high_node_list

        flag_put_low_coreval = False
        flag_put_high_coreval = False

        put_low_node_list = []
        put_high_node_list = []

        item = QTableWidgetItem('저가')
        self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)

        item = QTableWidgetItem('고가')
        self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)

        if put_open_list:

            loop_list = put_open_list
        else:
            loop_list = opt_total_list

        count_low = 0
        count_high = 0

        for i in loop_list:

            if opt_coreval_search_start_value < df_put.iloc[i]['시가'] < opt_search_end_value:

                if df_put.iloc[i]['시가'] in 진성맥점:

                    self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['저가'] in coreval:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))

                    if df_put.iloc[i]['저가'] in 진성맥점:

                        self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(검정색))
                        self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(대맥점색))

                        flag_put_low_coreval = True

                        count_low += 1

                        '''                        
                        if fut_code == cmshcode:

                            txt = '차월물 풋 저까 가 {} 입니다'.format(df_put.iloc[i]['저가'])
                        else:
                            txt = '풋 저까 가 {} 입니다'.format(df_put.iloc[i]['저가'])

                        Speak(txt)
                        '''
                    else:
                        pass
                else:
                    pass

                if df_put.iloc[i]['고가'] in coreval:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))

                    if df_put.iloc[i]['고가'] in 진성맥점:

                        self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(검정색))
                        self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(대맥점색))

                        flag_put_high_coreval = True

                        count_high += 1

                        '''
                        if fut_code == cmshcode:

                            txt = '차월물 풋 고까 가 {} 입니다'.format(df_put.iloc[i]['고가'])
                        else:
                            txt = '풋 고까 가 {} 입니다'.format(df_put.iloc[i]['고가'])

                        Speak(txt)
                        '''
                    else:
                        pass
                else:
                    pass
            else:
                pass

        put_low_node_count = count_low

        if count_low == 0:

            pass  

        elif count_low == 1:              

            item = QTableWidgetItem('★')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)

        elif count_low == 2:

            item = QTableWidgetItem('★ 2')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)

        elif count_low == 3:

            item = QTableWidgetItem('★ 3')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)
        else:
            item = QTableWidgetItem('★ +')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)

        put_high_node_count = count_high

        if count_high == 0:

            pass  

        elif count_high == 1:          

            item = QTableWidgetItem('★')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)

        elif count_high == 2:

            item = QTableWidgetItem('★ 2')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)

        elif count_high == 3:

            item = QTableWidgetItem('★ 3')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)
        else:
            item = QTableWidgetItem('★ +')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)

        self.tableWidget_put.resizeColumnsToContents()

        return    

    def put_low_coreval_color_update(self):

        global flag_put_low_coreval, put_low_coreval_str
        global put_low_node_list

        dt = datetime.datetime.now()

        flag_put_low_coreval = False
        put_low_node_list = []

        if put_open_list:

            loop_list = put_open_list
        else:
            loop_list = opt_total_list

        for i in loop_list:

            if opt_coreval_search_start_value < df_put.iloc[i]['시가'] < opt_search_end_value:

                if df_put.iloc[i]['시가'] in 진성맥점:

                    self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass

                if df_put.iloc[i]['저가'] in coreval:

                    self.tableWidget_put.item(i, Option_column.저가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.저가.value).setForeground(QBrush(검정색))

                    if df_put.iloc[i]['저가'] in 진성맥점:

                        flag_put_low_coreval = True                            

                        '''                        
                        if fut_code == cmshcode:

                            txt = '차월물 풋 저까 가 {} 입니다'.format(df_put.iloc[i]['저가'])
                        else:
                            txt = '풋 저까 가 {} 입니다'.format(df_put.iloc[i]['저가'])

                        Speak(txt)
                        '''
                    else:
                        pass
                else:
                    pass                
            else:
                pass        

        return

    def put_high_coreval_color_update(self):

        global flag_put_high_coreval, put_high_coreval_str
        global put_high_node_list

        dt = datetime.datetime.now()

        flag_put_high_coreval = False
        put_high_node_list = []

        if put_open_list:

            loop_list = put_open_list
        else:
            loop_list = opt_total_list

        for i in loop_list:

            if opt_coreval_search_start_value < df_put.iloc[i]['시가'] < opt_search_end_value:

                if df_put.iloc[i]['시가'] in 진성맥점:

                    self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                else:
                    pass                

                if df_put.iloc[i]['고가'] in coreval:

                    self.tableWidget_put.item(i, Option_column.고가.value).setBackground(QBrush(대맥점색))
                    self.tableWidget_put.item(i, Option_column.고가.value).setForeground(QBrush(검정색))

                    if df_put.iloc[i]['고가'] in 진성맥점:

                        flag_put_high_coreval = True                        

                        '''
                        if fut_code == cmshcode:

                            txt = '차월물 풋 고까 가 {} 입니다'.format(df_put.iloc[i]['고가'])
                        else:
                            txt = '풋 고까 가 {} 입니다'.format(df_put.iloc[i]['고가'])

                        Speak(txt)
                        '''
                    else:
                        pass
                else:
                    pass
            else:
                pass        

        return    
    
    def fut_node_color_clear(self):

        if overnight:

            self.tableWidget_fut.item(0, Futures_column.전저.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(0, Futures_column.전저.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(0, Futures_column.전고.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(0, Futures_column.전고.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(0, Futures_column.종가.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(0, Futures_column.종가.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(0, Futures_column.피봇.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(0, Futures_column.피봇.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(0, Futures_column.시가.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(0, Futures_column.시가.value).setForeground(QBrush(검정색))
            
            self.tableWidget_fut.item(0, Futures_column.저가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_fut.item(0, Futures_column.저가.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(0, Futures_column.고가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_fut.item(0, Futures_column.고가.value).setForeground(QBrush(검정색)) 
        else:
            self.tableWidget_fut.item(1, Futures_column.전저.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(1, Futures_column.전저.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(1, Futures_column.전고.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(1, Futures_column.전고.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(1, Futures_column.종가.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(1, Futures_column.종가.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(1, Futures_column.피봇.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(1, Futures_column.피봇.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(1, Futures_column.시가.value).setBackground(QBrush(흰색))
            self.tableWidget_fut.item(1, Futures_column.시가.value).setForeground(QBrush(검정색))
            
            self.tableWidget_fut.item(1, Futures_column.저가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_fut.item(1, Futures_column.저가.value).setForeground(QBrush(검정색))

            self.tableWidget_fut.item(1, Futures_column.고가.value).setBackground(QBrush(옅은회색))
            self.tableWidget_fut.item(1, Futures_column.고가.value).setForeground(QBrush(검정색))       

        return

    def OnReceiveData(self, szTrCode, result):

        global gmshcode, cmshcode, ccmshcode, fut_code
        global call_code, put_code
        global opt_actval
        global df_plotdata_fut
        global atm_index, atm_index_old
        global df_plotdata_call, df_plotdata_put
        global df_plotdata_call_volume, df_plotdata_put_volume, df_plotdata_volume_cha
        global df_plotdata_call_oi, df_plotdata_put_oi
        global atm_str, atm_val

        global fut_realdata, cme_realdata

        global call_ckbox
        global selected_call
        global df_call, df_call_hoga

        global put_ckbox
        global selected_put
        global df_put, df_put_hoga

        global df_call_volume, df_put_volume

        global call_행사가, put_행사가

        global call_기준가, call_월저, call_월고, call_전저, call_전고, call_종가, call_피봇, \
            call_시가, call_저가, call_고가, call_진폭
        global call_기준가_node_list, call_월저_node_list, call_월고_node_list, call_전저_node_list, call_전고_node_list, \
            call_종가_node_list, call_피봇_node_list, call_시가_node_list, call_저가_node_list, call_고가_node_list

        global put_기준가, put_월저, put_월고, put_전저, put_전고, put_종가, put_피봇, \
            put_시가, put_저가, put_고가, put_진폭
        global put_기준가_node_list, put_월저_node_list, put_월고_node_list, put_전저_node_list, put_전고_node_list, \
            put_종가_node_list, put_피봇_node_list, put_시가_node_list, put_저가_node_list, put_고가_node_list

        global option_pairs_count

        global df_plotdata_fut, df_plotdata_kp200, df_plotdata_fut_volume
        global 콜_순미결합, 풋_순미결합, 콜_순미결퍼센트, 풋_순미결퍼센트
        global 콜_수정미결합, 풋_수정미결합, 콜_수정미결퍼센트, 풋_수정미결퍼센트
        global call_atm_value, put_atm_value

        global df_fut
        global kp200_realdata

        global refresh_flag

        global call_oi_init_value, put_oi_init_value
        global call_gap_percent, call_db_percent, put_gap_percent, put_db_percent

        global call_open
        global call_ol
        global call_oh

        global put_open
        global put_ol
        global put_oh

        global call_volume_total, put_volume_total
        global 콜시가리스트, 콜저가리스트, 콜고가리스트, 풋시가리스트, 풋저가리스트, 풋고가리스트

        global df_plotdata_two_sum, df_plotdata_two_cha
        global start_time_str, end_time_str

        global df_plotdata_sp500, df_plotdata_dow, df_plotdata_nasdaq
        global view_actval
        
        global 선물_전저, 선물_전고, 선물_종가, 선물_피봇, 선물_시가, 선물_저가, 선물_현재가, 선물_고가
        global call_open_list, put_open_list, opt_total_list
        global call_below_atm_count, call_max_actval
        global put_above_atm_count, put_max_actval
        global kp200_종가
        global t2835_month_info
        global server_date, server_time, system_server_timegap

        dt = datetime.datetime.now()
        current_str = dt.strftime('%H:%M:%S')

        if szTrCode == 't0167':

            server_date, server_time = result
            
            print('server date =', server_date)
            print('server time =', server_time)

            system_server_timegap = int(dt.strftime('%H%M%S')) - int(server_time[0:6])

            print('system_server_timegap = ', system_server_timegap)

        elif szTrCode == 't1514':

            CTS일자, df = result
            
            if df.iloc[0]['업종코드'] == KOSPI:

                if df.iloc[0]['전일대비구분'] == '5':

                    jisu_str = "KOSPI: {0} (-{1:0.2f}, {2:0.1f}%)".format(df.iloc[0]['지수'], df.iloc[0]['전일대비'], df.iloc[0]['등락율'])
                    self.label_kospi.setText(jisu_str)
                    self.label_kospi.setStyleSheet('background-color: black ; color: cyan')

                elif df.iloc[0]['전일대비구분'] == '2':

                    jisu_str = "KOSPI: {0} ({1:0.2f}, {2:0.1f}%)".format(df.iloc[0]['지수'], df.iloc[0]['전일대비'], df.iloc[0]['등락율'])
                    self.label_kospi.setText(jisu_str)
                    self.label_kospi.setStyleSheet('background-color: black ; color: magenta')
                else:
                    pass

            elif df.iloc[0]['업종코드'] == KOSDAQ:

                if df.iloc[0]['전일대비구분'] == '5':

                    jisu_str = "KOSDAQ: {0} (-{1:0.2f}, {2:0.1f}%)".format(df.iloc[0]['지수'], df.iloc[0]['전일대비'], df.iloc[0]['등락율'])
                    self.label_kosdaq.setText(jisu_str)
                    self.label_kosdaq.setStyleSheet('background-color: black ; color: cyan')

                elif df.iloc[0]['전일대비구분'] == '2':

                    jisu_str = "KOSDAQ: {0} ({1:0.2f}, {2:0.1f}%)".format(df.iloc[0]['지수'], df.iloc[0]['전일대비'], df.iloc[0]['등락율'])
                    self.label_kosdaq.setText(jisu_str)
                    self.label_kosdaq.setStyleSheet('background-color: black ; color: magenta')
                else:
                    pass
            else:
                pass                    

        elif szTrCode == 't2101':

            df = result[0]

            fut_realdata['현재가'] = df['현재가']
            fut_realdata['KP200'] = df['KOSPI200지수']
            
            atm_str = self.find_ATM(fut_realdata['KP200'])

            if atm_str[-1] == '2' or atm_str[-1] == '7':

                atm_val = float(atm_str) + 0.5
            else:
                atm_val = float(atm_str)

            if atm_str in opt_actval:

                atm_index = opt_actval.index(atm_str)
                atm_index_old = atm_index

                view_actval = opt_actval[atm_index-5:atm_index+6]

                call_atm_value = df_call.iloc[atm_index]['현재가']
                put_atm_value = df_put.iloc[atm_index]['현재가']
                
                str = '{0:0.2f}({1:0.2f}:{2:0.2f})'.format(
                    fut_realdata['현재가'] - fut_realdata['KP200'],
                    call_atm_value + put_atm_value,
                    abs(call_atm_value - put_atm_value))
                self.label_atm.setText(str)                

                df_plotdata_two_sum[0][0] = call_atm_value + put_atm_value
                df_plotdata_two_cha[0][0] = call_atm_value - put_atm_value

                df_plotdata_two_sum[0][선물장간_시간차] = call_atm_value + put_atm_value
                df_plotdata_two_cha[0][선물장간_시간차] = call_atm_value - put_atm_value

                item_str = '{0:0.1f}%\n{1:0.1f}%'.format(콜_수정미결퍼센트, 풋_수정미결퍼센트)

                item = QTableWidgetItem(item_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_quote.setItem(0, Quote_column.미결종합.value - 1, item)
            else:
                print("atm_str이 리스트에 없습니다.", atm_str)            

            fut_realdata['종가'] = df['전일종가']

            item = QTableWidgetItem("{0:0.2f}".format(df['전일종가']))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(1, Futures_column.종가.value, item)

            fut_realdata['시가'] = df['시가']

            item = QTableWidgetItem("{0:0.2f}".format(df['시가']))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(흰색))

            if fut_realdata['시가'] > fut_realdata['종가']:
                item.setForeground(QBrush(적색))
            elif fut_realdata['시가'] < fut_realdata['종가']:
                item.setForeground(QBrush(청색))
            else:
                item.setForeground(QBrush(검정색))

            self.tableWidget_fut.setItem(1, Futures_column.시가.value, item)

            if not overnight:

                df_plotdata_kp200.iloc[0][0] = fut_realdata['KP200']
                df_plotdata_fut.iloc[0][0] = fut_realdata['종가']

                if fut_realdata['시가'] > 0:
                    df_plotdata_fut.iloc[0][선물장간_시간차] = fut_realdata['시가']
                else:
                    pass

                df_plotdata_fut_volume.iloc[0][0] = 0
                df_plotdata_fut_volume.iloc[0][선물장간_시간차] = 0
            else:
                pass

            if df['시가'] > 0:

                fut_realdata['피봇'] = self.calc_pivot(fut_realdata['전저'], fut_realdata['전고'],
                                                         fut_realdata['종가'], df['시가'])

                item = QTableWidgetItem("{0:0.2f}".format(fut_realdata['피봇']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_fut.setItem(1, Futures_column.피봇.value, item)

                선물_피봇 = fut_realdata['피봇']

                fut_realdata['시가갭'] = fut_realdata['시가'] - fut_realdata['종가']

                item = QTableWidgetItem("{0:0.2f}".format(fut_realdata['시가갭']))
                item.setTextAlignment(Qt.AlignCenter)

                if fut_realdata['시가'] > fut_realdata['종가']:
                    item.setBackground(QBrush(콜기준가색))
                    item.setForeground(QBrush(검정색))
                elif fut_realdata['시가'] < fut_realdata['종가']:
                    item.setBackground(QBrush(풋기준가색))
                    item.setForeground(QBrush(흰색))
                else:
                    item.setBackground(QBrush(흰색))  

                self.tableWidget_fut.setItem(1, Futures_column.시가갭.value, item)
            else:
                pass

            if pre_start:

                kp200_realdata['종가'] = df['KOSPI200지수']
            else:
                if df['KOSPI200전일대비구분'] == '2':

                    kp200_realdata['종가'] = df['KOSPI200지수'] - df['KOSPI200전일대비']

                elif df['KOSPI200전일대비구분'] == '5':

                    kp200_realdata['종가'] = df['KOSPI200지수'] + df['KOSPI200전일대비']

                else:
                    kp200_realdata['종가'] = df['KOSPI200지수']

            kp200_종가 = kp200_realdata['종가']

            item = QTableWidgetItem("{0:0.2f}".format(kp200_종가))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(2, Futures_column.종가.value, item)

            fut_realdata['현재가'] = df['현재가']

            item = QTableWidgetItem("{0:0.2f}".format(fut_realdata['현재가']))
            item.setTextAlignment(Qt.AlignCenter)
            #item.setBackground(QBrush(옅은회색))

            if df['현재가'] > df['시가']:
                item.setForeground(QBrush(적색))
            elif df['현재가'] < df['시가']:
                item.setForeground(QBrush(청색))
            else:
                item.setForeground(QBrush(검정색))

            self.tableWidget_fut.setItem(1, Futures_column.현재가.value, item)
            
            if df['시가'] > 0:

                fut_realdata['대비'] = round((df['현재가'] - df['시가']), 2)
            else:
                fut_realdata['대비'] = 0

            item = QTableWidgetItem("{0:0.2f}".format(fut_realdata['대비']))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(1, Futures_column.대비.value, item)
            
            fut_realdata['저가'] = df['저가']

            item = QTableWidgetItem("{0:0.2f}".format(fut_realdata['저가']))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(옅은회색))
            self.tableWidget_fut.setItem(1, Futures_column.저가.value, item)

            fut_realdata['고가'] = df['고가']

            item = QTableWidgetItem("{0:0.2f}".format(fut_realdata['고가']))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(옅은회색))
            self.tableWidget_fut.setItem(1, Futures_column.고가.value, item)

            fut_realdata['진폭'] = df['고가'] - df['저가']

            item = QTableWidgetItem("{0:0.2f}".format(fut_realdata['진폭']))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(1, Futures_column.진폭.value, item)

            fut_realdata['거래량'] = df['거래량']
            temp = format(fut_realdata['거래량'], ',')

            item = QTableWidgetItem(temp)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(1, Futures_column.거래량.value, item)

            fut_realdata['미결'] = df['미결제량']
            temp = format(fut_realdata['미결'], ',')

            item = QTableWidgetItem(temp)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(1, Futures_column.OI.value, item)

            fut_realdata['미결증감'] = df['미결제증감']
            temp = format(fut_realdata['미결증감'], ',')

            item = QTableWidgetItem(temp)
            item.setTextAlignment(Qt.AlignCenter)

            if fut_realdata['미결증감'] < 0:
                item.setBackground(QBrush(라임))
            else:
                item.setBackground(QBrush(흰색))

            self.tableWidget_fut.setItem(1, Futures_column.OID.value, item)            
            
            if not overnight:

                #선물_전저 = fut_realdata['전저']
                #선물_전고 = fut_realdata['전고']
                #선물_종가 = fut_realdata['종가']
                선물_피봇 = fut_realdata['피봇']
                선물_시가 = df['시가']
                선물_저가 = df['저가']
                선물_현재가 = df['현재가']
                선물_고가 = df['고가']
            else:
                pass
            
            self.tableWidget_fut.resizeColumnsToContents()

        elif szTrCode == 't2301':

            block, df, df1 = result

            dt = datetime.datetime.now()
            current_str = dt.strftime('%H:%M:%S')

            global 옵션잔존일

            if not refresh_flag:

                # 옵션 잔존일
                옵션잔존일 = block['옵션잔존일']

                # 옵션 행사가 갯수
                option_pairs_count = len(df)

                if not overnight:

                    call_open = [False] * option_pairs_count
                    put_open = [False] * option_pairs_count
                else:
                    pass

                for i in range(option_pairs_count):

                    opt_total_list.append(i)

                t2301_call = []
                callho_result = []
                t2301_put = []
                putho_result = []

                callche_result = []
                putche_result = []

                if not overnight:
                    
                    self.Plot1.setRange(xRange=[0, 선물장간_시간차 + day_timespan], padding=0)
                    plot1_time_line.setValue(선물장간_시간차 + day_timespan - 1)

                    self.Plot2.setRange(xRange=[0, 선물장간_시간차 + day_timespan], padding=0)
                    plot2_time_line.setValue(선물장간_시간차 + day_timespan - 1)

                    if UI_STYLE == 'Vertical_view.ui':

                        self.Plot3.setRange(xRange=[0, 선물장간_시간차 + day_timespan], padding=0)
                        plot3_time_line.setValue(선물장간_시간차 + day_timespan - 1)

                        self.Plot4.setRange(xRange=[0, 선물장간_시간차 + day_timespan], padding=0)
                        plot4_time_line.setValue(선물장간_시간차 + day_timespan - 1)
                    else:
                        pass

                    df_plotdata_call = DataFrame(index=range(0, option_pairs_count), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_put = DataFrame(index=range(0, option_pairs_count), columns=range(0, 선물장간_시간차 + day_timespan))

                    df_plotdata_call_volume = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_put_volume = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_volume_cha = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))

                    df_plotdata_call_oi = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_put_oi = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))

                    df_plotdata_two_sum = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_two_cha = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))

                    df_plotdata_fut = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_kp200 = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_fut_volume = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))

                    df_plotdata_sp500 = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_dow = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                    df_plotdata_nasdaq = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + day_timespan))
                else:
                    # 야간옵션은 4시, 야간선물은 5시 장마감됨                    
                    self.Plot1.setRange(xRange=[0, 선물장간_시간차 + overnight_timespan], padding=0)
                    plot1_time_line.setValue(선물장간_시간차 + overnight_timespan - 1)

                    self.Plot2.setRange(xRange=[0, 선물장간_시간차 + overnight_timespan], padding=0)
                    plot2_time_line.setValue(선물장간_시간차 + overnight_timespan - 1)

                    if UI_STYLE == 'Vertical_view.ui':

                        self.Plot3.setRange(xRange=[0, 선물장간_시간차 + overnight_timespan], padding=0)
                        plot3_time_line.setValue(선물장간_시간차 +overnight_timespan - 1)

                        self.Plot4.setRange(xRange=[0, 선물장간_시간차 + overnight_timespan], padding=0)
                        plot4_time_line.setValue(선물장간_시간차 + overnight_timespan - 1)
                    else:
                        pass

                    df_plotdata_call = DataFrame(index=range(0, option_pairs_count), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_put = DataFrame(index=range(0, option_pairs_count), columns=range(0, 선물장간_시간차 + overnight_timespan))

                    df_plotdata_call_volume = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_put_volume = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_volume_cha = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))

                    df_plotdata_call_oi = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_put_oi = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))

                    df_plotdata_two_sum = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_two_cha = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))

                    df_plotdata_fut = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_kp200 = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_fut_volume = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))

                    df_plotdata_sp500 = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_dow = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))
                    df_plotdata_nasdaq = DataFrame(index=range(0, 1), columns=range(0, 선물장간_시간차 + overnight_timespan))

                # 콜처리
                for i in range(option_pairs_count):

                    행사가 = df['행사가'][i]
                    item = QTableWidgetItem("{0:0.2f}".format(df['float_행사가'][i]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.행사가.value, item)

                    call_code.append(df['콜옵션코드'][i])
                    opt_actval.append(df['콜옵션코드'][i][5:8])

                    OLOH = ''
                    item = QTableWidgetItem(OLOH)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.OLOH.value, item)

                    시가 = round(df['시가'][i], 2)

                    현재가 = df['현재가'][i]
                    item = QTableWidgetItem("{0:0.2f}".format(현재가))
                    item.setTextAlignment(Qt.AlignCenter)
                    #item.setBackground(QBrush(옅은회색))

                    if pre_start:

                        item.setForeground(QBrush(검정색))
                    else:
                        if 시가 > 0:

                            if 현재가 > 시가:
                                item.setForeground(QBrush(적색))
                            elif 현재가 < 시가:
                                item.setForeground(QBrush(청색))
                            else:
                                item.setForeground(QBrush(검정색))
                        else:
                            pass

                    self.tableWidget_call.setItem(i, Option_column.현재가.value, item)

                    if df['전일대비구분'][i] == '2':

                        종가 = round((현재가 - df['전일대비'][i]), 2)

                    elif df['전일대비구분'][i] == '5':

                        종가 = round((현재가 + df['전일대비'][i]), 2)

                    else:
                        종가 = round(현재가, 2)                                            

                    item = QTableWidgetItem("{0:0.2f}".format(종가))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.종가.value, item)

                    df_plotdata_call.iloc[i][0] = 종가

                    저가 = df['저가'][i]
                    item = QTableWidgetItem("{0:0.2f}".format(저가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_call.setItem(i, Option_column.저가.value, item)

                    고가 = df['고가'][i]
                    item = QTableWidgetItem("{0:0.2f}".format(고가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_call.setItem(i, Option_column.고가.value, item)

                    if not overnight:

                        if 저가 < 고가:

                            call_open[i] = True
                            self.tableWidget_call.item(i, Option_column.행사가.value).setBackground(QBrush(라임))
                        else:
                            pass
                    else:
                        pass

                    진폭 = 고가 - 저가
                    item = QTableWidgetItem("{0:0.2f}".format(진폭))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.진폭.value, item)
                    
                    if not overnight:

                        if 시가 > opt_search_start_value and 저가 < 고가:

                            call_open_list.append(i)
                        else:
                            pass
                    else:
                        pass

                    if 시가 > 0:

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)

                        if 시가 > 종가:
                            item.setForeground(QBrush(적색))
                        elif 시가 < 종가:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))

                        self.tableWidget_call.setItem(i, Option_column.시가.value, item)

                        if 시가 in 진성맥점:

                            self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                            self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                        else:
                            pass

                        if not overnight:
                            df_plotdata_call.iloc[i][선물장간_시간차] = 시가
                        else:
                            pass

                        시가갭 = 시가 - 종가
                        대비 = int(round((현재가 - 시가) * 1, 2))

                        if 시가 > 0 and 저가 < 고가:

                            call_gap_percent[i] = (시가 / 종가 - 1) * 100

                            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(시가갭, call_gap_percent[i])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.시가갭.value, item)

                            call_db_percent[i] = (현재가 / 시가 - 1) * 100

                            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(대비, call_db_percent[i])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.대비.value, item)
                        else:
                            gap_str = "{0:0.2f}".format(시가갭)

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.시가갭.value, item)

                            gap_str = "{0:0.2f}".format(대비)

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.대비.value, item)
                    else:
                        시가 = 0.0
                        시가갭 = 0.0
                        대비 = 0

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.시가.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(시가갭))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.시가갭.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(대비))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.대비.value, item)

                    피봇 = 0.0
                    item = QTableWidgetItem("{0:0.2f}".format(피봇))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.피봇.value, item)

                    if overnight:
                        전저 = 저가
                        종가 = 현재가
                        전고 = 고가
                    else:
                        전저 = 0.0
                        전고 = 0.0

                    if df['현재가'][i] <= 시가갭:

                        수정미결 = int(df['미결제약정'][i] * df['현재가'][i])
                        수정거래량 = int((df['매수잔량'][i] - df['매도잔량'][i]) * df['현재가'][i])
                    else:
                        수정미결 = int(df['미결제약정'][i] * (df['현재가'][i] - 시가갭))
                        수정거래량 = int((df['매수잔량'][i] - df['매도잔량'][i]) * (df['현재가'][i] - 시가갭))
                    
                    순미결 = df['미결제약정'][i]
                    순거래량 = df['매수잔량'][i] - df['매도잔량'][i]

                    temp = format(수정거래량, ',')
                    
                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.VP.value, item)

                    if pre_start:

                        temp = format(순미결, ',')
                    else:
                        temp = format(수정미결, ',')               

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.OI.value, item)

                    순미결증감 = df['미결제약정증감'][i]
                    수정미결증감 = int(round(df['미결제약정증감'][i] * df['현재가'][i]))
                    temp = format(수정미결증감, ',')

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.OID.value, item)

                    단축코드 = 0
                    체결시간 = 0
                    기준가 = 0.0
                    월저 = 0.0
                    월고 = 0.0

                    lst = [단축코드, 체결시간, 행사가, OLOH, 기준가, 월저, 월고, 전저, 전고, 종가, 피봇, 시가, 시가갭, 저가, 현재가,
                           고가, 대비, 진폭, 순거래량, 수정거래량, 순미결, 수정미결, 순미결증감, 수정미결증감]
                    t2301_call.append(lst)

                    매도누적체결량 = 0
                    매도누적체결건수 = 0
                    매수누적체결량 = 0
                    매수누적체결건수 = 0

                    lst = [매도누적체결량, 매도누적체결건수, 매수누적체결량, 매수누적체결건수]
                    callche_result.append(lst)

                    매수건수 = 0
                    매도건수 = 0
                    매수잔량 = 0
                    매도잔량 = 0

                    lstho = [매수건수, 매도건수, 매수잔량, 매도잔량]
                    callho_result.append(lstho)

                columns = ['단축코드', '체결시간', '행사가', 'OLOH', '기준가', '월저', '월고', '전저', '전고', '종가', '피봇', '시가', '시가갭', '저가',
                           '현재가', '고가', '대비', '진폭', '순거래량', '수정거래량', '순미결', '수정미결', '순미결증감', '수정미결증감']

                df_call = DataFrame(data=t2301_call, columns=columns)

                columns = ['매도누적체결량', '매도누적체결건수', '매수누적체결량', '매수누적체결건수']
                df_call_volume = DataFrame(data=callche_result, columns=columns)

                columns = ['매수건수', '매도건수', '매수잔량', '매도잔량']
                df_call_hoga = DataFrame(data=callho_result, columns=columns)

                temp = format(df_call['수정거래량'].sum(), ',')

                item = QTableWidgetItem(temp)
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.VP.value, item)

                if pre_start:

                    순미결합 = format(df_call['순미결'].sum(), ',')

                    item = QTableWidgetItem(순미결합)
                    self.tableWidget_call.setHorizontalHeaderItem(Option_column.OI.value, item)
                else:
                    temp = '{0}k'.format(format(int(df_call['수정미결'].sum()/1000), ','))                       
                    
                    item = QTableWidgetItem(temp)
                    self.tableWidget_call.setHorizontalHeaderItem(Option_column.OI.value, item)

                call_행사가 = df_call['행사가'].values.tolist()

                print('t2301 주간 전광판 콜 데이타 = \r', df_call)

                #self.tableWidget_call.resizeColumnsToContents()

                str = '[{0:02d}:{1:02d}:{2:02d}] {3} 월물 Call 전광판 데이타 수신완료 !!!\r'.format(dt.hour, dt.minute, dt.second, t2301_month_info)
                self.textBrowser.append(str)

                # 풋처리
                for i in range(option_pairs_count):

                    행사가 = df1['행사가'][i]
                    item = QTableWidgetItem("{0:0.2f}".format(df1['float_행사가'][i]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.행사가.value, item)

                    put_code.append(df1['풋옵션코드'][i])

                    OLOH = ''
                    item = QTableWidgetItem(OLOH)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.OLOH.value, item)

                    시가 = round(df1['시가'][i], 2)

                    현재가 = df1['현재가'][i]
                    item = QTableWidgetItem("{0:0.2f}".format(현재가))
                    item.setTextAlignment(Qt.AlignCenter)
                    #item.setBackground(QBrush(옅은회색))

                    if pre_start:

                        item.setForeground(QBrush(검정색))
                    else:
                        if 시가 > 0:

                            if 현재가 > 시가:
                                item.setForeground(QBrush(적색))
                            elif 현재가 < 시가:
                                item.setForeground(QBrush(청색))
                            else:
                                item.setForeground(QBrush(검정색))
                        else:
                            pass

                    self.tableWidget_put.setItem(i, Option_column.현재가.value, item)

                    if df1['전일대비구분'][i] == '2':

                        종가 = round((현재가 - df1['전일대비'][i]), 2)

                    elif df['전일대비구분'][i] == '5':

                        종가 = round((현재가 + df1['전일대비'][i]), 2)

                    else:
                        종가 = round(현재가, 2)                                            

                    item = QTableWidgetItem("{0:0.2f}".format(종가))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.종가.value, item)

                    df_plotdata_put.iloc[i][0] = 종가

                    저가 = df1['저가'][i]
                    item = QTableWidgetItem("{0:0.2f}".format(저가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_put.setItem(i, Option_column.저가.value, item)

                    고가 = df1['고가'][i]
                    item = QTableWidgetItem("{0:0.2f}".format(고가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_put.setItem(i, Option_column.고가.value, item)

                    if not overnight:

                        if 저가 < 고가:

                            put_open[i] = True
                            self.tableWidget_put.item(i, Option_column.행사가.value).setBackground(QBrush(라임))
                        else:
                            pass
                    else:
                        pass

                    진폭 = 고가 - 저가
                    item = QTableWidgetItem("{0:0.2f}".format(진폭))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.진폭.value, item)
                    
                    if not overnight:

                        if 시가 > opt_search_start_value and 저가 < 고가:

                            put_open_list.append(i)
                        else:
                            pass
                    else:
                        pass

                    if 시가 > 0:

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)

                        if 시가 > 종가:
                            item.setForeground(QBrush(적색))
                        elif 시가 < 종가:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))

                        self.tableWidget_put.setItem(i, Option_column.시가.value, item)

                        if 시가 in 진성맥점:

                            self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                            self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                        else:
                            pass

                        if not overnight:
                            df_plotdata_put.iloc[i][선물장간_시간차] = 시가
                        else:
                            pass

                        시가갭 = 시가 - 종가
                        대비 = int(round((현재가 - 시가) * 1, 2))

                        if 시가 > 0 and 저가 < 고가:

                            put_gap_percent[i] = (시가 / 종가 - 1) * 100

                            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(시가갭, put_gap_percent[i])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.시가갭.value, item)

                            put_db_percent[i] = (현재가 / 시가 - 1) * 100

                            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(대비, put_db_percent[i])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.대비.value, item)
                        else:
                            gap_str = "{0:0.2f}".format(시가갭)

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.시가갭.value, item)

                            gap_str = "{0:0.2f}".format(대비)

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.대비.value, item)
                    else:
                        시가 = 0.0
                        시가갭 = 0.0
                        대비 = 0

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.시가.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(시가갭))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.시가갭.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(대비))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.대비.value, item)

                    피봇 = 0.0
                    item = QTableWidgetItem("{0:0.2f}".format(피봇))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.피봇.value, item)

                    if overnight:
                        전저 = 저가
                        종가 = 현재가
                        전고 = 고가
                    else:
                        전저 = 0.0
                        전고 = 0.0

                    if df1['현재가'][i] <= 시가갭:

                        수정미결 = int(df1['미결제약정'][i] * df1['현재가'][i])
                        수정거래량 = int((df1['매수잔량'][i] - df1['매도잔량'][i]) * df1['현재가'][i])
                    else:
                        수정미결 = int(df1['미결제약정'][i] * (df1['현재가'][i] - 시가갭))
                        수정거래량 = int((df1['매수잔량'][i] - df1['매도잔량'][i]) * (df1['현재가'][i] - 시가갭))
                    
                    순미결 = df1['미결제약정'][i]
                    순거래량 = df1['매수잔량'][i] - df1['매도잔량'][i] 

                    temp = format(수정거래량, ',')

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.VP.value, item)                   

                    if pre_start:

                        temp = format(순미결, ',')
                    else:
                        temp = format(수정미결, ',')                                                

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.OI.value, item)

                    순미결증감 = df1['미결제약정증감'][i]
                    수정미결증감 = int(round(df1['미결제약정증감'][i] * df1['현재가'][i]))
                    temp = format(수정미결증감, ',')

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.OID.value, item)

                    단축코드 = 0
                    체결시간 = 0
                    기준가 = 0.0
                    월저 = 0.0
                    월고 = 0.0

                    lst = [단축코드, 체결시간, 행사가, OLOH, 기준가, 월저, 월고, 전저, 전고, 종가, 피봇, 시가, 시가갭, 저가, 현재가,
                           고가, 대비, 진폭, 순거래량, 수정거래량, 순미결, 수정미결, 순미결증감, 수정미결증감]
                    t2301_put.append(lst)

                    매도누적체결량 = 0
                    매도누적체결건수 = 0
                    매수누적체결량 = 0
                    매수누적체결건수 = 0

                    lst = [매도누적체결량, 매도누적체결건수, 매수누적체결량, 매수누적체결건수]
                    putche_result.append(lst)

                    매수건수 = 0
                    매도건수 = 0
                    매수잔량 = 0
                    매도잔량 = 0

                    lstho = [매수건수, 매도건수, 매수잔량, 매도잔량]
                    putho_result.append(lstho)

                columns = ['단축코드', '체결시간', '행사가', 'OLOH', '기준가', '월저', '월고', '전저', '전고', '종가', '피봇', '시가', '시가갭', '저가',
                           '현재가', '고가', '대비', '진폭', '순거래량', '수정거래량', '순미결', '수정미결', '순미결증감', '수정미결증감']

                df_put = DataFrame(data=t2301_put, columns=columns)

                columns = ['매도누적체결량', '매도누적체결건수', '매수누적체결량', '매수누적체결건수']
                df_put_volume = DataFrame(data=putche_result, columns=columns)

                columns = ['매수건수', '매도건수', '매수잔량', '매도잔량']
                df_put_hoga = DataFrame(data=putho_result, columns=columns)

                temp = format(df_put['수정거래량'].sum(), ',')

                item = QTableWidgetItem(temp)
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.VP.value, item)

                if pre_start:

                    순미결합 = format(df_put['순미결'].sum(), ',')

                    item = QTableWidgetItem(순미결합)
                    self.tableWidget_put.setHorizontalHeaderItem(Option_column.OI.value, item)
                else:
                    temp = '{0}k'.format(format(int(df_put['수정미결'].sum()/1000), ','))                                   

                    item = QTableWidgetItem(temp)
                    self.tableWidget_put.setHorizontalHeaderItem(Option_column.OI.value, item)

                put_행사가 = df_put['행사가'].values.tolist()
                
                print('t2301 주간 전광판 풋 데이타 = \r', df_put)

                #self.tableWidget_put.resizeColumnsToContents()

                str = '[{0:02d}:{1:02d}:{2:02d}] {3} 월물 Put 전광판 데이타 수신완료 !!!\r'.format(dt.hour, dt.minute, dt.second, t2301_month_info)
                self.textBrowser.append(str)

                if not pre_start:

                    # 콜 컬러링 리스트 작성
                    call_시가 = df_call['시가'].values.tolist()
                    call_시가_node_list = self.make_node_list(call_시가)

                    call_피봇 = df_call['피봇'].values.tolist()
                    call_피봇_node_list = self.make_node_list(call_피봇)

                    call_저가 = df_call['저가'].values.tolist()
                    call_저가_node_list = self.make_node_list(call_저가)

                    call_고가 = df_call['고가'].values.tolist()
                    call_고가_node_list = self.make_node_list(call_고가)

                    call_진폭 = df_call['진폭'].values.tolist()
                    진폭최대값 = max(call_진폭)
                    max_str = '{0:0.2f}'.format(진폭최대값)

                    item = QTableWidgetItem(max_str)
                    self.tableWidget_call.setHorizontalHeaderItem(Option_column.진폭.value, item)

                    # 풋 컬러링 리스트 작성
                    put_시가 = df_put['시가'].values.tolist()
                    put_시가_node_list = self.make_node_list(put_시가)

                    put_피봇 = df_put['피봇'].values.tolist()
                    put_피봇_node_list = self.make_node_list(put_피봇)

                    put_저가 = df_put['저가'].values.tolist()
                    put_저가_node_list = self.make_node_list(put_저가)

                    put_고가 = df_put['고가'].values.tolist()
                    put_고가_node_list = self.make_node_list(put_고가)

                    put_진폭 = df_put['진폭'].values.tolist()
                    진폭최대값 = max(put_진폭)
                    max_str = '{0:0.2f}'.format(진폭최대값)

                    item = QTableWidgetItem(max_str)
                    self.tableWidget_put.setHorizontalHeaderItem(Option_column.진폭.value, item)
                else:
                    pass

                df_plotdata_call_volume.iloc[0][0] = 0                
                df_plotdata_put_volume.iloc[0][0] = 0
                df_plotdata_volume_cha.iloc[0][0] = 0

                df_plotdata_call_volume.iloc[0][선물장간_시간차] = 0                
                df_plotdata_put_volume.iloc[0][선물장간_시간차] = 0
                df_plotdata_volume_cha.iloc[0][선물장간_시간차] = 0
                
                df_plotdata_call_oi[0][0] = 0
                df_plotdata_put_oi[0][0] = 0

                df_plotdata_call_oi[0][선물장간_시간차] = 0
                df_plotdata_put_oi[0][선물장간_시간차] = 0
                
                콜_순미결합 = df_call['순미결'].sum()
                풋_순미결합 = df_put['순미결'].sum()

                순미결합 = 콜_순미결합 + 풋_순미결합

                콜_수정미결합 = df_call['수정미결'].sum()
                풋_수정미결합 = df_put['수정미결'].sum()

                수정미결합 = 콜_수정미결합 + 풋_수정미결합

                if 순미결합 > 0:

                    콜_순미결퍼센트 = (콜_순미결합 / 순미결합) * 100
                    풋_순미결퍼센트 = 100 - 콜_순미결퍼센트
                    
                    str = '[{0:02d}:{1:02d}:{2:02d}] Call/Put OI 초기값 : {3}/{4}\r'.format(dt.hour,
                                            dt.minute, dt.second, format(콜_순미결합, ','), format(풋_순미결합, ','))
                    self.textBrowser.append(str)

                    temp = '{0}k:{1}k'.format(format(int(콜_순미결합/1000), ','), format(int(풋_순미결합/1000), ','))

                    item = QTableWidgetItem(temp)
                    self.tableWidget_quote.setHorizontalHeaderItem(Quote_column.미결종합.value - 1, item)
                else:
                    pass

                if 수정미결합 > 0:

                    콜_수정미결퍼센트 = (콜_수정미결합 / 수정미결합) * 100
                    풋_수정미결퍼센트 = 100 - 콜_수정미결퍼센트

                    call_oi_init_value = 콜_수정미결합
                    put_oi_init_value = 풋_수정미결합
                else:
                    pass
                
                # 장운영정보 요청
                self.JIF.AdviseRealData('0')

                # S&P 500, DOW, NASDAQ 요청
                self.OVC.AdviseRealData(종목코드=SP500)
                self.OVC.AdviseRealData(종목코드=DOW)
                self.OVC.AdviseRealData(종목코드=NASDAQ)

                XQ = t2101(parent=self)
                XQ.Query(종목코드=fut_code)

                if fut_code == gmshcode:
                    str = '[{0:02d}:{1:02d}:{2:02d}] t2101 본월물 주간선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                elif fut_code == cmshcode:
                    str = '[{0:02d}:{1:02d}:{2:02d}] t2101 차월물 주간선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                elif fut_code == ccmshcode:
                    str = '[{0:02d}:{1:02d}:{2:02d}] t2101 차차월물 주간선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                else:
                    str = '[{0:02d}:{1:02d}:{2:02d}] 잘못된 선물코드({3})입니다.\r'.format(dt.hour, dt.minute, dt.second, fut_code)

                self.textBrowser.append(str)

                time.sleep(0.1)

                XQ = t2801(parent=self)
                XQ.Query(종목코드=fut_code)

                if fut_code == gmshcode:
                    str = '[{0:02d}:{1:02d}:{2:02d}] t2801 본월물 야간선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                elif fut_code == cmshcode:
                    str = '[{0:02d}:{1:02d}:{2:02d}] t2801 차월물 야간선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                elif fut_code == ccmshcode:
                    str = '[{0:02d}:{1:02d}:{2:02d}] t2801 차차월물 야간선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                else:
                    str = '[{0:02d}:{1:02d}:{2:02d}] 잘못된 선물코드({3})입니다.\r'.format(dt.hour, dt.minute, dt.second, fut_code)

                self.textBrowser.append(str)

                if not overnight:        

                    print('\r')
                    print('t2301 call open list = ', call_open_list, len(call_open_list))
                    print('\r')
                    print('t2301 put open list = ', put_open_list, len(put_open_list))
                    print('\r')            

                    if pre_start:

                        # FUTURES/KOSPI200 예상지수 요청
                        self.YJ.AdviseRealData(FUTURES)
                        self.YJ.AdviseRealData(KOSPI200)

                        # 지수선물예상체결 요청
                        self.YFC.AdviseRealData(fut_code)

                        # KOSPI예상체결 요청                        
                        self.YS3.AdviseRealData(SAMSUNG)
                        self.YS3.AdviseRealData(HYUNDAI)
                        #self.YS3.AdviseRealData(Celltrion)

                        # 지수옵션예상체결 요청
                        for i in range(option_pairs_count):
                            self.YOC.AdviseRealData(call_code[i])
                            self.YOC.AdviseRealData(put_code[i])
                    else:
                        pass

                    # 옵션 실시간테이타 요청
                    for i in range(option_pairs_count):
                        self.OPT_REAL.AdviseRealData(call_code[i])
                        self.OPT_REAL.AdviseRealData(put_code[i])

                    # 전일등가 중심 9개 행사가 호가요청
                    for i in range(option_pairs_count):
                        self.OPT_HO.AdviseRealData(call_code[i])
                        self.OPT_HO.AdviseRealData(put_code[i])

                    # 선물 실시간테이타 요청
                    self.FUT_REAL.AdviseRealData(fut_code)
                    self.FUT_HO.AdviseRealData(fut_code)

                    # KOSPI/KOSPI200/KOSDAQ 지수요청
                    self.IJ.AdviseRealData(KOSPI)
                    self.IJ.AdviseRealData(KOSPI200)
                    self.IJ.AdviseRealData(KOSDAQ)

                    # KOSPI체결 요청
                    self.S3.AdviseRealData(SAMSUNG)
                    #self.S3.AdviseRealData(HYUNDAI)
                    #self.S3.AdviseRealData(Celltrion)

                    # 업종별 투자자별 매매현황 요청
                    self.BM.AdviseRealData(FUTURES)
                    self.BM.AdviseRealData(KOSPI)

                    # 프로그램 매매현황 요청
                    self.PM.AdviseRealData()                    
                else:
                    pass

                # t8416 요청
                self.t8416_callworker.start()
                self.t8416_callworker.daemon = True

            else:
                # Refresh
                if not overnight:
                                    
                    str = '[{0:02d}:{1:02d}:{2:02d}] 주간옵션 전광판을 갱신합니다.\r'.format(dt.hour, dt.minute, dt.second)
                    self.textBrowser.append(str)

                    del call_open_list[:]
                    del put_open_list[:]

                    for i in range(option_pairs_count):

                        # 콜 데이타 획득                        
                        시가 = df['시가'][i]
                        df_call.loc[i, '시가'] = 시가

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.시가.value, item)

                        if 시가 > 0 and df['저가'][i] < df['고가'][i]:

                            시가갭 = 시가 - df_call.iloc[i]['종가']
                            df_call.loc[i, '시가갭'] = 시가갭

                            if df_call.iloc[i]['종가'] > 0:

                                call_gap_percent[i] = (df_call.iloc[i]['시가'] / df_call.iloc[i]['종가'] - 1) * 100
                                gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_call.iloc[i]['시가갭'], call_gap_percent[i])
                            else:
                                call_gap_percent[i] = 0.0
                                gap_str = "{0:0.2f}".format(df_call.iloc[i]['시가갭'])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.시가갭.value, item)

                            if df_call.iloc[i]['피봇'] == 0:

                                피봇 = self.calc_pivot(df_call.iloc[i]['전저'], df_call.iloc[i]['전고'], df_call.iloc[i]['종가'], 시가)

                                df_call.loc[i, '피봇'] = 피봇

                                item = QTableWidgetItem("{0:0.2f}".format(피봇))
                                item.setTextAlignment(Qt.AlignCenter)
                                self.tableWidget_call.setItem(i, Option_column.피봇.value, item)
                            else:
                                pass
                        else:
                            시가갭 = 0
                            df_call.loc[i, '시가갭'] = 시가갭

                        현재가 = df['현재가'][i]
                        df_call.loc[i, '현재가'] = 현재가

                        item = QTableWidgetItem("{0:0.2f}".format(현재가))
                        item.setTextAlignment(Qt.AlignCenter)
                        #item.setBackground(QBrush(옅은회색))

                        if 시가 > 0:

                            if 현재가 > 시가:
                                item.setForeground(QBrush(적색))
                            elif 현재가 < 시가:
                                item.setForeground(QBrush(청색))
                            else:
                                item.setForeground(QBrush(검정색))
                        else:
                            pass
                        
                        self.tableWidget_call.setItem(i, Option_column.현재가.value, item)
                        
                        저가 = df['저가'][i]
                        df_call.loc[i, '저가'] = 저가

                        item = QTableWidgetItem("{0:0.2f}".format(저가))
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(옅은회색))
                        self.tableWidget_call.setItem(i, Option_column.저가.value, item)

                        고가 = df['고가'][i]
                        df_call.loc[i, '고가'] = 고가

                        item = QTableWidgetItem("{0:0.2f}".format(고가))
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(옅은회색))
                        self.tableWidget_call.setItem(i, Option_column.고가.value, item)
                        
                        if 시가 > opt_search_start_value and 저가 < 고가:

                            call_open_list.append(i)
                        else:
                            pass

                        # 풋 데이타 획득                        
                        시가 = df1['시가'][i]
                        df_put.loc[i, '시가'] = 시가

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.시가.value, item)

                        if 시가 > 0 and df1['저가'][i] < df1['고가'][i]:

                            시가갭 = 시가 - df_put.iloc[i]['종가']
                            df_put.loc[i, '시가갭'] = 시가갭

                            if df_put.iloc[i]['종가'] > 0:

                                put_gap_percent[i] = (df_put.iloc[i]['시가'] / df_put.iloc[i]['종가'] - 1) * 100
                                gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_put.iloc[i]['시가갭'], put_gap_percent[i])
                            else:
                                put_gap_percent[i] = 0.0
                                gap_str = "{0:0.2f}".format(df_put.iloc[i]['시가갭'])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.시가갭.value, item)

                            if df_put.iloc[i]['피봇'] == 0:

                                피봇 = self.calc_pivot(df_put.iloc[i]['전저'], df_put.iloc[i]['전고'], df_put.iloc[i]['종가'], 시가)

                                df_put.loc[i, '피봇'] = 피봇                                         

                                item = QTableWidgetItem("{0:0.2f}".format(피봇))
                                item.setTextAlignment(Qt.AlignCenter)
                                self.tableWidget_put.setItem(i, Option_column.피봇.value, item)
                            else:
                                pass
                        else:
                            시가갭 = 0
                            df_put.loc[i, '시가갭'] = 시가갭

                        현재가 = df1['현재가'][i]
                        df_put.loc[i, '현재가'] = 현재가

                        item = QTableWidgetItem("{0:0.2f}".format(현재가))
                        item.setTextAlignment(Qt.AlignCenter)
                        #item.setBackground(QBrush(옅은회색))

                        if 시가 > 0:

                            if 현재가 > 시가:
                                item.setForeground(QBrush(적색))
                            elif 현재가 < 시가:
                                item.setForeground(QBrush(청색))
                            else:
                                item.setForeground(QBrush(검정색))
                        else:
                            pass
                        
                        self.tableWidget_put.setItem(i, Option_column.현재가.value, item)
                        
                        저가 = df1['저가'][i]
                        df_put.loc[i, '저가'] = 저가

                        item = QTableWidgetItem("{0:0.2f}".format(저가))
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(옅은회색))
                        self.tableWidget_put.setItem(i, Option_column.저가.value, item)

                        고가 = df1['고가'][i]
                        df_put.loc[i, '고가'] = 고가

                        item = QTableWidgetItem("{0:0.2f}".format(고가))
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(옅은회색))
                        self.tableWidget_put.setItem(i, Option_column.고가.value, item)
                        
                        if 시가 > opt_search_start_value and 저가 < 고가:

                            put_open_list.append(i)
                        else:
                            pass

                    call_시가 = df_call['시가'].values.tolist()
                    call_시가_node_list = self.make_node_list(call_시가)

                    call_피봇 = df_call['피봇'].values.tolist()
                    call_피봇_node_list = self.make_node_list(call_피봇)

                    call_저가 = df_call['저가'].values.tolist()
                    call_저가_node_list = self.make_node_list(call_저가)

                    call_고가 = df_call['고가'].values.tolist()
                    call_고가_node_list = self.make_node_list(call_고가)

                    put_시가 = df_put['시가'].values.tolist()
                    put_시가_node_list = self.make_node_list(put_시가)

                    put_피봇 = df_put['피봇'].values.tolist()
                    put_피봇_node_list = self.make_node_list(put_피봇)

                    put_저가 = df_put['저가'].values.tolist()
                    put_저가_node_list = self.make_node_list(put_저가)

                    put_고가 = df_put['고가'].values.tolist()
                    put_고가_node_list = self.make_node_list(put_고가)
                    
                    # 주야간 선물전광판 데이타 요청
                    XQ = t2101(parent=self)
                    XQ.Query(종목코드=fut_code)

                    str = '[{0:02d}:{1:02d}:{2:02d}] 주간 선물전광판 갱신을 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                    self.textBrowser.append(str)

                    time.sleep(0.1)

                    XQ = t2801(parent=self)
                    XQ.Query(종목코드=fut_code)

                    str = '[{0:02d}:{1:02d}:{2:02d}] 야간 선물전광판 갱신을 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                    self.textBrowser.append(str)

                    time.sleep(0.1)
                    
                else:                    
                    # EUREX 야간옵션 시세전광판
                    XQ = t2835(parent=self)
                    XQ.Query(월물=t2835_month_info)

                    str = '[{0:02d}:{1:02d}:{2:02d}] 야간옵션 전광판 갱신을 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                    self.textBrowser.append(str)                    

                    #str = '{0} 야간옵션 시세전광판 재요청...'.format(t2835_month_info)
                    #print(str)
            
            self.tableWidget_call.resizeColumnsToContents()
            self.tableWidget_put.resizeColumnsToContents()

        elif szTrCode == 't2801':

            df = result[0]

            if pre_start:

                if df['종합지수전일대비구분'] == '5':

                    jisu_str = "KOSPI: {0} (-{1:0.2f}, {2:0.1f}%)".format(df['종합지수'], df['종합지수전일대비'], df['종합지수등락율'])
                    self.label_kospi.setText(jisu_str)
                    self.label_kospi.setStyleSheet('background-color: black ; color: cyan')

                elif df['종합지수전일대비구분'] == '2':

                    jisu_str = "KOSPI: {0} ({1:0.2f}, {2:0.1f}%)".format(df['종합지수'], df['종합지수전일대비'], df['종합지수등락율'])
                    self.label_kospi.setText(jisu_str)
                    self.label_kospi.setStyleSheet('background-color: black ; color: magenta')
                else:
                    pass
            else:
                pass

            # 주간 데이타를 가져옴            
            item = QTableWidgetItem("{0:0.2f}".format(df['KOSPI200지수']))
            item.setTextAlignment(Qt.AlignCenter)
            #item.setBackground(QBrush(옅은회색))
            self.tableWidget_fut.setItem(2, Futures_column.현재가.value, item)

            # kp200 coreval 리스트 만듬
            kp200_realdata['종가'] = df['KOSPI200지수']
            
            atm_str = self.find_ATM(kp200_realdata['종가'])
            atm_index = opt_actval.index(atm_str)

            if atm_str[-1] == '2' or atm_str[-1] == '7':

                atm_val = float(atm_str) + 0.5
            else:
                atm_val = float(atm_str)

            if call_open_list:

                for index in call_open_list:

                    if index > atm_index:
                        call_below_atm_count += 1
                    else:
                        pass
                    
                    if index == option_pairs_count - 1:
                        call_max_actval = True
                    else:
                        pass
            else:
                pass                

            if put_open_list:

                for index in put_open_list:

                    if index > atm_index:
                        put_above_atm_count += 1
                    else:
                        pass
                    
                    if index == option_pairs_count - 1:
                        put_max_actval = True
                    else:
                        pass
            else:
                pass                    

            # kp200 맥점 10개를 리스트로 만듬
            global kp200_coreval

            # kp200_coreval 리스트 기존데이타 삭제(초기화)
            del kp200_coreval[:]

            for i in range(6):

                kp200_coreval.append(atm_val - 2.5 * i + 1.25) 

            for i in range(1, 5):

                kp200_coreval.append(atm_val + 2.5 * i + 1.25)

            kp200_coreval.sort()
            print('t2801 kp200_coreval', kp200_coreval)

            atm_str = self.find_ATM(kp200_realdata['종가'])

            if atm_str[-1] == '2' or atm_str[-1] == '7':

                atm_val = float(atm_str) + 0.5
            else:
                atm_val = float(atm_str)
            
            self.tableWidget_call.item(atm_index, Option_column.행사가.value).setBackground(QBrush(노란색))
            self.tableWidget_call.item(atm_index, Option_column.행사가.value).setForeground(QBrush(검정색))
            self.tableWidget_put.item(atm_index, Option_column.행사가.value).setBackground(QBrush(노란색))
            self.tableWidget_put.item(atm_index, Option_column.행사가.value).setForeground(QBrush(검정색))   
            
            if not refresh_flag:

                self.tableWidget_call.cellWidget(atm_index - 1, 0).findChild(type(QCheckBox())).setCheckState(Qt.Checked)
                self.tableWidget_call.cellWidget(atm_index, 0).findChild(type(QCheckBox())).setCheckState(Qt.Checked)
                self.tableWidget_call.cellWidget(atm_index + 1, 0).findChild(type(QCheckBox())).setCheckState(Qt.Checked)

                self.tableWidget_put.cellWidget(atm_index - 1, 0).findChild(type(QCheckBox())).setCheckState(Qt.Checked)
                self.tableWidget_put.cellWidget(atm_index, 0).findChild(type(QCheckBox())).setCheckState(Qt.Checked)
                self.tableWidget_put.cellWidget(atm_index + 1, 0).findChild(type(QCheckBox())).setCheckState(Qt.Checked)

                selected_call = [atm_index - 1, atm_index, atm_index + 1]
                selected_put = [atm_index - 1, atm_index, atm_index + 1]
            else:
                pass

            view_actval = opt_actval[atm_index-5:atm_index+6]

            call_atm_value = df_call.iloc[atm_index]['현재가']
            put_atm_value = df_put.iloc[atm_index]['현재가']

            str = '{0:0.2f}({1:0.2f}:{2:0.2f})'.format(
                fut_realdata['현재가'] - fut_realdata['KP200'],
                call_atm_value + put_atm_value,
                abs(call_atm_value - put_atm_value))
            self.label_atm.setText(str)
            
            if overnight:
                
                item_str = '{0:0.1f}%\n{1:0.1f}%'.format(콜_수정미결퍼센트, 풋_수정미결퍼센트)

                item = QTableWidgetItem(item_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_quote.setItem(0, Quote_column.미결종합.value - 1, item)

                df_plotdata_kp200.iloc[0][0] = kp200_realdata['종가']

                # 주간 현재가가 야간 종가임 
                df_plotdata_fut.iloc[0][0] = fut_realdata['현재가']

                if UI_STYLE == 'Vertical_view.ui':

                    # 초기 plot화면 설정
                    plot4_fut_jl_line.setValue(fut_realdata['현재가'])
                    plot4_fut_jh_line.setValue(fut_realdata['현재가'])
                    plot4_fut_close_line.setValue(fut_realdata['현재가'])
                    plot4_fut_pivot_line.setValue(fut_realdata['현재가'])
                    plot4_fut_open_line.setValue(fut_realdata['현재가'])
                else:
                    pass

                df_plotdata_fut_volume.iloc[0][0] = 0
                df_plotdata_fut_volume.iloc[0][선물장간_시간차] = 0

                if df['시가'] > 0:
                    df_plotdata_fut.iloc[0][선물장간_시간차] = df['시가']
                else:
                    pass

                cme_realdata['전저'] = fut_realdata['저가']

                item = QTableWidgetItem("{0:0.2f}".format(cme_realdata['전저']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_fut.setItem(0, Futures_column.전저.value, item)

                cme_realdata['전고'] = fut_realdata['고가']

                item = QTableWidgetItem("{0:0.2f}".format(cme_realdata['전고']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_fut.setItem(0, Futures_column.전고.value, item)

                cme_realdata['종가'] = fut_realdata['현재가']

                item = QTableWidgetItem("{0:0.2f}".format(cme_realdata['종가']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_fut.setItem(0, Futures_column.종가.value, item) 
            else:
                item = QTableWidgetItem("{0:0.2f}".format(df['전일종가']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_fut.setItem(0, Futures_column.종가.value, item)

                if UI_STYLE == 'Vertical_view.ui':

                    # 초기 plot화면 설정
                    plot4_fut_jl_line.setValue(df['현재가'])
                    plot4_fut_jh_line.setValue(df['현재가'])
                    plot4_fut_close_line.setValue(df['현재가'])
                    plot4_fut_pivot_line.setValue(df['현재가'])
                    plot4_fut_open_line.setValue(df['현재가'])
                else:
                    pass

            if df['시가'] > 0:

                cme_realdata['시가'] = df['시가']

                item = QTableWidgetItem("{0:0.2f}".format(df['시가']))
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(흰색))

                if df['시가'] > df['전일종가']:
                    item.setForeground(QBrush(적색))
                elif df['시가'] < df['전일종가']:
                    item.setForeground(QBrush(청색))
                else:
                    item.setForeground(QBrush(검정색))

                self.tableWidget_fut.setItem(0, Futures_column.시가.value, item)

                item = QTableWidgetItem("{0:0.2f}".format(df['시가'] - df['전일종가']))
                item.setTextAlignment(Qt.AlignCenter)

                if df['시가'] > df['전일종가']:
                    item.setBackground(QBrush(콜기준가색))
                    item.setForeground(QBrush(검정색))
                elif df['시가'] < df['전일종가']:
                    item.setBackground(QBrush(풋기준가색))
                    item.setForeground(QBrush(흰색))
                else:
                    item.setBackground(QBrush(흰색))  

                self.tableWidget_fut.setItem(0, Futures_column.시가갭.value, item)

                if cme_realdata['전저'] > 0 and cme_realdata['전고'] > 0:

                    cme_realdata['피봇'] = self.calc_pivot(cme_realdata['전저'], cme_realdata['전고'], 
                                            df['전일종가'], cme_realdata['시가'])

                    item = QTableWidgetItem("{0:0.2f}".format(cme_realdata['피봇']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_fut.setItem(0, Futures_column.피봇.value, item)
                else:
                    pass
            else:
                pass   

            cme_realdata['저가'] = df['저가']   

            item = QTableWidgetItem("{0:0.2f}".format(df['저가']))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(옅은회색))
            self.tableWidget_fut.setItem(0, Futures_column.저가.value, item)

            if overnight:
                cme_realdata['현재가'] = df['현재가']
            else:
                pass            

            item = QTableWidgetItem("{0:0.2f}".format(df['현재가']))
            item.setTextAlignment(Qt.AlignCenter)
            #item.setBackground(QBrush(옅은회색))

            if df['시가'] > 0:

                if df['현재가'] > df['시가']:
                    item.setForeground(QBrush(적색))
                elif df['현재가'] < df['시가']:
                    item.setForeground(QBrush(청색))
                else:
                    item.setForeground(QBrush(검정색))
            else:
                pass

            self.tableWidget_fut.setItem(0, Futures_column.현재가.value, item)

            temp = (round((df['현재가'] - df['시가']), 2))

            item = QTableWidgetItem("{0:0.2f}".format(temp))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(0, Futures_column.대비.value, item)
            
            if overnight:

                선물_전저 = cme_realdata['전저']
                선물_전고 = cme_realdata['전고']

                # 주간 현재가가 야간종가 임
                선물_종가 = cme_realdata['종가']

                if cme_realdata['피봇'] > 0:
                    선물_피봇 = cme_realdata['피봇']
                else:
                    선물_피봇 = cme_realdata['종가']

                if df['시가'] > 0:
                    선물_시가 = df['시가']
                else:
                    선물_시가 = cme_realdata['종가']

                if df['저가'] > 0:
                    선물_저가 = df['저가']
                else:
                    선물_저가 = cme_realdata['종가']

                if df['현재가'] > 0:
                    선물_현재가 = df['현재가']
                else:
                    선물_현재가 = cme_realdata['종가']

                if df['고가'] > 0:
                    선물_고가 = df['고가']
                else:
                    선물_고가 = cme_realdata['종가']
            else:
                if pre_start:
                    #선물_종가 = CME_INDEX
                    선물_피봇 = CME_INDEX 
                    선물_시가 = CME_INDEX
                    선물_저가 = CME_INDEX
                    선물_현재가 = CME_INDEX
                    선물_고가 = CME_INDEX 
                else:
                    pass           
            
            if overnight:

                df_plotdata_kp200.iloc[0][0] = fut_realdata['KP200']
                df_plotdata_fut.iloc[0][0] = cme_realdata['종가']

                if cme_realdata['시가'] > 0:
                    df_plotdata_fut.iloc[0][선물장간_시간차] = cme_realdata['시가']
                else:
                    pass

                df_plotdata_fut_volume.iloc[0][0] = 0
                df_plotdata_fut_volume.iloc[0][선물장간_시간차] = 0
            else:
                pass

            cme_realdata['고가'] = df['고가']           

            item = QTableWidgetItem("{0:0.2f}".format(df['고가']))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(옅은회색))
            self.tableWidget_fut.setItem(0, Futures_column.고가.value, item)

            cme_realdata['진폭'] = df['고가'] - df['저가']

            item = QTableWidgetItem("{0:0.2f}".format(cme_realdata['진폭']))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(0, Futures_column.진폭.value, item)

            temp = format(df['거래량'], ',')
            item = QTableWidgetItem(temp)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(0, Futures_column.거래량.value, item)

            temp = format(df['미결제량'], ',')
            item = QTableWidgetItem(temp)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(0, Futures_column.OI.value, item)

            temp = format(df['미결제증감'], ',')
            item = QTableWidgetItem(temp)
            item.setTextAlignment(Qt.AlignCenter)

            if df['미결제증감'] < 0:
                item.setBackground(QBrush(라임))
            else:
                item.setBackground(QBrush(흰색))

            self.tableWidget_fut.setItem(0, Futures_column.OID.value, item)                        

            self.tableWidget_fut.resizeColumnsToContents()

            columns = ['KP200', '전저', '전고', '종가', '피봇', '시가', '시가갭', '저가',
                       '현재가', '고가', '대비', '진폭', '거래량', '미결', '미결증감']

            df_fut = DataFrame(data=[cme_realdata, fut_realdata, kp200_realdata], columns=columns)

            print('df_fut', df_fut)

            # 선물 맥점 컬러 체크
            self.fut_node_color_clear()
            self.fut_oloh_check()
            self.fut_node_coloring()

            # 실시간에서만 표시됨
            t = dt.hour * 3600 + dt.minute * 60 + dt.second
            self.kp200_low_node_coloring(t)
            self.kp200_high_node_coloring(t)

            if refresh_flag:

                # 옵션 맥점 컬러링                    
                self.opt_node_coloring()
                
                str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 맥점 컬러링을 완료했습니다.\r'.format(dt.hour, dt.minute, dt.second)
                self.textBrowser.append(str)
            else:
                pass

        elif szTrCode == 't2830':

            pass

        elif szTrCode == 't2835':

            # EUREX 야간옵션 시세전광판

            block, df, df1 = result

            if not refresh_flag:

                # open, ol/oh 초기화
                if overnight:

                    call_open = [False] * option_pairs_count
                    put_open = [False] * option_pairs_count
                else:
                    pass

                # gap percent 초기화
                call_gap_percent = [NaN] * option_pairs_count
                put_gap_percent = [NaN] * option_pairs_count

                # db percent 초기화
                call_db_percent = [NaN] * option_pairs_count
                put_db_percent = [NaN] * option_pairs_count

                item = QTableWidgetItem('행사가')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.행사가.value, item)

                item = QTableWidgetItem('▲▼')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.OLOH.value, item)

                item = QTableWidgetItem('시가갭\n(%)')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.시가갭.value, item)

                item = QTableWidgetItem('대비\n(%)')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.대비.value, item)

                item = QTableWidgetItem('∑PVP')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.VP.value, item)

                item = QTableWidgetItem('∑OI')
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.OI.value, item)

                item = QTableWidgetItem('행사가')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.행사가.value, item)

                item = QTableWidgetItem('▲▼')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.OLOH.value, item)

                item = QTableWidgetItem('시가갭\n(%)')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.시가갭.value, item)

                item = QTableWidgetItem('대비\n(%)')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.대비.value, item)

                item = QTableWidgetItem('∑PVP')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.VP.value, item)

                item = QTableWidgetItem('∑OI')
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.OI.value, item)

                수정거래량 = 0

                for i in range(option_pairs_count):

                    # 수정거래량 초기화
                    #df_call.loc[i, '수정거래량'] = 0
                    df_call.loc[i, '시가갭'] = 0
                    df_call.loc[i, '대비'] = 0

                    # Call 처리
                    self.tableWidget_call.item(i, Option_column.행사가.value).setBackground(QBrush(흰색))

                    oloh_str = ''
                    item = QTableWidgetItem(oloh_str)
                    item.setBackground(QBrush(흰색))
                    item.setForeground(QBrush(검정색))
                    self.tableWidget_call.setItem(i, Option_column.OLOH.value, item)

                    전저 = df_call.iloc[i]['저가']
                    df_call.loc[i, '전저'] = 전저

                    item = QTableWidgetItem("{0:0.2f}".format(전저))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.전저.value, item)

                    전고 = df_call.iloc[i]['고가']
                    df_call.loc[i, '전고'] = 전고

                    item = QTableWidgetItem("{0:0.2f}".format(전고))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.전고.value, item)

                    if 18 <= dt.hour < 24 or 0 <= dt.hour < 4:
                        
                        시가 = df['시가'][i]
                    else:
                        시가 = 0.0

                    df_call.loc[i, '시가'] = 시가

                    종가 = df_call.iloc[i]['현재가']
                    df_call.loc[i, '종가'] = 종가

                    item = QTableWidgetItem("{0:0.2f}".format(종가))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.종가.value, item)

                    df_plotdata_call.iloc[i][0] = 종가

                    현재가 = df['현재가'][i]
                    df_call.loc[i, '현재가'] = 현재가

                    item = QTableWidgetItem("{0:0.2f}".format(현재가))
                    item.setTextAlignment(Qt.AlignCenter)                    
                    #item.setBackground(QBrush(옅은회색))

                    if 시가 > 0:

                        if 시가 < 현재가:
                            item.setForeground(QBrush(적색))
                        elif 시가 > 현재가:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))
                    else:
                        item.setForeground(QBrush(검정색))

                    self.tableWidget_call.setItem(i, Option_column.현재가.value, item)

                    저가 = df['저가'][i]
                    df_call.loc[i, '저가'] = df['저가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(저가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_call.setItem(i, Option_column.저가.value, item)

                    고가 = df['고가'][i]
                    df_call.loc[i, '고가'] = df['고가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(고가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_call.setItem(i, Option_column.고가.value, item)

                    if overnight:

                        if 저가 < 고가:

                            call_open[i] = True
                            self.tableWidget_call.item(i, Option_column.행사가.value).setBackground(QBrush(라임))
                        else:
                            pass
                    else:
                        pass

                    진폭 = 고가 - 저가
                    df_call.loc[i, '진폭'] = 진폭

                    item = QTableWidgetItem("{0:0.2f}".format(진폭))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.진폭.value, item)
                    
                    if 시가 > opt_search_start_value and 저가 < 고가:

                        call_open_list.append(i)
                    else:
                        pass

                    if 시가 > 0:

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)

                        if 시가 > 종가:
                            item.setForeground(QBrush(적색))
                        elif 시가 < 종가:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))

                        self.tableWidget_call.setItem(i, Option_column.시가.value, item)

                        if 시가 in 진성맥점:

                            self.tableWidget_call.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                            self.tableWidget_call.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                        else:
                            pass

                        df_plotdata_call.iloc[i][선물장간_시간차] = 시가

                        시가갭 = 시가 - 종가
                        df_call.loc[i, '시가갭'] = 시가갭

                        대비 = round((현재가 - 시가), 2)
                        df_call.loc[i, '대비'] = 대비

                        if 시가 > 0 and 저가 < 고가:

                            call_gap_percent[i] = (시가 / 종가 - 1) * 100

                            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(시가갭, call_gap_percent[i])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.시가갭.value, item)

                            call_db_percent[i] = (현재가 / 시가 - 1) * 100

                            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(대비, call_db_percent[i])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.대비.value, item)
                        else:
                            gap_str = "{0:0.2f}".format(시가갭)

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.시가갭.value, item)

                            gap_str = "{0:0.2f}".format(대비)

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.대비.value, item)

                        피봇 = self.calc_pivot(전저, 전고, 종가, 시가)
                        df_call.loc[i, '피봇'] = 피봇

                        item = QTableWidgetItem("{0:0.2f}".format(피봇))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.피봇.value, item)
                    else:
                        시가 = 0.0
                        피봇 = 0.0
                        시가갭 = 0.0
                        대비 = 0

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.시가.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(피봇))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.피봇.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(시가갭))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.시가갭.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(대비))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.대비.value, item)

                        self.tableWidget_call.item(i, Option_column.행사가.value).setBackground(QBrush(흰색))
                        self.tableWidget_call.item(i, Option_column.행사가.value).setForeground(QBrush(검정색))

                    df_call.loc[i, '피봇'] = 피봇

                    if 시가 > 0 and 저가 < 고가:
                        self.tableWidget_call.item(i, Option_column.행사가.value).setBackground(QBrush(라임))
                        self.tableWidget_call.item(i, Option_column.행사가.value).setForeground(QBrush(검정색))
                    else:
                        pass

                    if df['현재가'][i] <= 시가갭:

                        수정거래량 = int((df['매수잔량'][i] - df['매도잔량'][i]) * df['현재가'][i])
                    else:

                        수정거래량 = int((df['매수잔량'][i] - df['매도잔량'][i]) * (df['현재가'][i] - 시가갭))

                    # 수정거래량 초기화
                    df_call.loc[i, '수정거래량'] = 0

                    # t2835에 미결항목이 없음                    
                    df_call.loc[i, '순미결'] = 0
                    df_call.loc[i, '수정미결'] = 0
                    df_call.loc[i, '수정미결증감'] = 0

                    temp = format(0, ',')

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.VP.value, item)
                    
                    temp = format(0, ',')

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.OI.value, item)

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.OID.value, item)

                    df_plotdata_call_volume.iloc[0][0] = 0
                    df_plotdata_call_volume.iloc[0][선물장간_시간차] = 0

                    # Put 처리
                    #df_put.loc[i, '수정거래량'] = 0
                    df_put.loc[i, '시가갭'] = 0
                    df_put.loc[i, '대비'] = 0

                    self.tableWidget_put.item(i, Option_column.행사가.value).setBackground(QBrush(흰색))

                    item = QTableWidgetItem(oloh_str)
                    item.setBackground(QBrush(흰색))
                    item.setForeground(QBrush(검정색))
                    self.tableWidget_put.setItem(i, Option_column.OLOH.value, item)

                    전저 = df_put.iloc[i]['저가']
                    df_put.loc[i, '전저'] = 전저

                    item = QTableWidgetItem("{0:0.2f}".format(전저))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.전저.value, item)

                    전고 = df_put.iloc[i]['고가']
                    df_put.loc[i, '전고'] = 전고

                    item = QTableWidgetItem("{0:0.2f}".format(전고))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.전고.value, item)

                    if 18 <= dt.hour < 24 or 0 <= dt.hour < 4:
                        
                        시가 = df1['시가'][i]
                    else:
                        시가 = 0.0

                    df_put.loc[i, '시가'] = 시가

                    종가 = df_put.iloc[i]['현재가']
                    df_put.loc[i, '종가'] = 종가

                    item = QTableWidgetItem("{0:0.2f}".format(종가))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.종가.value, item)

                    df_plotdata_put.iloc[i][0] = 종가

                    현재가 = df1['현재가'][i]
                    df_put.loc[i, '현재가'] = 현재가

                    item = QTableWidgetItem("{0:0.2f}".format(현재가))
                    item.setTextAlignment(Qt.AlignCenter)                    
                    #item.setBackground(QBrush(옅은회색))

                    if 시가 > 0:

                        if 시가 < 현재가:
                            item.setForeground(QBrush(적색))
                        elif 시가 > 현재가:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))
                    else:
                        item.setForeground(QBrush(검정색))

                    self.tableWidget_put.setItem(i, Option_column.현재가.value, item)

                    저가 = df1['저가'][i]
                    df_put.loc[i, '저가'] = df1['저가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(저가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_put.setItem(i, Option_column.저가.value, item)

                    고가 = df1['고가'][i]
                    df_put.loc[i, '고가'] = df1['고가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(고가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_put.setItem(i, Option_column.고가.value, item)

                    if overnight:

                        if 저가 < 고가:

                            put_open[i] = True
                            self.tableWidget_put.item(i, Option_column.행사가.value).setBackground(QBrush(라임))
                        else:
                            pass
                    else:
                        pass

                    진폭 = 고가 - 저가
                    df_put.loc[i, '진폭'] = 진폭

                    item = QTableWidgetItem("{0:0.2f}".format(진폭))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.진폭.value, item)
                    
                    if 시가 > opt_search_start_value and 저가 < 고가:

                        put_open_list.append(i)
                    else:
                        pass

                    if 시가 > 0:

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)

                        if 시가 > 종가:
                            item.setForeground(QBrush(적색))
                        elif 시가 < 종가:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))

                        self.tableWidget_put.setItem(i, Option_column.시가.value, item)

                        if 시가 in 진성맥점:

                            self.tableWidget_put.item(i, Option_column.시가.value).setBackground(QBrush(대맥점색))
                            self.tableWidget_put.item(i, Option_column.시가.value).setForeground(QBrush(검정색))
                        else:
                            pass

                        df_plotdata_put.iloc[i][선물장간_시간차] = 시가

                        시가갭 = 시가 - 종가
                        df_put.loc[i, '시가갭'] = 시가갭

                        대비 = round((현재가 - 시가), 2)
                        df_put.loc[i, '대비'] = 대비

                        if 시가 > 0 and 저가 < 고가:

                            put_gap_percent[i] = (시가 / 종가 - 1) * 100

                            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(시가갭, put_gap_percent[i])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.시가갭.value, item)

                            put_db_percent[i] = (현재가 / 시가 - 1) * 100

                            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(대비, put_db_percent[i])

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.대비.value, item)
                        else:
                            gap_str = "{0:0.2f}".format(시가갭)

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.시가갭.value, item)

                            gap_str = "{0:0.2f}".format(대비)

                            item = QTableWidgetItem(gap_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.대비.value, item)

                        피봇 = self.calc_pivot(전저, 전고, 종가, 시가)
                        df_put.loc[i, '피봇'] = 피봇

                        item = QTableWidgetItem("{0:0.2f}".format(피봇))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.피봇.value, item)
                    else:
                        시가 = 0.0
                        피봇 = 0.0
                        시가갭 = 0.0
                        대비 = 0

                        item = QTableWidgetItem("{0:0.2f}".format(시가))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.시가.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(피봇))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.피봇.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(시가갭))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.시가갭.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(대비))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.대비.value, item)

                        self.tableWidget_put.item(i, Option_column.행사가.value).setBackground(QBrush(흰색))
                        self.tableWidget_put.item(i, Option_column.행사가.value).setForeground(QBrush(검정색))

                    df_put.loc[i, '피봇'] = 피봇

                    if 시가 > 0 and 저가 < 고가:
                        self.tableWidget_put.item(i, Option_column.행사가.value).setBackground(QBrush(라임))
                        self.tableWidget_put.item(i, Option_column.행사가.value).setForeground(QBrush(검정색))
                    else:
                        pass

                    if df1['현재가'][i] <= 시가갭:

                        수정거래량 = int((df1['매수잔량'][i] - df1['매도잔량'][i]) * df1['현재가'][i])
                    else:

                        수정거래량 = int((df1['매수잔량'][i] - df1['매도잔량'][i]) * (df1['현재가'][i] - 시가갭))

                    # 수정거래량 초기화
                    df_put.loc[i, '수정거래량'] = 0

                    # t2835에 미결항목이 없음
                    df_put.loc[i, '순미결'] = 0
                    df_put.loc[i, '수정미결'] = 0
                    df_put.loc[i, '수정미결증감'] = 0

                    temp = format(0, ',')

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.VP.value, item)

                    temp = format(0, ',')

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.OI.value, item)

                    item = QTableWidgetItem(temp)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.OID.value, item)

                    df_plotdata_put_volume.iloc[0][0] = 0
                    df_plotdata_volume_cha.iloc[0][0] = 0

                    df_plotdata_put_volume.iloc[0][선물장간_시간차] = 0
                    df_plotdata_volume_cha.iloc[0][선물장간_시간차] = 0
                
                print('\r')
                print('t2835 야간 전광판 콜 데이타 = ', df_call)
                print('\r')
                print('t2835 야간 전광판 풋 데이타 = ', df_put)
                print('\r')
                print('t2835 call open list = ', call_open_list, len(call_open_list))
                print('\r')
                print('t2835 put open list = ', put_open_list, len(put_open_list))
                print('\r')

                print('대비합 초기화 전...', round(df_call['대비'].sum(), 2), round(df_put['대비'].sum(), 2))

                '''
                for i in range(option_pairs_count):

                    # 대비 초기화
                    df_call.loc[i, '대비'] = 0
                    df_put.loc[i, '대비'] = 0

                print('대비합 초기화 후...', round(df_call['대비'].sum(), 2), round(df_put['대비'].sum(), 2))
                '''

                self.tableWidget_call.item(atm_index, Option_column.행사가.value).setBackground(QBrush(노란색))
                self.tableWidget_call.item(atm_index, Option_column.행사가.value).setForeground(QBrush(검정색))
                self.tableWidget_put.item(atm_index, Option_column.행사가.value).setBackground(QBrush(노란색))
                self.tableWidget_put.item(atm_index, Option_column.행사가.value).setForeground(QBrush(검정색))
                
                call_atm_value = df_call.iloc[atm_index]['현재가']
                put_atm_value = df_put.iloc[atm_index]['현재가']

                str = '{0:0.2f}({1:0.2f}:{2:0.2f})'.format(
                    fut_realdata['현재가'] - fut_realdata['KP200'],
                    call_atm_value + put_atm_value,
                    abs(call_atm_value - put_atm_value))
                self.label_atm.setText(str)             

                call_전저 = df_call['전저'].values.tolist()
                call_전저_node_list = self.make_node_list(call_전저)

                call_전고 = df_call['전고'].values.tolist()
                call_전고_node_list = self.make_node_list(call_전고)

                call_종가 = df_call['종가'].values.tolist()
                call_종가_node_list = self.make_node_list(call_종가)
                
                call_피봇 = df_call['피봇'].values.tolist()
                call_피봇_node_list = self.make_node_list(call_피봇)

                call_시가 = df_call['시가'].values.tolist()
                call_시가_node_list = self.make_node_list(call_시가)

                call_저가 = df_call['저가'].values.tolist()
                call_저가_node_list = self.make_node_list(call_저가)

                call_고가 = df_call['고가'].values.tolist()
                call_고가_node_list = self.make_node_list(call_고가)

                call_진폭 = df_call['진폭'].values.tolist()
                진폭최대값 = max(call_진폭)
                max_str = '{0:0.2f}'.format(진폭최대값)

                item = QTableWidgetItem(max_str)
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.진폭.value, item)

                put_전저 = df_put['전저'].values.tolist()
                put_전저_node_list = self.make_node_list(put_전저)

                put_전고 = df_put['전고'].values.tolist()
                put_전고_node_list = self.make_node_list(put_전고)

                put_종가 = df_put['종가'].values.tolist()
                put_종가_node_list = self.make_node_list(put_종가)
                
                put_피봇 = df_put['피봇'].values.tolist()
                put_피봇_node_list = self.make_node_list(put_피봇)

                put_시가 = df_put['시가'].values.tolist()
                put_시가_node_list = self.make_node_list(put_시가)

                put_저가 = df_put['저가'].values.tolist()
                put_저가_node_list = self.make_node_list(put_저가)

                put_고가 = df_put['고가'].values.tolist()
                put_고가_node_list = self.make_node_list(put_고가)

                put_진폭 = df_put['진폭'].values.tolist()
                진폭최대값 = max(put_진폭)
                max_str = '{0:0.2f}'.format(진폭최대값)

                item = QTableWidgetItem(max_str)
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.진폭.value, item)

                # 실시간테이타 요청                
                str = '[{0:02d}:{1:02d}:{2:02d}] 야간 실시간데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                self.textBrowser.append(str)

                self.OPT_REAL = EC0(parent=self)

                for i in range(option_pairs_count):
                    self.OPT_REAL.AdviseRealData(call_code[i])
                    self.OPT_REAL.AdviseRealData(put_code[i]) 

                self.OPT_HO = EH0(parent=self)

                for i in range(option_pairs_count):
                    self.OPT_HO.AdviseRealData(call_code[i])
                    self.OPT_HO.AdviseRealData(put_code[i]) 

                self.FUT_REAL = NC0(parent=self)
                self.FUT_REAL.AdviseRealData(fut_code)

                self.FUT_HO = NH0(parent=self)                
                self.FUT_HO.AdviseRealData(fut_code)

                # 업종별 투자자별 매매현황 요청
                self.BM.AdviseRealData(CME)
                
                str = '[{0:02d}:{1:02d}:{2:02d}] Screen Update 쓰레드가 시작됩니다.\r'.format(dt.hour, dt.minute, dt.second)
                self.textBrowser.append(str)
                print(str)
                
                self.screen_update_worker.start()
                self.screen_update_worker.daemon = True
                
                refresh_flag = True

                self.pushButton_add.setStyleSheet("background-color: lawngreen")
                self.pushButton_add.setText('Refresh')       
                
            else:
                # Refresh
                str = '[{0:02d}:{1:02d}:{2:02d}] 야간옵션 전광판을 갱신합니다.\r'.format(dt.hour, dt.minute, dt.second)
                self.textBrowser.append(str)

                del call_open_list[:]
                del put_open_list[:]

                for i in range(option_pairs_count):

                    # 콜 데이타 획득
                    종가 = df_call.iloc[i]['종가']

                    시가 = df['시가'][i]
                    df_call.loc[i, '시가'] = df['시가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(시가))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(i, Option_column.시가.value, item)

                    if 시가 > 0:

                        시가갭 = 시가 - 종가
                        df_call.loc[i, '시가갭'] = 시가갭

                        피봇 = self.calc_pivot(df_call.iloc[i]['전저'], df_call.iloc[i]['전고'], 종가, 시가)
                        df_call.loc[i, '피봇'] = 피봇

                        item = QTableWidgetItem("{0:0.2f}".format(피봇))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(i, Option_column.피봇.value, item)
                    else:
                        시가갭 = 0
                        df_call.loc[i, '시가갭'] = 시가갭

                    현재가 = df['현재가'][i]
                    df_call.loc[i, '현재가'] = 현재가

                    item = QTableWidgetItem("{0:0.2f}".format(현재가))
                    item.setTextAlignment(Qt.AlignCenter)                    
                    #item.setBackground(QBrush(옅은회색))

                    if 시가 > 0:

                        if 시가 < 현재가:
                            item.setForeground(QBrush(적색))
                        elif 시가 > 현재가:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))
                    else:
                        item.setForeground(QBrush(검정색))

                    self.tableWidget_call.setItem(i, Option_column.현재가.value, item)

                    저가 = df['저가'][i]
                    df_call.loc[i, '저가'] = df['저가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(저가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_call.setItem(i, Option_column.저가.value, item)

                    고가 = df['고가'][i]
                    df_call.loc[i, '고가'] = df['고가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(고가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_call.setItem(i, Option_column.고가.value, item)
                    
                    if 시가 > 0 and 저가 < 고가:

                        call_open_list.append(i)
                    else:
                        pass

                    # 풋 데이타 획득
                    종가 = df_put.iloc[i]['종가']

                    시가 = df1['시가'][i]
                    df_put.loc[i, '시가'] = df1['시가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(시가))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(i, Option_column.시가.value, item)

                    if 시가 > 0:

                        시가갭 = 시가 - 종가
                        df_put.loc[i, '시가갭'] = 시가갭

                        피봇 = self.calc_pivot(df_put.iloc[i]['전저'], df_put.iloc[i]['전고'], 종가, 시가)
                        df_put.loc[i, '피봇'] = 피봇

                        item = QTableWidgetItem("{0:0.2f}".format(피봇))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(i, Option_column.피봇.value, item)
                    else:
                        시가갭 = 0
                        df_put.loc[i, '시가갭'] = 시가갭

                    현재가 = df1['현재가'][i]
                    df_put.loc[i, '현재가'] = 현재가

                    item = QTableWidgetItem("{0:0.2f}".format(현재가))
                    item.setTextAlignment(Qt.AlignCenter)                    
                    #item.setBackground(QBrush(옅은회색))

                    if 시가 > 0:

                        if 시가 < 현재가:
                            item.setForeground(QBrush(적색))
                        elif 시가 > 현재가:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))
                    else:
                        item.setForeground(QBrush(검정색))

                    self.tableWidget_put.setItem(i, Option_column.현재가.value, item)
                    
                    저가 = df1['저가'][i]
                    df_put.loc[i, '저가'] = df1['저가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(저가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_put.setItem(i, Option_column.저가.value, item)

                    고가 = df1['고가'][i]
                    df_put.loc[i, '고가'] = df1['고가'][i]

                    item = QTableWidgetItem("{0:0.2f}".format(고가))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(옅은회색))
                    self.tableWidget_put.setItem(i, Option_column.고가.value, item)
                    
                    if 시가 > 0 and 저가 < 고가:

                        put_open_list.append(i)
                    else:
                        pass

                # Node 리스트 갱신
                call_시가 = df_call['시가'].values.tolist()
                call_시가_node_list = self.make_node_list(call_시가)

                call_피봇 = df_call['피봇'].values.tolist()
                call_피봇_node_list = self.make_node_list(call_피봇)

                call_저가 = df_call['저가'].values.tolist()
                call_저가_node_list = self.make_node_list(call_저가)

                call_고가 = df_call['고가'].values.tolist()
                call_고가_node_list = self.make_node_list(call_고가)

                put_시가 = df_put['시가'].values.tolist()
                put_시가_node_list = self.make_node_list(put_시가)

                put_피봇 = df_put['피봇'].values.tolist()
                put_피봇_node_list = self.make_node_list(put_피봇)

                put_저가 = df_put['저가'].values.tolist()
                put_저가_node_list = self.make_node_list(put_저가)

                put_고가 = df_put['고가'].values.tolist()
                put_고가_node_list = self.make_node_list(put_고가)  
                        
            self.tableWidget_call.resizeColumnsToContents()
            self.tableWidget_put.resizeColumnsToContents()

            # 주야간 선물전광판 데이타 요청
            XQ = t2101(parent=self)
            XQ.Query(종목코드=fut_code)
            print('t2101 요청')

            time.sleep(0.1)

            XQ = t2801(parent=self)
            XQ.Query(종목코드=fut_code)
            print('t2801 요청')

            time.sleep(0.1)

        elif szTrCode == 't8408':

            df = result

            print('\r')
            print('[t8408 cme data]')
            print('\r')
            print(df)
            print('\r')

            temp = df['현재가'].values.tolist()
            temp.reverse()
            temp1 = copy.deepcopy(temp)

            CME_전일종가 = temp1[1::2]
            
            print('[CME_전일종가] = \r', CME_전일종가)
            print('\r')

            str = '[{0:02d}:{1:02d}:{2:02d}] 야간선물 전일데이타 수신완료 !!!\r'.format(dt.hour, dt.minute, dt.second)
            self.textBrowser.append(str)           

        elif szTrCode == 't8415':

            block, df = result

            if block['단축코드'][0:3] == '101':

                print('\r')
                print('[t8415 fut block]')
                print('\r')
                print(block)
                print('\r')
                print('[t8415 fut data]')
                print('\r')
                print(df)
                print('\r')

                # 전일 장종료 전 1시간 데이타(60개)
                temp = df['저가'].values.tolist()
                선물_전일저가 = temp[440:]

                temp = df['고가'].values.tolist()
                선물_전일고가 = temp[440:]

                temp = df['종가'].values.tolist()
                선물_전일종가 = temp[440:]

                str = '[{0:02d}:{1:02d}:{2:02d}] 선물 전일데이타 수신완료 !!!\r'.format(dt.hour, dt.minute, dt.second)
                self.textBrowser.append(str)

            elif block['단축코드'][0:3] == '201':

                for i in range(len(selected_call)):

                    if result['단축코드'][5:8] == df_call.iloc[selected_call[i]]['행사가']:

                        pass
                    else:
                        pass

            elif block['단축코드'][0:3] == '301':

                for i in range(len(selected_put)):

                    if result['단축코드'][5:8] == df_put.iloc[selected_put[i]]['행사가']:

                        pass
                    else:
                        pass
            else:
                pass

        elif szTrCode == 't8416':

            block, df = result

            dt = datetime.datetime.now()
            current_str = dt.strftime('%H:%M:%S')

            global call_t8416_count, put_t8416_count
            global new_actval_up_count, new_actval_down_count, actval_increased

            str = '{0:02d}:{1:02d}:{2:02d}'.format(dt.hour, dt.minute, dt.second)
            self.label_msg.setText(str)

            if new_actval_up_count == 0 and new_actval_down_count == 0:

                item_str = '{0:d}'.format(option_pairs_count)
                item = QTableWidgetItem(item_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setHorizontalHeaderItem(0, item)
                self.tableWidget_call.resizeColumnsToContents()

                item_str = '{0:d}'.format(option_pairs_count)
                item = QTableWidgetItem(item_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setHorizontalHeaderItem(0, item) 
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass

            if block['단축코드'] == '':

                actval_increased = True

                if call_t8416_count == 0:

                    new_actval_up_count += 1
                    call_t8416_count += 1

                    str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 상방 행사가 {3}개 추가됨 !!!\r'.format(dt.hour, dt.minute, dt.second, new_actval_up_count)
                    #self.textBrowser.append(str)
                    print(str) 

                    # 추가된 행사가 갯수 표시
                    item_str = '+' + '{0:d}'.format(new_actval_up_count) + '\n' + '({0:d})'.format(option_pairs_count)
                    item = QTableWidgetItem(item_str)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setHorizontalHeaderItem(0, item)
                    self.tableWidget_call.resizeColumnsToContents()

                    item_str = '+' + '{0:d}'.format(new_actval_up_count) + '\n' + '({0:d})'.format(option_pairs_count)
                    item = QTableWidgetItem(item_str)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setHorizontalHeaderItem(0, item)
                    self.tableWidget_put.resizeColumnsToContents()
                else:
                    pass

                if new_actval_up_count == 0 and put_t8416_count == 0:

                    new_actval_down_count += 1 

                    str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 하방 행사가 {3}개 추가됨 !!!\r'.format(dt.hour, dt.minute, dt.second, new_actval_down_count)
                    #self.textBrowser.append(str) 
                    print(str)  

                    # 추가된 행사가 갯수 표시
                    item_str = '+' + '{0:d}'.format(new_actval_down_count) + '\n' + '({0:d})'.format(option_pairs_count)
                    item = QTableWidgetItem(item_str)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setHorizontalHeaderItem(0, item)
                    self.tableWidget_call.resizeColumnsToContents()

                    item_str = '+' + '{0:d}'.format(new_actval_down_count) + '\n' + '({0:d})'.format(option_pairs_count)
                    item = QTableWidgetItem(item_str)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setHorizontalHeaderItem(0, item)                    
                    self.tableWidget_put.resizeColumnsToContents()                  

                    if call_t8416_count == option_pairs_count - new_actval_down_count:

                        if self.t8416_callworker.isRunning():

                            call_기준가 = df_call['기준가'].values.tolist()
                            call_월저 = df_call['월저'].values.tolist()
                            call_월고 = df_call['월고'].values.tolist()
                            call_전저 = df_call['전저'].values.tolist()
                            call_전고 = df_call['전고'].values.tolist()
                            call_종가 = df_call['종가'].values.tolist()
                            call_피봇 = df_call['피봇'].values.tolist()
                            call_시가 = df_call['시가'].values.tolist()
                            call_저가 = df_call['저가'].values.tolist()
                            call_고가 = df_call['고가'].values.tolist()

                            call_기준가_node_list = self.make_node_list(call_기준가)
                            call_월저_node_list = self.make_node_list(call_월저)
                            call_월고_node_list = self.make_node_list(call_월고)
                            call_전저_node_list = self.make_node_list(call_전저)
                            call_전고_node_list = self.make_node_list(call_전고)
                            call_종가_node_list = self.make_node_list(call_종가)
                            call_피봇_node_list = self.make_node_list(call_피봇)
                            call_시가_node_list = self.make_node_list(call_시가)
                            call_저가_node_list = self.make_node_list(call_저가)
                            call_고가_node_list = self.make_node_list(call_고가)

                            print('Call 과거데이타 수신완료')

                            self.t8416_callworker.terminate()
                            str = '[{0:02d}:{1:02d}:{2:02d}] Call 과거데이타 수신완료 !!!\r'.format(dt.hour, dt.minute, dt.second)
                            self.textBrowser.append(str)                            

                            call_positionCell = self.tableWidget_call.item(atm_index + 3, 1)
                            self.tableWidget_call.scrollToItem(call_positionCell)

                            time.sleep(1.1)

                            self.t8416_putworker.start()
                            self.t8416_putworker.daemon = True
                        else:
                            pass
                    else:
                        pass                    
                else:
                    pass
                 
                '''
                if not actval_increased:

                    actval_increased = True

                    call_t8416_count += 1                

                    print('call_t8416_count =', call_t8416_count) 

                    if call_t8416_count == option_pairs_count:

                        if self.t8416_callworker.isRunning():

                            call_기준가 = df_call['기준가'].values.tolist()
                            call_월저 = df_call['월저'].values.tolist()
                            call_월고 = df_call['월고'].values.tolist()
                            call_전저 = df_call['전저'].values.tolist()
                            call_전고 = df_call['전고'].values.tolist()
                            call_종가 = df_call['종가'].values.tolist()
                            call_피봇 = df_call['피봇'].values.tolist()
                            call_시가 = df_call['시가'].values.tolist()
                            call_저가 = df_call['저가'].values.tolist()
                            call_고가 = df_call['고가'].values.tolist()

                            call_기준가_node_list = self.make_node_list(call_기준가)
                            call_월저_node_list = self.make_node_list(call_월저)
                            call_월고_node_list = self.make_node_list(call_월고)
                            call_전저_node_list = self.make_node_list(call_전저)
                            call_전고_node_list = self.make_node_list(call_전고)
                            call_종가_node_list = self.make_node_list(call_종가)
                            call_피봇_node_list = self.make_node_list(call_피봇)
                            call_시가_node_list = self.make_node_list(call_시가)
                            call_저가_node_list = self.make_node_list(call_저가)
                            call_고가_node_list = self.make_node_list(call_고가)

                            print('Call 과거데이타 수신완료')

                            self.t8416_callworker.terminate()
                            str = '[{0:02d}:{1:02d}:{2:02d}] Call 과거데이타 수신완료 !!!\r'.format(dt.hour, dt.minute, dt.second)
                            self.textBrowser.append(str)                        

                            self.tableWidget_call.resizeColumnsToContents()

                            call_positionCell = self.tableWidget_call.item(atm_index + 3, 1)
                            self.tableWidget_call.scrollToItem(call_positionCell)

                            time.sleep(1.1)

                            self.t8416_putworker.start()
                            self.t8416_putworker.daemon = True
                        else:
                            pass
                    else:
                        pass           
                else:
                    pass                   
                
                if call_t8416_count == option_pairs_count:
                    put_t8416_count += 1
                else:
                    call_t8416_count += 1
                    #put_t8416_count += 1

                    new_actval_count += 1 

                    print('new_actval_count =', new_actval_count)

                    # 추가된 행사가 갯수 표시
                    item_str = '+' + '{0:d}'.format(new_actval_count) + '\n' + '({0:d})'.format(option_pairs_count)
                    item = QTableWidgetItem(item_str)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setHorizontalHeaderItem(0, item)

                    item_str = '+' + '{0:d}'.format(new_actval_count) + '\n' + '({0:d})'.format(option_pairs_count)
                    item = QTableWidgetItem(item_str)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setHorizontalHeaderItem(0, item) 
                '''              
            else:
                pass
            
            if block['단축코드'][0:3] == '101':

                if not overnight:

                    item = QTableWidgetItem("{0:0.2f}".format(block['전일저가']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_fut.setItem(1, Futures_column.전저.value, item)

                    item = QTableWidgetItem("{0:0.2f}".format(block['전일고가']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_fut.setItem(1, Futures_column.전고.value, item)

                    if int(current_str[0:2]) == 8 and int(current_str[3:5]) <= 59:
                        item = QTableWidgetItem("{0:0.2f}".format(block['전일종가']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_fut.setItem(1, Futures_column.종가.value, item)
                    else:
                        pass

                    self.tableWidget_fut.resizeColumnsToContents()
                else:
                    pass

            elif block['단축코드'][0:3] == '201':

                if new_actval_up_count > 0:

                    str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 상방 행사가 {3}개 추가됨 !!!\r'.format(dt.hour, dt.minute, dt.second, new_actval_up_count)
                    #self.textBrowser.append(str)
                    print(str)
                else:
                    pass

                if today_str != MONTH_FIRSTDAY:

                    df_call.loc[call_t8416_count, '기준가'] = round(df['저가'][0], 2)
                    item = QTableWidgetItem("{0:0.2f}".format(df['저가'][0]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(call_t8416_count, Option_column.기준가.value, item)

                    df_call.loc[call_t8416_count, '월저'] = round(min(df['저가']), 2)
                    item = QTableWidgetItem("{0:0.2f}".format(min(df['저가'])))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(call_t8416_count, Option_column.월저.value, item)

                    df_call.loc[call_t8416_count, '월고'] = round(max(df['고가']), 2)
                    item = QTableWidgetItem("{0:0.2f}".format(max(df['고가'])))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(call_t8416_count, Option_column.월고.value, item)
                else:
                    pass

                df_call.loc[call_t8416_count, '전저'] = round(block['전일저가'], 2)
                item = QTableWidgetItem("{0:0.2f}".format(df_call.iloc[call_t8416_count]['전저']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setItem(call_t8416_count, Option_column.전저.value, item)

                df_call.loc[call_t8416_count, '전고'] = round(block['전일고가'], 2)
                item = QTableWidgetItem("{0:0.2f}".format(df_call.iloc[call_t8416_count]['전고']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setItem(call_t8416_count, Option_column.전고.value, item)

                if round(block['전일종가'], 2) != df_call.iloc[call_t8416_count]['종가']:

                    df_call.loc[call_t8416_count, '종가'] = round(block['전일종가'], 2)
                    item = QTableWidgetItem("{0:0.2f}".format(df_call.iloc[call_t8416_count]['종가']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_call.setItem(call_t8416_count, Option_column.종가.value, item)

                    df_plotdata_call.iloc[call_t8416_count][0] = round(block['전일종가'], 2)

                    #str = '[{0:02d}:{1:02d}:{2:02d}] t2301과 t8416의 콜[{3}] 종가가 상이합니다. !!!\r'.format(dt.hour, dt.minute, dt.second, call_t8416_count + 1)
                    #self.textBrowser.append(str)
                else:
                    pass

                if not pre_start:

                    if df_call.iloc[call_t8416_count]['시가'] > 0: 

                        피봇 = self.calc_pivot(df_call.iloc[call_t8416_count]['전저'],
                            df_call.iloc[call_t8416_count]['전고'],
                            df_call.iloc[call_t8416_count]['종가'],
                            df_call.iloc[call_t8416_count]['시가'])

                        df_call.loc[call_t8416_count, '피봇'] = round(피봇, 2)

                        item = QTableWidgetItem("{0:0.2f}".format(df_call.iloc[call_t8416_count]['피봇']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(call_t8416_count, Option_column.피봇.value, item)

                        temp = df_call.iloc[call_t8416_count]['시가'] - df_call.iloc[call_t8416_count]['종가']

                        df_call.loc[call_t8416_count, '시가갭'] = round(temp, 2)

                        if df_call.iloc[call_t8416_count]['종가'] > 0:

                            gap_percent = int((df_call.iloc[call_t8416_count]['시가'] /
                                               df_call.iloc[call_t8416_count]['종가'] - 1) * 100)

                            item = QTableWidgetItem(
                                "{0:0.2f}\n({1}%)".format(df_call.iloc[call_t8416_count]['시가갭'], gap_percent))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(call_t8416_count, Option_column.시가갭.value, item)
                        else:
                            pass

                        temp = round((df_call.iloc[call_t8416_count]['현재가'] -
                                      df_call.iloc[call_t8416_count]['시가']), 2) * 1

                        df_call.loc[call_t8416_count, '대비'] = int(temp)

                        item = QTableWidgetItem("{0:0.2f}".format(df_call.iloc[call_t8416_count]['대비']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(call_t8416_count, Option_column.대비.value, item)

                        df_call.loc[call_t8416_count, '진폭'] = df_call.iloc[call_t8416_count]['고가'] - \
                                                                    df_call.iloc[call_t8416_count]['저가']

                        item = QTableWidgetItem("{0:0.2f}".format(df_call.iloc[call_t8416_count]['진폭']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(call_t8416_count, Option_column.진폭.value, item)
                    else:
                        pass
                else:
                    pass

                str = '[{0:02d}:{1:02d}:{2:02d}] Call 행사가 {3}개중 {4}번째 Packet을 수신했습니다.\r'.\
                    format(dt.hour, dt.minute, dt.second, option_pairs_count, call_t8416_count + 1)

                self.textBrowser.append(str)

                call_t8416_count += 1

                print('Call 과거데이타 %d 개중 %d개 수신...' % (option_pairs_count, call_t8416_count))
                
                # to be checked !!!
                if call_t8416_count == option_pairs_count:

                    if self.t8416_callworker.isRunning():

                        call_기준가 = df_call['기준가'].values.tolist()
                        call_월저 = df_call['월저'].values.tolist()
                        call_월고 = df_call['월고'].values.tolist()
                        call_전저 = df_call['전저'].values.tolist()
                        call_전고 = df_call['전고'].values.tolist()
                        call_종가 = df_call['종가'].values.tolist()
                        call_피봇 = df_call['피봇'].values.tolist()
                        call_시가 = df_call['시가'].values.tolist()
                        call_저가 = df_call['저가'].values.tolist()
                        call_고가 = df_call['고가'].values.tolist()

                        call_기준가_node_list = self.make_node_list(call_기준가)
                        call_월저_node_list = self.make_node_list(call_월저)
                        call_월고_node_list = self.make_node_list(call_월고)
                        call_전저_node_list = self.make_node_list(call_전저)
                        call_전고_node_list = self.make_node_list(call_전고)
                        call_종가_node_list = self.make_node_list(call_종가)
                        call_피봇_node_list = self.make_node_list(call_피봇)
                        call_시가_node_list = self.make_node_list(call_시가)
                        call_저가_node_list = self.make_node_list(call_저가)
                        call_고가_node_list = self.make_node_list(call_고가)

                        print('Call 과거데이타 수신완료')

                        self.t8416_callworker.terminate()
                        str = '[{0:02d}:{1:02d}:{2:02d}] Call 과거데이타 수신완료 !!!\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)                        

                        self.tableWidget_call.resizeColumnsToContents()

                        call_positionCell = self.tableWidget_call.item(atm_index + 3, 1)
                        self.tableWidget_call.scrollToItem(call_positionCell)

                        time.sleep(1.1)

                        self.t8416_putworker.start()
                        self.t8416_putworker.daemon = True
                    else:
                        pass
                else:
                    pass
                
            elif block['단축코드'][0:3] == '301':

                if new_actval_down_count > 0:

                    str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 하방 행사가 {3}개 추가됨 !!!\r'.format(dt.hour, dt.minute, dt.second, new_actval_down_count)
                    #self.textBrowser.append(str)
                    print(str)
                else:
                    pass

                if today_str != MONTH_FIRSTDAY:

                    df_put.loc[put_t8416_count, '기준가'] = round(df['저가'][0], 2)
                    item = QTableWidgetItem("{0:0.2f}".format(df['저가'][0]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(put_t8416_count, Option_column.기준가.value, item)

                    df_put.loc[put_t8416_count, '월저'] = round(min(df['저가']), 2)
                    item = QTableWidgetItem("{0:0.2f}".format(min(df['저가'])))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(put_t8416_count, Option_column.월저.value, item)

                    df_put.loc[put_t8416_count, '월고'] = round(max(df['고가']), 2)
                    item = QTableWidgetItem("{0:0.2f}".format(max(df['고가'])))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(put_t8416_count, Option_column.월고.value, item)
                else:
                    pass                

                df_put.loc[put_t8416_count, '전저'] = round(block['전일저가'], 2)
                item = QTableWidgetItem("{0:0.2f}".format(df_put.iloc[put_t8416_count]['전저']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setItem(put_t8416_count, Option_column.전저.value, item)

                df_put.loc[put_t8416_count, '전고'] = round(block['전일고가'], 2)
                item = QTableWidgetItem("{0:0.2f}".format(df_put.iloc[put_t8416_count]['전고']))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setItem(put_t8416_count, Option_column.전고.value, item)

                if round(block['전일종가'], 2) != df_put.iloc[put_t8416_count]['종가']:

                    df_put.loc[put_t8416_count, '종가'] = round(block['전일종가'], 2)
                    item = QTableWidgetItem("{0:0.2f}".format(df_put.iloc[put_t8416_count]['종가']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_put.setItem(put_t8416_count, Option_column.종가.value, item)

                    df_plotdata_put.iloc[put_t8416_count][0] = round(block['전일종가'], 2)

                    #str = '[{0:02d}:{1:02d}:{2:02d}] t2301과 t8416의 풋[{3}] 종가가 상이합니다. !!!\r'.format(dt.hour, dt.minute, dt.second, put_t8416_count + 1)
                    #self.textBrowser.append(str)
                else:
                    pass
                
                if not pre_start:

                    if df_put.iloc[put_t8416_count]['시가'] > 0:

                        피봇 = self.calc_pivot(df_put.iloc[put_t8416_count]['전저'],
                            df_put.iloc[put_t8416_count]['전고'],
                            df_put.iloc[put_t8416_count]['종가'],
                            df_put.iloc[put_t8416_count]['시가'])

                        df_put.loc[put_t8416_count, '피봇'] = round(피봇, 2)

                        item = QTableWidgetItem("{0:0.2f}".format(df_put.iloc[put_t8416_count]['피봇']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(put_t8416_count, Option_column.피봇.value, item)

                        temp = df_put.iloc[put_t8416_count]['시가'] - df_put.iloc[put_t8416_count]['종가']

                        df_put.loc[put_t8416_count, '시가갭'] = round(temp, 2)

                        if df_put.iloc[put_t8416_count]['종가'] > 0:

                            gap_percent = int((df_put.iloc[put_t8416_count]['시가'] /
                                               df_put.iloc[put_t8416_count]['종가'] - 1) * 100)

                            item = QTableWidgetItem(
                                "{0:0.2f}\n({1}%)".format(df_put.iloc[put_t8416_count]['시가갭'], gap_percent))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(put_t8416_count, Option_column.시가갭.value, item)
                        else:
                            pass

                        temp = round((df_put.iloc[put_t8416_count]['현재가'] -
                                      df_put.iloc[put_t8416_count]['시가']), 2) * 1

                        df_put.loc[put_t8416_count, '대비'] = int(temp)

                        item = QTableWidgetItem("{0:0.2f}".format(df_put.iloc[put_t8416_count]['대비']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(put_t8416_count, Option_column.대비.value, item)

                        df_put.loc[put_t8416_count, '진폭'] = df_put.iloc[put_t8416_count]['고가'] - \
                                                                  df_put.iloc[put_t8416_count]['저가']

                        item = QTableWidgetItem("{0:0.2f}".format(df_put.iloc[put_t8416_count]['진폭']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(put_t8416_count, Option_column.진폭.value, item)
                    else:
                        pass
                else:
                    pass

                str = '[{0:02d}:{1:02d}:{2:02d}] Put 행사가 {3}개중 {4}번째 Packet을 수신했습니다.\r'.format(dt.hour, dt.minute, dt.second, 
                    option_pairs_count, put_t8416_count + 1)
                self.textBrowser.append(str)

                put_t8416_count += 1

                print('Put 과거데이타 %d 개중 %d개 수신...' % (option_pairs_count, put_t8416_count))

                if put_t8416_count == option_pairs_count - new_actval_down_count:

                    print('\r')
                    print('t8416 Call 전광판\r')
                    print(df_call)
                    print('\r')
                    print('t8416 Put 전광판\r')
                    print(df_put)
                    print('\r')

                    self.tableWidget_put.resizeColumnsToContents()

                    put_positionCell = self.tableWidget_put.item(atm_index + 3, 1)
                    self.tableWidget_put.scrollToItem(put_positionCell)

                    if self.t8416_putworker.isRunning():

                        put_기준가 = df_put['기준가'].values.tolist()
                        put_월저 = df_put['월저'].values.tolist()
                        put_월고 = df_put['월고'].values.tolist()
                        put_전저 = df_put['전저'].values.tolist()
                        put_전고 = df_put['전고'].values.tolist()
                        put_종가 = df_put['종가'].values.tolist()
                        put_피봇 = df_put['피봇'].values.tolist()
                        put_시가 = df_put['시가'].values.tolist()
                        put_저가 = df_put['저가'].values.tolist()
                        put_고가 = df_put['고가'].values.tolist()

                        put_기준가_node_list = self.make_node_list(put_기준가)
                        put_월저_node_list = self.make_node_list(put_월저)
                        put_월고_node_list = self.make_node_list(put_월고)
                        put_전저_node_list = self.make_node_list(put_전저)
                        put_전고_node_list = self.make_node_list(put_전고)
                        put_종가_node_list = self.make_node_list(put_종가)
                        put_피봇_node_list = self.make_node_list(put_피봇)
                        put_시가_node_list = self.make_node_list(put_시가)
                        put_저가_node_list = self.make_node_list(put_저가)
                        put_고가_node_list = self.make_node_list(put_고가)

                        self.t8416_putworker.terminate()
                        
                        str = '[{0:02d}:{1:02d}:{2:02d}] Put 과거데이타 수신완료 !!!\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)
                    else:
                        pass                

                    if overnight:                        

                        # EUREX 야간옵션 시세전광판
                        XQ = t2835(parent=self)

                        if TARGET_MONTH_SELECT == 1:

                            if MANGI_YAGAN == 'YES':
                                t2835_month_info = NEXT_MONTH
                            else:
                                t2835_month_info = CURRENT_MONTH

                            str = '[{0:02d}:{1:02d}:{2:02d}] EUREX(t2835) 본월물 야간옵션 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                            self.textBrowser.append(str) 

                        elif TARGET_MONTH_SELECT == 2:

                            if MANGI_YAGAN == 'YES':
                                t2835_month_info = MONTH_AFTER_NEXT
                            else:
                                t2835_month_info = NEXT_MONTH

                            str = '[{0:02d}:{1:02d}:{2:02d}] EUREX(t2835) 차월물 야간옵션 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                            self.textBrowser.append(str)

                        else:
                            if MANGI_YAGAN == 'YES':
                                # to be checked !!!
                                pass
                            else:
                                t2835_month_info = MONTH_AFTER_NEXT

                            str = '[{0:02d}:{1:02d}:{2:02d}] EUREX(t2835) 차차월물 야간옵션 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                            self.textBrowser.append(str)

                        XQ.Query(월물=t2835_month_info)

                    else:
                            
                        수정거래량 = 0
                        수정미결 = 0
                        수정미결증감 = 0

                        for i in range(option_pairs_count):

                            df_call.loc[i, '수정거래량'] = 수정거래량
                            df_put.loc[i, '수정거래량'] = 수정거래량

                            temp = format(수정거래량, ',')

                            item = QTableWidgetItem(temp)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.VP.value, item)

                            item = QTableWidgetItem(temp)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.VP.value, item)

                            df_call.loc[i, '수정미결'] = 수정미결
                            df_put.loc[i, '수정미결'] = 수정미결

                            temp = format(수정미결, ',')

                            item = QTableWidgetItem(temp)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.OI.value, item)

                            item = QTableWidgetItem(temp)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.OI.value, item)

                            df_call.loc[i, '수정미결증감'] = 수정미결증감
                            df_put.loc[i, '수정미결증감'] = 수정미결증감

                            temp = format(수정미결증감, ',')

                            item = QTableWidgetItem(temp)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(i, Option_column.OID.value, item)

                            item = QTableWidgetItem(temp)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(i, Option_column.OID.value, item)

                        str = '[{0:02d}:{1:02d}:{2:02d}] 수정거래량 및 수정미결 초기화...\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)       

                        self.screen_update_worker.start()
                        self.screen_update_worker.daemon = True

                        str = '[{0:02d}:{1:02d}:{2:02d}] Screen Update 쓰레드가 시작됩니다.\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)
                        print(str)

                        refresh_flag = True

                        self.pushButton_add.setStyleSheet("background-color: lawngreen")
                        self.pushButton_add.setText('Refresh')

                    # 옵션 맥점 컬러링
                    str = '[{0:02d}:{1:02d}:{2:02d}] t8416 옵션 맥점 컬러링을 시작합니다.\r'.format(dt.hour, dt.minute, dt.second)
                    self.textBrowser.append(str)
                    
                    self.opt_node_coloring()
                    
                    str = '[{0:02d}:{1:02d}:{2:02d}] 옵션 만기일은 {3}일 남았습니다.\r'.format(dt.hour, dt.minute, dt.second, 옵션잔존일)
                    self.textBrowser.append(str)

                    if new_actval_up_count > 0:

                        str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 상방 행사가 {3}개 추가됨 !!!\r'.format(dt.hour, dt.minute, dt.second, new_actval_up_count)
                        self.textBrowser.append(str)
                    else:
                        pass

                    if new_actval_down_count > 0:

                        str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 하방 행사가 {3}개 추가됨 !!!\r'.format(dt.hour, dt.minute, dt.second, new_actval_down_count)
                        self.textBrowser.append(str)
                    else:
                        pass
                    
                    if NEW_NODE_VAL1 > 0:

                        str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 동적맥점({3}, {4}번 출현) 추가되었습니다.\r'.format \
                            (dt.hour, dt.minute, dt.second, NEW_NODE_VAL1, 동적맥점_빈도수_1st)
                        self.textBrowser.append(str)
                        print(str)
                    else:
                        pass

                    if NEW_NODE_VAL2 > 0:

                        str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 동적맥점({3}, {4}번 출현) 추가되었습니다.\r'.format \
                            (dt.hour, dt.minute, dt.second, NEW_NODE_VAL2, 동적맥점_빈도수_2nd)
                        self.textBrowser.append(str)
                        print(str)
                    else:
                        pass 

                    if NEW_NODE_VAL3 > 0:

                        str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 동적맥점({3}, {4}번 출현) 추가되었습니다.\r'.format \
                            (dt.hour, dt.minute, dt.second, NEW_NODE_VAL3, 동적맥점_빈도수_3rd)
                        self.textBrowser.append(str)
                        print(str)
                    else:
                        pass

                    str = '[{0:02d}:{1:02d}:{2:02d}] 새로운 진성맥점은 {3} 입니다.\r'.format(dt.hour, dt.minute, dt.second, 진성맥점)
                    self.textBrowser.append(str)
                    print(str)
                    
                    str = '[{0:02d}:{1:02d}:{2:02d}] 시스템시간 - 서버시간 = {3}초\r'.format(dt.hour, dt.minute, dt.second, system_server_timegap)
                    self.textBrowser.append(str)                                                                
                else:
                    pass
            else:
                pass

        elif szTrCode == 't8432':

            df = result[0]

            근월물선물코드 = df.iloc[0]['단축코드']
            차월물선물코드 = df.iloc[1]['단축코드']
            차차월물선물코드 = df.iloc[2]['단축코드']

            if MANGI_YAGAN == 'YES':

                if current_month == 3 or current_month == 6 or current_month == 9 or current_month == 12:
                    gmshcode = 차월물선물코드
                    cmshcode = 차차월물선물코드
                else:
                    gmshcode = 근월물선물코드
                    cmshcode = 차월물선물코드
                    ccmshcode = 차차월물선물코드
            else:
                gmshcode = 근월물선물코드
                cmshcode = 차월물선물코드
                ccmshcode = 차차월물선물코드

            if TARGET_MONTH_SELECT == 1:

                fut_code = gmshcode
                str = '[{0:02d}:{1:02d}:{2:02d}] 본월물({3:02d}월물, {4}) 선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second, current_month, fut_code)
                self.textBrowser.append(str)
                print(str)

            elif TARGET_MONTH_SELECT == 2:

                fut_code = cmshcode
                str = '[{0:02d}:{1:02d}:{2:02d}] 차월물({3:02d}월물, {4}) 선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second, next_month, fut_code)
                self.textBrowser.append(str)
                print(str)

            else:
                fut_code = ccmshcode
                str = '[{0:02d}:{1:02d}:{2:02d}] 차차월물({3:02d}월물, {4}) 선물 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second, month_after_next, fut_code)
                self.textBrowser.append(str)
                print(str)
            
            fut_realdata['전저'] = df.iloc[0]['전일저가']
            선물_전저 = df.iloc[0]['전일저가']

            item = QTableWidgetItem("{0:0.2f}".format(df.iloc[0]['전일저가']))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(1, Futures_column.전저.value, item)

            fut_realdata['전고'] = df.iloc[0]['전일고가']
            선물_전고 = df.iloc[0]['전일고가']

            item = QTableWidgetItem("{0:0.2f}".format(df.iloc[0]['전일고가']))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(1, Futures_column.전고.value, item)

            fut_realdata['종가'] = df.iloc[0]['전일종가']
            선물_종가 = df.iloc[0]['전일종가']

            item = QTableWidgetItem("{0:0.2f}".format(df.iloc[0]['전일종가']))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_fut.setItem(1, Futures_column.종가.value, item)

            self.tableWidget_fut.resizeColumnsToContents()

        elif szTrCode == 't8433':

            pass
        else:
            pass
    
    def kp200_low_node_coloring(self, t):

        dt = datetime.datetime.now()

        global flag_kp200_low_node, kp200_low_node_time, kp200_low_node_str  

        flag_kp200_low_node = False    
        
        # kp200 맥점 컬러링
        self.tableWidget_fut.item(2, Futures_column.저가.value).setBackground(QBrush(옅은회색))
        self.tableWidget_fut.item(2, Futures_column.저가.value).setForeground(QBrush(검정색))
        
        for i in range(10):

            if self.within_n_tick(kp200_realdata['저가'], kp200_coreval[i], 10):
                
                self.tableWidget_fut.item(2, Futures_column.저가.value).setBackground(QBrush(대맥점색))
                self.tableWidget_fut.item(2, Futures_column.저가.value).setForeground(QBrush(검정색))

                flag_kp200_low_node = True

                kp200_low_node_str = "[{0:02d}:{1:02d}:{2:02d}] kp200 저가맥점 {3:.2f} 발생 !!!".format(\
                                        dt.hour, dt.minute, dt.second, kp200_realdata['저가'])
            else:
                pass

        return

    def kp200_high_node_coloring(self, t):  

        dt = datetime.datetime.now() 

        global flag_kp200_high_node, kp200_high_node_time, kp200_high_node_str 

        flag_kp200_high_node = False    
        
        # kp200 맥점 컬러링
        self.tableWidget_fut.item(2, Futures_column.고가.value).setBackground(QBrush(옅은회색))
        self.tableWidget_fut.item(2, Futures_column.고가.value).setForeground(QBrush(검정색))
        
        for i in range(10):

            if self.within_n_tick(kp200_realdata['고가'], kp200_coreval[i], 10):
                
                self.tableWidget_fut.item(2, Futures_column.고가.value).setBackground(QBrush(대맥점색))
                self.tableWidget_fut.item(2, Futures_column.고가.value).setForeground(QBrush(검정색))

                flag_kp200_high_node = True

                kp200_high_node_str = "[{0:02d}:{1:02d}:{2:02d}] kp200 고가맥점 {3:.2f} 발생 !!!".format(\
                                        dt.hour, dt.minute, dt.second, kp200_realdata['고가'])
            else:
                pass

        return

    def fut_oloh_check(self):

        global flag_fut_ol, flag_fut_oh, n_oloh_str

        dt = datetime.datetime.now()

        # FUT OL/OH
        if self.within_n_tick(선물_시가, 선물_저가, 10) and not self.within_n_tick(선물_시가, 선물_고가, 10):

            item = QTableWidgetItem('▲')
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(적색))
            item.setForeground(QBrush(검정색))

            if overnight:
                self.tableWidget_fut.setItem(0, Futures_column.OLOH.value, item)
            else:
                self.tableWidget_fut.setItem(1, Futures_column.OLOH.value, item)

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.시가.value).setBackground(QBrush(적색))
                self.tableWidget_fut.item(0, Futures_column.시가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setBackground(QBrush(적색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setForeground(QBrush(검정색))
            else:
                self.tableWidget_fut.item(1, Futures_column.시가.value).setBackground(QBrush(적색))
                self.tableWidget_fut.item(1, Futures_column.시가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setBackground(QBrush(적색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setForeground(QBrush(검정색))

            if TARGET_MONTH_SELECT == 2 and not flag_fut_ol:

                n_oloh_str = "[{0:02d}:{1:02d}:{2:02d}] NM 선물 OL ▲".format(dt.hour, dt.minute, dt.second)

            elif TARGET_MONTH_SELECT == 3 and not flag_fut_ol:

                n_oloh_str = "[{0:02d}:{1:02d}:{2:02d}] MAN 선물 OL ▲".format(dt.hour, dt.minute, dt.second)
            else:
                pass
            
            flag_fut_ol = True

        elif not self.within_n_tick(선물_시가, 선물_저가, 10) and self.within_n_tick(선물_시가, 선물_고가, 10):

            item = QTableWidgetItem('▼')
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(청색))
            item.setForeground(QBrush(흰색))

            if overnight:
                self.tableWidget_fut.setItem(0, Futures_column.OLOH.value, item)
            else:
                self.tableWidget_fut.setItem(1, Futures_column.OLOH.value, item)

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.시가.value).setBackground(QBrush(청색))
                self.tableWidget_fut.item(0, Futures_column.시가.value).setForeground(QBrush(흰색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setBackground(QBrush(청색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setForeground(QBrush(흰색))
            else:
                self.tableWidget_fut.item(1, Futures_column.시가.value).setBackground(QBrush(청색))
                self.tableWidget_fut.item(1, Futures_column.시가.value).setForeground(QBrush(흰색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setBackground(QBrush(청색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setForeground(QBrush(흰색))

            if TARGET_MONTH_SELECT == 2 and not flag_fut_oh:

                n_oloh_str = "[{0:02d}:{1:02d}:{2:02d}] NM 선물 OH ▼".format(dt.hour, dt.minute, dt.second)

            elif TARGET_MONTH_SELECT == 3 and not flag_fut_oh:

                n_oloh_str = "[{0:02d}:{1:02d}:{2:02d}] MAN 선물 OH ▼".format(dt.hour, dt.minute, dt.second)
            else:
                pass
            
            flag_fut_oh = True

        else:
            flag_fut_ol = False
            flag_fut_oh = False
            n_oloh_str = ''

            item = QTableWidgetItem('')

            if overnight:
                self.tableWidget_fut.setItem(0, Futures_column.OLOH.value, item)
            else:
                self.tableWidget_fut.setItem(1, Futures_column.OLOH.value, item) 

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.시가.value).setBackground(QBrush(흰색))
                self.tableWidget_fut.item(0, Futures_column.시가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setBackground(QBrush(옅은회색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setBackground(QBrush(옅은회색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setForeground(QBrush(검정색))
            else:
                self.tableWidget_fut.item(1, Futures_column.시가.value).setBackground(QBrush(흰색))
                self.tableWidget_fut.item(1, Futures_column.시가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setBackground(QBrush(옅은회색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setBackground(QBrush(옅은회색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setForeground(QBrush(검정색))
        
        return

    def fut_node_coloring(self):

        dt = datetime.datetime.now()

        if 선물_시가 > 0:

            if 선물_현재가 > 선물_시가:

                if overnight:

                    self.tableWidget_fut.item(0, 0).setBackground(QBrush(적색))
                    self.tableWidget_fut.item(0, 0).setForeground(QBrush(검정색))
                else:
                    self.tableWidget_fut.item(1, 0).setBackground(QBrush(적색))
                    self.tableWidget_fut.item(1, 0).setForeground(QBrush(검정색))

            elif 선물_현재가 < 선물_시가:

                if overnight:

                    self.tableWidget_fut.item(0, 0).setBackground(QBrush(청색))
                    self.tableWidget_fut.item(0, 0).setForeground(QBrush(흰색))
                else:
                    self.tableWidget_fut.item(1, 0).setBackground(QBrush(청색))
                    self.tableWidget_fut.item(1, 0).setForeground(QBrush(흰색))

            else:

                if overnight:

                    self.tableWidget_fut.item(0, 0).setBackground(QBrush(검정색))
                    self.tableWidget_fut.item(0, 0).setForeground(QBrush(흰색))
                else:
                    self.tableWidget_fut.item(1, 0).setBackground(QBrush(검정색))
                    self.tableWidget_fut.item(1, 0).setForeground(QBrush(흰색))
        else:
            pass
                
        # 전저, 전고, 종가, 피봇 컬러링
        if self.within_n_tick(선물_전저, 선물_저가, 10):

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.전저.value).setBackground(QBrush(콜전저색))
                self.tableWidget_fut.item(0, Futures_column.전저.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setBackground(QBrush(콜전저색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setForeground(QBrush(검정색))
            else:
                self.tableWidget_fut.item(1, Futures_column.전저.value).setBackground(QBrush(콜전저색))
                self.tableWidget_fut.item(1, Futures_column.전저.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setBackground(QBrush(콜전저색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setForeground(QBrush(검정색))
        else:
            pass

        if self.within_n_tick(선물_전고, 선물_저가, 10):

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.전고.value).setBackground(QBrush(콜전고색))
                self.tableWidget_fut.item(0, Futures_column.전고.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setBackground(QBrush(콜전고색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setForeground(QBrush(검정색))
            else:
                self.tableWidget_fut.item(1, Futures_column.전고.value).setBackground(QBrush(콜전고색))
                self.tableWidget_fut.item(1, Futures_column.전고.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setBackground(QBrush(콜전고색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setForeground(QBrush(검정색))
        else:
            pass

        if self.within_n_tick(선물_종가, 선물_저가, 10):

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.종가.value).setBackground(QBrush(콜종가색))
                self.tableWidget_fut.item(0, Futures_column.종가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setBackground(QBrush(콜종가색))
                self.tableWidget_fut.item(0, Futures_column.저가.value).setForeground(QBrush(검정색))
            else:
                self.tableWidget_fut.item(1, Futures_column.종가.value).setBackground(QBrush(콜종가색))
                self.tableWidget_fut.item(1, Futures_column.종가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setBackground(QBrush(콜종가색))
                self.tableWidget_fut.item(1, Futures_column.저가.value).setForeground(QBrush(검정색))
        else:
            pass

        if 선물_피봇 > 0:

            if self.within_n_tick(선물_피봇, 선물_저가, 10):

                if overnight:

                    self.tableWidget_fut.item(0, Futures_column.피봇.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_fut.item(0, Futures_column.피봇.value).setForeground(QBrush(검정색))
                    self.tableWidget_fut.item(0, Futures_column.저가.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_fut.item(0, Futures_column.저가.value).setForeground(QBrush(검정색))
                else:
                    self.tableWidget_fut.item(1, Futures_column.피봇.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_fut.item(1, Futures_column.피봇.value).setForeground(QBrush(검정색))
                    self.tableWidget_fut.item(1, Futures_column.저가.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_fut.item(1, Futures_column.저가.value).setForeground(QBrush(검정색))
            else:
                pass
        else:
            pass        

        if self.within_n_tick(선물_전저, 선물_고가, 10):

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.전저.value).setBackground(QBrush(콜전저색))
                self.tableWidget_fut.item(0, Futures_column.전저.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setBackground(QBrush(콜전저색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setForeground(QBrush(검정색))
            else:
                self.tableWidget_fut.item(1, Futures_column.전저.value).setBackground(QBrush(콜전저색))
                self.tableWidget_fut.item(1, Futures_column.전저.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setBackground(QBrush(콜전저색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setForeground(QBrush(검정색))
        else:
            pass        

        if self.within_n_tick(선물_전고, 선물_고가, 10):

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.전고.value).setBackground(QBrush(콜전고색))
                self.tableWidget_fut.item(0, Futures_column.전고.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setBackground(QBrush(콜전고색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setForeground(QBrush(검정색))
            else:
                self.tableWidget_fut.item(1, Futures_column.전고.value).setBackground(QBrush(콜전고색))
                self.tableWidget_fut.item(1, Futures_column.전고.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setBackground(QBrush(콜전고색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setForeground(QBrush(검정색))
        else:
            pass        

        if self.within_n_tick(선물_종가, 선물_고가, 10):

            if overnight:

                self.tableWidget_fut.item(0, Futures_column.종가.value).setBackground(QBrush(콜종가색))
                self.tableWidget_fut.item(0, Futures_column.종가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setBackground(QBrush(콜종가색))
                self.tableWidget_fut.item(0, Futures_column.고가.value).setForeground(QBrush(검정색))
            else:
                self.tableWidget_fut.item(1, Futures_column.종가.value).setBackground(QBrush(콜종가색))
                self.tableWidget_fut.item(1, Futures_column.종가.value).setForeground(QBrush(검정색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setBackground(QBrush(콜종가색))
                self.tableWidget_fut.item(1, Futures_column.고가.value).setForeground(QBrush(검정색))
        else:
            pass

        if 선물_피봇 > 0:

            if self.within_n_tick(선물_피봇, 선물_고가, 10):                

                if overnight:

                    self.tableWidget_fut.item(0, Futures_column.피봇.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_fut.item(0, Futures_column.피봇.value).setForeground(QBrush(검정색))
                    self.tableWidget_fut.item(0, Futures_column.고가.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_fut.item(0, Futures_column.고가.value).setForeground(QBrush(검정색))
                else:
                    self.tableWidget_fut.item(1, Futures_column.피봇.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_fut.item(1, Futures_column.피봇.value).setForeground(QBrush(검정색))
                    self.tableWidget_fut.item(1, Futures_column.고가.value).setBackground(QBrush(콜피봇색))
                    self.tableWidget_fut.item(1, Futures_column.고가.value).setForeground(QBrush(검정색))
            else:
                pass  
        else:
            pass

        # 선물 맥점 컬러링
        str = '[{0:02d}:{1:02d}:{2:02d}] 선물 맥점 컬러링을 완료했습니다.\r'.format(dt.hour, dt.minute, dt.second)
        self.textBrowser.append(str)
        
        return

    # 선물표시	
    def futures_display(self, result):        

        global cme_realdata, fut_realdata
        global df_fut
        global df_plotdata_fut, df_plotdata_kp200, df_plotdata_fut_volume
        global atm_str, atm_val, atm_index, atm_index_old
        global fut_tick_list, fut_value_list, df_fut_ohlc
        global 선물_시가, 선물_현재가, 선물_저가, 선물_고가, 선물_피봇
        global flag_fut_low, flag_fut_high 
        global 선물_누적거래량
        global first_refresh, fut_first_arrive
        global flag_telegram_listen_worker, telegram_send_worker_on_time
        global flag_telegram_send_worker

        dt = datetime.datetime.now()
        current_str = dt.strftime('%H:%M:%S')

        체결시간 = result['체결시간']

        시가 = result['시가']
        현재가 = result['현재가']
        저가 = result['저가']
        고가 = result['고가']

        선물_시가 = round(float(시가), 2)
        선물_현재가 = round(float(현재가), 2)
        선물_저가 = round(float(저가), 2)
        선물_고가 = round(float(고가), 2)        
        
        # 선물 OHLC 데이타프레임 생성
        '''
        time_str = 체결시간[0:2] + ':' + 체결시간[2:4] + ':' + 체결시간[4:6]
        chetime = nowDate + ' ' + time_str

        fut_tick_list.append(chetime)
        fut_value_list.append(선물_현재가)

        fut_dict = {"value": fut_value_list}
        df = pd.DataFrame(fut_dict, index=fut_tick_list)

        # Converting the index as DatetimeIndex
        df.index = pd.to_datetime(df.index)

        # 1 Minute resample
        df_fut_ohlc = df.resample('1T').ohlc()
        #print('\r선물 틱 데이타 {}\r 선물 OHLC {}\r'.format(df, df_fut_ohlc))
        '''
        
        df_plotdata_fut.iloc[0][x_idx] = 선물_현재가
        df_plotdata_kp200.iloc[0][x_idx] = round(float(result['KOSPI200지수']), 2)

        #print('fut_first_arrive = {0}, first_refresh = {1}, market_service = {2}\r'.format(fut_first_arrive, first_refresh, market_service))

        fut_time = int(current_str[0:2]) * 3600 + int(current_str[3:5]) * 60 + int(current_str[6:8])

        if not flag_telegram_send_worker:            

            self.telegram_send_worker.start()
            self.telegram_send_worker.daemon = True

            telegram_send_worker_on_time = fut_time 
            
            str = '[{0:02d}:{1:02d}:{2:02d}] telegram send worker({3})가 시작됩니다.\r'.format(dt.hour, dt.minute, dt.second, telegram_send_worker_on_time)
            self.textBrowser.append(str)
            print(str) 

            if TARGET_MONTH_SELECT == 1:

                str = '[{0:02d}:{1:02d}:{2:02d}] CM 텔레그램이 시작됩니다.\r'.format(dt.hour, dt.minute, dt.second)
                ToTelegram(str)

            elif TARGET_MONTH_SELECT == 2:

                str = '[{0:02d}:{1:02d}:{2:02d}] NM 텔레그램이 시작됩니다.\r'.format(dt.hour, dt.minute, dt.second)
                ToTelegram(str)

            elif TARGET_MONTH_SELECT == 3:

                str = '[{0:02d}:{1:02d}:{2:02d}] MAN 텔레그램이 시작됩니다.\r'.format(dt.hour, dt.minute, dt.second)
                ToTelegram(str)
            else:
                pass         

            flag_telegram_send_worker = True             
        else:
            pass

        #if market_service and (fut_time == fut_first_arrive + 1 or fut_time == fut_first_arrive + 2):
        if fut_time == telegram_send_worker_on_time + 2 or fut_time == telegram_send_worker_on_time + 3:
            
            # 선물 시가갭 컬러링(주간 장시작시 표시안되는 오류 대응)
            if overnight:

                if 선물_시가 > 선물_종가:
                    self.tableWidget_fut.item(0, Futures_column.시가갭.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_fut.item(0, Futures_column.시가갭.value).setForeground(QBrush(검정색))
                elif 선물_시가 < 선물_종가:
                    self.tableWidget_fut.item(0, Futures_column.시가갭.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_fut.item(0, Futures_column.시가갭.value).setForeground(QBrush(흰색))
                else:
                    self.tableWidget_fut.item(0, Futures_column.시가갭.value).setBackground(QBrush(흰색))
            else:

                if 선물_시가 > 선물_종가:
                    self.tableWidget_fut.item(1, Futures_column.시가갭.value).setBackground(QBrush(콜기준가색))
                    self.tableWidget_fut.item(1, Futures_column.시가갭.value).setForeground(QBrush(검정색))
                elif 선물_시가 < 선물_종가:
                    self.tableWidget_fut.item(1, Futures_column.시가갭.value).setBackground(QBrush(풋기준가색))
                    self.tableWidget_fut.item(1, Futures_column.시가갭.value).setForeground(QBrush(흰색))
                else:
                    self.tableWidget_fut.item(1, Futures_column.시가갭.value).setBackground(QBrush(흰색))   
        else:
            pass

        # Telegram Send Worker 시작 후 TELEGRAM_START_TIME분에 Telegram Listen을 위한 Polling Thread 시작 !!!
        if not flag_telegram_listen_worker and fut_time > telegram_send_worker_on_time + 60 * TELEGRAM_START_TIME:

            if TELEGRAM_SERVICE == 'ON':

                self.telegram_listen_worker.start()
                self.telegram_listen_worker.daemon = True

                if TARGET_MONTH_SELECT == 1:

                    ToTelegram("CM 텔레그램 Polling이 시작됩니다.")

                elif TARGET_MONTH_SELECT == 2:

                    ToTelegram("NM 텔레그램 Polling이 시작됩니다.")

                elif TARGET_MONTH_SELECT == 3:

                    ToTelegram("MAN 텔레그램 Polling이 시작됩니다.")
                else:
                    pass
                
                self.pushButton_remove.setStyleSheet("background-color: lawngreen")
                #self.telegram_flag = True
                
                flag_telegram_listen_worker = True
            else:
                pass            
        else:
            pass

        # 현재가 갱신
        if overnight:
            fut_price = self.tableWidget_fut.item(0, Futures_column.현재가.value).text()[0:6]
        else:
            fut_price = self.tableWidget_fut.item(1, Futures_column.현재가.value).text()[0:6]

        if 현재가 != fut_price:

            if overnight:
                
                df_fut.loc[0, '현재가'] = 선물_현재가
                cme_realdata['현재가'] = 선물_현재가

                if float(현재가) < float(self.tableWidget_fut.item(0, Futures_column.현재가.value).text()[0:6]):
                    item = QTableWidgetItem(현재가 + '\n' + self.상태그림[0])
                elif float(현재가) > float(self.tableWidget_fut.item(0, Futures_column.현재가.value).text()[0:6]):
                    item = QTableWidgetItem(현재가 + '\n' + self.상태그림[1])
                else:    
                    item = QTableWidgetItem(현재가)

                item.setTextAlignment(Qt.AlignCenter)

                if float(현재가) < float(self.tableWidget_fut.item(0, Futures_column.현재가.value).text()[0:6]):
                    item.setBackground(QBrush(lightskyblue))
                elif float(현재가) > float(self.tableWidget_fut.item(0, Futures_column.현재가.value).text()[0:6]):
                    item.setBackground(QBrush(pink))
                else:
                    item.setBackground(QBrush(옅은회색))

                self.tableWidget_fut.setItem(0, Futures_column.현재가.value, item)
            else:
                df_fut.loc[1, '현재가'] = 선물_현재가
                fut_realdata['현재가'] = 선물_현재가 

                if float(현재가) < float(self.tableWidget_fut.item(1, Futures_column.현재가.value).text()[0:6]):
                    item = QTableWidgetItem(현재가 + '\n' + self.상태그림[0])
                elif float(현재가) > float(self.tableWidget_fut.item(1, Futures_column.현재가.value).text()[0:6]):
                    item = QTableWidgetItem(현재가 + '\n' + self.상태그림[1])
                else:    
                    item = QTableWidgetItem(현재가)

                item.setTextAlignment(Qt.AlignCenter)

                if float(현재가) < float(self.tableWidget_fut.item(1, Futures_column.현재가.value).text()[0:6]):
                    item.setBackground(QBrush(lightskyblue))
                elif float(현재가) > float(self.tableWidget_fut.item(1, Futures_column.현재가.value).text()[0:6]):
                    item.setBackground(QBrush(pink))
                else:
                    #item.setBackground(QBrush(옅은회색))
                    pass

                self.tableWidget_fut.setItem(1, Futures_column.현재가.value, item)                              

            if 선물_시가 < 선물_현재가:

                if overnight:
                    self.tableWidget_fut.item(0, Futures_column.현재가.value).setForeground(QBrush(적색))
                else:
                    self.tableWidget_fut.item(1, Futures_column.현재가.value).setForeground(QBrush(적색))

            elif 선물_시가 > 선물_현재가:

                if overnight:
                    self.tableWidget_fut.item(0, Futures_column.현재가.value).setForeground(QBrush(청색))
                else:
                    self.tableWidget_fut.item(1, Futures_column.현재가.value).setForeground(QBrush(청색))

            else:
                if overnight:
                    self.tableWidget_fut.item(0, Futures_column.현재가.value).setForeground(QBrush(검정색))
                else:
                    self.tableWidget_fut.item(1, Futures_column.현재가.value).setForeground(QBrush(검정색))

            대비 = 선물_현재가 - 선물_시가
            등락율 = result['등락율']

            item = QTableWidgetItem("{0:0.2f}\n({1:0.2f}%)".format(대비, 등락율))
            item.setTextAlignment(Qt.AlignCenter)

            if overnight:
                self.tableWidget_fut.setItem(0, Futures_column.대비.value, item)
            else:
                self.tableWidget_fut.setItem(1, Futures_column.대비.value, item)
            
            if 대비 > 0:

                direction = '▲'

                if direction != self.tableWidget_fut.horizontalHeaderItem(0).text():
                    item = QTableWidgetItem(direction)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_fut.setHorizontalHeaderItem(0, item)
                else:
                    pass

                if overnight:

                    self.tableWidget_fut.item(0, 0).setBackground(QBrush(적색))
                    self.tableWidget_fut.item(0, 0).setForeground(QBrush(검정색))
                else:
                    self.tableWidget_fut.item(1, 0).setBackground(QBrush(적색))
                    self.tableWidget_fut.item(1, 0).setForeground(QBrush(검정색))

            elif 대비 < 0:

                direction = '▼'

                if direction != self.tableWidget_fut.horizontalHeaderItem(0).text():
                    item = QTableWidgetItem(direction)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_fut.setHorizontalHeaderItem(0, item)
                else:
                    pass  

                if overnight:

                    self.tableWidget_fut.item(0, 0).setBackground(QBrush(청색))
                    self.tableWidget_fut.item(0, 0).setForeground(QBrush(흰색))
                else:
                    self.tableWidget_fut.item(1, 0).setBackground(QBrush(청색))
                    self.tableWidget_fut.item(1, 0).setForeground(QBrush(흰색)) 

            else:

                direction = ''

                if direction != self.tableWidget_fut.horizontalHeaderItem(0).text():
                    item = QTableWidgetItem(direction)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_fut.setHorizontalHeaderItem(0, item)
                else:
                    pass  

                if overnight:

                    self.tableWidget_fut.item(0, 0).setBackground(QBrush(검정색))
                    self.tableWidget_fut.item(0, 0).setForeground(QBrush(흰색))
                else:
                    self.tableWidget_fut.item(1, 0).setBackground(QBrush(검정색))
                    self.tableWidget_fut.item(1, 0).setForeground(QBrush(흰색))     
        else:
            pass 

        # 시가 및 피봇 갱신
        if overnight:
            fut_open = self.tableWidget_fut.item(0, Futures_column.시가.value).text()
        else:
            fut_open = self.tableWidget_fut.item(1, Futures_column.시가.value).text()

        if 시가 != fut_open:

            df_plotdata_fut.iloc[0][선물장간_시간차] = 선물_시가

            선물_피봇 = self.calc_pivot(선물_전저, 선물_전고, 선물_종가, 선물_시가)

            시가갭 = 선물_시가 - 선물_종가

            item = QTableWidgetItem(시가)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(흰색))        

            if 선물_시가 > 선물_종가:
                item.setForeground(QBrush(적색))
            elif 선물_시가 < 선물_종가:
                item.setForeground(QBrush(청색))
            else:
                item.setForeground(QBrush(검정색))    

            if overnight:

                self.tableWidget_fut.setItem(0, Futures_column.시가.value, item)

                df_fut.loc[0, '시가'] = 선물_시가
                cme_realdata['시가'] = 선물_시가

                item = QTableWidgetItem("{0:0.2f}".format(선물_피봇))
                item.setTextAlignment(Qt.AlignCenter)

                self.tableWidget_fut.setItem(0, Futures_column.피봇.value, item)

                df_fut.loc[0, '피봇'] = 선물_피봇
                cme_realdata['피봇'] = 선물_피봇

                item = QTableWidgetItem("{0:0.2f}".format(시가갭))
                item.setTextAlignment(Qt.AlignCenter)

                if 선물_시가 > 선물_종가:
                    item.setBackground(QBrush(콜기준가색))
                    item.setForeground(QBrush(검정색))
                elif 선물_시가 < 선물_종가:
                    item.setBackground(QBrush(풋기준가색))
                    item.setForeground(QBrush(흰색))
                else:
                    item.setBackground(QBrush(흰색))  

                self.tableWidget_fut.setItem(0, Futures_column.시가갭.value, item)
                
                cme_realdata['시가갭'] = 시가갭
                df_fut.loc[0, '시가갭'] = 시가갭
            else:

                self.tableWidget_fut.setItem(1, Futures_column.시가.value, item)

                df_fut.loc[1, '시가'] = 선물_시가
                fut_realdata['시가'] = 선물_시가

                item = QTableWidgetItem("{0:0.2f}".format(선물_피봇))
                item.setTextAlignment(Qt.AlignCenter)

                self.tableWidget_fut.setItem(1, Futures_column.피봇.value, item)

                df_fut.loc[1, '피봇'] = 선물_피봇
                fut_realdata['피봇'] = 선물_피봇             

                item = QTableWidgetItem("{0:0.2f}".format(시가갭))
                item.setTextAlignment(Qt.AlignCenter)

                if 선물_시가 > 선물_종가:
                    item.setBackground(QBrush(콜기준가색))
                    item.setForeground(QBrush(검정색))
                elif 선물_시가 < 선물_종가:
                    item.setBackground(QBrush(풋기준가색))
                    item.setForeground(QBrush(흰색))
                else:
                    item.setBackground(QBrush(흰색))  

                self.tableWidget_fut.setItem(1, Futures_column.시가갭.value, item)
                
                fut_realdata['시가갭'] = 시가갭
                df_fut.loc[1, '시가갭'] = 시가갭                
        else:

            if 선물_피봇 == 0 and 선물_시가 > 0:

                선물_피봇 = self.calc_pivot(선물_전저, 선물_전고, 선물_종가, 선물_시가)

                시가갭 = 선물_시가 - 선물_종가

                item = QTableWidgetItem("{0:0.2f}".format(선물_피봇))
                item.setTextAlignment(Qt.AlignCenter)

                if overnight:
                    self.tableWidget_fut.setItem(0, Futures_column.피봇.value, item)
                    df_fut.loc[0, '피봇'] = 선물_피봇
                    cme_realdata['피봇'] = 선물_피봇
                else:
                    self.tableWidget_fut.setItem(1, Futures_column.피봇.value, item)
                    df_fut.loc[1, '피봇'] = 선물_피봇
                    fut_realdata['피봇'] = 선물_피봇

                item = QTableWidgetItem("{0:0.2f}".format(시가갭))
                item.setTextAlignment(Qt.AlignCenter)

                if 선물_시가 > 선물_종가:
                    item.setBackground(QBrush(콜기준가색))
                    item.setForeground(QBrush(검정색))
                elif 선물_시가 < 선물_종가:
                    item.setBackground(QBrush(풋기준가색))
                    item.setForeground(QBrush(흰색))
                else:
                    item.setBackground(QBrush(흰색)) 

                if overnight:
                    self.tableWidget_fut.setItem(0, Futures_column.시가갭.value, item)
                    df_fut.loc[0, '시가갭'] = 시가갭
                    cme_realdata['시가갭'] = 시가갭
                else:
                    self.tableWidget_fut.setItem(1, Futures_column.시가갭.value, item)
                    df_fut.loc[1, '시가갭'] = 시가갭
                    fut_realdata['시가갭'] = 시가갭
            else:
                pass 
                
        # 저가 갱신
        if overnight:
            fut_low = self.tableWidget_fut.item(0, Futures_column.저가.value).text()
        else:
            fut_low = self.tableWidget_fut.item(1, Futures_column.저가.value).text()

        if 저가 != fut_low:

            flag_fut_low = True

            item = QTableWidgetItem(저가)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(회색))            

            if overnight:
                self.tableWidget_fut.setItem(0, Futures_column.저가.value, item)
                df_fut.loc[0, '저가'] = 선물_저가
                cme_realdata['저가'] = 선물_저가
            else:
                self.tableWidget_fut.setItem(1, Futures_column.저가.value, item)
                df_fut.loc[1, '저가'] = 선물_저가
                fut_realdata['저가'] = 선물_저가

            if 선물_전저 >= 선물_저가:

                #str = repr(선물_전저) + ' ▼'
                str = '{0:0.2f}'.format(선물_전저) + '\n▼'

                item = QTableWidgetItem(str)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QBrush(청색))  

                if overnight:           
                    self.tableWidget_fut.setItem(0, Futures_column.전저.value, item)
                else:
                    self.tableWidget_fut.setItem(1, Futures_column.전저.value, item)
            else:
                pass

            self.fut_node_color_clear()                    
            self.fut_oloh_check()
            self.fut_node_coloring()

            str = '[{0:02d}:{1:02d}:{2:02d}] 선물 저가 {3} Update...\r'.format(dt.hour, dt.minute, dt.second, 선물_저가)
            self.textBrowser.append(str)
            
            진폭 = 선물_고가 - 선물_저가

            item = QTableWidgetItem("{0:0.2f}".format(진폭))
            item.setTextAlignment(Qt.AlignCenter)

            if overnight:
                self.tableWidget_fut.setItem(0, Futures_column.진폭.value, item)
                df_fut.loc[0, '진폭'] = 진폭
                cme_realdata['진폭'] = 진폭
            else:
                self.tableWidget_fut.setItem(1, Futures_column.진폭.value, item)
                df_fut.loc[1, '진폭'] = 진폭
                fut_realdata['진폭'] = 진폭            
        else:
            pass

        # 고가 갱신
        if overnight:
            fut_high = self.tableWidget_fut.item(0, Futures_column.고가.value).text()
        else:
            fut_high = self.tableWidget_fut.item(1, Futures_column.고가.value).text()

        if 고가 != fut_high:

            flag_fut_high = True

            item = QTableWidgetItem(고가)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(회색))            

            if overnight:
                self.tableWidget_fut.setItem(0, Futures_column.고가.value, item)
                df_fut.loc[0, '고가'] = 선물_고가
            else:
                self.tableWidget_fut.setItem(1, Futures_column.고가.value, item)
                df_fut.loc[1, '고가'] = 선물_고가

            if 선물_전고 <= 선물_고가:

                #str = repr(선물_전고) + ' ▲'
                str = '{0:0.2f}'.format(선물_전고) + '\n▲'

                item = QTableWidgetItem(str)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QBrush(적색))  

                if overnight:           
                    self.tableWidget_fut.setItem(0, Futures_column.전고.value, item)
                else:
                    self.tableWidget_fut.setItem(1, Futures_column.전고.value, item)
            else:
                pass

            self.fut_node_color_clear()                    
            self.fut_oloh_check()
            self.fut_node_coloring()

            str = '[{0:02d}:{1:02d}:{2:02d}] 선물 고가 {3} Update...\r'.format(dt.hour, dt.minute, dt.second, 선물_고가)
            self.textBrowser.append(str)
            
            진폭 = 선물_고가 - 선물_저가

            item = QTableWidgetItem("{0:0.2f}".format(진폭))
            item.setTextAlignment(Qt.AlignCenter)

            if overnight:
                self.tableWidget_fut.setItem(0, Futures_column.진폭.value, item)
                df_fut.loc[0, '진폭'] = 진폭
                cme_realdata['진폭'] = 진폭
            else:
                self.tableWidget_fut.setItem(1, Futures_column.진폭.value, item)
                df_fut.loc[1, '진폭'] = 진폭  
                fut_realdata['진폭'] = 진폭          
        else:
            pass

        # 장중 거래량 갱신, 장중 거래량은 누적거래량이 아닌 수정거래량 임
        선물_누적거래량 = result['매수누적체결량'] - result['매도누적체결량']
        df_plotdata_fut_volume.iloc[0][x_idx] = 선물_누적거래량

        temp = format(선물_누적거래량, ',')

        item = QTableWidgetItem(temp)
        item.setTextAlignment(Qt.AlignCenter)

        if 선물_누적거래량 > 0:

            item.setBackground(QBrush(적색))
            item.setForeground(QBrush(검정색))
        elif 선물_누적거래량 < 0:

            item.setBackground(QBrush(청색))
            item.setForeground(QBrush(흰색))
        else:
            item.setBackground(QBrush(흰색))
            item.setForeground(QBrush(검정색))

        if overnight:
            self.tableWidget_fut.setItem(0, Futures_column.거래량.value, item)
            df_fut.loc[0, '거래량'] = 선물_누적거래량
            cme_realdata['거래량'] = 선물_누적거래량
        else:
            self.tableWidget_fut.setItem(1, Futures_column.거래량.value, item)
            df_fut.loc[1, '거래량'] = 선물_누적거래량
            fut_realdata['거래량'] = 선물_누적거래량        
        
        # 미결 갱신
        fut_realdata['미결'] = result['미결제약정수량']  
        temp = format(fut_realdata['미결'], ',')                     

        item = QTableWidgetItem(temp)
        item.setTextAlignment(Qt.AlignCenter)

        if not overnight:
            self.tableWidget_fut.setItem(1, Futures_column.OI.value, item)
            df_fut.loc[1, '미결'] = fut_realdata['미결']
        else:
            pass

        # 미결증감 갱신
        fut_realdata['미결증감'] = result['미결제약정증감']
        temp = format(fut_realdata['미결증감'], ',')  

        item = QTableWidgetItem(temp)
        item.setTextAlignment(Qt.AlignCenter)

        if result['미결제약정증감'] < 0:
            item.setBackground(QBrush(라임))
        else:
            item.setBackground(QBrush(흰색))

        if not overnight:
            self.tableWidget_fut.setItem(1, Futures_column.OID.value, item)
            df_fut.loc[1, '미결증감'] = fut_realdata['미결증감']   
        else:
            pass
        
        self.tableWidget_fut.resizeColumnsToContents() 

        return

    # 콜 표시
    def call_display(self, result):

        global call_result, call_open, call_below_atm_count
        global df_call, df_plotdata_call, df_plotdata_call_oi
        global call_atm_value
        global call_시가, call_시가_node_list, call_피봇, call_피봇_node_list, 콜시가리스트
        global call_저가, call_저가_node_list, call_고가, call_고가_node_list
        global call_gap_percent, call_db_percent
        global opt_callreal_update_counter
        global df_call_volume, call_volume_total, df_plotdata_call_volume
        global node_coloring
        global call_open_list
        global call_max_actval, call_open
        global 콜_인덱스, 콜_시가, 콜_현재가, 콜_저가, 콜_고가
        global call_low_touch, call_high_touch

        dt = datetime.datetime.now()

        index = call_행사가.index(result['단축코드'][5:8])
        #콜_인덱스 = index
        
        시가 = result['시가']
        현재가 = result['현재가']
        저가 = result['저가']
        고가 = result['고가']
        '''
        콜_시가 = result['시가']
        콜_현재가 = result['현재가']
        콜_저가 = result['저가']
        콜_고가 = result['고가']
        '''
        if 저가 != 고가:

            if not call_open[index]:

                call_open[index] = True
                
                # 콜 시가 갱신
                if round(float(시가), 2) > opt_search_start_value:
                    call_open_list.append(index)
                    call_open_list = list(set(call_open_list))
                else:
                    pass

                str = '[{0:02d}:{1:02d}:{2:02d}] Call Open List = {3}\r'.format(int(result['체결시간'][0:2]), \
                            int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), call_open_list)
                self.textBrowser.append(str)

                if index > atm_index:
                    call_below_atm_count += 1
                else:
                    pass
                
                if index == option_pairs_count - 1:

                    str = '[{0:02d}:{1:02d}:{2:02d}] 콜 최대 시작가 {3} 오픈되었습니다.\r'.format(\
                        int(result['체결시간'][0:2]), int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), 시가)
                    self.textBrowser.append(str)
                else:
                    pass
            else:
                pass

            if index == atm_index:

                call_atm_value = float(현재가)
                self.tableWidget_call.item(index, Option_column.행사가.value).setBackground(QBrush(노란색)) 
            else:
                self.tableWidget_call.item(index, Option_column.행사가.value).setBackground(QBrush(라임))
        else:
            pass        

        # 시가 갱신
        if 시가 != self.tableWidget_call.item(index, Option_column.시가.value).text():

            df_call.loc[index, '시가'] = round(float(시가), 2)
            df_plotdata_call.iloc[index][선물장간_시간차] = df_call.iloc[index]['시가']                
            
            item = QTableWidgetItem(시가)
            item.setTextAlignment(Qt.AlignCenter)

            if df_call.iloc[index]['시가'] > df_call.iloc[index]['종가']:
                item.setForeground(QBrush(적색))
            elif df_call.iloc[index]['시가'] < df_call.iloc[index]['종가']:
                item.setForeground(QBrush(청색))
            else:
                item.setForeground(QBrush(검정색))

            self.tableWidget_call.setItem(index, Option_column.시가.value, item)
            
            df_call.loc[index, '시가갭'] = df_call.iloc[index]['시가'] - df_call.iloc[index]['종가']
        
            gap_str = "{0:0.2f}".format(df_call.iloc[index]['시가갭'])

            item = QTableWidgetItem(gap_str)
            item.setTextAlignment(Qt.AlignCenter)

            if df_call.iloc[index]['시가'] > df_call.iloc[index]['종가']:
                item.setBackground(QBrush(콜기준가색))
                item.setForeground(QBrush(검정색))
            elif df_call.iloc[index]['시가'] < df_call.iloc[index]['종가']:
                item.setBackground(QBrush(풋기준가색))
                item.setForeground(QBrush(흰색))
            else:
                item.setBackground(QBrush(흰색))

            self.tableWidget_call.setItem(index, Option_column.시가갭.value, item)

            if df_call.iloc[index]['시가'] in 진성맥점:

                self.tableWidget_call.item(index, Option_column.시가.value).setBackground(QBrush(대맥점색))
                self.tableWidget_call.item(index, Option_column.시가.value).setForeground(QBrush(검정색))
            else:
                pass
            
            call_시가 = df_call['시가'].values.tolist()
            call_시가_node_list = self.make_node_list(call_시가)

            피봇 = self.calc_pivot(df_call.iloc[index]['전저'], df_call.iloc[index]['전고'],
                                    df_call.iloc[index]['종가'], df_call.iloc[index]['시가'])

            df_call.loc[index, '피봇'] = 피봇

            item = QTableWidgetItem("{0:0.2f}".format(피봇))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setItem(index, Option_column.피봇.value, item)                

            call_피봇 = df_call['피봇'].values.tolist()
            call_피봇_node_list = self.make_node_list(call_피봇)

            str = '[{0:02d}:{1:02d}:{2:02d}] Call {3:.2f} Open Update !!!\r'.format(int(result['체결시간'][0:2]), \
                        int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), df_call.iloc[index]['시가'])
            self.textBrowser.append(str)
                        
            #self.call_open_gap_update(index)
        else:
            pass

        # 현재가 갱신
        if 현재가 != self.tableWidget_call.item(index, Option_column.현재가.value).text()[0:4]:

            df_call.loc[index, '현재가'] = round(float(현재가), 2)
            df_plotdata_call.iloc[index][opt_x_idx] = float(현재가)

            if float(현재가) < float(self.tableWidget_call.item(index, Option_column.현재가.value).text()[0:4]):
                item = QTableWidgetItem(현재가 + '\n' + self.상태그림[0])
            elif float(현재가) > float(self.tableWidget_call.item(index, Option_column.현재가.value).text()[0:4]):
                item = QTableWidgetItem(현재가 + '\n' + self.상태그림[1])
            else:    
                item = QTableWidgetItem(현재가)
            
            item.setTextAlignment(Qt.AlignCenter)

            if float(현재가) < float(self.tableWidget_call.item(index, Option_column.현재가.value).text()[0:4]):
                item.setBackground(QBrush(lightskyblue))
            elif float(현재가) > float(self.tableWidget_call.item(index, Option_column.현재가.value).text()[0:4]):
                item.setBackground(QBrush(pink))
            else:
                item.setBackground(QBrush(옅은회색))

            if float(시가) < float(현재가):
                item.setForeground(QBrush(적색))
            elif float(시가) > float(현재가):
                item.setForeground(QBrush(청색))
            else:
                item.setForeground(QBrush(검정색))

            self.tableWidget_call.setItem(index, Option_column.현재가.value, item)
            
            대비 = round((float(현재가) - float(시가)), 2)
            df_call.loc[index, '대비'] = 대비

            call_db_percent[index] = (float(현재가) / float(시가) - 1) * 100
            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(대비, call_db_percent[index])

            item = QTableWidgetItem(gap_str)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setItem(index, Option_column.대비.value, item)
        else:
            pass

        # 저가 갱신
        if 저가 != self.tableWidget_call.item(index, Option_column.저가.value).text():

            call_low_touch = True

            item = QTableWidgetItem('▼')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.저가.value, item)
            
            df_call.loc[index, '저가'] = round(float(저가), 2)

            item = QTableWidgetItem(저가)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(회색))             
            self.tableWidget_call.setItem(index, Option_column.저가.value, item)

            # 시가 0.5 ~ 9.x 탐색
            if 저가_고가_갱신_탐색치1 < df_call.iloc[index]['시가'] < 저가_고가_갱신_탐색치2:

                if df_call.iloc[index]['전저'] >= df_call.iloc[index]['저가']:

                    str = '{0:0.2f}'.format(df_call.iloc[index]['전저']) + '\n' + '▼'

                    if str != self.tableWidget_call.item(index, Option_column.전저.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(청색))             
                        self.tableWidget_call.setItem(index, Option_column.전저.value, item)
                        self.tableWidget_call.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass

                if df_call.iloc[index]['월저'] >= df_call.iloc[index]['저가']:

                    str = '{0:0.2f}'.format(df_call.iloc[index]['월저']) + '\n' + '▼'

                    if str != self.tableWidget_call.item(index, Option_column.월저.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(청색))             
                        self.tableWidget_call.setItem(index, Option_column.월저.value, item)
                        self.tableWidget_call.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass

                if df_call.iloc[index]['기준가'] >= df_call.iloc[index]['저가']:

                    str = '{0:0.2f}'.format(df_call.iloc[index]['기준가']) + '\n' + '▼'

                    if str != self.tableWidget_call.item(index, Option_column.기준가.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(청색))             
                        self.tableWidget_call.setItem(index, Option_column.기준가.value, item)
                        self.tableWidget_call.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass
            else:
                pass

            진폭 = float(고가) - float(저가)
            df_call.loc[index, '진폭'] = 진폭
                                
            item = QTableWidgetItem("{0:0.2f}".format(진폭))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setItem(index, Option_column.진폭.value, item)                    

            call_저가 = df_call['저가'].values.tolist()
            call_저가_node_list = self.make_node_list(call_저가)

            str = '[{0:02d}:{1:02d}:{2:02d}] Call 저가 {3} Update...\r'.format(\
                int(result['체결시간'][0:2]), int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), round(float(저가), 2))
            self.textBrowser.append(str)

            if 1.1 < df_call.iloc[index]['저가'] < 10.0:

                self.opt_call_low_node_coloring()
            else:
                pass
        else:
            pass

        # 고가 갱신
        if 고가 != self.tableWidget_call.item(index, Option_column.고가.value).text():

            call_high_touch = True

            item = QTableWidgetItem('▲')
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.고가.value, item)
            
            df_call.loc[index, '고가'] = round(float(고가), 2)

            item = QTableWidgetItem(고가)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(회색))
            self.tableWidget_call.setItem(index, Option_column.고가.value, item)

            # 시가 0.5 ~ 9.x 탐색
            if 저가_고가_갱신_탐색치1 < df_call.iloc[index]['시가'] < 저가_고가_갱신_탐색치2:

                if df_call.iloc[index]['전고'] <= df_call.iloc[index]['고가']:

                    str = '{0:0.2f}'.format(df_call.iloc[index]['전고']) + '\n' + '▲'

                    if str != self.tableWidget_call.item(index, Option_column.전고.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(적색))             
                        self.tableWidget_call.setItem(index, Option_column.전고.value, item)
                        self.tableWidget_call.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass

                if df_call.iloc[index]['월고'] <= df_call.iloc[index]['고가']:

                    str = '{0:0.2f}'.format(df_call.iloc[index]['월고']) + '\n' + '▲'

                    if str != self.tableWidget_call.item(index, Option_column.월고.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(적색))             
                        self.tableWidget_call.setItem(index, Option_column.월고.value, item)
                        self.tableWidget_call.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass
            else:
                pass

            진폭 = float(고가) - float(저가)
            df_call.loc[index, '진폭'] = 진폭
                                
            item = QTableWidgetItem("{0:0.2f}".format(진폭))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setItem(index, Option_column.진폭.value, item)

            call_고가 = df_call['고가'].values.tolist()
            call_고가_node_list = self.make_node_list(call_고가)

            str = '[{0:02d}:{1:02d}:{2:02d}] Call 고가 {3} Update...\r'.format(\
                int(result['체결시간'][0:2]), int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), round(float(고가), 2))
            self.textBrowser.append(str)

            if 1.1 < df_call.iloc[index]['고가'] < 10.0:

                self.opt_call_high_node_coloring()
            else:
                pass
        else:
            pass               
                   
        opt_callreal_update_counter += 1
        
        return

    '''
    def call_open_update(self):

        global call_open, call_below_atm_count
        global df_call, call_gap_percent, df_plotdata_call
        global call_시가, call_시가_node_list, call_피봇, call_피봇_node_list
        global call_max_actval                
        global 콜시가갭합, 콜시가갭합_퍼센트, 콜시가갭합_단위평균

        index = call_행사가.index(call_result['단축코드'][5:8])

        if not call_open[index]:

            call_open[index] = True

            if index > atm_index:
                call_below_atm_count += 1
            else:
                pass
        else:
            pass
        
        if index != atm_index:
            self.tableWidget_call.item(index, Option_column.행사가.value).setBackground(QBrush(라임))
        else:
            self.tableWidget_call.item(index, Option_column.행사가.value).setBackground(QBrush(노란색))
        
        item = QTableWidgetItem(call_result['시가'])
        item.setTextAlignment(Qt.AlignCenter)

        if float(call_result['시가']) > df_call.iloc[index]['종가']:
            item.setForeground(QBrush(적색))
        elif float(call_result['시가']) < df_call.iloc[index]['종가']:
            item.setForeground(QBrush(청색))
        else:
            item.setForeground(QBrush(검정색))

        self.tableWidget_call.setItem(index, Option_column.시가.value, item)  

        if df_call.iloc[index]['종가'] > 0:     
        
            df_call.loc[index, '시가갭'] = float(call_result['시가']) - df_call.iloc[index]['종가']

            call_gap_percent[index] = (float(call_result['시가']) / df_call.iloc[index]['종가'] - 1) * 100
            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_call.iloc[index]['시가갭'], call_gap_percent[index])
        else:
            call_gap_percent[index] = 0.0
            gap_str = "{0:0.2f}".format(df_call.iloc[index]['시가갭'])

        item = QTableWidgetItem(gap_str)
        item.setTextAlignment(Qt.AlignCenter)

        if float(call_result['시가']) > df_call.iloc[index]['종가']:
            item.setBackground(QBrush(콜기준가색))
            item.setForeground(QBrush(검정색))
        elif float(call_result['시가']) < df_call.iloc[index]['종가']:
            item.setBackground(QBrush(풋기준가색))
            item.setForeground(QBrush(흰색))
        else:
            item.setBackground(QBrush(흰색))

        self.tableWidget_call.setItem(index, Option_column.시가갭.value, item)

        # 시가갭 갱신
        콜시가갭합 = round(df_call['시가갭'].sum(), 2)

        temp = call_gap_percent[:]
        call_gap_percent_local = [value for value in temp if not math.isnan(value)]
        call_gap_percent_local.sort()

        if call_gap_percent_local:

            tmp = np.array(call_gap_percent_local)            
            콜시가갭합_퍼센트 = int(round(np.mean(tmp), 2))
            call_str = repr(콜시가갭합) + '\n(' + repr(콜시가갭합_퍼센트) + '%' + ')'

            if call_str != self.tableWidget_call.horizontalHeaderItem(Option_column.시가갭.value).text():
                item = QTableWidgetItem(call_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.시가갭.value, item)
            else:
                pass
        else:
            print('call_gap_percent_local is empty...')    
        
        str = '[{0:02d}:{1:02d}:{2:02d}] Call[{3}] 시가 {4} Update됨 !!!\r'.format(int(call_result['체결시간'][0:2]), \
                        int(call_result['체결시간'][2:4]), int(call_result['체결시간'][4:6]), index+1, call_result['시가'])
        self.textBrowser.append(str)
        
        if index == option_pairs_count - 1:

            call_max_actval = True
        else:
            pass

        return
    '''

    def call_db_update(self):

        global call_진폭, 콜대비합, 콜대비합_단위평균

        temp = call_db_percent[:]
        call_db_percent_local = [value for value in temp if not math.isnan(value)]
        call_db_percent_local.sort()

        if call_db_percent_local:

            콜대비합 = round(df_call['대비'].sum(), 2)
            콜대비합_단위평균 = round(콜대비합/len(call_db_percent_local), 2) 

            tmp = np.array(call_db_percent_local)            
            대비평균 = int(round(np.mean(tmp), 2))
            call_str = repr(콜대비합_단위평균) + '\n(' + repr(대비평균) + '%' + ')'

            if call_str != self.tableWidget_call.horizontalHeaderItem(Option_column.대비.value).text():
                item = QTableWidgetItem(call_str)
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.대비.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass                               
        else:
            print('call_db_percent_local is empty...')

            콜대비합 = 0

        call_진폭 = df_call['진폭'].values.tolist()
        진폭최대값 = max(call_진폭)

        max_str = '{0:0.2f}'.format(진폭최대값)

        if max_str != self.tableWidget_call.horizontalHeaderItem(Option_column.진폭.value).text():
            item = QTableWidgetItem(max_str)
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.진폭.value, item)
            self.tableWidget_call.resizeColumnsToContents()
        else:
            pass 

        return

    def call_oi_update(self):
	
        global df_call
	
        index = call_행사가.index(call_result['단축코드'][5:8])

        if df_call.iloc[index]['시가'] > 0 and df_call.iloc[index]['저가'] < df_call.iloc[index]['고가']:

            if df_call.iloc[index]['현재가'] <= df_call.iloc[index]['시가갭']:

                수정미결 = call_result['미결제약정수량'] * df_call.iloc[index]['현재가']
                수정미결증감 = call_result['미결제약정증감'] * df_call.iloc[index]['현재가']
            else:
                수정미결 = call_result['미결제약정수량'] * (df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가갭'])
                수정미결증감 = call_result['미결제약정증감'] * (df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가갭'])

            df_call.loc[index, '수정미결'] = int(수정미결)
            df_call.loc[index, '수정미결증감'] = int(수정미결증감)

            수정미결 = format(df_call.iloc[index]['수정미결'], ',')

            if 수정미결 != self.tableWidget_call.item(index, Option_column.OI.value).text():

                item = QTableWidgetItem(수정미결)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setItem(index, Option_column.OI.value, item)
            else:
                pass          

            수정미결증감 = format(df_call.iloc[index]['수정미결증감'], ',')

            if 수정미결증감 != self.tableWidget_call.item(index, Option_column.OID.value).text():

                item = QTableWidgetItem(수정미결증감)
                item.setTextAlignment(Qt.AlignCenter)

                if call_result['미결제약정증감'] < 0:
                    item.setBackground(QBrush(라임))
                else:
                    item.setBackground(QBrush(흰색))

                self.tableWidget_call.setItem(index, Option_column.OID.value, item)
            else:
                pass
            
            수정미결합 = '{0}k'.format(format(int(df_call['수정미결'].sum()/1000), ','))

            if 수정미결합 != self.tableWidget_call.horizontalHeaderItem(Option_column.OI.value).text():
                item = QTableWidgetItem(수정미결합)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.OI.value, item)
            else:
                pass     
        else:
            pass

        return
    
    def call_volume_power_update(self):

        global df_call, df_call_volume, call_volume_total, df_plotdata_call_volume, call_volume    
        global 콜_순매수_체결량

        index = call_행사가.index(call_result['단축코드'][5:8])

        if df_call.iloc[index]['시가'] > 0 and df_call.iloc[index]['저가'] < df_call.iloc[index]['고가']:

            if df_call.iloc[index]['현재가'] <= df_call.iloc[index]['시가갭']:

                수정거래량 = (call_result['매수누적체결량'] - call_result['매도누적체결량']) * df_call.iloc[index]['현재가']
                매도누적체결량 = call_result['매도누적체결량'] * df_call.iloc[index]['현재가']
                매수누적체결량 = call_result['매수누적체결량'] * df_call.iloc[index]['현재가']

                if not overnight:

                    매도누적체결건수 = call_result['매도누적체결건수'] * df_call.iloc[index]['현재가']
                    매수누적체결건수 = call_result['매수누적체결건수'] * df_call.iloc[index]['현재가']
                else:
                    pass
            else:
                수정거래량 = (call_result['매수누적체결량'] - call_result['매도누적체결량']) * (df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가갭'])
                매도누적체결량 = call_result['매도누적체결량'] * (df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가갭'])
                매수누적체결량 = call_result['매수누적체결량'] * (df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가갭'])

                if not overnight:

                    매도누적체결건수 = call_result['매도누적체결건수'] * (df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가갭'])
                    매수누적체결건수 = call_result['매수누적체결건수'] * (df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가갭'])
                else:
                    pass

            df_call.loc[index, '수정거래량'] = int(수정거래량)
            df_call_volume.loc[index, '매도누적체결량'] = int(매도누적체결량)
            df_call_volume.loc[index, '매수누적체결량'] = int(매수누적체결량)

            df_call.loc[index, '거래량'] = call_result['누적거래량']

            if not overnight:

                df_call_volume.loc[index, '매도누적체결건수'] = int(매도누적체결건수)
                df_call_volume.loc[index, '매수누적체결건수'] = int(매수누적체결건수)
            else:
                pass
            
            수정거래량 = format(df_call.iloc[index]['수정거래량'], ',')

            if 수정거래량 != self.tableWidget_call.item(index, Option_column.VP.value).text():

                item = QTableWidgetItem(수정거래량)
                item.setTextAlignment(Qt.AlignCenter)

                if index == df_call['수정거래량'].idxmax():
                    item.setBackground(QBrush(라임))
                else:
                    item.setBackground(QBrush(흰색))

                self.tableWidget_call.setItem(index, Option_column.VP.value, item)
            else:
                pass
        else:
            pass        

        call_volume_total = df_call_volume['매수누적체결량'].sum() - df_call_volume['매도누적체결량'].sum()
        df_plotdata_call_volume.iloc[0][opt_x_idx] = call_volume_total

        순매수누적체결량 = format(call_volume_total, ',')

        if 순매수누적체결량 != self.tableWidget_call.horizontalHeaderItem(Option_column.VP.value).text():
            item = QTableWidgetItem(순매수누적체결량)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setHorizontalHeaderItem(Option_column.VP.value, item)
        else:
            pass
        
        call_volume = df_call_volume.sum()

        매수잔량 = format(call_volume['매수누적체결량'], ',')
        매도잔량 = format(call_volume['매도누적체결량'], ',')
        
        if not overnight:

            매수건수 = format(call_volume['매수누적체결건수'], ',')

            if 매수건수 != self.tableWidget_quote.item(0, 0).text():
                item = QTableWidgetItem(매수건수)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_quote.setItem(0, 0, item)
            else:
                pass

            매도건수 = format(call_volume['매도누적체결건수'], ',')

            if 매도건수 != self.tableWidget_quote.item(0, 1).text():
                item = QTableWidgetItem(매도건수)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_quote.setItem(0, 1, item)
            else:
                pass
        else:
            pass
        
        콜_순매수_체결량 = call_volume['매수누적체결량'] - call_volume['매도누적체결량']

        if 매수잔량 != self.tableWidget_quote.item(0, 2).text():
            item = QTableWidgetItem(매수잔량)
            item.setTextAlignment(Qt.AlignCenter)

            if 콜_순매수_체결량 > 0 and 풋_순매수_체결량 < 0:

                item.setBackground(QBrush(적색))
                item.setForeground(QBrush(검정색))

            elif 콜_순매수_체결량 < 0 and 풋_순매수_체결량 > 0:

                item.setBackground(QBrush(청색))
                item.setForeground(QBrush(흰색))

            elif 콜_순매수_체결량 < 0 and 풋_순매수_체결량 < 0:

                item.setBackground(QBrush(검정색))
                item.setForeground(QBrush(흰색))
            else:
                item.setBackground(QBrush(흰색))
                item.setForeground(QBrush(검정색))         

            self.tableWidget_quote.setItem(0, 2, item)
        else:
            pass

        temp = format(콜_순매수_체결량, ',')
        item_str = "{0}\n({1})".format(매도잔량, temp)

        if item_str != self.tableWidget_quote.item(0, 3).text():
            item = QTableWidgetItem(item_str)
            item.setTextAlignment(Qt.AlignCenter)

            if 콜_순매수_체결량 > 0 and 풋_순매수_체결량 < 0:

                item.setBackground(QBrush(적색))
                item.setForeground(QBrush(검정색))

            elif 콜_순매수_체결량 < 0 and 풋_순매수_체결량 > 0:

                item.setBackground(QBrush(청색))
                item.setForeground(QBrush(흰색))

            elif 콜_순매수_체결량 < 0 and 풋_순매수_체결량 < 0:

                item.setBackground(QBrush(검정색))
                item.setForeground(QBrush(흰색))
            else:
                item.setBackground(QBrush(흰색))
                item.setForeground(QBrush(검정색))            

            self.tableWidget_quote.setItem(0, 3, item)
        else:
            pass

        return

    def check_call_oloh(self, index):

        global call_ol, call_oh        

        if df_call.iloc[index]['시가'] >= oloh_cutoff:

            if df_call.iloc[index]['시가'] < 1.0:

                oloh_threshold = 1

            elif df_call.iloc[index]['시가'] >= 1.0 and df_call.iloc[index]['시가'] < 2.0:

                oloh_threshold = 2

            elif df_call.iloc[index]['시가'] >= 2.0 and df_call.iloc[index]['시가'] < 3.0:

                oloh_threshold = 3

            elif df_call.iloc[index]['시가'] >= 3.0 and df_call.iloc[index]['시가'] < 4.0:

                oloh_threshold = 4

            else:
                oloh_threshold = 5   

            # call OL/OH count
            if self.within_n_tick(df_call.iloc[index]['시가'], df_call.iloc[index]['저가'], oloh_threshold) \
                    and not self.within_n_tick(df_call.iloc[index]['시가'], df_call.iloc[index]['고가'], oloh_threshold):

                oloh_str = '▲'

                item = QTableWidgetItem(oloh_str)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(적색))
                item.setForeground(QBrush(검정색))
                self.tableWidget_call.setItem(index, Option_column.OLOH.value, item)

                call_ol[index] = True

            elif self.within_n_tick(df_call.iloc[index]['시가'], df_call.iloc[index]['고가'], oloh_threshold) \
                    and not self.within_n_tick(df_call.iloc[index]['시가'], df_call.iloc[index]['저가'], oloh_threshold):

                oloh_str = '▼'

                item = QTableWidgetItem(oloh_str)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(청색))
                item.setForeground(QBrush(흰색))
                self.tableWidget_call.setItem(index, Option_column.OLOH.value, item)

                call_oh[index] = True

            else:
                oloh_str = ''

                item = QTableWidgetItem(oloh_str)
                item.setBackground(QBrush(흰색))
                item.setForeground(QBrush(검정색))
                self.tableWidget_call.setItem(index, Option_column.OLOH.value, item)

                call_ol[index] = False
                call_oh[index] = False              
        else:
            pass
    
    def call_state_update(self):

        global call_open_count

        dt = datetime.datetime.now()

        call_open_count = len(call_open_list)

        if call_open[option_pairs_count - 1]:
            new_actval = repr(call_below_atm_count) + '/' + repr(call_open_count) + '*'
        else:
            new_actval = repr(call_below_atm_count) + '/' + repr(call_open_count)

        if new_actval != self.tableWidget_call.horizontalHeaderItem(1).text():
            item = QTableWidgetItem(new_actval)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setHorizontalHeaderItem(1, item)
            self.tableWidget_call.resizeColumnsToContents()
        else:
            pass 

        new_oloh = repr(call_ol.count(True)) + ':' + repr(call_oh.count(True))

        if new_oloh != self.tableWidget_call.horizontalHeaderItem(2).text():

            item = QTableWidgetItem(new_oloh)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setHorizontalHeaderItem(2, item)
            self.tableWidget_call.resizeColumnsToContents()

            str = '[{0:02d}:{1:02d}:{2:02d}] Call OLOH 갱신 !!!\r'.format(dt.hour, dt.minute, dt.second)
            self.textBrowser.append(str)

            # 차월물에서 OLOH 판단
            if fut_code == cmshcode:

                txt = '차월물 콜 오엘 {}개, 오에이치 {}개'.format(call_ol.count(True), call_oh.count(True))
                #Speak(txt)
            else:
                pass           
        else:
            pass                               

        return
    '''
    def call_open_gap_update(self, index):

        global df_call, call_gap_percent
        global df_plotdata_call
        global call_피봇, call_피봇_node_list

        dt = datetime.datetime.now()

        df_plotdata_call.iloc[index][선물장간_시간차] = df_call.iloc[index]['시가']
        
        gap_str = "{0:0.2f}".format(df_call.iloc[index]['시가갭'])

        item = QTableWidgetItem(gap_str)
        item.setTextAlignment(Qt.AlignCenter)

        if df_call.iloc[index]['시가'] > df_call.iloc[index]['종가']:
            item.setBackground(QBrush(콜기준가색))
            item.setForeground(QBrush(검정색))
        elif df_call.iloc[index]['시가'] < df_call.iloc[index]['종가']:
            item.setBackground(QBrush(풋기준가색))
            item.setForeground(QBrush(흰색))
        else:
            item.setBackground(QBrush(흰색))

        self.tableWidget_call.setItem(index, Option_column.시가갭.value, item)
        
        return
    '''
    def call_open_check(self):

        global df_call, call_below_atm_count
        global call_open, call_ol, call_oh
        global call_gap_percent, call_db_percent      
        global 콜시가갭합, 콜시가갭합_퍼센트
        global call_ol_count, call_oh_count
        global 콜대비합, 콜대비합_단위평균
        global call_open_count        
        global 콜시가갭합, 콜시가갭합_퍼센트, 콜시가갭합_단위평균 
        
        call_ol = [False] * option_pairs_count
        call_oh = [False] * option_pairs_count
        call_gap_percent = [NaN] * option_pairs_count
        call_db_percent = [NaN] * option_pairs_count
        call_below_atm_count = 0

        if not market_service:
            call_open = [False] * option_pairs_count
        else:
            pass

        dt = datetime.datetime.now()

        if call_open_list:

            loop_list = call_open_list

            if market_service:
                '''
                str = '[{0:02d}:{1:02d}:{2:02d}] Call Open Check List = {3}\r'.format(\
                    int(call_result['체결시간'][0:2]), int(call_result['체결시간'][2:4]), int(call_result['체결시간'][4:6]), call_open_list)
                self.textBrowser.append(str)
                '''
                pass
            else:
                #str = '[{0:02d}:{1:02d}:{2:02d}] Call Open Check List = {3}\r'.format(dt.hour, dt.minute, dt.second, call_open_list)
                #self.textBrowser.append(str)
                pass
        else:
            loop_list = opt_total_list

        for index in loop_list:

            if df_call.iloc[index]['시가'] > opt_search_start_value:
                
                if not market_service:

                    if index != atm_index:
                        self.tableWidget_call.item(index, Option_column.행사가.value).setBackground(QBrush(라임))
                    else:
                        self.tableWidget_call.item(index, Option_column.행사가.value).setBackground(QBrush(노란색))
                else:
                    pass
                
                if df_call.iloc[index]['종가'] > 0 and df_call.iloc[index]['저가'] < df_call.iloc[index]['고가']:

                    df_call.loc[index, '시가갭'] = df_call.iloc[index]['시가'] - df_call.iloc[index]['종가']

                    call_gap_percent[index] = (df_call.iloc[index]['시가'] / df_call.iloc[index]['종가'] - 1) * 100
                    gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_call.iloc[index]['시가갭'], call_gap_percent[index])

                    item = QTableWidgetItem(gap_str)
                    item.setTextAlignment(Qt.AlignCenter)

                    if df_call.iloc[index]['시가'] > df_call.iloc[index]['종가']:
                        item.setBackground(QBrush(콜기준가색))
                        item.setForeground(QBrush(검정색))
                    elif df_call.iloc[index]['시가'] < df_call.iloc[index]['종가']:
                        item.setBackground(QBrush(풋기준가색))
                        item.setForeground(QBrush(흰색))
                    else:
                        item.setBackground(QBrush(흰색))

                    self.tableWidget_call.setItem(index, Option_column.시가갭.value, item)
                else:
                    pass

                if df_call.iloc[index]['저가'] < df_call.iloc[index]['고가']:
                    
                    if index > atm_index:
                        call_below_atm_count += 1
                    else:
                        pass

                    if not market_service:

                        call_open[index] = True
                    else:
                        pass                    

                    if df_call.iloc[index]['시가'] >= oloh_cutoff:

                        if df_call.iloc[index]['시가'] < 1.0:

                            oloh_threshold = 1

                        elif df_call.iloc[index]['시가'] >= 1.0 and df_call.iloc[index]['시가'] < 2.0:

                            oloh_threshold = 2

                        elif df_call.iloc[index]['시가'] >= 2.0 and df_call.iloc[index]['시가'] < 3.0:

                            oloh_threshold = 3

                        elif df_call.iloc[index]['시가'] >= 3.0 and df_call.iloc[index]['시가'] < 4.0:

                            oloh_threshold = 4

                        else:
                            oloh_threshold = 5   

                        # call OL/OH count
                        if self.within_n_tick(df_call.iloc[index]['시가'], df_call.iloc[index]['저가'], oloh_threshold) \
                                and not self.within_n_tick(df_call.iloc[index]['시가'], df_call.iloc[index]['고가'], oloh_threshold):

                            oloh_str = '▲'

                            item = QTableWidgetItem(oloh_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(적색))
                            item.setForeground(QBrush(검정색))
                            self.tableWidget_call.setItem(index, Option_column.OLOH.value, item)

                            self.tableWidget_call.item(index, Option_column.시가.value).setBackground(QBrush(적색))
                            self.tableWidget_call.item(index, Option_column.시가.value).setForeground(QBrush(검정색))  

                            self.tableWidget_call.item(index, Option_column.저가.value).setBackground(QBrush(적색))
                            self.tableWidget_call.item(index, Option_column.저가.value).setForeground(QBrush(검정색))

                            call_ol[index] = True

                        elif self.within_n_tick(df_call.iloc[index]['시가'], df_call.iloc[index]['고가'], oloh_threshold) \
                                and not self.within_n_tick(df_call.iloc[index]['시가'], df_call.iloc[index]['저가'], oloh_threshold):

                            oloh_str = '▼'

                            item = QTableWidgetItem(oloh_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(청색))
                            item.setForeground(QBrush(흰색))
                            self.tableWidget_call.setItem(index, Option_column.OLOH.value, item)

                            self.tableWidget_call.item(index, Option_column.시가.value).setBackground(QBrush(적색))
                            self.tableWidget_call.item(index, Option_column.시가.value).setForeground(QBrush(검정색))  

                            self.tableWidget_call.item(index, Option_column.고가.value).setBackground(QBrush(적색))
                            self.tableWidget_call.item(index, Option_column.고가.value).setForeground(QBrush(검정색)) 

                            call_oh[index] = True
                        else:
                            oloh_str = ''

                            if oloh_str != self.tableWidget_call.item(index, Option_column.OLOH.value).text():
                                item = QTableWidgetItem(oloh_str)
                                item.setBackground(QBrush(흰색))
                                item.setForeground(QBrush(검정색))
                                self.tableWidget_call.setItem(index, Option_column.OLOH.value, item)
                            else:
                                pass

                            call_ol[index] = False
                            call_oh[index] = False
                    else:
                        pass
                else:
                    pass
                    
                if df_call.iloc[index]['시가'] > 0 and df_call.iloc[index]['저가'] < df_call.iloc[index]['고가']:

                    df_call.loc[index, '대비'] = \
                        round((df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가']), 2)
                    call_db_percent[index] = (df_call.iloc[index]['현재가'] / df_call.iloc[index]['시가'] - 1) * 100

                    gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_call.iloc[index]['대비'], call_db_percent[index])

                    if gap_str != self.tableWidget_call.item(index, Option_column.대비.value).text():

                        item = QTableWidgetItem(gap_str)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(index, Option_column.대비.value, item)
                    else:
                        pass
                else:
                    pass
            else:
                pass

        # Call Open Count 및 OLOH 표시
        call_open_count = len(call_open_list)

        if call_open[option_pairs_count - 1]:

            new_actval = repr(call_below_atm_count) + '/' + repr(call_open_count) + '*'
        else:
            new_actval = repr(call_below_atm_count) + '/' + repr(call_open_count)

        if new_actval != self.tableWidget_call.horizontalHeaderItem(1).text():
            item = QTableWidgetItem(new_actval)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setHorizontalHeaderItem(1, item)
        else:
            pass

        call_ol_count = call_ol.count(True)
        call_oh_count = call_oh.count(True)

        new_oloh = repr(call_ol_count) + ':' + repr(call_oh_count)

        if new_oloh != self.tableWidget_call.horizontalHeaderItem(2).text():
            item = QTableWidgetItem(new_oloh)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_call.setHorizontalHeaderItem(2, item)
        else:
            pass

        # 시가갭 갱신
        temp = call_gap_percent[:]
        call_gap_percent_local = [value for value in temp if not math.isnan(value)]
        call_gap_percent_local.sort()

        콜시가갭합 = round(df_call['시가갭'].sum(), 2)

        if call_gap_percent_local:
            
            콜시가갭합_단위평균 = round(콜시가갭합/len(call_gap_percent_local), 2)

            tmp = np.array(call_gap_percent_local)            
            콜시가갭합_퍼센트 = int(round(np.mean(tmp), 2))
            call_str = repr(콜시가갭합_단위평균) + '\n(' + repr(콜시가갭합_퍼센트) + '%' + ')'

            if call_str != self.tableWidget_call.horizontalHeaderItem(Option_column.시가갭.value).text():
                item = QTableWidgetItem(call_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.시가갭.value, item)
            else:
                pass
            '''
            str = '[{0:02d}:{1:02d}:{2:02d}] Call Open Check 콜시가갭합 = {3}, 퍼센트 = {4}\r'.\
                format(dt.hour, dt.minute, dt.second, 콜시가갭합, 콜시가갭합_퍼센트)
            self.textBrowser.append(str)
            '''
        else:
            print('call_gap_percent_local is empty...')

        # 대비 갱신
        temp = call_db_percent[:]
        call_db_percent_local = [value for value in temp if not math.isnan(value)]
        call_db_percent_local.sort()

        if call_db_percent_local:

            콜대비합 = round(df_call['대비'].sum(), 2)
            콜대비합_단위평균 = round(콜대비합/len(call_db_percent_local), 2)

            print('콜대비합 =', 콜대비합)

            tmp = np.array(call_db_percent_local)            
            대비평균 = int(round(np.mean(tmp), 2))
            call_str = repr(콜대비합_단위평균) + '\n(' + repr(대비평균) + '%' + ')'

            if call_str != self.tableWidget_call.horizontalHeaderItem(Option_column.대비.value).text():
                item = QTableWidgetItem(call_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.대비.value, item)
            else:
                pass            
        else:
            print('call_db_percent_local is empty...')

            콜대비합 = 0        

        self.tableWidget_call.resizeColumnsToContents()

        return
    '''
    def call_db_check(self):

        global df_call, call_db_percent

        for index in range(option_pairs_count):

            if df_call.iloc[index]['시가'] > opt_search_start_value:

                if df_call.iloc[index]['시가'] >= oloh_cutoff and df_call.iloc[index]['저가'] < df_call.iloc[index]['고가']:

                    df_call.loc[index, '대비'] = \
                        round((df_call.iloc[index]['현재가'] - df_call.iloc[index]['시가']), 2)
                    call_db_percent[index] = (df_call.iloc[index]['현재가'] / df_call.iloc[index]['시가'] - 1) * 100

                    gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_call.iloc[index]['대비'], call_db_percent[index])

                    if gap_str != self.tableWidget_call.item(index, Option_column.대비.value).text():

                        item = QTableWidgetItem(gap_str)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_call.setItem(index, Option_column.대비.value, item)
                    else:
                        pass
                else:
                    pass
            else:
                pass            

        temp = call_db_percent[:]
        call_db_percent_local = [value for value in temp if not math.isnan(value)]
        call_db_percent_local.sort()

        if call_db_percent_local:

            sumc = round(df_call['대비'].sum(), 2)
            tmp = np.array(call_db_percent_local)            
            meanc = int(round(np.mean(tmp), 2))
            call_str = repr(sumc) + '\n (' + repr(meanc) + '%' + ')'

            if call_str != self.tableWidget_call.horizontalHeaderItem(Option_column.대비.value).text():
                item = QTableWidgetItem(call_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_call.setHorizontalHeaderItem(Option_column.대비.value, item)
                self.tableWidget_call.resizeColumnsToContents()
            else:
                pass
        else:
            print('call_db_percent_local is empty...')

        return
    '''
    # 풋 표시
    def put_display(self, result):

        global put_result, put_open, put_above_atm_count
        global df_put, df_plotdata_put, df_plotdata_put_oi
        global put_atm_value
        global put_시가, put_시가_node_list, put_피봇, put_피봇_node_list, 풋시가리스트
        global put_저가, put_저가_node_list, put_고가, put_고가_node_list
        global put_gap_percent, put_db_percent
        global opt_putreal_update_counter
        global df_put_volume, put_volume_total, df_plotdata_put_volume, df_plotdata_volume_cha
        global put_open_list
        global put_max_actval, put_open
        global 풋_인덱스, 풋_시가, 풋_현재가, 풋_저가, 풋_고가
        global put_low_touch, put_high_touch

        dt = datetime.datetime.now()

        index = put_행사가.index(result['단축코드'][5:8])
        #풋_인덱스 = index
        
        시가 = result['시가']
        현재가 = result['현재가']
        저가 = result['저가']
        고가 = result['고가']
        '''
        풋_시가 = result['시가']
        풋_현재가 = result['현재가']
        풋_저가 = result['저가']
        풋_고가 = result['고가']
        '''
        if 저가 != 고가:

            if not put_open[index]:

                put_open[index] = True
                
                # 풋 시가 갱신
                if round(float(시가), 2) > opt_search_start_value:
                    put_open_list.append(index)
                    put_open_list = list(set(put_open_list))
                else:
                    pass

                str = '[{0:02d}:{1:02d}:{2:02d}] Put Open List = {3}\r'.format(int(result['체결시간'][0:2]), \
                            int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), put_open_list)
                self.textBrowser.append(str)

                if index < atm_index:
                    put_above_atm_count += 1
                else:
                    pass

                if index == 0:

                    str = '[{0:02d}:{1:02d}:{2:02d}] 풋 최대 시작가 {3} 오픈되었습니다.\r'.format(\
                        int(result['체결시간'][0:2]), int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), 시가)
                    self.textBrowser.append(str)
                else:
                    pass
            else:
                pass

            if index == atm_index:
                put_atm_value = float(현재가)
                self.tableWidget_put.item(index, Option_column.행사가.value).setBackground(QBrush(노란색))
            else:
                self.tableWidget_put.item(index, Option_column.행사가.value).setBackground(QBrush(라임))            
        else:
            pass        
        
        # 시가 갱신
        if 시가 != self.tableWidget_put.item(index, Option_column.시가.value).text():

            df_put.loc[index, '시가'] = round(float(시가), 2)
            df_plotdata_put.iloc[index][선물장간_시간차] = df_put.iloc[index]['시가']
            
            item = QTableWidgetItem(시가)
            item.setTextAlignment(Qt.AlignCenter)

            if df_put.iloc[index]['시가'] > df_put.iloc[index]['종가']:
                item.setForeground(QBrush(적색))
            elif df_put.iloc[index]['시가'] < df_put.iloc[index]['종가']:
                item.setForeground(QBrush(청색))
            else:
                item.setForeground(QBrush(검정색))

            self.tableWidget_put.setItem(index, Option_column.시가.value, item)

            df_put.loc[index, '시가갭'] = df_put.iloc[index]['시가'] - df_put.iloc[index]['종가']
        
            gap_str = "{0:0.2f}".format(df_put.iloc[index]['시가갭'])

            item = QTableWidgetItem(gap_str)
            item.setTextAlignment(Qt.AlignCenter)

            if df_put.iloc[index]['시가'] > df_put.iloc[index]['종가']:
                item.setBackground(QBrush(콜기준가색))
                item.setForeground(QBrush(검정색))
            elif df_put.iloc[index]['시가'] < df_put.iloc[index]['종가']:
                item.setBackground(QBrush(풋기준가색))
                item.setForeground(QBrush(흰색))
            else:
                item.setBackground(QBrush(흰색))

            self.tableWidget_put.setItem(index, Option_column.시가갭.value, item)

            if df_put.iloc[index]['시가'] in 진성맥점:

                self.tableWidget_put.item(index, Option_column.시가.value).setBackground(QBrush(대맥점색))
                self.tableWidget_put.item(index, Option_column.시가.value).setForeground(QBrush(검정색))
            else:
                pass
            
            put_시가 = df_put['시가'].values.tolist()
            put_시가_node_list = self.make_node_list(put_시가)
            
            피봇 = self.calc_pivot(df_put.iloc[index]['전저'], df_put.iloc[index]['전고'],
                                    df_put.iloc[index]['종가'], df_put.iloc[index]['시가'])

            df_put.loc[index, '피봇'] = 피봇

            item = QTableWidgetItem("{0:0.2f}".format(피봇))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setItem(index, Option_column.피봇.value, item)

            put_피봇 = df_put['피봇'].values.tolist()
            put_피봇_node_list = self.make_node_list(put_피봇)

            str = '[{0:02d}:{1:02d}:{2:02d}] Put {3:.2f} Open Update !!!\r'.format(int(result['체결시간'][0:2]), \
                        int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), df_put.iloc[index]['시가'])
            self.textBrowser.append(str)
                        
            #self.put_open_gap_update(index)
        else:
            pass

        # 현재가 갱신
        if 현재가 != self.tableWidget_put.item(index, Option_column.현재가.value).text()[0:4]:

            df_put.loc[index, '현재가'] = round(float(현재가), 2)
            df_plotdata_put.iloc[index][opt_x_idx] = float(현재가)

            if float(현재가) < float(self.tableWidget_put.item(index, Option_column.현재가.value).text()[0:4]):
                item = QTableWidgetItem(현재가 + '\n' + self.상태그림[0])
            elif float(현재가) > float(self.tableWidget_put.item(index, Option_column.현재가.value).text()[0:4]):
                item = QTableWidgetItem(현재가 + '\n' + self.상태그림[1])
            else:    
                item = QTableWidgetItem(현재가)

            item.setTextAlignment(Qt.AlignCenter)

            if float(현재가) < float(self.tableWidget_put.item(index, Option_column.현재가.value).text()[0:4]):
                item.setBackground(QBrush(lightskyblue))
            elif float(현재가) > float(self.tableWidget_put.item(index, Option_column.현재가.value).text()[0:4]):
                item.setBackground(QBrush(pink))
            else:
                item.setBackground(QBrush(옅은회색))

            if float(시가) < float(현재가):
                item.setForeground(QBrush(적색))
            elif float(시가) > float(현재가):
                item.setForeground(QBrush(청색))
            else:
                item.setForeground(QBrush(검정색))

            self.tableWidget_put.setItem(index, Option_column.현재가.value, item)
            
            대비 = round((float(현재가) - float(시가)), 2)
            df_put.loc[index, '대비'] = 대비

            put_db_percent[index] = (float(현재가) / float(시가) - 1) * 100
            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(대비, put_db_percent[index])  

            item = QTableWidgetItem(gap_str)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setItem(index, Option_column.대비.value, item)
        else:
            pass

        # 저가 갱신
        if 저가 != self.tableWidget_put.item(index, Option_column.저가.value).text():

            put_low_touch = True

            item = QTableWidgetItem('▼')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.저가.value, item)
            
            df_put.loc[index, '저가'] = round(float(저가), 2)

            item = QTableWidgetItem(저가)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(회색))
            self.tableWidget_put.setItem(index, Option_column.저가.value, item)

            # 시가 0.5 ~ 9.x 탐색
            if 저가_고가_갱신_탐색치1 < df_put.iloc[index]['시가'] < 저가_고가_갱신_탐색치2:

                if df_put.iloc[index]['전저'] >= df_put.iloc[index]['저가']:

                    str = '{0:0.2f}'.format(df_put.iloc[index]['전저']) + '\n' + '▼'

                    if str != self.tableWidget_put.item(index, Option_column.전저.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(청색))             
                        self.tableWidget_put.setItem(index, Option_column.전저.value, item)
                        self.tableWidget_put.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass

                if df_put.iloc[index]['월저'] >= df_put.iloc[index]['저가']:

                    str = '{0:0.2f}'.format(df_put.iloc[index]['월저']) + '\n' + '▼'

                    if str != self.tableWidget_put.item(index, Option_column.월저.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(청색))             
                        self.tableWidget_put.setItem(index, Option_column.월저.value, item)
                        self.tableWidget_put.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass

                if df_put.iloc[index]['기준가'] >= df_put.iloc[index]['저가']:

                    str = '{0:0.2f}'.format(df_put.iloc[index]['기준가']) + '\n' + '▼'

                    if str != self.tableWidget_put.item(index, Option_column.기준가.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(청색))             
                        self.tableWidget_put.setItem(index, Option_column.기준가.value, item)
                        self.tableWidget_put.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass
            else:
                pass

            진폭 = float(고가) - float(저가)
            df_put.loc[index, '진폭'] = 진폭
                                
            item = QTableWidgetItem("{0:0.2f}".format(진폭))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setItem(index, Option_column.진폭.value, item)

            put_저가 = df_put['저가'].values.tolist()
            put_저가_node_list = self.make_node_list(put_저가)

            str = '[{0:02d}:{1:02d}:{2:02d}] Put 저가 {3} Update...\r'.format(\
                int(result['체결시간'][0:2]), int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), round(float(저가), 2))
            self.textBrowser.append(str)

            if 1.1 < df_put.iloc[index]['저가'] < 10.0:

                self.opt_put_low_node_coloring()
            else:
                pass
        else:
            pass

        # 고가 갱신
        if 고가 != self.tableWidget_put.item(index, Option_column.고가.value).text():

            put_high_touch = True

            item = QTableWidgetItem('▲')
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.고가.value, item)
            
            df_put.loc[index, '고가'] = round(float(고가), 2)

            item = QTableWidgetItem(고가)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(회색))
            self.tableWidget_put.setItem(index, Option_column.고가.value, item)

            # 시가 0.5 ~ 9.x 탐색
            if 저가_고가_갱신_탐색치1 < df_put.iloc[index]['시가'] < 저가_고가_갱신_탐색치2:

                if df_put.iloc[index]['전고'] <= df_put.iloc[index]['고가']:

                    str = '{0:0.2f}'.format(df_put.iloc[index]['전고']) + '\n' + '▲'

                    if str != self.tableWidget_put.item(index, Option_column.전고.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(적색))             
                        self.tableWidget_put.setItem(index, Option_column.전고.value, item)
                        self.tableWidget_put.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass

                if df_put.iloc[index]['월고'] <= df_put.iloc[index]['고가']:

                    str = '{0:0.2f}'.format(df_put.iloc[index]['월고']) + '\n' + '▲'

                    if str != self.tableWidget_put.item(index, Option_column.월고.value).text():
                        item = QTableWidgetItem(str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setForeground(QBrush(적색))             
                        self.tableWidget_put.setItem(index, Option_column.월고.value, item)
                        self.tableWidget_put.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass
            else:
                pass

            진폭 = float(고가) - float(저가)
            df_put.loc[index, '진폭'] = 진폭
                                
            item = QTableWidgetItem("{0:0.2f}".format(진폭))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setItem(index, Option_column.진폭.value, item)

            put_고가 = df_put['고가'].values.tolist()
            put_고가_node_list = self.make_node_list(put_고가)

            str = '[{0:02d}:{1:02d}:{2:02d}] Put 고가 {3} Update...\r'.format(\
                int(result['체결시간'][0:2]), int(result['체결시간'][2:4]), int(result['체결시간'][4:6]), round(float(고가), 2))
            self.textBrowser.append(str)

            if 1.1 < df_put.iloc[index]['고가'] < 10.0:

                self.opt_put_high_node_coloring()
            else:
                pass            
        else:
            pass                
                    
        opt_putreal_update_counter += 1            

        return
    
    '''
    def put_open_update(self):

        global put_open, put_above_atm_count
        global df_put, put_gap_percent, df_plotdata_put
        global put_시가, put_시가_node_list, put_피봇, put_피봇_node_list
        global put_max_actval        
        global 풋시가갭합, 풋시가갭합_퍼센트, 풋시가갭합_단위평균 

        index = put_행사가.index(put_result['단축코드'][5:8])

        if not put_open[index]:

            put_open[index] = True

            if index < atm_index:
                put_above_atm_count += 1
            else:
                pass
        else:
            pass
        
        if index != atm_index:
            self.tableWidget_put.item(index, Option_column.행사가.value).setBackground(QBrush(라임))
        else:
            self.tableWidget_put.item(index, Option_column.행사가.value).setBackground(QBrush(노란색))
        
        item = QTableWidgetItem(put_result['시가'])
        item.setTextAlignment(Qt.AlignCenter)

        if float(put_result['시가']) > df_put.iloc[index]['종가']:
            item.setForeground(QBrush(적색))
        elif float(put_result['시가']) < df_put.iloc[index]['종가']:
            item.setForeground(QBrush(청색))
        else:
            item.setForeground(QBrush(검정색))

        self.tableWidget_put.setItem(index, Option_column.시가.value, item)

        if df_put.iloc[index]['종가'] > 0:
            
            df_put.loc[index, '시가갭'] = float(put_result['시가']) - df_call.iloc[index]['종가']

            put_gap_percent[index] = (float(put_result['시가']) / df_put.iloc[index]['종가'] - 1) * 100
            gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_put.iloc[index]['시가갭'], put_gap_percent[index])
        else:
            put_gap_percent[index] = 0.0
            gap_str = "{0:0.2f}".format(df_put.iloc[index]['시가갭'])

        item = QTableWidgetItem(gap_str)
        item.setTextAlignment(Qt.AlignCenter)

        if float(put_result['시가']) > df_put.iloc[index]['종가']:
            item.setBackground(QBrush(콜기준가색))
            item.setForeground(QBrush(검정색))
        elif float(put_result['시가']) < df_put.iloc[index]['종가']:
            item.setBackground(QBrush(풋기준가색))
            item.setForeground(QBrush(흰색))
        else:
            item.setBackground(QBrush(흰색))

        self.tableWidget_put.setItem(index, Option_column.시가갭.value, item)

        # 시가갭 갱신
        풋시가갭합 = round(df_put['시가갭'].sum(), 2)

        temp = put_gap_percent[:]
        put_gap_percent_local = [value for value in temp if not math.isnan(value)]
        put_gap_percent_local.sort()

        if put_gap_percent_local:

            tmp = np.array(put_gap_percent_local)            
            풋시가갭합_퍼센트 = int(round(np.mean(tmp), 2))
            put_str = repr(풋시가갭합) + '\n(' + repr(풋시가갭합_퍼센트) + '%' + ')'

            if put_str != self.tableWidget_put.horizontalHeaderItem(Option_column.시가갭.value).text():
                item = QTableWidgetItem(put_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.시가갭.value, item)
            else:
                pass
        else:
            print('put_gap_percent_local is empty...')
        
        str = '[{0:02d}:{1:02d}:{2:02d}] Put[{3}] 시가 {4} Update됨 !!!\r'.format(int(put_result['체결시간'][0:2]), \
                        int(put_result['체결시간'][2:4]), int(put_result['체결시간'][4:6]), index+1, put_result['시가'])
        self.textBrowser.append(str)
        
        if index == 0:

            put_max_actval = True
        else:
            pass

        return
    '''
    
    def put_db_update(self):

        global put_진폭, 풋대비합, 풋대비합_단위평균 

        temp = put_db_percent[:]
        put_db_percent_local = [value for value in temp if not math.isnan(value)]
        put_db_percent_local.sort()

        if put_db_percent_local:

            풋대비합 = round(df_put['대비'].sum(), 2)
            풋대비합_단위평균 = round(풋대비합/len(put_db_percent_local), 2)

            tmp = np.array(put_db_percent_local)            
            대비평균 = int(round(np.mean(tmp), 2))
            put_str = repr(풋대비합_단위평균) + '\n(' + repr(대비평균) + '%' + ')'

            if put_str != self.tableWidget_put.horizontalHeaderItem(Option_column.대비.value).text():
                item = QTableWidgetItem(put_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.대비.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass            
        else:
            print('put_db_percent_local is empty...')

            풋대비합 = 0

        put_진폭 = df_put['진폭'].values.tolist()
        진폭최대값 = max(put_진폭)

        max_str = '{0:0.2f}'.format(진폭최대값)

        if max_str != self.tableWidget_put.horizontalHeaderItem(Option_column.진폭.value).text():
            item = QTableWidgetItem(max_str)
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.진폭.value, item)
            self.tableWidget_put.resizeColumnsToContents()
        else:
            pass 

        return

    def put_oi_update(self):
	
        global df_put
		
        index = put_행사가.index(put_result['단축코드'][5:8])

        if df_put.iloc[index]['시가'] > 0 and df_put.iloc[index]['저가'] < df_put.iloc[index]['고가']:

            if df_put.iloc[index]['현재가'] <= df_put.iloc[index]['시가갭']:

                수정미결 = put_result['미결제약정수량'] * df_put.iloc[index]['현재가']
                수정미결증감 = put_result['미결제약정증감'] * df_put.iloc[index]['현재가']
            else:
                수정미결 = put_result['미결제약정수량'] * (df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가갭'])
                수정미결증감 = put_result['미결제약정증감'] * (df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가갭'])

            df_put.loc[index, '수정미결'] = int(수정미결)
            df_put.loc[index, '수정미결증감'] = int(수정미결증감)

            수정미결 = format(df_put.iloc[index]['수정미결'], ',')

            if 수정미결 != self.tableWidget_put.item(index, Option_column.OI.value).text():

                item = QTableWidgetItem(수정미결)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setItem(index, Option_column.OI.value, item)
            else:
                pass            

            미결증감 = format(df_put.iloc[index]['수정미결증감'], ',')

            if 미결증감 != self.tableWidget_put.item(index, Option_column.OID.value).text():

                item = QTableWidgetItem(미결증감)
                item.setTextAlignment(Qt.AlignCenter)

                if put_result['미결제약정증감'] < 0:
                    item.setBackground(QBrush(라임))
                else:
                    item.setBackground(QBrush(흰색))

                self.tableWidget_put.setItem(index, Option_column.OID.value, item)
            else:
                pass

            수정미결합 = '{0}k'.format(format(int(df_put['수정미결'].sum()/1000), ','))

            if 수정미결합 != self.tableWidget_put.horizontalHeaderItem(Option_column.OI.value).text():
                item = QTableWidgetItem(수정미결합)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.OI.value, item)
            else:
                pass
        else:
            pass

        return
        
    def put_volume_power_update(self):

        global df_put, df_put_volume, put_volume_total, df_plotdata_put_volume, df_plotdata_volume_cha, put_volume
        global 풋_순매수_체결량

        index = put_행사가.index(put_result['단축코드'][5:8])

        if df_put.iloc[index]['시가'] > 0 and df_put.iloc[index]['저가'] < df_put.iloc[index]['고가']:

            if df_put.iloc[index]['현재가'] <= df_put.iloc[index]['시가갭']:

                수정거래량 = (put_result['매수누적체결량'] - put_result['매도누적체결량']) * df_put.iloc[index]['현재가']
                매도누적체결량 = put_result['매도누적체결량'] * df_put.iloc[index]['현재가']
                매수누적체결량 = put_result['매수누적체결량'] * df_put.iloc[index]['현재가']

                if not overnight:

                    매도누적체결건수 = put_result['매도누적체결건수'] * df_put.iloc[index]['현재가']
                    매수누적체결건수 = put_result['매수누적체결건수'] * df_put.iloc[index]['현재가']
                else:
                    pass
            else:
                수정거래량 = (put_result['매수누적체결량'] - put_result['매도누적체결량']) * (df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가갭'])
                매도누적체결량 = put_result['매도누적체결량'] * (df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가갭'])
                매수누적체결량 = put_result['매수누적체결량'] * (df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가갭'])

                if not overnight:

                    매도누적체결건수 = put_result['매도누적체결건수'] * (df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가갭'])
                    매수누적체결건수 = put_result['매수누적체결건수'] * (df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가갭'])
                else:
                    pass

            df_put.loc[index, '수정거래량'] = int(수정거래량)
            df_put_volume.loc[index, '매도누적체결량'] = int(매도누적체결량)
            df_put_volume.loc[index, '매수누적체결량'] = int(매수누적체결량)

            df_put.loc[index, '거래량'] = put_result['누적거래량']

            if not overnight:
                
                df_put_volume.loc[index, '매도누적체결건수'] = int(매도누적체결건수)
                df_put_volume.loc[index, '매수누적체결건수'] = int(매수누적체결건수)
            else:
                pass
            
            수정거래량 = format(df_put.iloc[index]['수정거래량'], ',')

            if 수정거래량 != self.tableWidget_put.item(index, Option_column.VP.value).text():

                item = QTableWidgetItem(수정거래량)
                item.setTextAlignment(Qt.AlignCenter)

                if index == df_put['수정거래량'].idxmax():
                    item.setBackground(QBrush(라임))
                else:
                    item.setBackground(QBrush(흰색))

                self.tableWidget_put.setItem(index, Option_column.VP.value, item)
            else:
                pass
        else:
            pass        

        put_volume_total = df_put_volume['매수누적체결량'].sum() - df_put_volume['매도누적체결량'].sum()
        df_plotdata_put_volume.iloc[0][opt_x_idx] = put_volume_total

        df_plotdata_volume_cha.iloc[0][opt_x_idx] = call_volume_total - put_volume_total

        순매수누적체결량 = format(put_volume_total, ',')

        if 순매수누적체결량 != self.tableWidget_put.horizontalHeaderItem(Option_column.VP.value).text():
            item = QTableWidgetItem(순매수누적체결량)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setHorizontalHeaderItem(Option_column.VP.value, item)
        else:
            pass        

        put_volume = df_put_volume.sum()

        매수잔량 = format(put_volume['매수누적체결량'], ',')
        매도잔량 = format(put_volume['매도누적체결량'], ',')

        if not overnight:

            매수건수 = format(put_volume['매수누적체결건수'], ',')

            if 매수건수 != self.tableWidget_quote.item(0, 4).text():
                item = QTableWidgetItem(매수건수)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_quote.setItem(0, 4, item)
            else:
                pass

            매도건수 = format(put_volume['매도누적체결건수'], ',')

            if 매도건수 != self.tableWidget_quote.item(0, 5).text():
                item = QTableWidgetItem(매도건수)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_quote.setItem(0, 5, item)
            else:
                pass
        else:
            pass
        
        풋_순매수_체결량 = put_volume['매수누적체결량'] - put_volume['매도누적체결량']

        if 매수잔량 != self.tableWidget_quote.item(0, 6).text():
            item = QTableWidgetItem(매수잔량)
            item.setTextAlignment(Qt.AlignCenter)

            if 콜_순매수_체결량 > 0 and 풋_순매수_체결량 < 0:

                item.setBackground(QBrush(적색))
                item.setForeground(QBrush(검정색))

            elif 콜_순매수_체결량 < 0 and 풋_순매수_체결량 > 0:

                item.setBackground(QBrush(청색))
                item.setForeground(QBrush(흰색))
                
            elif 콜_순매수_체결량 < 0 and 풋_순매수_체결량 < 0:

                item.setBackground(QBrush(검정색))
                item.setForeground(QBrush(흰색))
            else:
                item.setBackground(QBrush(흰색))
                item.setForeground(QBrush(검정색))   

            self.tableWidget_quote.setItem(0, 6, item)
        else:
            pass

        temp = format(풋_순매수_체결량, ',')
        item_str = "{0}\n({1})".format(매도잔량, temp)

        if item_str != self.tableWidget_quote.item(0, 7).text():
            item = QTableWidgetItem(item_str)
            item.setTextAlignment(Qt.AlignCenter)

            if 콜_순매수_체결량 > 0 and 풋_순매수_체결량 < 0:

                item.setBackground(QBrush(적색))
                item.setForeground(QBrush(검정색))

            elif 콜_순매수_체결량 < 0 and 풋_순매수_체결량 > 0:

                item.setBackground(QBrush(청색))
                item.setForeground(QBrush(흰색))
                
            elif 콜_순매수_체결량 < 0 and 풋_순매수_체결량 < 0:

                item.setBackground(QBrush(검정색))
                item.setForeground(QBrush(흰색))
            else:
                item.setBackground(QBrush(흰색))
                item.setForeground(QBrush(검정색))   

            self.tableWidget_quote.setItem(0, 7, item)
        else:
            pass

        return

    def check_put_oloh(self, index):

        global put_ol, put_oh        

        if df_put.iloc[index]['시가'] >= oloh_cutoff:

            if df_put.iloc[index]['시가'] < 1.0:

                oloh_threshold = 1

            elif df_put.iloc[index]['시가'] >= 1.0 and df_put.iloc[index]['시가'] < 2.0:

                oloh_threshold = 2

            elif df_put.iloc[index]['시가'] >= 2.0 and df_put.iloc[index]['시가'] < 3.0:

                oloh_threshold = 3

            elif df_put.iloc[index]['시가'] >= 3.0 and df_put.iloc[index]['시가'] < 4.0:

                oloh_threshold = 4

            else:
                oloh_threshold = 5   

            # put OL/OH count
            if self.within_n_tick(df_put.iloc[index]['시가'], df_put.iloc[index]['저가'], oloh_threshold) \
                    and not self.within_n_tick(df_put.iloc[index]['시가'], df_put.iloc[index]['고가'], oloh_threshold):

                oloh_str = '▲'

                item = QTableWidgetItem(oloh_str)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(청색))
                item.setForeground(QBrush(흰색))
                self.tableWidget_put.setItem(index, Option_column.OLOH.value, item)

                put_ol[index] = True

            elif self.within_n_tick(df_put.iloc[index]['시가'], df_put.iloc[index]['고가'], oloh_threshold) \
                    and not self.within_n_tick(df_put.iloc[index]['시가'], df_put.iloc[index]['저가'], oloh_threshold):

                oloh_str = '▼'

                item = QTableWidgetItem(oloh_str)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(적색))
                item.setForeground(QBrush(검정색))
                self.tableWidget_put.setItem(index, Option_column.OLOH.value, item)

                put_oh[index] = True

            else:
                oloh_str = ''

                item = QTableWidgetItem(oloh_str)
                item.setBackground(QBrush(흰색))
                item.setForeground(QBrush(검정색))
                self.tableWidget_put.setItem(index, Option_column.OLOH.value, item)

                put_ol[index] = False
                put_oh[index] = False    
        else:
            pass
    
    def put_state_update(self):

        global put_open_count

        dt = datetime.datetime.now()

        put_open_count = len(put_open_list)

        if put_open[0]:
            new_actval = repr(put_above_atm_count) + '/' + repr(put_open_count) + '*'
        else:
            new_actval = repr(put_above_atm_count) + '/' + repr(put_open_count)

        if new_actval != self.tableWidget_put.horizontalHeaderItem(1).text():
            item = QTableWidgetItem(new_actval)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setHorizontalHeaderItem(1, item)
            self.tableWidget_put.resizeColumnsToContents()
        else:
            pass

        new_oloh = repr(put_ol.count(True)) + ':' + repr(put_oh.count(True))

        if new_oloh != self.tableWidget_put.horizontalHeaderItem(2).text():

            item = QTableWidgetItem(new_oloh)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setHorizontalHeaderItem(2, item)
            self.tableWidget_put.resizeColumnsToContents()

            str = '[{0:02d}:{1:02d}:{2:02d}] Put OLOH 갱신 !!!\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
            self.textBrowser.append(str)

            # 차월물에서 OLOH 판단
            if fut_code == cmshcode:

                txt = '차월물 풋 오엘 {}개, 오에이치 {}개'.format(put_ol.count(True), put_oh.count(True))
                #Speak(txt)
            else:
                pass           
        else:
            pass           

        return
    '''
    def put_open_gap_update(self, index):

        global df_put, put_gap_percent
        global df_plotdata_put
        global put_피봇, put_피봇_node_list

        dt = datetime.datetime.now()

        df_plotdata_put.iloc[index][선물장간_시간차] = df_put.iloc[index]['시가']
        
        gap_str = "{0:0.2f}".format(df_put.iloc[index]['시가갭'])

        item = QTableWidgetItem(gap_str)
        item.setTextAlignment(Qt.AlignCenter)

        if df_put.iloc[index]['시가'] > df_put.iloc[index]['종가']:
            item.setBackground(QBrush(콜기준가색))
            item.setForeground(QBrush(검정색))
        elif df_put.iloc[index]['시가'] < df_put.iloc[index]['종가']:
            item.setBackground(QBrush(풋기준가색))
            item.setForeground(QBrush(흰색))
        else:
            item.setBackground(QBrush(흰색))

        self.tableWidget_put.setItem(index, Option_column.시가갭.value, item)
        
        return
    '''
    def put_open_check(self):

        global df_put, put_above_atm_count
        global put_open, put_ol, put_oh
        global put_gap_percent, put_db_percent     
        global 풋시가갭합, 풋시가갭합_퍼센트
        global put_ol_count, put_oh_count
        global 풋대비합, 풋대비합_단위평균 
        global put_open_count
        global 풋시가갭합, 풋시가갭합_퍼센트, 풋시가갭합_단위평균
        
        put_ol = [False] * option_pairs_count
        put_oh = [False] * option_pairs_count
        put_gap_percent = [NaN] * option_pairs_count
        put_db_percent = [NaN] * option_pairs_count
        put_above_atm_count = 0

        if not market_service:
            put_open = [False] * option_pairs_count
        else:
            pass
        
        dt = datetime.datetime.now()

        if put_open_list:

            loop_list = put_open_list

            if market_service:
                '''
                str = '[{0:02d}:{1:02d}:{2:02d}] Put Open Check List = {3}\r'.format(\
                    int(put_result['체결시간'][0:2]), int(put_result['체결시간'][2:4]), int(put_result['체결시간'][4:6]), put_open_list)
                self.textBrowser.append(str)
                '''
                pass
            else:
                #str = '[{0:02d}:{1:02d}:{2:02d}] Put Open Check List = {3}\r'.format(dt.hour, dt.minute, dt.second, put_open_list)
                #self.textBrowser.append(str)
                pass
        else:
            loop_list = opt_total_list

        for index in loop_list:

            if df_put.iloc[index]['시가'] > opt_search_start_value:

                if not market_service:

                    if index != atm_index:
                        self.tableWidget_put.item(index, Option_column.행사가.value).setBackground(QBrush(라임))
                    else:
                        self.tableWidget_put.item(index, Option_column.행사가.value).setBackground(QBrush(노란색))
                else:
                    pass

                if df_put.iloc[index]['종가'] > 0 and df_put.iloc[index]['저가'] < df_put.iloc[index]['고가']:

                    df_put.loc[index, '시가갭'] = df_put.iloc[index]['시가'] - df_put.iloc[index]['종가']   

                    put_gap_percent[index] = (df_put.iloc[index]['시가'] / df_put.iloc[index]['종가'] - 1) * 100
                    gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_put.iloc[index]['시가갭'], put_gap_percent[index])

                    item = QTableWidgetItem(gap_str)
                    item.setTextAlignment(Qt.AlignCenter)

                    if df_put.iloc[index]['시가'] > df_put.iloc[index]['종가']:
                        item.setBackground(QBrush(콜기준가색))
                        item.setForeground(QBrush(검정색))
                    elif df_put.iloc[index]['시가'] < df_put.iloc[index]['종가']:
                        item.setBackground(QBrush(풋기준가색))
                        item.setForeground(QBrush(흰색))
                    else:
                        item.setBackground(QBrush(흰색))

                    self.tableWidget_put.setItem(index, Option_column.시가갭.value, item)
                else:
                    pass

                if df_put.iloc[index]['저가'] < df_put.iloc[index]['고가']:

                    if index < atm_index:
                        put_above_atm_count += 1
                    else:
                        pass

                    if not market_service:

                        put_open[index] = True                        
                    else:
                        pass                    

                    if df_put.iloc[index]['시가'] >= oloh_cutoff:

                        if df_put.iloc[index]['시가'] < 1.0:

                            oloh_threshold = 1

                        elif df_put.iloc[index]['시가'] >= 1.0 and df_put.iloc[index]['시가'] < 2.0:

                            oloh_threshold = 2

                        elif df_put.iloc[index]['시가'] >= 2.0 and df_put.iloc[index]['시가'] < 3.0:

                            oloh_threshold = 3

                        elif df_put.iloc[index]['시가'] >= 3.0 and df_put.iloc[index]['시가'] < 4.0:

                            oloh_threshold = 4

                        else:
                            oloh_threshold = 5   

                        # put OL/OH count
                        if self.within_n_tick(df_put.iloc[index]['시가'], df_put.iloc[index]['저가'], oloh_threshold) \
                                and not self.within_n_tick(df_put.iloc[index]['시가'], df_put.iloc[index]['고가'], oloh_threshold):

                            oloh_str = '▲'

                            item = QTableWidgetItem(oloh_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(청색))
                            item.setForeground(QBrush(흰색))
                            self.tableWidget_put.setItem(index, Option_column.OLOH.value, item)

                            self.tableWidget_put.item(index, Option_column.시가.value).setBackground(QBrush(청색))
                            self.tableWidget_put.item(index, Option_column.시가.value).setForeground(QBrush(흰색))

                            self.tableWidget_put.item(index, Option_column.저가.value).setBackground(QBrush(청색))
                            self.tableWidget_put.item(index, Option_column.저가.value).setForeground(QBrush(흰색)) 

                            put_ol[index] = True

                        elif self.within_n_tick(df_put.iloc[index]['시가'], df_put.iloc[index]['고가'], oloh_threshold) \
                                and not self.within_n_tick(df_put.iloc[index]['시가'], df_put.iloc[index]['저가'], oloh_threshold):

                            oloh_str = '▼'

                            item = QTableWidgetItem(oloh_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(적색))
                            item.setForeground(QBrush(검정색))
                            self.tableWidget_put.setItem(index, Option_column.OLOH.value, item)

                            self.tableWidget_put.item(index, Option_column.시가.value).setBackground(QBrush(청색))
                            self.tableWidget_put.item(index, Option_column.시가.value).setForeground(QBrush(흰색))

                            self.tableWidget_put.item(index, Option_column.고가.value).setBackground(QBrush(청색))
                            self.tableWidget_put.item(index, Option_column.고가.value).setForeground(QBrush(흰색))

                            put_oh[index] = True
                        else:
                            oloh_str = ''

                            if oloh_str != self.tableWidget_put.item(index, Option_column.OLOH.value).text():
                                item = QTableWidgetItem(oloh_str)
                                item.setBackground(QBrush(흰색))
                                item.setForeground(QBrush(검정색))
                                self.tableWidget_put.setItem(index, Option_column.OLOH.value, item)                                
                            else:
                                pass

                            put_ol[index] = False
                            put_oh[index] = False
                    else:
                        pass
                else:
                    pass

                if df_put.iloc[index]['시가'] > 0 and df_put.iloc[index]['저가'] < df_put.iloc[index]['고가']:

                    df_put.loc[index, '대비'] = \
                        round((df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가']), 2)
                    put_db_percent[index] = (df_put.iloc[index]['현재가'] / df_put.iloc[index]['시가'] - 1) * 100

                    gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_put.iloc[index]['대비'], put_db_percent[index])

                    if gap_str != self.tableWidget_put.item(index, Option_column.대비.value).text():

                        item = QTableWidgetItem(gap_str)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(index, Option_column.대비.value, item)
                    else:
                        pass
                else:
                    pass
            else:
                pass

        # Put Open Count 및 OLOH 표시
        put_open_count = len(put_open_list)

        if put_open[0]:

            new_actval = repr(put_above_atm_count) + '/' + repr(put_open_count) + '*'
        else:
            new_actval = repr(put_above_atm_count) + '/' + repr(put_open_count)

        if new_actval != self.tableWidget_put.horizontalHeaderItem(1).text():
            item = QTableWidgetItem(new_actval)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setHorizontalHeaderItem(1, item)
        else:
            pass

        put_ol_count = put_ol.count(True)
        put_oh_count = put_oh.count(True)

        new_oloh = repr(put_ol_count) + ':' + repr(put_oh_count)

        if new_oloh != self.tableWidget_put.horizontalHeaderItem(2).text():
            item = QTableWidgetItem(new_oloh)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_put.setHorizontalHeaderItem(2, item)
        else:
            pass

        # 시가갭 갱신
        temp = put_gap_percent[:]
        put_gap_percent_local = [value for value in temp if not math.isnan(value)]
        put_gap_percent_local.sort()

        풋시가갭합 = round(df_put['시가갭'].sum(), 2)

        if put_gap_percent_local:

            풋시가갭합_단위평균 = round(풋시가갭합/len(put_gap_percent_local), 2)

            tmp = np.array(put_gap_percent_local)            
            풋시가갭합_퍼센트 = int(round(np.mean(tmp), 2))
            put_str = repr(풋시가갭합_단위평균) + '\n(' + repr(풋시가갭합_퍼센트) + '%' + ')'

            if put_str != self.tableWidget_put.horizontalHeaderItem(Option_column.시가갭.value).text():
                item = QTableWidgetItem(put_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.시가갭.value, item)
            else:
                pass
            '''
            str = '[{0:02d}:{1:02d}:{2:02d}] Put Open Check 풋시가갭합 = {3}, 퍼센트 = {4}\r'.\
                format(dt.hour, dt.minute, dt.second, 풋시가갭합, 풋시가갭합_퍼센트)
            self.textBrowser.append(str)
            '''
        else:
            print('put_gap_percent_local is empty...')

        # 대비 갱신
        temp = put_db_percent[:]
        put_db_percent_local = [value for value in temp if not math.isnan(value)]
        put_db_percent_local.sort()

        if put_db_percent_local:

            풋대비합 = round(df_put['대비'].sum(), 2)
            풋대비합_단위평균 = round(풋대비합/len(put_db_percent_local), 2)

            print('풋대비합 =', 풋대비합)

            tmp = np.array(put_db_percent_local)            
            대비평균 = int(round(np.mean(tmp), 2))
            put_str = repr(풋대비합_단위평균) + '\n(' + repr(대비평균) + '%' + ')'

            if put_str != self.tableWidget_put.horizontalHeaderItem(Option_column.대비.value).text():
                item = QTableWidgetItem(put_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.대비.value, item)
            else:
                pass            
        else:
            print('put_db_percent_local is empty...')

            풋대비합 = 0

        self.tableWidget_put.resizeColumnsToContents()

        return
    '''
    def put_db_check(self):

        global df_put, put_db_percent

        for index in range(option_pairs_count):

            if df_put.iloc[index]['시가'] > opt_search_start_value:

                if df_put.iloc[index]['시가'] >= oloh_cutoff and df_put.iloc[index]['저가'] < df_put.iloc[index]['고가']:

                    df_put.loc[index, '대비'] = \
                        round((df_put.iloc[index]['현재가'] - df_put.iloc[index]['시가']), 2)
                    put_db_percent[index] = (df_put.iloc[index]['현재가'] / df_put.iloc[index]['시가'] - 1) * 100

                    gap_str = "{0:0.2f}\n({1:0.0f}%)".format(df_put.iloc[index]['대비'], put_db_percent[index])

                    if gap_str != self.tableWidget_put.item(index, Option_column.대비.value).text():

                        item = QTableWidgetItem(gap_str)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_put.setItem(index, Option_column.대비.value, item)
                    else:
                        pass
                else:
                    pass
            else:
                pass

        temp = put_db_percent[:]
        put_db_percent_local = [value for value in temp if not math.isnan(value)]
        put_db_percent_local.sort()

        if put_db_percent_local:

            sump = round(df_put['대비'].sum(), 2)
            tmp = np.array(put_db_percent_local)            
            meanp = int(round(np.mean(tmp), 2))
            put_str = repr(sump) + '\n (' + repr(meanp) + '%' + ')'

            if put_str != self.tableWidget_put.horizontalHeaderItem(Option_column.대비.value).text():
                item = QTableWidgetItem(put_str)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_put.setHorizontalHeaderItem(Option_column.대비.value, item)
                self.tableWidget_put.resizeColumnsToContents()
            else:
                pass
        else:
            print('put_db_percent_local is empty...')

        return
    '''
    # 호가표시
    def quote_display(self):
        
        global call_quote, put_quote

        call_quote = df_call_hoga.sum()
        put_quote = df_put_hoga.sum()

        if call_quote['매도건수'] > 0:
            call_count_ratio = call_quote['매수건수'] / call_quote['매도건수']
        else:
            call_count_ratio = 0

        if call_quote['매도잔량'] > 0:
            call_remainder_ratio = call_quote['매수잔량'] / call_quote['매도잔량']
        else:
            call_remainder_ratio = 0

        if put_quote['매도건수'] > 0:
            put_count_ratio = put_quote['매수건수'] / put_quote['매도건수']
        else:
            put_count_ratio = 0

        if put_quote['매도잔량'] > 0:
            put_remainder_ratio = put_quote['매수잔량'] / put_quote['매도잔량']
        else:
            put_remainder_ratio = 0

        temp = (call_quote['매수건수'] + call_quote['매도건수']) - (put_quote['매수건수'] + put_quote['매도건수'])
        건수차 = format(temp, ',')

        temp = (call_quote['매수잔량'] + call_quote['매도잔량']) - (put_quote['매수잔량'] + put_quote['매도잔량'])
        잔량차 = format(temp, ',')

        item_str = "{0:0.2f}/{1:0.2f}\n({2}/{3})".format(call_count_ratio - put_count_ratio,
                                                         call_remainder_ratio - put_remainder_ratio,
                                                         건수차, 잔량차)

        if item_str != self.tableWidget_quote.item(0, 12).text():

            item = QTableWidgetItem(item_str)
            item.setTextAlignment(Qt.AlignCenter)

            if call_count_ratio > put_count_ratio and call_remainder_ratio > put_remainder_ratio:
                item.setBackground(QBrush(적색))
                item.setForeground(QBrush(검정색))
            elif call_count_ratio < put_count_ratio and call_remainder_ratio < put_remainder_ratio:
                item.setBackground(QBrush(청색))
                item.setForeground(QBrush(흰색))
            else:
                item.setBackground(QBrush(흰색))
                item.setForeground(QBrush(검정색))

            self.tableWidget_quote.setItem(0, 12, item)
        else:
            pass

        temp = call_quote['매수건수'] + call_quote['매도건수']
        건수합 = format(temp, ',')

        item_str = "{0:0.2f}\n({1})".format(call_count_ratio, 건수합)

        if item_str != self.tableWidget_quote.item(0, 8).text():

            item = QTableWidgetItem(item_str)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_quote.setItem(0, 8, item)
        else:
            pass

        temp = call_quote['매수잔량'] + call_quote['매도잔량']
        잔량합 = format(temp, ',')

        item_str = "{0:0.2f}\n({1})".format(call_remainder_ratio, 잔량합)

        if item_str != self.tableWidget_quote.item(0, 9).text():

            item = QTableWidgetItem(item_str)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_quote.setItem(0, 9, item)
        else:
            pass

        temp = put_quote['매수건수'] + put_quote['매도건수']
        건수합 = format(temp, ',')

        item_str = "{0:0.2f}\n({1})".format(put_count_ratio, 건수합)

        if item_str != self.tableWidget_quote.item(0, 10).text():

            item = QTableWidgetItem(item_str)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_quote.setItem(0, 10, item)
        else:
            pass

        temp = put_quote['매수잔량'] + put_quote['매도잔량']
        잔량합 = format(temp, ',')

        item_str = "{0:0.2f}\n({1})".format(put_remainder_ratio, 잔량합)

        if item_str != self.tableWidget_quote.item(0, 11).text():

            item = QTableWidgetItem(item_str)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_quote.setItem(0, 11, item)
        else:
            pass

        return

    def oi_sum_display(self):
        
        global 콜_수정미결합, 풋_수정미결합
        global oi_delta, oi_delta_old, 수정미결_직전대비        

        #콜_수정미결합 = df_call['수정미결'].sum() - call_oi_init_value
        #풋_수정미결합 = df_put['수정미결'].sum() - put_oi_init_value

        콜_수정미결합 = df_call['수정미결'].sum()
        풋_수정미결합 = df_put['수정미결'].sum()
                    
        df_plotdata_call_oi.iloc[0][opt_x_idx] = 콜_수정미결합
        df_plotdata_put_oi.iloc[0][opt_x_idx] = 풋_수정미결합

        oi_delta_old = oi_delta
        oi_delta = 콜_수정미결합 - 풋_수정미결합
        
        수정미결합 = 콜_수정미결합 + 풋_수정미결합
        
        수정미결_직전대비.extend([oi_delta - oi_delta_old])
        temp = list(수정미결_직전대비)

        if 수정미결합 > 0:

            콜_수정미결퍼센트 = (콜_수정미결합 / 수정미결합) * 100
            풋_수정미결퍼센트 = 100 - 콜_수정미결퍼센트
        else:
            콜_수정미결퍼센트 = 0
            풋_수정미결퍼센트 = 0

        '''
        if oi_delta > 0:

            if min(temp) > 0:

                item_str = '{0}\n{1}⬈'.format(format(콜_수정미결합, ','), format(풋_수정미결합, ','))

            elif max(temp) < 0:

                item_str = '{0}\n{1}⬊'.format(format(콜_수정미결합, ','), format(풋_수정미결합, ','))
            else:
                item_str = '{0}\n{1}'.format(format(콜_수정미결합, ','), format(풋_수정미결합, ','))

        elif oi_delta < 0:

            if min(temp) > 0:

                item_str = '{0}\n{1}⬊'.format(format(콜_수정미결합, ','), format(풋_수정미결합, ','))

            elif max(temp) < 0:

                item_str = '{0}\n{1}⬈'.format(format(콜_수정미결합, ','), format(풋_수정미결합, ','))
            else:
                item_str = '{0}\n{1}'.format(format(콜_수정미결합, ','), format(풋_수정미결합, ','))

        else:
            item_str = '{0:0.1f}%\n{1:0.1f}%'.format(콜_수정미결퍼센트, 풋_수정미결퍼센트)
        '''

        item_str = '{0:0.1f}%\n{1:0.1f}%'.format(콜_수정미결퍼센트, 풋_수정미결퍼센트)

        if item_str != self.tableWidget_quote.item(0, Quote_column.미결종합.value - 1).text():

            item = QTableWidgetItem(item_str)
            item.setTextAlignment(Qt.AlignCenter)

            '''
            if oi_delta > 0:

                item.setBackground(QBrush(적색))
                item.setForeground(QBrush(검정색))

            elif oi_delta < 0:

                item.setBackground(QBrush(청색))
                item.setForeground(QBrush(흰색))

            else:
                item.setBackground(QBrush(흰색))
                item.setForeground(QBrush(검정색))
            '''

            self.tableWidget_quote.setItem(0, Quote_column.미결종합.value - 1, item)
        else:
            pass

        return

    def OnReceiveRealData(self, szTrCode, result):

        try:
            global pre_start
            global atm_str, atm_val, atm_index
            global atm_index_yj

            global fut_realdata

            global df_call, df_put
            global df_call_hoga, df_put_hoga

            global df_plotdata_fut, df_plotdata_kp200
            global df_plotdata_call, df_plotdata_put

            global opt_callreal_update_counter, opt_putreal_update_counter
            global opt_call_ho_update_counter, opt_put_ho_update_counter
            global call_atm_value, put_atm_value
            global atm_index_old           
            global receive_quote

            global FUT_FOREIGNER_거래대금순매수, FUT_RETAIL_거래대금순매수, FUT_INSTITUTIONAL_거래대금순매수, FUT_STOCK_거래대금순매수, \
                FUT_BOHEOM_거래대금순매수, FUT_TOOSIN_거래대금순매수, FUT_BANK_거래대금순매수, FUT_JONGGEUM_거래대금순매수, \
                FUT_GIGEUM_거래대금순매수, FUT_GITA_거래대금순매수

            global FUT_FOREIGNER_거래대금순매수_직전대비, FUT_RETAIL_거래대금순매수_직전대비, FUT_INSTITUTIONAL_거래대금순매수_직전대비, \
                FUT_STOCK_거래대금순매수_직전대비, FUT_BOHEOM_거래대금순매수_직전대비, FUT_TOOSIN_거래대금순매수_직전대비, \
                FUT_BANK_거래대금순매수_직전대비, FUT_JONGGEUM_거래대금순매수_직전대비, FUT_GIGEUM_거래대금순매수_직전대비, \
                FUT_GITA_거래대금순매수_직전대비

            global KOSPI_FOREIGNER_거래대금순매수, KOSPI_RETAIL_거래대금순매수, KOSPI_INSTITUTIONAL_거래대금순매수, KOSPI_STOCK_거래대금순매수, \
                KOSPI_BOHEOM_거래대금순매수, KOSPI_TOOSIN_거래대금순매수, KOSPI_BANK_거래대금순매수, KOSPI_JONGGEUM_거래대금순매수, \
                KOSPI_GIGEUM_거래대금순매수, KOSPI_GITA_거래대금순매수

            global KOSPI_FOREIGNER_거래대금순매수_직전대비, KOSPI_RETAIL_거래대금순매수_직전대비, KOSPI_INSTITUTIONAL_거래대금순매수_직전대비, \
                KOSPI_STOCK_거래대금순매수_직전대비, KOSPI_BOHEOM_거래대금순매수_직전대비, KOSPI_TOOSIN_거래대금순매수_직전대비, \
                KOSPI_BANK_거래대금순매수_직전대비, KOSPI_JONGGEUM_거래대금순매수_직전대비, KOSPI_GIGEUM_거래대금순매수_직전대비, \
                KOSPI_GITA_거래대금순매수_직전대비

            global FUT_FOREIGNER_직전대비, FUT_RETAIL_직전대비, FUT_INSTITUTIONAL_직전대비, \
                KOSPI_FOREIGNER_직전대비, PROGRAM_직전대비

            global 프로그램_전체순매수금액, 프로그램_전체순매수금액직전대비
            global 선물_거래대금순매수, 현물_거래대금순매수

            global kp200_realdata
            global call_result, put_result
            global yoc_call_gap_percent, yoc_put_gap_percent

            global time_delta

            global opt_callreal_update_counter
            global call_atm_value, call_db_percent
            global call_피봇, call_피봇_node_list, call_시가, call_시가_node_list
            global call_저가, call_저가_node_list, call_고가, call_고가_node_list

            global opt_putreal_update_counter
            global put_atm_value, put_db_percent
            global put_피봇, put_피봇_node_list, put_시가, put_시가_node_list
            global put_저가, put_저가_node_list, put_고가, put_고가_node_list
            global market_service, service_terminate, jugan_service_terminate, yagan_service_terminate

            global yoc_stop
            global OVC_체결시간, 호가시간
            global df_plotdata_sp500, df_plotdata_dow, df_plotdata_nasdaq

            global sp500_delta, sp500_delta_old, sp500_직전대비
            global dow_delta, dow_delta_old, dow_직전대비
            global nasdaq_delta, nasdaq_delta_old, nasdaq_직전대비
            global receive_real_ovc
            global x_idx, ovc_x_idx
            global call_result, put_result
            
            global 선물현재가
            global opt_x_idx, 콜현재가, 풋현재가
            global flag_telegram_send_worker
            global dongsi_hoga

            global nasdaq_price, nasdaq_text_color, nasdaq_시가, nasdaq_전일종가, nasdaq_피봇, nasdaq_저가, nasdaq_고가 
            global sp500_price, sp500_text_color, sp500_시가, sp500_전일종가, sp500_피봇, sp500_저가, sp500_고가            
            global dow_price, dow_text_color, dow_시가, dow_전일종가, dow_피봇, dow_저가, dow_고가 

            global cme_close, dow_close
            global 시스템시간, 서버시간, 시스템_서버_시간차

            start_time = timeit.default_timer()

            dt = datetime.datetime.now()
            
            시스템시간 = dt.hour * 3600 + dt.minute * 60 + dt.second

            if szTrCode == 'JIF':

                str = '[{0:02d}:{1:02d}:{2:02d}] 장구분[{3}], 장상태[{4}]\r'.format(\
                    int(OVC_체결시간[0:2]), int(OVC_체결시간[2:4]), int(OVC_체결시간[4:6]), result['장구분'], result['장상태'])
                self.textBrowser.append(str)

                # 장시작 10분전
                if result['장구분'] == '5' and result['장상태'] == '25':

                    str = '[{0:02d}:{1:02d}:{2:02d}] 장시작 10분전입니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    '''
                    # 서버시간과 동기를 위한 delta time 계산
                    time_delta = 시스템시간 - ((kse_start_hour - 1) * 3600 + 50 * 60 + 0)

                    if time_delta > 0:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 시스템시간이 서버시간보다 {3}초 빠릅니다.\r'.format(\
                            dt.hour, dt.minute, dt.second, time_delta)
                        self.textBrowser.append(str)
                    elif time_delta < 0:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 시스템시간이 서버시간보다 {3}초 느립니다.\r'.format(\
                            dt.hour, dt.minute, dt.second, time_delta)
                        self.textBrowser.append(str)
                    else:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 시스템시간과 서버시간이 같습니다.\r'.format(\
                            dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)

                    str = '[{0:02d}:{1:02d}:{2:02d}] 장시작 10분전입니다.\r'.format(dt.hour, dt.minute, dt.second)
                    self.textBrowser.append(str)
                    
                    if not START_ON:

                        self.AddCode()
                        str = '[{0:02d}:{1:02d}:{2:02d}] Auto Start...\r'.format(dt.hour, dt.minute, dt.second)
                        self.textBrowser.append(str)

                        pre_start = True
                    else:
                        pass
                    '''

                # 현물장 시작 10초전
                elif result['장구분'] == '1' and result['장상태'] == '22':

                    str = '[{0:02d}:{1:02d}:{2:02d}] 현물장 시작 10초전입니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                # 선물장 시작 10초전
                elif result['장구분'] == '5' and result['장상태'] == '22':
                    
                    str = '[{0:02d}:{1:02d}:{2:02d}] 선물장 시작 10초전입니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                # 주간 선물/옵션장 시작
                elif result['장구분'] == '5' and result['장상태'] == '21':

                    yoc_stop = not yoc_stop

                    market_service = True

                    str = '[{0:02d}:{1:02d}:{2:02d}] 주간장이 시작됩니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                # 야간 선물장 시작
                elif result['장구분'] == '7' and result['장상태'] == '21':
                    
                    market_service = True

                    str = '[{0:02d}:{1:02d}:{2:02d}] 야간 선물장이 시작됩니다.\r'.format(int(OVC_체결시간[0:2]), int(OVC_체결시간[2:4]), int(OVC_체결시간[4:6]))
                    self.textBrowser.append(str)

                # 야간 옵션장 시작
                elif result['장구분'] == '8' and result['장상태'] == '21':

                    '''
                    # 서버시간과 동기를 위한 delta time 계산
                    time_delta = 시스템시간 - (kse_start_hour * 3600 + 0 * 60 + 0)

                    if time_delta > 0:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 시스템시간이 서버시간보다 {3}초 빠릅니다.\r'.format(dt.hour, dt.minute,
                                                                    dt.second, time_delta)
                        self.textBrowser.append(str)
                    elif time_delta < 0:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 시스템시간이 서버시간보다 {3}초 느립니다.\r'.format(dt.hour, dt.minute,
                                                                                dt.second, time_delta)
                        self.textBrowser.append(str)
                    else:
                        str = '[{0:02d}:{1:02d}:{2:02d}] 시스템시간과 서버시간이 같습니다.\r'.format(dt.hour, dt.minute,
                                                                                dt.second)
                        self.textBrowser.append(str)
                    '''

                    str = '[{0:02d}:{1:02d}:{2:02d}] 야간 옵션장이 시작됩니다.\r'.format(int(OVC_체결시간[0:2]), int(OVC_체결시간[2:4]), int(OVC_체결시간[4:6]))
                    self.textBrowser.append(str)

                # 현물 장마감 5분전
                elif result['장구분'] == '1' and result['장상태'] == '44':

                    str = '[{0:02d}:{1:02d}:{2:02d}] 현물 장마감 5분전입니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                # 현물 장마감 1분전
                elif result['장구분'] == '1' and result['장상태'] == '43':

                    str = '[{0:02d}:{1:02d}:{2:02d}] 현물 장마감 1분전입니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    # FUTURES/KOSPI200 예상지수 요청취소
                    self.YJ.UnadviseRealData()

                    str = '[{0:02d}:{1:02d}:{2:02d}] FUTURES/KOSPI200 예상지수 요청을 취소합니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    # 지수선물예상체결 요청취소
                    self.YFC.UnadviseRealData()

                    str = '[{0:02d}:{1:02d}:{2:02d}] 지수선물 예상체결 요청을 취소합니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    # KOSPI예상체결 요청취소
                    self.YS3.UnadviseRealData()

                    str = '[{0:02d}:{1:02d}:{2:02d}] KOSPI 예상체결 요청을 취소합니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    # 지수옵션예상체결 요청취소
                    self.YOC.UnadviseRealData()

                    str = '[{0:02d}:{1:02d}:{2:02d}] 지수옵션 예상체결 요청을 취소합니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                # 장후 동시호가 시작
                elif result['장구분'] == '5' and result['장상태'] == '31':

                    str = '[{0:02d}:{1:02d}:{2:02d}] 장후 동시호가가 시작되었습니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    dongsi_hoga = True

                    str = '[{0:02d}:{1:02d}:{2:02d}] 텔레그램 스레드를 종료합니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    if self.telegram_send_worker.isRunning():
                        self.telegram_send_worker.terminate()
                    else:
                        pass

                    if self.telegram_listen_worker.isRunning():
                        self.telegram_listen_worker.terminate()
                    else:
                        pass

                # 주간 선물/옵션장 종료
                elif result['장구분'] == '5' and result['장상태'] == '41':

                    str = '[{0:02d}:{1:02d}:{2:02d}] 주간 선물/옵션장이 종료되었습니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)

                    str = '[{0:02d}:{1:02d}:{2:02d}] 주간장 종료시 DOW 지수 = {3}\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]), dow_price)
                    self.textBrowser.append(str)

                    if market_service:

                        self.SaveResult()     

                        market_service = False
                        service_terminate = True
                        jugan_service_terminate = True

                        receive_quote = False

                        self.pushButton_add.setText('ScrShot')

                        if TARGET_MONTH_SELECT == 1:

                            self.capture_screenshot()
                        else:
                            pass                    
                    else:
                        pass                                               

                # 야간 선물장 종료
                elif result['장구분'] == '7' and result['장상태'] == '41':

                    str = '[{0:02d}:{1:02d}:{2:02d}] 야간 선물장이 종료되었습니다.\r'.format(int(OVC_체결시간[0:2]), int(OVC_체결시간[2:4]), int(OVC_체결시간[4:6]))
                    self.textBrowser.append(str)

                    cme_close = cme_realdata['현재가']
                    dow_close = dow_price

                    str = '[{0:02d}:{1:02d}:{2:02d}] 야간장 종료시 DOW 지수 = {3}\r'.format(int(OVC_체결시간[0:2]), int(OVC_체결시간[2:4]), int(OVC_체결시간[4:6]), dow_price)
                    self.textBrowser.append(str)

                    if market_service:

                        self.SaveResult()

                        market_service = False
                        service_terminate = True
                        yagan_service_terminate = True

                        receive_quote = False

                        self.pushButton_add.setText('ScrShot')
                        
                        str = '[{0:02d}:{1:02d}:{2:02d}] 텔레그램 스레드를 종료합니다.\r'.format(int(OVC_체결시간[0:2]), int(OVC_체결시간[2:4]), int(OVC_체결시간[4:6]))
                        self.textBrowser.append(str)

                        if self.telegram_send_worker.isRunning():
                            self.telegram_send_worker.terminate()
                        else:
                            pass

                        if self.telegram_listen_worker.isRunning():
                            self.telegram_listen_worker.terminate()
                        else:
                            pass

                        if TARGET_MONTH_SELECT == 1:

                            self.capture_screenshot()
                        else:
                            pass
                    else:
                        pass                    

                # 야간 옵션장 종료
                elif result['장구분'] == '8' and result['장상태'] == '41':

                    str = '[{0:02d}:{1:02d}:{2:02d}] 야간 옵션장이 종료되었습니다.\r'.format(int(OVC_체결시간[0:2]), int(OVC_체결시간[2:4]), int(OVC_체결시간[4:6]))
                    self.textBrowser.append(str)
                else:
                    pass

            elif szTrCode == 'YJ_':

                if pre_start:

                    if result['업종코드'] == KOSPI200:

                        if result['시간'] != '':
                            x_yj_idx = int(result['시간'][2:4]) + 1
                        else:
                            pass

                        if result['예상지수'] != float(self.tableWidget_fut.item(2, Futures_column.시가.value).text()):

                            kp200_realdata['시가'] = result['예상지수']
                            fut_realdata['KP200'] = result['예상지수']

                            if x_yj_idx > 0:
                                df_plotdata_kp200.iloc[0][x_yj_idx] = result['예상지수']
                            else:
                                pass

                            item = QTableWidgetItem("{0:0.2f}".format(result['예상지수']))
                            item.setTextAlignment(Qt.AlignCenter)

                            if kp200_realdata['시가'] > kp200_realdata['종가']:

                                item.setForeground(QBrush(적색))
                            elif kp200_realdata['시가'] < kp200_realdata['종가']:

                                item.setForeground(QBrush(청색))
                            else:
                                item.setForeground(QBrush(검정색))

                            self.tableWidget_fut.setItem(2, Futures_column.시가.value, item)
                        else:
                            pass

                        atm_str = self.find_ATM(result['예상지수'])

                        if atm_str[-1] == '2' or atm_str[-1] == '7':

                            atm_val = float(atm_str) + 0.5
                        else:
                            atm_val = float(atm_str)

                        if fut_realdata['시가'] > 0 and fut_realdata['KP200'] > 0:

                            예상_Basis = fut_realdata['시가'] - fut_realdata['KP200']
                            '''
                            str = '[{0:02d}:{1:02d}:{2:02d}] 예상 등가지수 : {3}, 예상 Basis : {4:0.2f}\r'.format(
                                            int(result['시간'][0:2]),
                                            int(result['시간'][2:4]),
                                            int(result['시간'][4:6]),
                                            atm_str, 예상_Basis)
                            self.textBrowser.append(str)
                            '''
                        else:
                            pass

                        if atm_str in opt_actval:
                            atm_index_yj = opt_actval.index(atm_str)
                            #print('예상 등가지수 index : ', atm_index_yj)
                        else:
                            print("atm_str이 리스트에 없습니다.", atm_str)

                    elif result['업종코드'] == FUTURES:

                        print('선물 예상지수 : ', result['예상지수'])

                    else:
                        pass
                else:
                    pass

            elif szTrCode == 'YS3':                
                
                if pre_start:

                    현재가 = format(result['예상체결가격'], ',')

                    if result['단축코드'] == SAMSUNG:

                        if result['예상체결가전일종가대비구분'] == '5':

                            jisu_str = "SAMSUNG: {0}({1}, {2:0.1f}%)".format(현재가, format(-result['예상체결가전일종가대비'], ','),
                                                                                result['예상체결가전일종가등락율'])
                            self.label_samsung.setText(jisu_str)
                            self.label_samsung.setStyleSheet('background-color: blue ; color: white')

                        elif result['예상체결가전일종가대비구분'] == '2':

                            jisu_str = "SAMSUNG: {0}({1}, {2:0.1f}%)".format(현재가, format(result['예상체결가전일종가대비'], ','),
                                                                                result['예상체결가전일종가등락율'])
                            self.label_samsung.setText(jisu_str)
                            self.label_samsung.setStyleSheet('background-color: red ; color: white')

                        else:
                            jisu_str = "SAMSUNG: {0}({1})".format(현재가, format(result['예상체결가전일종가대비'], ','))
                            self.label_samsung.setText(jisu_str)
                            self.label_samsung.setStyleSheet('background-color: yellow ; color: black')
                    
                    elif result['단축코드'] == HYUNDAI:

                        if result['예상체결가전일종가대비구분'] == '5':

                            jisu_str = "HYUNDAI: {0}({1}, {2:0.1f}%)".format(현재가, format(-result['예상체결가전일종가대비'], ','),
                                                                              result['예상체결가전일종가등락율'])
                            self.label_kosdaq.setText(jisu_str)
                            self.label_kosdaq.setStyleSheet('background-color: blue ; color: white')

                        elif result['예상체결가전일종가대비구분'] == '2':

                            jisu_str = "HYUNDAI: {0}({1}, {2:0.1f}%)".format(현재가, format(result['예상체결가전일종가대비'], ','),
                                                                              result['예상체결가전일종가등락율'])
                            self.label_kosdaq.setText(jisu_str)
                            self.label_kosdaq.setStyleSheet('background-color: red ; color: white')

                        else:
                            jisu_str = "HYUNDAI: {0}({1})".format(현재가, format(result['예상체결가전일종가대비'], ','))
                            self.label_kosdaq.setText(jisu_str)
                            self.label_kosdaq.setStyleSheet('background-color: yellow ; color: black')
                    else:
                        pass

                    '''
                    elif result['단축코드'] == Celltrion:
                        
                        if result['예상체결가전일종가대비구분'] == '5':

                            jisu_str = "CTRO : {0}({1}, {2:0.1f}%)".format(현재가, format(-result['예상체결가전일종가대비'], ','),
                                                                              result['예상체결가전일종가등락율'])
                            self.label_3rd.setText(jisu_str)
                            self.label_3rd.setStyleSheet('background-color: blue ; color: white')

                        elif result['예상체결가전일종가대비구분'] == '2':

                            jisu_str = "CTRO : {0}({1}, {2:0.1f}%)".format(현재가, format(result['예상체결가전일종가대비'], ','),
                                                                              result['예상체결가전일종가등락율'])
                            self.label_3rd.setText(jisu_str)
                            self.label_3rd.setStyleSheet('background-color: red ; color: white')

                        else:
                            jisu_str = "CTRO : {0}({1})".format(현재가, format(result['예상체결가전일종가대비'], ','))
                            self.label_3rd.setText(jisu_str)
                            self.label_3rd.setStyleSheet('background-color: yellow ; color: black')                        
                    else:
                        #print('단축코드', result['단축코드'])
                        pass
                    '''
                else:
                    pass                

            elif szTrCode == 'YOC':

                if int(result['예상체결시간'][0:2]) == (kse_start_hour - 1) and int(result['예상체결시간'][2:4]) == 59 and \
                    (int(result['예상체결시간'][4:6]) == 58 or int(result['예상체결시간'][4:6]) == 59):

                    # 지수옵션 예상체결 요청취소(안하면 시작시 지연발생함)
                    self.YOC.UnadviseRealData()

                    yoc_stop = True

                    str = '[{0:02d}:{1:02d}:{2:02d}] 지수옵션 예상체결 요청을 취소합니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)
                else:
                    pass

                if not yoc_stop:

                    if result['단축코드'][0:3] == '201':

                        index = call_행사가.index(result['단축코드'][5:8])

                        if result['예상체결가격'] != self.tableWidget_call.item(index, Option_column.시가.value).text():

                            df_plotdata_call.iloc[index][선물장간_시간차] = float(result['예상체결가격'])

                            df_call.loc[index, '시가'] = round(float(result['예상체결가격']), 2)

                            self.tableWidget_call.item(index, Option_column.시가.value).setBackground(QBrush(흰색))

                            item = QTableWidgetItem("{0}".format(result['예상체결가격']))
                            item.setTextAlignment(Qt.AlignCenter)

                            if float(result['예상체결가격']) > df_call.iloc[index]['종가']:
                                item.setForeground(QBrush(적색))
                            elif float(result['예상체결가격']) < df_call.iloc[index]['종가']:
                                item.setForeground(QBrush(청색))
                            else:
                                item.setForeground(QBrush(검정색))

                            self.tableWidget_call.setItem(index, Option_column.시가.value, item)

                            if df_call.iloc[index]['시가'] in coreval:

                                self.tableWidget_call.item(index, Option_column.시가.value).setBackground(QBrush(대맥점색))
                                self.tableWidget_call.item(index, Option_column.시가.value).setForeground(QBrush(검정색))
                            else:
                                pass

                            df_call.loc[index, '피봇'] = self.calc_pivot(df_call.iloc[index]['전저'],
                                                                          df_call.iloc[index]['전고'],
                                                                          df_call.iloc[index]['종가'],
                                                                          df_call.iloc[index]['시가'])

                            item = QTableWidgetItem("{0:0.2f}".format(df_call.iloc[index]['피봇']))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_call.setItem(index, Option_column.피봇.value, item)

                            if float(result['예상체결가격']) > 0 and df_call.iloc[index]['종가'] > 0:

                                시가갭 = float(result['예상체결가격']) - df_call.iloc[index]['종가']
                                df_call.loc[index, '시가갭'] = 시가갭

                                yoc_call_gap_percent[index] = (float(result['예상체결가격']) / df_call.iloc[index][
                                    '종가'] - 1) * 100

                                gap_str = "{0:0.2f}\n({1:0.0f}%)".format(시가갭, yoc_call_gap_percent[index])

                                if gap_str != self.tableWidget_call.item(index, Option_column.시가갭.value).text():

                                    item = QTableWidgetItem(gap_str)
                                    item.setTextAlignment(Qt.AlignCenter)
                                    self.tableWidget_call.setItem(index, Option_column.시가갭.value, item)
                                    self.tableWidget_call.resizeColumnsToContents()
                                else:
                                    pass
                            else:
                                pass
                            '''
                            str = '[{0:02d}:{1:02d}:{2:02d}] [{3}] Call {4} 시작예상가 수신... \r'.format(
                                int(result['예상체결시간'][0:2]),
                                int(result['예상체결시간'][2:4]),
                                int(result['예상체결시간'][4:6]),
                                szTrCode,
                                result['예상체결가격'])
                            self.textBrowser.append(str)
                            '''
                        else:
                            pass

                        global 콜시가갭합, 콜시가갭합_퍼센트, 콜시가갭합_단위평균

                        콜시가갭합 = round(df_call['시가갭'].sum(), 2)

                        temp = yoc_call_gap_percent[:]
                        call_gap_percent_local = [value for value in temp if not math.isnan(value)]
                        call_gap_percent_local.sort()

                        if call_gap_percent_local:

                            콜시가갭합_단위평균 = round(콜시가갭합/len(call_gap_percent_local), 2)

                            tmp = np.array(call_gap_percent_local)                            
                            콜시가갭합_퍼센트 = int(round(np.mean(tmp), 2))
                            call_str = repr(콜시가갭합_단위평균) + '\n(' + repr(콜시가갭합_퍼센트) + '%' + ')'

                            if call_str != self.tableWidget_call.horizontalHeaderItem(Option_column.시가갭.value).text():
                                item = QTableWidgetItem(call_str)
                                self.tableWidget_call.setHorizontalHeaderItem(Option_column.시가갭.value, item)
                                self.tableWidget_call.resizeColumnsToContents()
                            else:
                                pass

                            new_actval = repr(len(call_gap_percent_local))

                            if new_actval != self.tableWidget_call.horizontalHeaderItem(1).text():
                                item = QTableWidgetItem(new_actval)
                                item.setTextAlignment(Qt.AlignCenter)
                                self.tableWidget_call.setHorizontalHeaderItem(1, item)
                            else:
                                pass
                        else:
                            pass

                    elif result['단축코드'][0:3] == '301':

                        index = put_행사가.index(result['단축코드'][5:8])

                        if result['예상체결가격'] != self.tableWidget_put.item(index, Option_column.시가.value).text():

                            df_plotdata_put.iloc[index][선물장간_시간차] = float(result['예상체결가격'])

                            df_put.loc[index, '시가'] = round(float(result['예상체결가격']), 2)

                            self.tableWidget_put.item(index, Option_column.시가.value).setBackground(QBrush(흰색))

                            item = QTableWidgetItem("{0}".format(result['예상체결가격']))
                            item.setTextAlignment(Qt.AlignCenter)

                            if float(result['예상체결가격']) > df_put.iloc[index]['종가']:
                                item.setForeground(QBrush(적색))
                            elif float(result['예상체결가격']) < df_put.iloc[index]['종가']:
                                item.setForeground(QBrush(청색))
                            else:
                                item.setForeground(QBrush(검정색))

                            self.tableWidget_put.setItem(index, Option_column.시가.value, item)

                            if df_put.iloc[index]['시가'] in coreval:

                                self.tableWidget_put.item(index, Option_column.시가.value).setBackground(QBrush(대맥점색))
                                self.tableWidget_put.item(index, Option_column.시가.value).setForeground(QBrush(검정색))
                            else:
                                pass

                            df_put.loc[index, '피봇'] = self.calc_pivot(df_put.iloc[index]['전저'],
                                                                          df_put.iloc[index]['전고'],
                                                                          df_put.iloc[index]['종가'],
                                                                          df_put.iloc[index]['시가'])

                            item = QTableWidgetItem("{0:0.2f}".format(df_put.iloc[index]['피봇']))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tableWidget_put.setItem(index, Option_column.피봇.value, item)

                            if float(result['예상체결가격']) > 0 and df_put.iloc[index]['종가'] > 0:

                                시가갭 = float(result['예상체결가격']) - df_put.iloc[index]['종가']
                                df_put.loc[index, '시가갭'] = 시가갭

                                yoc_put_gap_percent[index] = (float(result['예상체결가격']) / df_put.iloc[index][
                                    '종가'] - 1) * 100

                                gap_str = "{0:0.2f}\n({1:0.0f}%)".format(시가갭, yoc_put_gap_percent[index])

                                if gap_str != self.tableWidget_put.item(index, Option_column.시가갭.value).text():

                                    item = QTableWidgetItem(gap_str)
                                    item.setTextAlignment(Qt.AlignCenter)
                                    self.tableWidget_put.setItem(index, Option_column.시가갭.value, item)
                                    self.tableWidget_put.resizeColumnsToContents()
                                else:
                                    pass
                            else:
                                pass
                            '''
                            str = '[{0:02d}:{1:02d}:{2:02d}] [{3}] Put {4} 시작예상가 수신... \r'.format(
                                int(result['예상체결시간'][0:2]),
                                int(result['예상체결시간'][2:4]),
                                int(result['예상체결시간'][4:6]),
                                szTrCode,
                                result['예상체결가격'])
                            self.textBrowser.append(str)
                            '''
                        else:
                            pass

                        global 풋시가갭합, 풋시가갭합_퍼센트, 풋시가갭합_단위평균 

                        풋시가갭합 = round(df_put['시가갭'].sum(), 2)

                        temp = yoc_put_gap_percent[:]
                        put_gap_percent_local = [value for value in temp if not math.isnan(value)]
                        put_gap_percent_local.sort()

                        if put_gap_percent_local:

                            풋시가갭합_단위평균 = round(풋시가갭합/len(put_gap_percent_local), 2)

                            tmp = np.array(put_gap_percent_local)                            
                            풋시가갭합_퍼센트 = int(round(np.mean(tmp), 2))
                            put_str = repr(풋시가갭합_단위평균) + '\n(' + repr(풋시가갭합_퍼센트) + '%' + ')'

                            if put_str != self.tableWidget_put.horizontalHeaderItem(Option_column.시가갭.value).text():
                                item = QTableWidgetItem(put_str)
                                self.tableWidget_put.setHorizontalHeaderItem(Option_column.시가갭.value, item)
                                self.tableWidget_put.resizeColumnsToContents()
                            else:
                                pass

                            new_actval = repr(len(put_gap_percent_local))

                            if new_actval != self.tableWidget_put.horizontalHeaderItem(1).text():
                                item = QTableWidgetItem(new_actval)
                                item.setTextAlignment(Qt.AlignCenter)
                                self.tableWidget_put.setHorizontalHeaderItem(1, item)
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    str = '[{0:02d}:{1:02d}:{2:02d}] Wrong [{3}] 수신... \r'.format(
                        int(result['예상체결시간'][0:2]),
                        int(result['예상체결시간'][2:4]),
                        int(result['예상체결시간'][4:6]),
                        szTrCode)
                    self.textBrowser.append(str)

            elif szTrCode == 'YFC':

                if result['단축코드'] == gmshcode:

                    global 선물_시가, 선물_피봇

                    if result['예상체결시간'] != '':
                        x_yfc_idx = int(result['예상체결시간'][2:4]) + 1
                        x_idx = x_yfc_idx
                    else:
                        pass

                    if result['예상체결가격'] != float(self.tableWidget_fut.item(1, Futures_column.시가.value).text()):

                        선물_시가 = result['예상체결가격']
                        fut_realdata['시가'] = result['예상체결가격']

                        if x_yfc_idx > 0:
                            df_plotdata_fut.iloc[0][x_yfc_idx] = 선물_시가
                        else:
                            pass

                        item = QTableWidgetItem("{0:0.2f}".format(선물_시가))
                        item.setTextAlignment(Qt.AlignCenter)

                        if 선물_시가 > fut_realdata['종가']:
                            item.setForeground(QBrush(적색))
                        elif 선물_시가 < fut_realdata['종가']:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))

                        self.tableWidget_fut.setItem(1, Futures_column.시가.value, item)

                        시가갭 = 선물_시가 - fut_realdata['종가']

                        item = QTableWidgetItem("{0:0.2f}".format(시가갭))
                        item.setTextAlignment(Qt.AlignCenter)

                        if 선물_시가 > fut_realdata['종가']:
                            item.setBackground(QBrush(콜기준가색))
                            item.setForeground(QBrush(검정색))
                        elif 선물_시가 < fut_realdata['종가']:
                            item.setBackground(QBrush(풋기준가색))
                            item.setForeground(QBrush(흰색))
                        else:
                            item.setBackground(QBrush(흰색))

                        self.tableWidget_fut.setItem(1, Futures_column.시가갭.value, item)

                        선물_피봇 = self.calc_pivot(선물_전저, 선물_전고, 선물_종가, 선물_시가)

                        item = QTableWidgetItem("{0:0.2f}".format(fut_realdata['피봇']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_fut.setItem(1, Futures_column.피봇.value, item)

                        fut_realdata['피봇'] = 선물_피봇

                        예상시가 = (CME_INDEX * dow_price) / DOW_INDEX

                        item = QTableWidgetItem("{0:0.2f}".format(예상시가))
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(검정색))
                        item.setForeground(QBrush(대맥점색))
                        self.tableWidget_fut.setItem(0, Futures_column.시가.value, item)                            

                        str = '[{0:02d}:{1:02d}:{2:02d}] 선물 예상시가 = {3:0.2f}\r'.format(\
                                        int(result['예상체결시간'][0:2]),
                                        int(result['예상체결시간'][2:4]),
                                        int(result['예상체결시간'][4:6]),
                                        예상시가)
                        self.textBrowser.append(str)

                        self.tableWidget_fut.resizeColumnsToContents()
                    else:
                        pass
                else:
                    pass

            elif szTrCode == 'S3_':
                
                #현재가 = format(result['현재가'], ',')

                # S3 데이타표시
                if result['단축코드'] == SAMSUNG:
                    '''
                    if result['전일대비구분'] == '5':

                        jisu_str = "SAMSUNG: {0}({1}, {2:0.1f}%)".format(현재가, format(-result['전일대비'], ','), result['등락율'])
                        self.label_samsung.setText(jisu_str)
                        self.label_samsung.setStyleSheet('background-color: blue ; color: white')

                    elif result['전일대비구분'] == '2':

                        jisu_str = "SAMSUNG: {0}({1}, {2:0.1f}%)".format(현재가, format(result['전일대비'], ','), result['등락율'])
                        self.label_samsung.setText(jisu_str)
                        self.label_samsung.setStyleSheet('background-color: red ; color: white')

                    else:
                        jisu_str = "SAMSUNG: {0}({1})".format(현재가, format(result['전일대비'], ','))
                        self.label_samsung.setText(jisu_str)
                        self.label_samsung.setStyleSheet('background-color: yellow ; color: black')
                    '''
                    global samsung_price, samsung_text_color                    

                    if result['현재가'] != samsung_price:

                        if result['현재가'] > samsung_price:

                            temp_str = format(result['현재가'], ',')

                            if result['전일대비구분'] == '5':

                                jisu_str = "SS: {0} ▲ (-{1}, {2:0.1f}%)".format(temp_str, format(result['전일대비'], ','), result['등락율'])
                                self.label_samsung.setText(jisu_str)
                                self.label_samsung.setStyleSheet('background-color: pink ; color: blue')
                                samsung_text_color = 'blue'

                            elif result['전일대비구분'] == '2':

                                jisu_str = "SS: {0} ▲ ({1}, {2:0.1f}%)".format(temp_str, format(result['전일대비'], ','), result['등락율'])
                                self.label_samsung.setText(jisu_str)
                                self.label_samsung.setStyleSheet('background-color: pink ; color: red')
                                samsung_text_color = 'red'
                            else:
                                pass

                        elif result['현재가'] < samsung_price:

                            temp_str = format(result['현재가'], ',')

                            if result['전일대비구분'] == '5':

                                jisu_str = "SS: {0} ▼ (-{1}, {2:0.1f}%)".format(temp_str, format(result['전일대비'], ','), result['등락율'])
                                self.label_samsung.setText(jisu_str)
                                self.label_samsung.setStyleSheet('background-color: lightskyblue ; color: blue')
                                samsung_text_color = 'blue'

                            elif result['전일대비구분'] == '2':

                                jisu_str = "SS: {0} ▼ ({1}, {2:0.1f}%)".format(temp_str, format(result['전일대비'], ','), result['등락율'])
                                self.label_samsung.setText(jisu_str)
                                self.label_samsung.setStyleSheet('background-color: lightskyblue ; color: red')
                                samsung_text_color = 'red'
                            else:
                                pass
                        else:
                            pass

                        samsung_price = result['현재가']
                    else:
                        pass
                    
                else:
                    pass
                
                '''
                elif result['단축코드'] == HYUNDAI:

                    if result['전일대비구분'] == '5':

                        jisu_str = "HD : {0}({1}, {2:0.1f}%)".format(현재가, format(-result['전일대비'], ','), result['등락율'])
                        self.label_2nd.setText(jisu_str)
                        self.label_2nd.setStyleSheet('background-color: blue ; color: white')

                    elif result['전일대비구분'] == '2':

                        jisu_str = "HD : {0}({1}, {2:0.1f}%)".format(현재가, format(result['전일대비'], ','), result['등락율'])
                        self.label_2nd.setText(jisu_str)
                        self.label_2nd.setStyleSheet('background-color: red ; color: white')

                    else:
                        jisu_str = "HD : {0}({1})".format(현재가, format(result['전일대비'], ','))
                        self.label_2nd.setText(jisu_str)
                        self.label_2nd.setStyleSheet('background-color: yellow ; color: black')

                elif result['단축코드'] == Celltrion:                    
                    
                    if result['전일대비구분'] == '5':

                        jisu_str = "CTRO : {0}({1}, {2:0.1f}%)".format(현재가, format(-result['전일대비'], ','), result['등락율'])
                        self.label_3rd.setText(jisu_str)
                        self.label_3rd.setStyleSheet('background-color: blue ; color: white')

                    elif result['전일대비구분'] == '2':

                        jisu_str = "CTRO : {0}({1}, {2:0.1f}%)".format(현재가, format(result['전일대비'], ','), result['등락율'])
                        self.label_3rd.setText(jisu_str)
                        self.label_3rd.setStyleSheet('background-color: red ; color: white')

                    else:
                        jisu_str = "CTRO : {0}({1})".format(현재가, format(result['전일대비'], ','))
                        self.label_3rd.setText(jisu_str)
                        self.label_3rd.setStyleSheet('background-color: yellow ; color: black')                    
                else:
                    pass
                '''

            elif szTrCode == 'IJ_':

                global kospi_price, kospi_text_color   
                global kosdaq_price, kosdaq_text_color 
                global flag_kp200_low, flag_kp200_high
                global flag_kp200_start_set

                # IJ 데이타표시
                if result['업종코드'] == KOSPI200:

                    # kp200 현재가
                    if result['지수'] != self.tableWidget_fut.item(2, Futures_column.현재가.value).text()[0:6]:

                        fut_realdata['KP200'] = round(float(result['지수']), 2)
                        kp200_realdata['현재가'] = round(float(result['지수']), 2)
                        df_fut.loc[2, '현재가'] = round(float(result['지수']), 2)
                        
                        #df_plotdata_kp200.iloc[0][x_idx] = kp200_realdata['현재가']

                        if float(result['지수']) < float(self.tableWidget_fut.item(2, Futures_column.현재가.value).text()[0:6]):
                            item = QTableWidgetItem(result['지수'] + '\n' + self.상태그림[0])
                        elif float(result['지수']) > float(self.tableWidget_fut.item(2, Futures_column.현재가.value).text()[0:6]):
                            item = QTableWidgetItem(result['지수'] + '\n' + self.상태그림[1])
                        else:    
                            item = QTableWidgetItem(result['지수'])

                        item.setTextAlignment(Qt.AlignCenter)

                        if float(result['지수']) < float(self.tableWidget_fut.item(2, Futures_column.현재가.value).text()[0:6]):
                            item.setBackground(QBrush(lightskyblue))
                        elif float(result['지수']) > float(self.tableWidget_fut.item(2, Futures_column.현재가.value).text()[0:6]):
                            item.setBackground(QBrush(pink))
                        else:
                            #item.setBackground(QBrush(옅은회색))
                            pass 

                        if kp200_realdata['현재가'] > kp200_realdata['시가']:
                            item.setForeground(QBrush(적색))
                        elif kp200_realdata['현재가'] < kp200_realdata['시가']:
                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))

                        self.tableWidget_fut.setItem(2, Futures_column.현재가.value, item)
                    else:
                        pass

                    if result['시가지수'] != self.tableWidget_fut.item(2, Futures_column.시가.value).text() and not flag_kp200_start_set:

                        flag_kp200_start_set = True

                        kp200_realdata['시가'] = round(float(result['시가지수']), 2)
                        df_plotdata_kp200.iloc[0][선물장간_시간차] = round(float(result['시가지수']), 2)

                        item = QTableWidgetItem(result['시가지수'])
                        item.setTextAlignment(Qt.AlignCenter)

                        if kp200_realdata['시가'] > kp200_종가:

                            item.setForeground(QBrush(적색))
                        elif kp200_realdata['시가'] < kp200_종가:

                            item.setForeground(QBrush(청색))
                        else:
                            item.setForeground(QBrush(검정색))

                        self.tableWidget_fut.setItem(2, Futures_column.시가.value, item)

                        item = QTableWidgetItem("{0:0.2f}".format(kp200_realdata['시가'] - kp200_종가))
                        item.setTextAlignment(Qt.AlignCenter)

                        if kp200_realdata['시가'] > kp200_종가:
                            item.setBackground(QBrush(콜기준가색))
                            item.setForeground(QBrush(검정색))
                        elif kp200_realdata['시가'] < kp200_종가:
                            item.setBackground(QBrush(풋기준가색))
                            item.setForeground(QBrush(흰색))
                        else:
                            item.setBackground(QBrush(흰색)) 

                        self.tableWidget_fut.setItem(2, Futures_column.시가갭.value, item)

                        str = '[{0:02d}:{1:02d}:{2:02d}] KP200 시작가 {3:0.2f}를 수신했습니다.\r'.format(
                            int(result['시간'][0:2]),
                            int(result['시간'][2:4]),
                            int(result['시간'][4:6]),
                            kp200_realdata['시가'])
                        self.textBrowser.append(str)                        
                        
                        atm_str = self.find_ATM(kp200_realdata['시가'])
                        atm_index = opt_actval.index(atm_str)

                        if atm_str[-1] == '2' or atm_str[-1] == '7':

                            atm_val = float(atm_str) + 0.5
                        else:
                            atm_val = float(atm_str)                     

                        # kp200 맥점 10개를 리스트로 만듬
                        global kp200_coreval

                        # kp200_coreval 리스트 기존데이타 삭제(초기화)
                        del kp200_coreval[:]

                        for i in range(6):

                            kp200_coreval.append(atm_val - 2.5 * i + 1.25) 

                        for i in range(1, 5):

                            kp200_coreval.append(atm_val + 2.5 * i + 1.25)

                        kp200_coreval.sort()

                        str = '[{0:02d}:{1:02d}:{2:02d}] KP200 맥점리스트 = {3}\r'.format(
                            int(result['시간'][0:2]),
                            int(result['시간'][2:4]),
                            int(result['시간'][4:6]),
                            kp200_coreval)
                        self.textBrowser.append(str)                         
                    else:
                        pass

                    if result['저가지수'] != self.tableWidget_fut.item(2, Futures_column.저가.value).text():

                        flag_kp200_low = True

                        kp200_realdata['저가'] = round(float(result['저가지수']), 2)

                        item = QTableWidgetItem(result['저가지수'])
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(흰색))                     
                        self.tableWidget_fut.setItem(2, Futures_column.저가.value, item)

                        if TARGET_MONTH_SELECT == 1:

                            t = int(result['시간'][0:2]) * 3600 + int(result['시간'][2:4]) * 60 + int(result['시간'][4:6])
                            self.kp200_low_node_coloring(t)

                        else:
                            pass

                        str = '[{0:02d}:{1:02d}:{2:02d}] kp200 저가 {3} Update...\r'.format(
                            int(result['시간'][0:2]),
                            int(result['시간'][2:4]),
                            int(result['시간'][4:6]), kp200_realdata['저가'])
                        self.textBrowser.append(str)
                    else:
                        pass

                    if result['고가지수'] != self.tableWidget_fut.item(2, Futures_column.고가.value).text():

                        flag_kp200_high = True

                        kp200_realdata['고가'] = round(float(result['고가지수']), 2)

                        item = QTableWidgetItem(result['고가지수'])
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(흰색))
                        self.tableWidget_fut.setItem(2, Futures_column.고가.value, item)

                        if TARGET_MONTH_SELECT == 1:

                            t = int(result['시간'][0:2]) * 3600 + int(result['시간'][2:4]) * 60 + int(result['시간'][4:6])
                            self.kp200_high_node_coloring(t)

                        else:
                            pass

                        str = '[{0:02d}:{1:02d}:{2:02d}] kp200 고가 {3} Update...\r'.format(
                            int(result['시간'][0:2]),
                            int(result['시간'][2:4]),
                            int(result['시간'][4:6]), kp200_realdata['고가'])
                        self.textBrowser.append(str)
                    else:
                        pass

                elif result['업종코드'] == KOSPI:                                     

                    if round(float(result['지수']), 2) != kospi_price:

                        if round(float(result['지수']), 2) > kospi_price:

                            temp_str = format(round(float(result['지수']), 2), ',')

                            if result['전일대비구분'] == '5':

                                jisu_str = "KOSPI: {0} ▲ (-{1:0.2f}, {2:0.1f}%)".format(temp_str, result['전일비'], result['등락율'])
                                self.label_kospi.setText(jisu_str)
                                self.label_kospi.setStyleSheet('background-color: pink ; color: blue')
                                kospi_text_color = 'blue'

                            elif result['전일대비구분'] == '2':

                                jisu_str = "KOSPI: {0} ▲ ({1:0.2f}, {2:0.1f}%)".format(temp_str, result['전일비'], result['등락율'])
                                self.label_kospi.setText(jisu_str)
                                self.label_kospi.setStyleSheet('background-color: pink ; color: red')
                                kospi_text_color = 'red'
                            else:
                                pass

                        elif round(float(result['지수']), 2) < kospi_price:

                            temp_str = format(round(float(result['지수']), 2), ',')

                            if result['전일대비구분'] == '5':

                                jisu_str = "KOSPI: {0} ▼ (-{1:0.2f}, {2:0.1f}%)".format(temp_str, result['전일비'], result['등락율'])
                                self.label_kospi.setText(jisu_str)
                                self.label_kospi.setStyleSheet('background-color: lightskyblue ; color: blue')
                                kospi_text_color = 'blue'

                            elif result['전일대비구분'] == '2':

                                jisu_str = "KOSPI: {0} ▼ ({1:0.2f}, {2:0.1f}%)".format(temp_str, result['전일비'], result['등락율'])
                                self.label_kospi.setText(jisu_str)
                                self.label_kospi.setStyleSheet('background-color: lightskyblue ; color: red')
                                kospi_text_color = 'red'
                            else:
                                pass
                        else:
                            pass

                        kospi_price = round(float(result['지수']), 2)
                    else:
                        pass                    

                elif result['업종코드'] == KOSDAQ:                                       

                    if round(float(result['지수']), 2) != kosdaq_price:                        

                        if round(float(result['지수']), 2) > kosdaq_price:

                            temp_str = format(round(float(result['지수']), 2), ',')

                            if result['전일대비구분'] == '5':

                                jisu_str = "KOSDAQ: {0} ▲ (-{1:0.2f}, {2:0.1f}%)".format(temp_str, result['전일비'], result['등락율'])
                                self.label_kosdaq.setText(jisu_str)
                                self.label_kosdaq.setStyleSheet('background-color: pink ; color: blue')
                                kosdaq_text_color = 'blue'

                            elif result['전일대비구분'] == '2':

                                jisu_str = "KOSDAQ: {0} ▲ ({1:0.2f}, {2:0.1f}%)".format(temp_str, result['전일비'], result['등락율'])
                                self.label_kosdaq.setText(jisu_str)
                                self.label_kosdaq.setStyleSheet('background-color: pink ; color: red')
                                kosdaq_text_color = 'red'
                            else:
                                pass

                        elif round(float(result['지수']), 2) < kosdaq_price:

                            temp_str = format(round(float(result['지수']), 2), ',')

                            if result['전일대비구분'] == '5':

                                jisu_str = "KOSDAQ: {0} ▼ (-{1:0.2f}, {2:0.1f}%)".format(temp_str, result['전일비'], result['등락율'])
                                self.label_kosdaq.setText(jisu_str)
                                self.label_kosdaq.setStyleSheet('background-color: lightskyblue ; color: blue')
                                kosdaq_text_color = 'blue'

                            elif result['전일대비구분'] == '2':

                                jisu_str = "KOSDAQ: {0} ▼ ({1:0.2f}, {2:0.1f}%)".format(temp_str, result['전일비'], result['등락율'])
                                self.label_kosdaq.setText(jisu_str)
                                self.label_kosdaq.setStyleSheet('background-color: lightskyblue ; color: red')
                                kosdaq_text_color = 'red'
                            else:
                                pass
                        else:
                            pass

                        kosdaq_price = round(float(result['지수']), 2)
                    else:
                        pass                    
                else:
                    pass

            elif szTrCode == 'BM_':

                if result['업종코드'] == FUTURES and result['투자자코드'] == FOREIGNER or result['업종코드'] == CME and result['투자자코드'] == FOREIGNER:

                    FUT_FOREIGNER_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_FOREIGNER_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                    FUT_FOREIGNER_직전대비.extend([int(result['거래대금순매수직전대비'])])
                    temp = list(FUT_FOREIGNER_직전대비)

                    순매수 = format(FUT_FOREIGNER_거래대금순매수, ',')

                    if min(temp) > 0:

                        item_str = "{0}\n({1})⬈".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 0).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(적색))
                            item.setForeground(QBrush(검정색))
                            self.tableWidget_supply.setItem(0, 0, item)
                        else:
                            pass

                    elif max(temp) < 0:

                        item_str = "{0}\n({1})⬊".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 0).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(청색))
                            item.setForeground(QBrush(흰색))
                            self.tableWidget_supply.setItem(0, 0, item)
                        else:
                            pass

                    else:

                        item_str = "{0}\n({1})".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 0).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(흰색))
                            item.setForeground(QBrush(검정색))
                            self.tableWidget_supply.setItem(0, 0, item)
                        else:
                            pass

                elif result['업종코드'] == FUTURES and result['투자자코드'] == RETAIL or result['업종코드'] == CME and result['투자자코드'] == RETAIL:

                    FUT_RETAIL_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_RETAIL_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                    FUT_RETAIL_직전대비.extend([int(result['거래대금순매수직전대비'])])
                    temp = list(FUT_RETAIL_직전대비)

                    순매수 = format(FUT_RETAIL_거래대금순매수, ',')

                    if min(temp) > 0:

                        item_str = "{0}\n({1})⬈".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 3).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            #item.setBackground(QBrush(적색))
                            #item.setForeground(QBrush(흰색))
                            self.tableWidget_supply.setItem(0, 3, item)
                        else:
                            pass

                    elif max(temp) < 0:

                        item_str = "{0}\n({1})⬊".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 3).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            #item.setBackground(QBrush(청색))
                            #item.setForeground(QBrush(흰색))
                            self.tableWidget_supply.setItem(0, 3, item)
                        else:
                            pass

                    else:
                        item_str = "{0}\n({1})".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 3).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            #item.setBackground(QBrush(흰색))
                            #item.setForeground(QBrush(검정색))
                            self.tableWidget_supply.setItem(0, 3, item)
                        else:
                            pass

                elif result['업종코드'] == FUTURES and result['투자자코드'] == INSTITUTIONAL or result['업종코드'] == CME and result['투자자코드'] == INSTITUTIONAL:

                    FUT_INSTITUTIONAL_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_INSTITUTIONAL_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                    기관_거래대금순매수 = FUT_INSTITUTIONAL_거래대금순매수 + FUT_STOCK_거래대금순매수 + FUT_BOHEOM_거래대금순매수 + \
                                 FUT_TOOSIN_거래대금순매수 + FUT_BANK_거래대금순매수 + FUT_JONGGEUM_거래대금순매수 + \
                                 FUT_GIGEUM_거래대금순매수 + FUT_GITA_거래대금순매수

                    기관_거래대금순매수_직전대비 = FUT_INSTITUTIONAL_거래대금순매수_직전대비 + FUT_STOCK_거래대금순매수_직전대비 + \
                                      FUT_BOHEOM_거래대금순매수_직전대비 + FUT_TOOSIN_거래대금순매수_직전대비 + FUT_BANK_거래대금순매수_직전대비 + \
                                      FUT_JONGGEUM_거래대금순매수_직전대비 + FUT_GIGEUM_거래대금순매수_직전대비 + FUT_GITA_거래대금순매수_직전대비

                    FUT_INSTITUTIONAL_직전대비.extend([기관_거래대금순매수_직전대비])
                    temp = list(FUT_INSTITUTIONAL_직전대비)

                    순매수 = format(기관_거래대금순매수, ',')

                    if min(temp) > 0:

                        item_str = "{0}\n({1})⬈".format(순매수, 기관_거래대금순매수_직전대비)

                        if item_str != self.tableWidget_supply.item(0, 4).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(적색))
                            item.setForeground(QBrush(검정색))
                            self.tableWidget_supply.setItem(0, 4, item)
                        else:
                            pass

                    elif max(temp) < 0:

                        item_str = "{0}\n({1})⬊".format(순매수, 기관_거래대금순매수_직전대비)

                        if item_str != self.tableWidget_supply.item(0, 4).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(청색))
                            item.setForeground(QBrush(흰색))
                            self.tableWidget_supply.setItem(0, 4, item)
                        else:
                            pass

                    else:
                        item_str = "{0}\n({1})".format(순매수, 기관_거래대금순매수_직전대비)

                        if item_str != self.tableWidget_supply.item(0, 4).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(흰색))
                            item.setForeground(QBrush(검정색))
                            self.tableWidget_supply.setItem(0, 4, item)
                        else:
                            pass

                elif result['업종코드'] == FUTURES and result['투자자코드'] == STOCK or result['업종코드'] == CME and result['투자자코드'] == STOCK:

                    FUT_STOCK_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_STOCK_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == FUTURES and result['투자자코드'] == BOHEOM or result['업종코드'] == CME and result['투자자코드'] == BOHEOM:

                    FUT_BOHEOM_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_BOHEOM_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == FUTURES and result['투자자코드'] == TOOSIN or result['업종코드'] == CME and result['투자자코드'] == TOOSIN:

                    FUT_TOOSIN_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_TOOSIN_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == FUTURES and result['투자자코드'] == BANK or result['업종코드'] == CME and result['투자자코드'] == BANK:

                    FUT_BANK_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_BANK_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == FUTURES and result['투자자코드'] == JONGGEUM or result['업종코드'] == CME and result['투자자코드'] == JONGGEUM:

                    FUT_JONGGEUM_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_JONGGEUM_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == FUTURES and result['투자자코드'] == GIGEUM or result['업종코드'] == CME and result['투자자코드'] == GIGEUM:

                    FUT_GIGEUM_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_GIGEUM_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == FUTURES and result['투자자코드'] == GITA or result['업종코드'] == CME and result['투자자코드'] == GITA:

                    FUT_GITA_거래대금순매수 = int(result['거래대금순매수'])
                    FUT_GITA_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == FOREIGNER:

                    KOSPI_FOREIGNER_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_FOREIGNER_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                    KOSPI_FOREIGNER_직전대비.extend([int(result['거래대금순매수직전대비'])])
                    temp = list(KOSPI_FOREIGNER_직전대비)

                    순매수 = format(KOSPI_FOREIGNER_거래대금순매수, ',')

                    if min(temp) > 0:

                        item_str = "{0}\n({1})⬈".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 2).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(적색))
                            item.setForeground(QBrush(검정색))
                            self.tableWidget_supply.setItem(0, 2, item)
                        else:
                            pass

                    elif max(temp) < 0:

                        item_str = "{0}\n({1})⬊".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 2).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(청색))
                            item.setForeground(QBrush(흰색))
                            self.tableWidget_supply.setItem(0, 2, item)
                        else:
                            pass

                    else:
                        item_str = "{0}\n({1})".format(순매수, result['거래대금순매수직전대비'])

                        if item_str != self.tableWidget_supply.item(0, 2).text():
                            item = QTableWidgetItem(item_str)
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setBackground(QBrush(흰색))
                            item.setForeground(QBrush(검정색))
                            self.tableWidget_supply.setItem(0, 2, item)
                        else:
                            pass

                elif result['업종코드'] == KOSPI and result['투자자코드'] == RETAIL:

                    KOSPI_RETAIL_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_RETAIL_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == INSTITUTIONAL:

                    KOSPI_INSTITUTIONAL_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_INSTITUTIONAL_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == STOCK:

                    KOSPI_STOCK_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_STOCK_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == BOHEOM:

                    KOSPI_BOHEOM_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_BOHEOM_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == TOOSIN:

                    KOSPI_TOOSIN_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_TOOSIN_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == BANK:

                    KOSPI_BANK_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_BANK_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == JONGGEUM:

                    KOSPI_JONGGEUM_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_JONGGEUM_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == GIGEUM:

                    KOSPI_GIGEUM_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_GIGEUM_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])

                elif result['업종코드'] == KOSPI and result['투자자코드'] == GITA:

                    KOSPI_GITA_거래대금순매수 = int(result['거래대금순매수'])
                    KOSPI_GITA_거래대금순매수_직전대비 = int(result['거래대금순매수직전대비'])
                else:
                    pass

                if overnight:

                    선물_거래대금순매수 = FUT_FOREIGNER_거래대금순매수 + FUT_RETAIL_거래대금순매수 + \
                                 FUT_INSTITUTIONAL_거래대금순매수 + FUT_STOCK_거래대금순매수 + FUT_BOHEOM_거래대금순매수 + \
                                 FUT_TOOSIN_거래대금순매수 + FUT_BANK_거래대금순매수 + FUT_JONGGEUM_거래대금순매수 + \
                                 FUT_GIGEUM_거래대금순매수 + FUT_GITA_거래대금순매수

                    선물_거래대금순매수_직전대비 = FUT_FOREIGNER_거래대금순매수_직전대비 + FUT_RETAIL_거래대금순매수_직전대비 + \
                                      FUT_INSTITUTIONAL_거래대금순매수_직전대비 + FUT_STOCK_거래대금순매수_직전대비 + \
                                      FUT_BOHEOM_거래대금순매수_직전대비 + FUT_TOOSIN_거래대금순매수_직전대비 + FUT_BANK_거래대금순매수_직전대비 + \
                                      FUT_JONGGEUM_거래대금순매수_직전대비 + FUT_GIGEUM_거래대금순매수_직전대비 + \
                                      FUT_GITA_거래대금순매수_직전대비

                    현물_거래대금순매수 = 0
                    현물_거래대금순매수_직전대비 = 0

                    temp1 = format(선물_거래대금순매수, ',')
                    temp2 = format(현물_거래대금순매수, ',')
                    '''
                    item_str = "{0}({1})/{2}({3})\n({4} : {5})".format(temp1, 선물_거래대금순매수_직전대비, temp2, 현물_거래대금순매수_직전대비, \
                        repr(pre_콜시가갭합), repr(pre_풋시가갭합))
                    '''
                    item_str = "{0}({1})/{2}({3})".format(temp1, 선물_거래대금순매수_직전대비, temp2, 현물_거래대금순매수_직전대비)

                    if item_str != self.tableWidget_supply.item(0, 5).text():
                        item = QTableWidgetItem(item_str)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget_supply.setItem(0, 5, item)
                    else:
                        pass
                else:
                    pass

            elif szTrCode == 'PM_':

                프로그램_전체순매수금액 = int(result['전체순매수금액합계'] / 100)
                프로그램_전체순매수금액직전대비 = int(result['전체순매수금액직전대비'] / 100)

                선물_거래대금순매수 = FUT_FOREIGNER_거래대금순매수 + FUT_RETAIL_거래대금순매수 + \
                             FUT_INSTITUTIONAL_거래대금순매수 + FUT_STOCK_거래대금순매수 + FUT_BOHEOM_거래대금순매수 + \
                             FUT_TOOSIN_거래대금순매수 + FUT_BANK_거래대금순매수 + FUT_JONGGEUM_거래대금순매수 + \
                             FUT_GIGEUM_거래대금순매수 + FUT_GITA_거래대금순매수

                선물_거래대금순매수_직전대비 = FUT_FOREIGNER_거래대금순매수_직전대비 + FUT_RETAIL_거래대금순매수_직전대비 + \
                                  FUT_INSTITUTIONAL_거래대금순매수_직전대비 + FUT_STOCK_거래대금순매수_직전대비 + \
                                  FUT_BOHEOM_거래대금순매수_직전대비 + FUT_TOOSIN_거래대금순매수_직전대비 + FUT_BANK_거래대금순매수_직전대비 + \
                                  FUT_JONGGEUM_거래대금순매수_직전대비 + FUT_GIGEUM_거래대금순매수_직전대비 + \
                                  FUT_GITA_거래대금순매수_직전대비

                현물_거래대금순매수 = KOSPI_FOREIGNER_거래대금순매수 + KOSPI_RETAIL_거래대금순매수 + \
                             KOSPI_INSTITUTIONAL_거래대금순매수 + KOSPI_STOCK_거래대금순매수 + KOSPI_BOHEOM_거래대금순매수 + \
                             KOSPI_TOOSIN_거래대금순매수 + KOSPI_BANK_거래대금순매수 + KOSPI_JONGGEUM_거래대금순매수 + \
                             KOSPI_GIGEUM_거래대금순매수 + KOSPI_GITA_거래대금순매수 + 프로그램_전체순매수금액

                현물_거래대금순매수_직전대비 = KOSPI_FOREIGNER_거래대금순매수_직전대비 + KOSPI_RETAIL_거래대금순매수_직전대비 + \
                                  KOSPI_INSTITUTIONAL_거래대금순매수_직전대비 + KOSPI_STOCK_거래대금순매수_직전대비 + \
                                  KOSPI_BOHEOM_거래대금순매수_직전대비 + KOSPI_TOOSIN_거래대금순매수_직전대비 + KOSPI_BANK_거래대금순매수_직전대비 + \
                                  KOSPI_JONGGEUM_거래대금순매수_직전대비 + KOSPI_GIGEUM_거래대금순매수_직전대비 + \
                                  KOSPI_GITA_거래대금순매수_직전대비 + 프로그램_전체순매수금액직전대비

                PROGRAM_직전대비.extend([프로그램_전체순매수금액직전대비])
                temp = list(PROGRAM_직전대비)

                순매수 = format(프로그램_전체순매수금액, ',')

                if min(temp) > 0:

                    item_str = "{0}\n({1})⬈".format(순매수, 프로그램_전체순매수금액직전대비)

                    if item_str != self.tableWidget_supply.item(0, 1).text():
                        item = QTableWidgetItem(item_str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(적색))
                        item.setForeground(QBrush(검정색))
                        self.tableWidget_supply.setItem(0, 1, item)
                    else:
                        pass

                elif max(temp) < 0:

                    item_str = "{0}\n({1})⬊".format(순매수, 프로그램_전체순매수금액직전대비)

                    if item_str != self.tableWidget_supply.item(0, 1).text():
                        item = QTableWidgetItem(item_str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(청색))
                        item.setForeground(QBrush(흰색))
                        self.tableWidget_supply.setItem(0, 1, item)
                    else:
                        pass

                else:
                    item_str = "{0}\n({1})".format(순매수, 프로그램_전체순매수금액직전대비)

                    if item_str != self.tableWidget_supply.item(0, 1).text():
                        item = QTableWidgetItem(item_str)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setBackground(QBrush(흰색))
                        item.setForeground(QBrush(검정색))
                        self.tableWidget_supply.setItem(0, 1, item)
                    else:
                        pass

                temp1 = format(선물_거래대금순매수, ',')
                temp2 = format(현물_거래대금순매수, ',')
                '''
                item_str = "{0}({1})/{2}({3})\n({4} : {5})".format(temp1, 선물_거래대금순매수_직전대비, temp2, 현물_거래대금순매수_직전대비, \
                        repr(pre_콜시가갭합), repr(pre_풋시가갭합))
                '''
                item_str = "{0}({1})/{2}({3})".format(temp1, 선물_거래대금순매수_직전대비, temp2, 현물_거래대금순매수_직전대비)

                if item_str != self.tableWidget_supply.item(0, 5).text():
                    item = QTableWidgetItem(item_str)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget_supply.setItem(0, 5, item)
                else:
                    pass

            elif szTrCode == 'FC0' or szTrCode == 'NC0':

                if pre_start:
                    pre_start = False
                else:
                    pass

                if szTrCode == 'FC0':

                    if not market_service: 

                        market_service = True

                        str = '[{0:02d}:{1:02d}:{2:02d}] 실시간 주간 선물 데이타를 수신했습니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                        self.textBrowser.append(str)
                    else:
                        pass
                else:
                    pass

                if szTrCode == 'NC0':    

                    if not market_service: 

                        market_service = True

                        str = '[{0:02d}:{1:02d}:{2:02d}] 실시간 야간 선물 데이타를 수신했습니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                        self.textBrowser.append(str)
                    else:
                        pass
                else:
                    pass                

                # 세로축 시간 좌표값 계산
                if overnight:

                    if result['체결시간'] != '':
                        nighttime = int(result['체결시간'][0:2])

                        if 0 <= nighttime <= 5:
                            nighttime = nighttime + 24
                        else:
                            pass

                        x_idx = (nighttime - kse_start_hour) * 60 + int(result['체결시간'][2:4]) + 1
                    else:
                        x_idx = 1
                else:

                    if result['체결시간'] != '':
                        x_idx = (int(result['체결시간'][0:2]) - kse_start_hour) * 60 + int(result['체결시간'][2:4]) + 1
                    else:
                        x_idx = 1

                # 해외선물 시작시간과 동기를 맞춤
                x_idx = x_idx + 선물장간_시간차

                if result['현재가'] != 선물현재가:
                       
                    선물현재가 = result['현재가']

                    self.futures_display(result)

                    '''
                    if szTrCode == 'FC0':

                        if result['전일동시간대거래량'] > 0:

                            if overnight:
                                fut_vr = float(self.tableWidget_fut.item(0, Futures_column.FR.value).text())
                            else:
                                fut_vr = float(self.tableWidget_fut.item(1, Futures_column.FR.value).text())

                            vr = result['누적거래량'] / result['전일동시간대거래량']

                            if vr != fut_vr:
                                item = QTableWidgetItem("{0:0.1f}".format(vr))
                                item.setTextAlignment(Qt.AlignCenter)

                                if overnight:
                                    self.tableWidget_fut.setItem(0, Futures_column.FR.value, item)
                                else:
                                    self.tableWidget_fut.setItem(1, Futures_column.FR.value, item)
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                    '''                
                else:
                    pass

            elif szTrCode == 'OC0' or szTrCode == 'EC0':

                if not market_service: 

                    market_service = True

                    str = '[{0:02d}:{1:02d}:{2:02d}] 실시간 옵션 데이타를 수신했습니다.\r'.format(int(호가시간[0:2]), int(호가시간[2:4]), int(호가시간[4:6]))
                    self.textBrowser.append(str)
                else:
                    pass

                if pre_start:
                    pre_start = False
                else:
                    pass

                # X축 시간좌표 계산
                if overnight:

                    if result['체결시간'] != '':

                        nighttime = int(result['체결시간'][0:2])

                        if 0 <= nighttime <= 5:
                            nighttime = nighttime + 24
                        else:
                            pass

                        opt_x_idx = (nighttime - kse_start_hour) * 60 + int(result['체결시간'][2:4]) + 1
                    else:
                        opt_x_idx = 1
                else:

                    if result['체결시간'] != '':
                        opt_x_idx = (int(result['체결시간'][0:2]) - kse_start_hour) * 60 + int(result['체결시간'][2:4]) + 1
                    else:
                        opt_x_idx = 1

                # 해외선물 시작시간과 동기를 맞춤
                opt_x_idx = opt_x_idx + 선물장간_시간차  

                '''
                str = '[{0:02d}:{1:02d}:{2:02d}] opt_x_idx = {3} \r'.format(
                            int(result['체결시간'][0:2]),
                            int(result['체결시간'][2:4]),
                            int(result['체결시간'][4:6]),
                            opt_x_idx)              
                
                if overnight:                    
                    self.textBrowser.append(str)
                else:
                    print(str)
                '''

                if result['단축코드'][0:3] == '201':
                    
                    if result['현재가'] != 콜현재가:
                        
                        콜현재가 = result['현재가']

                        call_result = copy.deepcopy(result)                        
                        self.call_display(result)                      
                        '''
                        if opt_callreal_update_counter >= 500:

                            opt_callreal_update_counter = 0
                            opt_putreal_update_counter = 0
                        else:
                            pass

                        process_time = (timeit.default_timer() - start_time) * 1000

                        if opt_callreal_update_counter >= opt_putreal_update_counter:

                            str = '[{0:02d}:{1:02d}:{2:02d}] Call {3} 수신, C({4}/{5}) : {6:0.2f} ms... \r'.format(
                                int(result['체결시간'][0:2]),
                                int(result['체결시간'][2:4]),
                                int(result['체결시간'][4:6]),
                                result['현재가'],
                                opt_callreal_update_counter,
                                opt_putreal_update_counter,
                                process_time)
                            self.textBrowser.append(str)
                        else:

                            str = '[{0:02d}:{1:02d}:{2:02d}] Call {3} 수신, P({4}/{5}) : {6:0.2f} ms... \r'.format(
                                int(result['체결시간'][0:2]),
                                int(result['체결시간'][2:4]),
                                int(result['체결시간'][4:6]),
                                result['현재가'],
                                opt_callreal_update_counter,
                                opt_putreal_update_counter,
                                process_time)
                            self.textBrowser.append(str)
                        '''
                    else:
                        pass 

                elif result['단축코드'][0:3] == '301':
                    
                    if result['현재가'] != 풋현재가:

                        풋현재가 = result['현재가']

                        put_result = copy.deepcopy(result)
                        self.put_display(result)                      
                        '''
                        if opt_putreal_update_counter >= 500:

                            opt_callreal_update_counter = 0
                            opt_putreal_update_counter = 0
                        else:
                            pass

                        process_time = (timeit.default_timer() - start_time) * 1000

                        if opt_callreal_update_counter >= opt_putreal_update_counter:

                            str = '[{0:02d}:{1:02d}:{2:02d}] Put {3} 수신, C({4}/{5}) : {6:0.2f} ms... \r'.format(
                                int(result['체결시간'][0:2]),
                                int(result['체결시간'][2:4]),
                                int(result['체결시간'][4:6]),
                                result['현재가'],
                                opt_callreal_update_counter,
                                opt_putreal_update_counter,
                                process_time)
                            self.textBrowser.append(str)
                        else:

                            str = '[{0:02d}:{1:02d}:{2:02d}] Put {3} 수신, P({4}/{5}) : {6:0.2f} ms... \r'.format(
                                int(result['체결시간'][0:2]),
                                int(result['체결시간'][2:4]),
                                int(result['체결시간'][4:6]),
                                result['현재가'],
                                opt_callreal_update_counter,
                                opt_putreal_update_counter,
                                process_time)
                            self.textBrowser.append(str)
                        '''   
                    else:
                        pass 
                else:
                    pass

            elif szTrCode == 'OH0' or szTrCode == 'EH0':

                if not receive_quote:
                    receive_quote = True
                else:
                    pass

                if result['단축코드'][0:3] == '201':

                    index = call_행사가.index(result['단축코드'][5:8])

                    df_call_hoga.loc[index, '매수건수'] = result['매수호가총건수']
                    df_call_hoga.loc[index, '매도건수'] = result['매도호가총건수']
                    df_call_hoga.loc[index, '매수잔량'] = result['매수호가총수량']
                    df_call_hoga.loc[index, '매도잔량'] = result['매도호가총수량']

                    opt_call_ho_update_counter += 1

                elif result['단축코드'][0:3] == '301':

                    index = put_행사가.index(result['단축코드'][5:8])

                    df_put_hoga.loc[index, '매수건수'] = result['매수호가총건수']
                    df_put_hoga.loc[index, '매도건수'] = result['매도호가총건수']
                    df_put_hoga.loc[index, '매수잔량'] = result['매수호가총수량']
                    df_put_hoga.loc[index, '매도잔량'] = result['매도호가총수량']

                    opt_put_ho_update_counter += 1

                else:
                    pass

                if opt_call_ho_update_counter == 1000 or opt_put_ho_update_counter == 1000:

                    opt_call_ho_update_counter = 0
                    opt_put_ho_update_counter = 0
                else:
                    pass

                '''
                process_time = (timeit.default_timer() - start_time) * 1000

                if process_time > 0:

                    if opt_call_ho_update_counter >= opt_put_ho_update_counter:

                        str = '[{0:02d}:{1:02d}:{2:02d}] RealData Call {3}=[{4}/{5}] --> {6:0.2f} ms... \r'.format(
                            dt.hour,
                            dt.minute,
                            dt.second,
                            szTrCode,
                            opt_call_ho_update_counter,
                            opt_put_ho_update_counter,
                            process_time)
                        # self.textBrowser.append(str)
                        print(str)
                    else:
                        str = '[{0:02d}:{1:02d}:{2:02d}] RealData Put {3}=[{4}/{5}] --> {6:0.2f} ms... \r'.format(
                            dt.hour,
                            dt.minute,
                            dt.second,
                            szTrCode,
                            opt_call_ho_update_counter,
                            opt_put_ho_update_counter,
                            process_time)
                        # self.textBrowser.append(str)
                        print(str)
                else:
                    pass
                '''

            elif szTrCode == 'FH0' or szTrCode == 'NH0':
                
                호가시간 = result['호가시간']

                # 선물호가 갱신
                item = QTableWidgetItem("{0}".format(format(result['매수호가총건수'], ',')))
                item.setTextAlignment(Qt.AlignCenter)

                if overnight:
                    self.tableWidget_fut.setItem(0, Futures_column.매수건수.value, item)
                else:
                    self.tableWidget_fut.setItem(1, Futures_column.매수건수.value, item)

                item = QTableWidgetItem("{0}".format(format(result['매도호가총건수'], ',')))
                item.setTextAlignment(Qt.AlignCenter)

                if overnight:
                    self.tableWidget_fut.setItem(0, Futures_column.매도건수.value, item)
                else:
                    self.tableWidget_fut.setItem(1, Futures_column.매도건수.value, item)

                item = QTableWidgetItem("{0}".format(format(result['매수호가총수량'], ',')))
                item.setTextAlignment(Qt.AlignCenter)

                if overnight:
                    self.tableWidget_fut.setItem(0, Futures_column.매수잔량.value, item)
                else:
                    self.tableWidget_fut.setItem(1, Futures_column.매수잔량.value, item)

                item = QTableWidgetItem("{0}".format(format(result['매도호가총수량'], ',')))
                item.setTextAlignment(Qt.AlignCenter)

                if overnight:
                    self.tableWidget_fut.setItem(0, Futures_column.매도잔량.value, item)
                else:
                    self.tableWidget_fut.setItem(1, Futures_column.매도잔량.value, item)

                if result['매도호가총건수'] > 0:

                    fut_cr = result['매수호가총건수'] / result['매도호가총건수']

                    item = QTableWidgetItem("{0:0.2f}".format(fut_cr))
                    item.setTextAlignment(Qt.AlignCenter)

                    if overnight:
                        self.tableWidget_fut.setItem(0, Futures_column.건수비.value, item)
                    else:
                        self.tableWidget_fut.setItem(1, Futures_column.건수비.value, item)
                else:
                    pass

                if result['매도호가총수량'] > 0:

                    fut_rr = result['매수호가총수량'] / result['매도호가총수량']

                    item = QTableWidgetItem("{0:0.2f}".format(fut_rr))
                    item.setTextAlignment(Qt.AlignCenter)

                    if overnight:
                        self.tableWidget_fut.setItem(0, Futures_column.잔량비.value, item)
                    else:
                        self.tableWidget_fut.setItem(1, Futures_column.잔량비.value, item)
                else:
                    pass

                if not overnight:

                    if fut_cr > 1 and fut_cr > fut_rr:

                        self.tableWidget_fut.item(1, Futures_column.건수비.value).setBackground(QBrush(적색))
                        self.tableWidget_fut.item(1, Futures_column.건수비.value).setForeground(QBrush(검정색))
                        self.tableWidget_fut.item(1, Futures_column.잔량비.value).setBackground(QBrush(적색))
                        self.tableWidget_fut.item(1, Futures_column.잔량비.value).setForeground(QBrush(검정색))

                    elif fut_cr < 1 and fut_cr < fut_rr:

                        self.tableWidget_fut.item(1, Futures_column.건수비.value).setBackground(QBrush(청색))
                        self.tableWidget_fut.item(1, Futures_column.건수비.value).setForeground(QBrush(흰색))
                        self.tableWidget_fut.item(1, Futures_column.잔량비.value).setBackground(QBrush(청색))
                        self.tableWidget_fut.item(1, Futures_column.잔량비.value).setForeground(QBrush(흰색))
                    else:
                        self.tableWidget_fut.item(1, Futures_column.건수비.value).setBackground(QBrush(흰색))
                        self.tableWidget_fut.item(1, Futures_column.건수비.value).setForeground(QBrush(검정색))
                        self.tableWidget_fut.item(1, Futures_column.잔량비.value).setBackground(QBrush(흰색))
                        self.tableWidget_fut.item(1, Futures_column.잔량비.value).setForeground(QBrush(검정색))
                else:
                    pass

                if pre_start:

                    self.tableWidget_fut.resizeColumnsToContents()
                else:
                    pass

                '''
                process_time = (timeit.default_timer() - start_time) * 1000

                if process_time > 0:
                    str = '[{0:02d}:{1:02d}:{2:02d}] RealData 처리시간 {3} --> {4:0.2f} ms... \r'.format(
                        dt.hour,
                        dt.minute,
                        dt.second,
                        szTrCode,
                        process_time)
                    # self.textBrowser.append(str)
                    #print(str)
                else:
                    pass
                '''
            
            elif szTrCode == 'OVC':
                
                if not receive_real_ovc:
                    receive_real_ovc = True
                else:
                    pass

                OVC_체결시간 = result['체결시간_한국']                

                # X축 시간좌표 계산
                if overnight:

                    global night_time

                    if result['체결시간_한국'] != '':

                        night_time = int(result['체결시간_한국'][0:2])

                        if 0 <= night_time <= 6:
                            night_time = night_time + 24
                        else:
                            pass

                        ovc_x_idx = (night_time - (kse_start_hour - 1)) * 60 + int(result['체결시간_한국'][2:4]) + 1
                    else:
                        ovc_x_idx = 1

                    if ovc_x_idx < 0:

                        str = '{0}--{1}'.format(night_time, kse_start_hour)

                        self.label_atm.setText(str)
                    else:
                        pass                    
                else:
                    # 해외선물 개장시간은 국내시장의 1시간 전
                    if result['체결시간_한국'] != '':
                        ovc_x_idx = (int(result['체결시간_한국'][0:2]) - ovc_start_hour) * 60 + int(result['체결시간_한국'][2:4]) + 1
                    else:
                        ovc_x_idx = 1    

                # 해외선물 시작시간과 동기를 맞춤

                서버시간 = int(OVC_체결시간[0:2]) * 3600 + int(OVC_체결시간[2:4]) * 60 + int(OVC_체결시간[4:6])

                시스템_서버_시간차 = 시스템시간 - 서버시간

                if result['종목코드'] == NASDAQ:                    

                    nasdaq_저가 =  result['저가']
                    nasdaq_고가 =  result['고가']              

                    if result['체결가격'] != nasdaq_price:
                        
                        nasdaq_delta_old = nasdaq_delta
                        nasdaq_delta = result['체결가격']
                        nasdaq_직전대비.extend([nasdaq_delta - nasdaq_delta_old])
                        temp = list(nasdaq_직전대비)
                        
                        if 2 <= ovc_x_idx <= overnight_timespan - 1:
                            df_plotdata_nasdaq.iloc[0][ovc_x_idx] = result['체결가격']
                        else:
                            pass

                        if result['체결가격'] > nasdaq_price:

                            if result['전일대비기호'] == '5':

                                if nasdaq_전일종가 == 0.0:
                                    nasdaq_전일종가 = result['체결가격'] + result['전일대비']
                                    df_plotdata_nasdaq.iloc[0][0] = nasdaq_전일종가
                                    df_plotdata_nasdaq.iloc[0][1] = result['시가']
                                    nasdaq_시가 = result['시가']

                                    if NASDAQ_LAST_LOW > 0 and NASDAQ_LAST_HIGH > 0:

                                        nasdaq_피봇 = self.calc_pivot(NASDAQ_LAST_LOW, NASDAQ_LAST_HIGH, nasdaq_전일종가, nasdaq_시가)
                                    else:
                                        pass
                                else:
                                    pass                                

                                if min(temp) > 0:
                                    jisu_str = "NASDAQ: {0:.2f} (-{1:.2f}, {2:0.2f}%)⬈".format(result['체결가격'], result['전일대비'], result['등락율'])                                    
                                else:
                                    jisu_str = "NASDAQ: {0:.2f} ▲ (-{1:.2f}, {2:0.2f}%)".format(result['체결가격'], result['전일대비'], result['등락율'])

                                self.label_3rd.setText(jisu_str)
                                self.label_3rd.setStyleSheet('background-color: pink ; color: blue')
                                nasdaq_text_color = 'blue'

                            elif result['전일대비기호'] == '2':

                                if nasdaq_전일종가 == 0.0:
                                    nasdaq_전일종가 = result['체결가격'] - result['전일대비']
                                    df_plotdata_nasdaq.iloc[0][0] = nasdaq_전일종가
                                    df_plotdata_nasdaq.iloc[0][1] = result['시가']
                                    nasdaq_시가 = result['시가']

                                    if NASDAQ_LAST_LOW > 0 and NASDAQ_LAST_HIGH > 0:

                                        nasdaq_피봇 = self.calc_pivot(NASDAQ_LAST_LOW, NASDAQ_LAST_HIGH, nasdaq_전일종가, nasdaq_시가)
                                    else:
                                        pass
                                else:
                                    pass                                

                                if min(temp) > 0:
                                    jisu_str = "NASDAQ: {0:.2f} ({1:.2f}, {2:0.2f}%)⬈".format(result['체결가격'], result['전일대비'], result['등락율'])                                    
                                else:
                                    jisu_str = "NASDAQ: {0:.2f} ▲ ({1:.2f}, {2:0.2f}%)".format(result['체결가격'], result['전일대비'], result['등락율'])

                                self.label_3rd.setText(jisu_str)
                                self.label_3rd.setStyleSheet('background-color: pink ; color: red')
                                nasdaq_text_color = 'red'
                            else:
                                pass

                        elif result['체결가격'] < nasdaq_price:

                            if result['전일대비기호'] == '5':

                                if nasdaq_전일종가 == 0.0:
                                    nasdaq_전일종가 = result['체결가격'] + result['전일대비']
                                    df_plotdata_nasdaq.iloc[0][0] = nasdaq_전일종가
                                    df_plotdata_nasdaq.iloc[0][1] = result['시가']
                                    nasdaq_시가 = result['시가']

                                    if NASDAQ_LAST_LOW > 0 and NASDAQ_LAST_HIGH > 0:

                                        nasdaq_피봇 = self.calc_pivot(NASDAQ_LAST_LOW, NASDAQ_LAST_HIGH, nasdaq_전일종가, nasdaq_시가)
                                    else:
                                        pass
                                else:
                                    pass                                

                                if max(temp) < 0:
                                    jisu_str = "NASDAQ: {0:.2f} (-{1:.2f}, {2:0.2f}%)⬊".format(result['체결가격'], result['전일대비'], result['등락율'])                                    
                                else:
                                    jisu_str = "NASDAQ: {0:.2f} ▼ (-{1:.2f}, {2:0.2f}%)".format(result['체결가격'], result['전일대비'], result['등락율'])

                                self.label_3rd.setText(jisu_str)
                                self.label_3rd.setStyleSheet('background-color: lightskyblue ; color: blue')
                                nasdaq_text_color = 'blue'

                            elif result['전일대비기호'] == '2':

                                if nasdaq_전일종가 == 0.0:
                                    nasdaq_전일종가 = result['체결가격'] - result['전일대비']
                                    df_plotdata_nasdaq.iloc[0][0] = nasdaq_전일종가
                                    df_plotdata_nasdaq.iloc[0][1] = result['시가']
                                    nasdaq_시가 = result['시가']

                                    if NASDAQ_LAST_LOW > 0 and NASDAQ_LAST_HIGH > 0:

                                        nasdaq_피봇 = self.calc_pivot(NASDAQ_LAST_LOW, NASDAQ_LAST_HIGH, nasdaq_전일종가, nasdaq_시가)
                                    else:
                                        pass
                                else:
                                    pass                                

                                if max(temp) < 0:
                                    jisu_str = "NASDAQ: {0:.2f} ({1:.2f}, {2:0.2f}%)⬊".format(result['체결가격'], result['전일대비'], result['등락율'])                                    
                                else:
                                    jisu_str = "NASDAQ: {0:.2f} ▼ ({1:.2f}, {2:0.2f}%)".format(result['체결가격'], result['전일대비'], result['등락율'])

                                self.label_3rd.setText(jisu_str)
                                self.label_3rd.setStyleSheet('background-color: lightskyblue ; color: red')
                                nasdaq_text_color = 'red'
                            else:
                                pass
                        else:
                            pass

                        nasdaq_price = result['체결가격']
                    else:
                        pass                    

                elif result['종목코드'] == SP500:                    

                    sp500_저가 =  result['저가']
                    sp500_고가 =  result['고가']

                    if result['체결가격'] != sp500_price:
                        
                        sp500_delta_old = sp500_delta
                        sp500_delta = result['체결가격']
                        sp500_직전대비.extend([sp500_delta - sp500_delta_old])
                        temp = list(sp500_직전대비)
                        
                        if 2 <= ovc_x_idx <= overnight_timespan - 1:
                            df_plotdata_sp500.iloc[0][ovc_x_idx] = result['체결가격']
                        else:
                            pass
                        
                        if result['체결가격'] > sp500_price:

                            체결가격 = locale.format('%.2f', result['체결가격'], 1)
                            
                            if result['전일대비기호'] == '5':

                                if sp500_전일종가 == 0.0:
                                    sp500_전일종가 = result['체결가격'] + result['전일대비']
                                    df_plotdata_sp500.iloc[0][0] = sp500_전일종가
                                    df_plotdata_sp500.iloc[0][1] = result['시가']
                                    sp500_시가 = result['시가']

                                    if SP500_LAST_LOW > 0 and SP500_LAST_HIGH > 0:

                                        sp500_피봇 = self.calc_pivot(SP500_LAST_LOW, SP500_LAST_HIGH, sp500_전일종가, sp500_시가)
                                    else:
                                        pass
                                else:
                                    pass

                                전일대비 = locale.format('%.2f', -result['전일대비'], 1)                                

                                if min(temp) > 0:
                                    jisu_str = "S&P 500: {0} ({1}, {2:0.2f}%)⬈".format(체결가격, 전일대비, result['등락율'])                                    
                                else:
                                    jisu_str = "S&P 500: {0} ▲ ({1}, {2:0.2f}%)".format(체결가격, 전일대비, result['등락율'])

                                self.label_1st.setText(jisu_str)
                                self.label_1st.setStyleSheet('background-color: pink; color: blue')
                                sp500_text_color = 'blue'

                            elif result['전일대비기호'] == '2':

                                if sp500_전일종가 == 0.0:
                                    sp500_전일종가 = result['체결가격'] - result['전일대비']
                                    df_plotdata_sp500.iloc[0][0] = sp500_전일종가
                                    df_plotdata_sp500.iloc[0][1] = result['시가']
                                    sp500_시가 = result['시가']

                                    if SP500_LAST_LOW > 0 and SP500_LAST_HIGH > 0:

                                        sp500_피봇 = self.calc_pivot(SP500_LAST_LOW, SP500_LAST_HIGH, sp500_전일종가, sp500_시가)
                                    else:
                                        pass
                                else:
                                    pass

                                전일대비 = locale.format('%.2f', result['전일대비'], 1)                                

                                if min(temp) > 0:
                                    jisu_str = "S&P 500: {0} ▲ ({1}, {2:0.2f}%)⬈".format(체결가격, 전일대비, result['등락율'])                                    
                                else:
                                    jisu_str = "S&P 500: {0} ▲ ({1}, {2:0.2f}%)".format(체결가격, 전일대비, result['등락율'])

                                self.label_1st.setText(jisu_str)
                                self.label_1st.setStyleSheet('background-color: pink; color: red')
                                sp500_text_color = 'red'
                            else:
                                pass
                            
                        elif result['체결가격'] < sp500_price:

                            체결가격 = locale.format('%.2f', result['체결가격'], 1)
                            
                            if result['전일대비기호'] == '5':

                                if sp500_전일종가 == 0.0:
                                    sp500_전일종가 = result['체결가격'] + result['전일대비']
                                    df_plotdata_sp500.iloc[0][0] = sp500_전일종가
                                    df_plotdata_sp500.iloc[0][1] = result['시가']
                                    sp500_시가 = result['시가']

                                    if SP500_LAST_LOW > 0 and SP500_LAST_HIGH > 0:

                                        sp500_피봇 = self.calc_pivot(SP500_LAST_LOW, SP500_LAST_HIGH, sp500_전일종가, sp500_시가)
                                    else:
                                        pass
                                else:
                                    pass

                                전일대비 = locale.format('%.2f', -result['전일대비'], 1)                                

                                if max(temp) < 0:
                                    jisu_str = "S&P 500: {0} ({1}, {2:0.2f}%)⬊".format(체결가격, 전일대비, result['등락율'])                                    
                                else:
                                    jisu_str = "S&P 500: {0} ▼ ({1}, {2:0.2f}%)".format(체결가격, 전일대비, result['등락율'])

                                self.label_1st.setText(jisu_str)
                                self.label_1st.setStyleSheet('background-color: lightskyblue; color: blue')
                                sp500_text_color = 'blue'

                            elif result['전일대비기호'] == '2':

                                if sp500_전일종가 == 0.0:
                                    sp500_전일종가 = result['체결가격'] - result['전일대비']
                                    df_plotdata_sp500.iloc[0][0] = sp500_전일종가
                                    df_plotdata_sp500.iloc[0][1] = result['시가']
                                    sp500_시가 = result['시가']

                                    if SP500_LAST_LOW > 0 and SP500_LAST_HIGH > 0:

                                        sp500_피봇 = self.calc_pivot(SP500_LAST_LOW, SP500_LAST_HIGH, sp500_전일종가, sp500_시가)
                                    else:
                                        pass
                                else:
                                    pass

                                전일대비 = locale.format('%.2f', result['전일대비'], 1)
                                
                                if max(temp) < 0:
                                    jisu_str = "S&P 500: {0} ({1}, {2:0.2f}%)⬊".format(체결가격, 전일대비, result['등락율'])                                    
                                else:
                                    jisu_str = "S&P 500: {0} ▼ ({1}, {2:0.2f}%)".format(체결가격, 전일대비, result['등락율'])

                                self.label_1st.setText(jisu_str)
                                self.label_1st.setStyleSheet('background-color: lightskyblue; color: red')
                                sp500_text_color = 'red'
                            else:
                                pass                            
                        else:
                            pass

                        sp500_price = result['체결가격']
                    else:
                        pass                    

                elif result['종목코드'] == DOW:

                    dow_저가 =  result['저가']
                    dow_고가 =  result['고가']

                    진폭 = int(result['고가'] - result['저가'])
                    체결가격 = int(result['체결가격'])
                    전일대비 = int(result['전일대비'])

                    if 체결가격 != dow_price:
                        
                        dow_delta_old = dow_delta
                        dow_delta = 체결가격
                        dow_직전대비.extend([dow_delta - dow_delta_old])
                        temp = list(dow_직전대비)
                        
                        if 2 <= ovc_x_idx <= overnight_timespan - 1:
                            df_plotdata_dow.iloc[0][ovc_x_idx] = result['체결가격']
                        else:
                            pass

                        if 체결가격 > dow_price:

                            if result['전일대비기호'] == '5':

                                if dow_전일종가 == 0.0:
                                    dow_전일종가 = result['체결가격'] + result['전일대비']
                                    df_plotdata_dow.iloc[0][0] = dow_전일종가
                                    df_plotdata_dow.iloc[0][1] = result['시가']
                                    dow_시가 = result['시가']

                                    if DOW_LAST_LOW > 0 and DOW_LAST_HIGH > 0:

                                        dow_피봇 = self.calc_pivot(DOW_LAST_LOW, DOW_LAST_HIGH, dow_전일종가, dow_시가)
                                    else:
                                        pass
                                else:
                                    pass                                

                                if min(temp) > 0:
                                    jisu_str = "DOW: {0} ({1}, {2:0.2f}%, {3})⬈". \
                                    format(format(체결가격, ','), format(-전일대비, ','), result['등락율'], format(진폭, ','))                                    
                                else:
                                    jisu_str = "DOW: {0} ▲ ({1}, {2:0.2f}%, {3})". \
                                    format(format(체결가격, ','), format(-전일대비, ','), result['등락율'], format(진폭, ','))

                                self.label_2nd.setText(jisu_str)
                                self.label_2nd.setStyleSheet('background-color: pink ; color: blue')
                                dow_text_color = 'blue'

                            elif result['전일대비기호'] == '2':

                                if dow_전일종가 == 0.0:
                                    dow_전일종가 = result['체결가격'] - result['전일대비']
                                    df_plotdata_dow.iloc[0][0] = dow_전일종가
                                    df_plotdata_dow.iloc[0][1] = result['시가']
                                    dow_시가 = result['시가']

                                    if DOW_LAST_LOW > 0 and DOW_LAST_HIGH > 0:

                                        dow_피봇 = self.calc_pivot(DOW_LAST_LOW, DOW_LAST_HIGH, dow_전일종가, dow_시가)
                                    else:
                                        pass
                                else:
                                    pass                                

                                if min(temp) > 0:
                                    jisu_str = "DOW: {0} ({1}, {2:0.2f}%, {3})⬈". \
                                    format(format(체결가격, ','), format(전일대비, ','), result['등락율'], format(진폭, ','))                                    
                                else:
                                    jisu_str = "DOW: {0} ▲ ({1}, {2:0.2f}%, {3})". \
                                    format(format(체결가격, ','), format(전일대비, ','), result['등락율'], format(진폭, ','))

                                self.label_2nd.setText(jisu_str)
                                self.label_2nd.setStyleSheet('background-color: pink ; color: red')
                                dow_text_color = 'red'
                            else:
                                pass

                        elif 체결가격 < dow_price:

                            if result['전일대비기호'] == '5':

                                if dow_전일종가 == 0.0:
                                    dow_전일종가 = result['체결가격'] + result['전일대비']
                                    df_plotdata_dow.iloc[0][0] = dow_전일종가
                                    df_plotdata_dow.iloc[0][1] = result['시가']
                                    dow_시가 = result['시가']

                                    if DOW_LAST_LOW > 0 and DOW_LAST_HIGH > 0:

                                        dow_피봇 = self.calc_pivot(DOW_LAST_LOW, DOW_LAST_HIGH, dow_전일종가, dow_시가)
                                    else:
                                        pass
                                else:
                                    pass                                

                                if max(temp) < 0:
                                    jisu_str = "DOW: {0} ({1}, {2:0.2f}%, {3})⬊". \
                                    format(format(체결가격, ','), format(-전일대비, ','), result['등락율'], format(진폭, ','))                                    
                                else:
                                    jisu_str = "DOW: {0} ▼ ({1}, {2:0.2f}%, {3})". \
                                    format(format(체결가격, ','), format(-전일대비, ','), result['등락율'], format(진폭, ','))

                                self.label_2nd.setText(jisu_str)
                                self.label_2nd.setStyleSheet('background-color: lightskyblue ; color: blue')
                                dow_text_color = 'blue'

                            elif result['전일대비기호'] == '2':

                                if dow_전일종가 == 0.0:
                                    dow_전일종가 = result['체결가격'] - result['전일대비']
                                    df_plotdata_dow.iloc[0][0] = dow_전일종가
                                    df_plotdata_dow.iloc[0][1] = result['시가']
                                    dow_시가 = result['시가']

                                    if DOW_LAST_LOW > 0 and DOW_LAST_HIGH > 0:

                                        dow_피봇 = self.calc_pivot(DOW_LAST_LOW, DOW_LAST_HIGH, dow_전일종가, dow_시가)
                                    else:
                                        pass
                                else:
                                    pass                                

                                if max(temp) < 0:
                                    jisu_str = "DOW: {0} ({1}, {2:0.2f}%, {3})⬊". \
                                    format(format(체결가격, ','), format(전일대비, ','), result['등락율'], format(진폭, ','))                                    
                                else:
                                    jisu_str = "DOW: {0} ▼ ({1}, {2:0.2f}%, {3})". \
                                    format(format(체결가격, ','), format(전일대비, ','), result['등락율'], format(진폭, ','))

                                self.label_2nd.setText(jisu_str)
                                self.label_2nd.setStyleSheet('background-color: lightskyblue ; color: red')
                                dow_text_color = 'red'
                            else:
                                pass
                        else:
                            pass

                        dow_price = 체결가격
                    else:
                        pass                    
                else:
                    pass
            else:
                print('요청하지 않은 TR 코드 : ', szTrCode)
            '''
            process_time = (timeit.default_timer() - start_time) * 1000

            if process_time > 0:
                pass
                
                str = '[{0:02d}:{1:02d}:{2:02d}] OnReceiveRealData[{3}] 처리시간 --> {4:0.2f} ms...\r'.format(dt.hour,
                                                                        dt.minute, dt.second, szTrCode, process_time)
                self.textBrowser.append(str)
                print(str)
                
            else:
                pass
            '''

        except Exception as e:
            pass

    def AddCode(self):

        global pre_start
        global START_ON
        global t2301_month_info

        dt = datetime.datetime.now()
        current_str = dt.strftime('%H:%M:%S')

        # 서버시간 확인        
        XQ = t0167(parent=self)
        XQ.Query()

        #time.sleep(1.1)        

        # 코스피 조회
        XQ = t1514(parent=self)
        XQ.Query(업종코드=KOSPI,구분1='',구분2='1',CTS일자='',조회건수='0001',비중구분='', 연속조회=False)

        time.sleep(1.1)

        # 코스닥지수 조회
        XQ = t1514(parent=self)
        XQ.Query(업종코드=KOSDAQ,구분1='',구분2='1',CTS일자='',조회건수='0001',비중구분='', 연속조회=False)

        if service_terminate:

            file = open('skybot.log', 'w')
            text = self.textBrowser.toPlainText()
            file.write(text)
            file.close()

            if TARGET_MONTH_SELECT == 1:

                self.capture_screenshot()
            else:
                pass 
        else:
            if not refresh_flag:

                START_ON = True
                
                self.pushButton_add.setStyleSheet("background-color: lawngreen")
                self.pushButton_add.setText('Starting...')

                # 지수선물 마스터조회 API용
                XQ = t8432(parent=self)
                XQ.Query(구분='F')

                str = '[{0:02d}:{1:02d}:{2:02d}] t8432 지수선물 마스터 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second)
                self.textBrowser.append(str)
            else:
                pass

            if not overnight:

                if int(current_str[0:2]) == 7 and int(current_str[3:5]) > 10:
                    pre_start = True
                elif int(current_str[0:2]) == 8 and int(current_str[3:5]) <= 59:
                    pre_start = True
                elif 9 <= int(current_str[0:2]) <= 16:
                    pass
                else:
                    pass
            else:
                pass
            
            # 옵션 전광판 요청(주간=FC0/OC0, 야간=NC0/EC0)
            XQ = t2301(parent=self)

            if TARGET_MONTH_SELECT == 1:

                if MANGI_YAGAN == 'YES':
                    t2301_month_info = NEXT_MONTH
                else:
                    t2301_month_info = CURRENT_MONTH

                str = '[{0:02d}:{1:02d}:{2:02d}] 본월물({3}) 주간옵션 전광판 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second, t2301_month_info)
                self.textBrowser.append(str)

            elif TARGET_MONTH_SELECT == 2:

                if MANGI_YAGAN == 'YES':
                    t2301_month_info = MONTH_AFTER_NEXT
                else:
                    t2301_month_info = NEXT_MONTH   

                str = '[{0:02d}:{1:02d}:{2:02d}] 차월물({3}) 주간옵션 전광판 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second, t2301_month_info)
                self.textBrowser.append(str)

            else:
                if MANGI_YAGAN == 'YES':
                    t2301_month_info = MONTH_AFTER_NEXT
                else:
                    t2301_month_info = MONTH_AFTER_NEXT   

                str = '[{0:02d}:{1:02d}:{2:02d}] 차차월물({3}) 주간옵션 전광판 데이타를 요청합니다.\r'.format(dt.hour, dt.minute, dt.second, t2301_month_info)
                self.textBrowser.append(str)

            XQ.Query(월물=t2301_month_info, 미니구분='G')

        return

    def SaveResult(self):

        dt = datetime.datetime.now()

        now = time.localtime()

        times = "%04d-%02d-%02d-%02d-%02d-%02d" % \
                (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        file = open('skybot.log', 'w')
        text = self.textBrowser.toPlainText()
        file.write(text)
        file.close()

        str = '[{0:02d}:{1:02d}:{2:02d}] 로그파일을 저장했습니다.\r'.format(dt.hour, dt.minute, dt.second)
        self.textBrowser.append(str)

        self.high_low_list_save_to_file()

        str = '[{0:02d}:{1:02d}:{2:02d}] High-Low 리스트파일을 저장했습니다.\r'.format(dt.hour, dt.minute, dt.second)
        self.textBrowser.append(str)

        '''
        if df_fut.empty:

            pass
        else:
            fut_csv = "Futures 전광판 {}{}".format(times, '.csv')
            # temp = df_cme.append(df_fut, ignore_index=True)
            # temp = pd.concat([df_cme, df_fut], ignore_index=True)
            df_fut.to_csv(fut_csv, encoding='ms949')

            fut_ohlc_csv = "Futures OHLC {}{}".format(times, '.csv')
            df_fut_ohlc.to_csv(fut_ohlc_csv, encoding='ms949')

            kp200_graph_csv = "KP200 Graph {}{}".format(times, '.csv')
            df_plotdata_kp200.to_csv(kp200_graph_csv, encoding='ms949')

            fut_graph_csv = "Fut Graph {}{}".format(times, '.csv')
            df_plotdata_fut.to_csv(fut_graph_csv, encoding='ms949')

        if df_call.empty:

            pass
        else:
            self.call_open_check()

            call_csv = "Call 전광판 {}{}".format(times, '.csv')
            df_call.loc[0:, '행사가':].to_csv(call_csv, encoding='ms949')

            call_graph_csv = "Call Graph {}{}".format(times, '.csv')
            df_plotdata_call.to_csv(call_graph_csv, encoding='ms949')

            self.put_open_check()

            put_csv = "Put 전광판 {}{}".format(times, '.csv')
            df_put.loc[0:, '행사가':].to_csv(put_csv, encoding='ms949')

            put_graph_csv = "Put Graph {}{}".format(times, '.csv')
            df_plotdata_put.to_csv(put_graph_csv, encoding='ms949')

            call_volume_csv = "Call Volume {}{}".format(times, '.csv')
            df_plotdata_call_volume.to_csv(call_volume_csv, encoding='ms949')

            put_volume_csv = "Put Volume {}{}".format(times, '.csv')
            df_plotdata_put_volume.to_csv(put_volume_csv, encoding='ms949')
        '''
        
        return

    def RemoveCode(self):

        global flag_telegram_on
        global flag_telegram_listen_worker, flag_telegram_send_worker

        dt = datetime.datetime.now()

        flag_telegram_on = not flag_telegram_on
        
        if not flag_telegram_send_worker:

            # 가끔 send worker가 오동작함(쓰레드 재시작...)
            self.telegram_send_worker.start()
            self.telegram_send_worker.daemon = True

            str = '[{0:02d}:{1:02d}:{2:02d}] 텔레그램 Send Worker를 재시작합니다.\r'.format(dt.hour, dt.minute, dt.second)
            self.textBrowser.append(str)

            flag_telegram_send_worker = True
        else:
            pass
        
        if TELEGRAM_SERVICE == 'ON' and not flag_telegram_listen_worker:

            flag_telegram_on = True

            self.telegram_listen_worker.start()
            self.telegram_listen_worker.daemon = True

            str = '[{0:02d}:{1:02d}:{2:02d}] 텔레그램 Polling이 시작됩니다.\r'.format(dt.hour, dt.minute, dt.second)
            self.textBrowser.append(str)

            if TARGET_MONTH_SELECT == 1:

                ToTelegram("본월물 텔레그램 Polling이 시작됩니다.")

            elif TARGET_MONTH_SELECT == 2:

                ToTelegram("차월물 텔레그램 Polling이 시작됩니다.")

            else:
                ToTelegram("MAN 텔레그램 Polling이 시작됩니다.")
            
            self.pushButton_remove.setStyleSheet("background-color: lawngreen")
            
            flag_telegram_listen_worker = True            
        else:
            pass               

        if flag_telegram_on:
            
            if TARGET_MONTH_SELECT == 1:

                self.capture_screenshot()
            else:
                pass

            #self.high_low_list_save_to_file()
            #print('화면을 캡처했습니다...')  

            self.pushButton_remove.setStyleSheet("background-color: lawngreen")
            print('flag_telegram_on =', flag_telegram_on)
        else:
            self.pushButton_remove.setStyleSheet("background-color: lightGray")
            print('flag_telegram_on =', flag_telegram_on)
        
        return

    def high_low_list_save_to_file(self):
        
        #now = time.localtime()
        #times = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

        call_low_list = []
        call_high_list = []
        put_low_list = []
        put_high_list = []
        list_final = []

        for i in range(option_pairs_count):

            if 1.2 < df_call.iloc[i]['저가'] < 10.0:
                call_low_list.append(df_call.iloc[i]['저가'])
            else:
                pass

            if 1.2 < df_call.iloc[i]['고가'] < 10.0:
                call_high_list.append(df_call.iloc[i]['고가'])
            else:
                pass

            if 1.2 < df_put.iloc[i]['저가'] < 10.0:
                put_low_list.append(df_put.iloc[i]['저가'])
            else:
                pass

            if 1.2 < df_put.iloc[i]['고가'] < 10.0:
                put_high_list.append(df_put.iloc[i]['고가'])
            else:
                pass

        print('call_low_list =', call_low_list)
        print('call_high_list =', call_high_list)
        print('put_low_list =', put_low_list)
        print('put_high_list =', put_high_list)

        list_final = call_low_list + call_high_list + put_low_list + put_high_list
        list_final.sort()

        print('list_final =', list_final)

        #file_name = "HL-List {}.txt".format(times)
        file_name = "HL-List.txt"

        self.list_to_file_write(list_final, file_name, sep = ' ')

        return

    def list_to_file_write(self, list, fname, sep):  
        
        if os.path.isfile('HL-List.txt'):
            print("Yes. Here is the file...")
            file = open(fname, 'a')
        else:
            print("Nothing...")
            file = open(fname, 'w')        
        
        vstr = ''

        for a in list:
            vstr = vstr + str(a) + sep
        
        #vstr = vstr.rstrip(sep)

        file.writelines(vstr)
        file.close()

        print('파일쓰기 성공!!!')

        return

    def closeEvent(self,event):

        pass
        '''
        result = QMessageBox.question(self,"옵션전광판 종료","정말 종료하시겠습니까 ?", QMessageBox.Yes| QMessageBox.No)

        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        '''

########################################################################################################################
# 메인
########################################################################################################################
if TARGET_MONTH_SELECT == 1:

    Ui_MainWindow, QtBaseClass_MainWindow = uic.loadUiType(UI_DIR+"mymoneybot_cm.ui")

elif TARGET_MONTH_SELECT == 2:

    Ui_MainWindow, QtBaseClass_MainWindow = uic.loadUiType(UI_DIR+"mymoneybot_nm.ui")

else:
    Ui_MainWindow, QtBaseClass_MainWindow = uic.loadUiType(UI_DIR+"mymoneybot_man.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("SkyBot ver1.0")

        self.plugins = CPluginManager.plugin_loader()
        menuitems = self.plugins.keys()
        menu = self.menubar.addMenu('&플러그인로봇')
        for item in menuitems:
            icon = QIcon()
            icon.addPixmap(QPixmap("PNG/approval.png"), QIcon.Normal, QIcon.Off)
            entry = menu.addAction(icon, item)
            entry.setObjectName(item)

        self.시작시각 = datetime.datetime.now()

        self.robots = []

        self.dialog = dict()

        self.portfolio_columns = ['종목코드', '종목명', 'TAG', '매수가', '수량', '매수일']
        self.robot_columns = ['Robot타입', 'Robot명', 'RobotID', '실행상태', '포트수', '포트폴리오']

        self.model = PandasModel()
        self.tableView_robot.setModel(self.model)
        self.tableView_robot.setSelectionBehavior(QTableView.SelectRows)
        self.tableView_robot.setSelectionMode(QTableView.SingleSelection)

        self.tableView_robot.pressed.connect(self.RobotCurrentIndex)
        self.tableView_robot_current_index = None

        self.portfolio_model = PandasModel()
        self.tableView_portfolio.setModel(self.portfolio_model)
        self.tableView_portfolio.setSelectionBehavior(QTableView.SelectRows)
        self.tableView_portfolio.setSelectionMode(QTableView.SingleSelection)
        self.tableView_portfolio.pressed.connect(self.PortfolioCurrentIndex)
        self.tableView_portfolio_current_index = None

        self.portfolio_model.update((DataFrame(columns=self.portfolio_columns)))

        self.주문제한 = 0
        self.조회제한 = 0
        self.금일백업작업중 = False
        self.종목선정작업중 = False

        self.계좌번호 = None
        self.거래비밀번호 = None

        # AxtiveX 설정
        # self.connection = XASession(parent=self)
        self.connection = None
        self.XQ_t0167 = t0167(parent=self)

    def OnQApplicationStarted(self):
        self.clock = QtCore.QTimer()
        self.clock.timeout.connect(self.OnClockTick)
        self.clock.start(1000)

        try:
            with open('mymoneybot.robot', 'rb') as handle:
                self.robots = pickle.load(handle)
        except Exception as e:
            pass

        self.RobotView()


        #TODO:자동로그인
        self.MyLogin()

    def OnClockTick(self):
        current = datetime.datetime.now()
        current_str = current.strftime('%H:%M:%S')

        if current.second == 0: # 매 0초
            try:
                if self.connection is not None:
                    msg = '오프라인'
                    if self.connection.IsConnected():
                        msg = "온라인"

                        # 현재시간 조회
                        self.XQ_t0167.Query()
                    else:
                        msg = "오프라인"
                    self.statusbar.showMessage(msg)
            except Exception as e:
                pass

            _temp = []
            for r in self.robots:
                if r.running == True:
                    _temp.append(r.Name)

            if current_str in ['09:01:00']:
                self.RobotRun()
                self.RobotView()

            if current_str in ['15:31:00']:
                self.SaveRobots()
                self.RobotView()

            if current_str[3:] in ['00:00', '30:00']:
                #ToTelegram("%s : 로봇 %s개가 실행중입니다. ([%s])" % (current_str, len(_temp), ','.join(_temp)))
                pass

            if current.minute % 10 == 0: # 매 10 분
                pass

    def closeEvent(self,event):
        result = QMessageBox.question(self,"프로그램 종료","정말 종료하시겠습니까 ?", QMessageBox.Yes| QMessageBox.No)

        if result == QMessageBox.Yes:
            event.accept()
            self.clock.stop()
            self.SaveRobots()
        else:
            event.ignore()

    def SaveRobots(self):
        for r in self.robots:
            r.Run(flag=False, parent=None)

        try:
            with open('mymoneybot.robot', 'wb') as handle:
                pickle.dump(self.robots, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)
        finally:
            for r in self.robots:
                r.Run(flag=False, parent=self)

    def LoadRobots(self):
        with open('mymoneybot.robot', 'rb') as handle:
            try:
                self.robots = pickle.load(handle)
            except Exception as e:
                print(e)
            finally:
                pass

    def robot_selected(self, QModelIndex):
        Robot타입 = self.model._data[QModelIndex.row():QModelIndex.row()+1]['Robot타입'].values[0]

        uuid = self.model._data[QModelIndex.row():QModelIndex.row()+1]['RobotID'].values[0]
        portfolio = None
        for r in self.robots:
            if r.UUID == uuid:
                portfolio = r.portfolio
                model = PandasModel()
                result = []
                for p, v in portfolio.items():
                    result.append((v.종목코드, v.종목명.strip(), p, v.매수가, v.수량, v.매수일))
                self.portfolio_model.update((DataFrame(data=result, columns=['종목코드','종목명','TAG','매수가','수량','매수일'])))

                break

    def robot_double_clicked(self, QModelIndex):
        self.RobotEdit(QModelIndex)
        self.RobotView()

    def portfolio_selected(self, QModelIndex):
        pass

    def portfolio_double_clicked(self, QModelIndex):
        RobotUUID = self.model._data[self.tableView_robot_current_index.row():self.tableView_robot_current_index.row() + 1]['RobotID'].values[0]
        Portfolio라벨 = self.portfolio_model._data[self.tableView_portfolio_current_index.row():self.tableView_portfolio_current_index.row() + 1]['TAG'].values[0]

        for r in self.robots:
            if r.UUID == RobotUUID:
                portfolio_keys = list(r.portfolio.keys())
                for k in portfolio_keys:
                    if k == Portfolio라벨:
                        v = r.portfolio[k]
                        result = QMessageBox.question(self, "포트폴리오 종목 삭제", "[%s-%s] 을/를 삭제 하시겠습니까 ?" %(v.종목코드, v.종목명), QMessageBox.Yes | QMessageBox.No)
                        if result == QMessageBox.Yes:
                            r.portfolio.pop(Portfolio라벨)

                        self.PortfolioView()

    def RobotCurrentIndex(self, index):
        self.tableView_robot_current_index = index

    def RobotRun(self):
        for r in self.robots:
            r.초기조건()
            # logger.debug('%s %s %s %s' % (r.sName, r.UUID, len(r.portfolio), r.GetStatus()))
            r.Run(flag=True, parent=self)

    def RobotView(self):
        result = []
        for r in self.robots:
            result.append(r.getstatus())

        self.model.update(DataFrame(data=result, columns=self.robot_columns))

        # RobotID 숨김
        self.tableView_robot.setColumnHidden(2, True)

        for i in range(len(self.robot_columns)):
            self.tableView_robot.resizeColumnToContents(i)

    def RobotEdit(self, QModelIndex):
        Robot타입 = self.model._data[QModelIndex.row():QModelIndex.row()+1]['Robot타입'].values[0]
        RobotUUID = self.model._data[QModelIndex.row():QModelIndex.row()+1]['RobotID'].values[0]

        for r in self.robots:
            if r.UUID == RobotUUID:
                r.modal(parent=self)

    def PortfolioView(self):
        RobotUUID = self.model._data[self.tableView_robot_current_index.row():self.tableView_robot_current_index.row() + 1]['RobotID'].values[0]
        portfolio = None
        for r in self.robots:
            if r.UUID == RobotUUID:
                portfolio = r.portfolio
                # model = PandasModel()
                result = []
                for p, v in portfolio.items():
                    매수일 = "%s" % v.매수일
                    result.append((v.종목코드, v.종목명.strip(), p, v.매수가, v.수량, 매수일[:19]))

                df = DataFrame(data=result, columns=self.portfolio_columns)
                df = df.sort_values(['종목명'], ascending=True)
                self.portfolio_model.update(df)

                for i in range(len(self.portfolio_columns)):
                    self.tableView_portfolio.resizeColumnToContents(i)

    def PortfolioCurrentIndex(self, index):
        self.tableView_portfolio_current_index = index

    # ------------------------------------------------------------------------------------------------------------------
    def MyLogin(self):
        계좌정보 = pd.read_csv("secret/passwords.csv", converters={'계좌번호': str, '거래비밀번호': str})
        주식계좌정보 = 계좌정보.query("구분 == '거래'")

        if len(주식계좌정보) > 0:
            if self.connection is None:
                self.connection = XASession(parent=self)

            self.계좌번호 = 주식계좌정보['계좌번호'].values[0].strip()
            self.id = 주식계좌정보['사용자ID'].values[0].strip()
            self.pwd = 주식계좌정보['비밀번호'].values[0].strip()
            self.cert = 주식계좌정보['공인인증비밀번호'].values[0].strip()
            self.거래비밀번호 = 주식계좌정보['거래비밀번호'].values[0].strip()
            self.url = 주식계좌정보['url'].values[0].strip()
            self.connection.login(url='hts.ebestsec.co.kr', id=self.id, pwd=self.pwd, cert=self.cert)
        else:
            print("secret디렉토리의 passwords.csv 파일에서 거래 계좌를 지정해 주세요")

    def OnLogin(self, code, msg):
        if code == '0000':
            self.statusbar.showMessage("로그인 되었습니다.")
        else:
            self.statusbar.showMessage("%s %s" % (code, msg))

    def OnLogout(self):
        self.statusbar.showMessage("로그아웃 되었습니다.")

    def OnDisconnect(self):
        # 로봇 상태 저장
        self.SaveRobots()

        self.statusbar.showMessage("연결이 끊겼습니다.")

        self.connection.login(url='demo.ebestsec.co.kr', id=self.id, pwd=self.pwd, cert=self.cert)

    def OnReceiveMessage(self, systemError, messageCode, message):
        # 클래스이름 = self.__class__.__name__
        # 함수이름 = inspect.currentframe().f_code.co_name
        # print("%s-%s " % (클래스이름, 함수이름), systemError, messageCode, message)
        pass

    def OnReceiveData(self, szTrCode, result):
        # print(szTrCode, result)
        pass

    def OnReceiveRealData(self, szTrCode, result):
        # print(szTrCode, result)
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def MENU_Action(self, qaction):
        logger.debug("Action Slot %s %s " % (qaction.objectName(), qaction.text()))
        _action = qaction.objectName()

        if _action == "actionExit":
            self.connection.disconnect()
            self.close()

        if _action == "actionLogin":
            self.MyLogin()

        if _action == "actionLogout":
            #self.connection.logout()
            self.connection.disconnect()
            self.statusbar.showMessage("접속종료 되었습니다.")

        # 일별가격정보 백업
        if _action == "actionPriceBackupDay":
            if self.dialog.get('일별가격정보백업') is not None:
                try:
                    self.dialog['일별가격정보백업'].show()
                except Exception as e:
                    self.dialog['일별가격정보백업'] = 화면_일별가격정보백업(parent=self)
                    self.dialog['일별가격정보백업'].show()
            else:
                self.dialog['일별가격정보백업'] = 화면_일별가격정보백업(parent=self)
                self.dialog['일별가격정보백업'].show()

        # 분별가격정보 백업
        if _action == "actionPriceBackupMin":
            if self.dialog.get('분별가격정보백업') is not None:
                try:
                    self.dialog['분별가격정보백업'].show()
                except Exception as e:
                    self.dialog['분별가격정보백업'] = 화면_분별가격정보백업(parent=self)
                    self.dialog['분별가격정보백업'].show()
            else:
                self.dialog['분별가격정보백업'] = 화면_분별가격정보백업(parent=self)
                self.dialog['분별가격정보백업'].show()

        # 일별업종정보 백업
        if _action == "actionSectorBackupDay":
            if self.dialog.get('일별업종정보백업') is not None:
                try:
                    self.dialog['일별업종정보백업'].show()
                except Exception as e:
                    self.dialog['일별업종정보백업'] = 화면_일별업종정보백업(parent=self)
                    self.dialog['일별업종정보백업'].show()
            else:
                self.dialog['일별업종정보백업'] = 화면_일별업종정보백업(parent=self)
                self.dialog['일별업종정보백업'].show()

        # 종목별 투자자정보 백업
        if _action == "actionInvestorBackup":
            if self.dialog.get('종목별투자자정보백업') is not None:
                try:
                    self.dialog['종목별투자자정보백업'].show()
                except Exception as e:
                    self.dialog['종목별투자자정보백업'] = 화면_종목별투자자정보백업(parent=self)
                    self.dialog['종목별투자자정보백업'].show()
            else:
                self.dialog['종목별투자자정보백업'] = 화면_종목별투자자정보백업(parent=self)
                self.dialog['종목별투자자정보백업'].show()

        # 종목코드 조회/저장
        if _action == "actionStockcode":
            if self.dialog.get('종목코드조회') is not None:
                try:
                    self.dialog['종목코드조회'].show()
                except Exception as e:
                    self.dialog['종목코드조회'] = 화면_종목코드(parent=self)
                    self.dialog['종목코드조회'].show()
            else:
                self.dialog['종목코드조회'] = 화면_종목코드(parent=self)
                self.dialog['종목코드조회'].show()

        # 거래결과
        if _action == "actionTool2ebest":
            if self.dialog.get('외부신호2eBEST') is not None:
                try:
                    self.dialog['외부신호2eBEST'].show()
                except Exception as e:
                    self.dialog['외부신호2eBEST'] = 화면_외부신호2eBEST(parent=self)
                    self.dialog['외부신호2eBEST'].show()
            else:
                self.dialog['외부신호2eBEST'] = 화면_외부신호2eBEST(parent=self)
                self.dialog['외부신호2eBEST'].show()

        if _action == "actionTradeResult":
            if self.dialog.get('거래결과') is not None:
                try:
                    self.dialog['거래결과'].show()
                except Exception as e:
                    self.dialog['거래결과'] = 화면_거래결과(parent=self)
                    self.dialog['거래결과'].show()
            else:
                self.dialog['거래결과'] = 화면_거래결과(parent=self)
                self.dialog['거래결과'].show()

        # 일자별 주가
        if _action == "actionDailyPrice":
            if self.dialog.get('일자별주가') is not None:
                try:
                    self.dialog['일자별주가'].show()
                except Exception as e:
                    self.dialog['일자별주가'] = 화면_일별주가(parent=self)
                    self.dialog['일자별주가'].show()
            else:
                self.dialog['일자별주가'] = 화면_일별주가(parent=self)
                self.dialog['일자별주가'].show()

        # 분별 주가
        if _action == "actionMinuitePrice":
            if self.dialog.get('분별주가') is not None:
                try:
                    self.dialog['분별주가'].show()
                except Exception as e:
                    self.dialog['분별주가'] = 화면_분별주가(parent=self)
                    self.dialog['분별주가'].show()
            else:
                self.dialog['분별주가'] = 화면_분별주가(parent=self)
                self.dialog['분별주가'].show()

        # 업종정보
        if _action == "actionSectorView":
            if self.dialog.get('업종정보조회') is not None:
                try:
                    self.dialog['업종정보조회'].show()
                except Exception as e:
                    self.dialog['업종정보조회'] = 화면_업종정보(parent=self)
                    self.dialog['업종정보조회'].show()
            else:
                self.dialog['업종정보조회'] = 화면_업종정보(parent=self)
                self.dialog['업종정보조회'].show()

        # 테마정보
        if _action == "actionTheme":
            if self.dialog.get('테마정보조회') is not None:
                try:
                    self.dialog['테마정보조회'].show()
                except Exception as e:
                    self.dialog['테마정보조회'] = 화면_테마정보(parent=self)
                    self.dialog['테마정보조회'].show()
            else:
                self.dialog['테마정보조회'] = 화면_테마정보(parent=self)
                self.dialog['테마정보조회'].show()

        # 종목별 투자자
        if _action == "actionInvestors":
            if self.dialog.get('종목별투자자') is not None:
                try:
                    self.dialog['종목별투자자'].show()
                except Exception as e:
                    self.dialog['종목별투자자'] = 화면_종목별투자자(parent=self)
                    self.dialog['종목별투자자'].show()
            else:
                self.dialog['종목별투자자'] = 화면_종목별투자자(parent=self)
                self.dialog['종목별투자자'].show()

        # 종목별 투자자2
        if _action == "actionInvestors2":
            if self.dialog.get('종목별투자자2') is not None:
                try:
                    self.dialog['종목별투자자2'].show()
                except Exception as e:
                    self.dialog['종목별투자자2'] = 화면_종목별투자자2(parent=self)
                    self.dialog['종목별투자자2'].show()
            else:
                self.dialog['종목별투자자2'] = 화면_종목별투자자2(parent=self)
                self.dialog['종목별투자자2'].show()

        # 호가창정보
        if _action == "actionAskBid":
            if self.dialog.get('호가창정보') is not None:
                try:
                    self.dialog['호가창정보'].show()
                except Exception as e:
                    self.dialog['호가창정보'] = 화면_호가창정보(parent=self)
                    self.dialog['호가창정보'].show()
            else:
                self.dialog['호가창정보'] = 화면_호가창정보(parent=self)
                self.dialog['호가창정보'].show()

        # 실시간정보
        if _action == "actionRealDataDialog":
            if self.dialog.get('실시간정보') is not None:
                try:
                    self.dialog['실시간정보'].show()
                except Exception as e:
                    self.dialog['실시간정보'] = 화면_실시간정보(parent=self)
                    self.dialog['실시간정보'].show()
            else:
                self.dialog['실시간정보'] = 화면_실시간정보(parent=self)
                self.dialog['실시간정보'].show()

        # 뉴스
        if _action == "actionNews":
            if self.dialog.get('뉴스') is not None:
                try:
                    self.dialog['뉴스'].show()
                except Exception as e:
                    self.dialog['뉴스'] = 화면_뉴스(parent=self)
                    self.dialog['뉴스'].show()
            else:
                self.dialog['뉴스'] = 화면_뉴스(parent=self)
                self.dialog['뉴스'].show()

        # 계좌정보 조회
        if _action == "actionAccountDialog":
            if self.dialog.get('계좌정보조회') is not None:
                try:
                    self.dialog['계좌정보조회'].show()
                except Exception as e:
                    self.dialog['계좌정보조회'] = 화면_계좌정보(parent=self)
                    self.dialog['계좌정보조회'].show()
            else:
                self.dialog['계좌정보조회'] = 화면_계좌정보(parent=self)
                self.dialog['계좌정보조회'].show()

        # 차트인덱스
        if _action == "actionChartIndex":
            if self.dialog.get('차트인덱스') is not None:
                try:
                    self.dialog['차트인덱스'].show()
                except Exception as e:
                    self.dialog['차트인덱스'] = 화면_차트인덱스(parent=self)
                    self.dialog['차트인덱스'].show()
            else:
                self.dialog['차트인덱스'] = 화면_차트인덱스(parent=self)
                self.dialog['차트인덱스'].show()

        # 종목검색
        if _action == "actionSearchItems":
            if self.dialog.get('종목검색') is not None:
                try:
                    self.dialog['종목검색'].show()
                except Exception as e:
                    self.dialog['종목검색'] = 화면_종목검색(parent=self)
                    self.dialog['종목검색'].show()
            else:
                self.dialog['종목검색'] = 화면_종목검색(parent=self)
                self.dialog['종목검색'].show()

        # e종목검색
        if _action == "actionESearchItems":
            if self.dialog.get('e종목검색') is not None:
                try:
                    self.dialog['e종목검색'].show()
                except Exception as e:
                    self.dialog['e종목검색'] = 화면_e종목검색(parent=self)
                    self.dialog['e종목검색'].show()
            else:
                self.dialog['e종목검색'] = 화면_e종목검색(parent=self)
                self.dialog['e종목검색'].show()

        if _action == "actionOpenScreen":
            XQ = t8430(parent=self)
            XQ.Query(구분='0')

            res = XQ.RequestLinkToHTS("&STOCK_CODE", "069500", "")

        # 주문테스트
        if _action == "actionOrder":
            if self.dialog.get('주문테스트') is not None:
                try:
                    self.dialog['주문테스트'].show()
                except Exception as e:
                    self.dialog['주문테스트'] = 화면_주문테스트(parent=self)
                    self.dialog['주문테스트'].show()
            else:
                self.dialog['주문테스트'] = 화면_주문테스트(parent=self)
                self.dialog['주문테스트'].show()

        # 사용법
        if _action == "actionMustRead":
            webbrowser.open('https://thinkpoolost.wixsite.com/moneybot')

        if _action == "actionUsage":
            webbrowser.open('https://docs.google.com/document/d/1BGENxWqJyZdihQFuWcmTNy3_4J0kHolCc-qcW3RULzs/edit')

        if _action == "actionVersion":
            if self.dialog.get('Version') is not None:
                try:
                    self.dialog['Version'].show()
                except Exception as e:
                    self.dialog['Version'] = 화면_버전(parent=self)
                    self.dialog['Version'].show()
            else:
                self.dialog['Version'] = 화면_버전(parent=self)
                self.dialog['Version'].show()

        if _action == "actionRobotLoad":
            reply = QMessageBox.question(self, "로봇 탑제", "저장된 로봇을 읽어올까요?", QMessageBox.Yes | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                pass
            elif reply == QMessageBox.Yes:
                self.LoadRobots()

            self.RobotView()

        elif _action == "actionRobotSave":
            reply = QMessageBox.question(self, "로봇 저장", "현재 로봇을 저장할까요?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                pass
            elif reply == QMessageBox.No:
                pass
            elif reply == QMessageBox.Yes:
                self.SaveRobots()

            self.RobotView()

        elif _action == "actionRobotOneRun":
            try:
                RobotUUID = self.model._data[self.tableView_robot_current_index.row():self.tableView_robot_current_index.row() + 1]['RobotID'].values[0]
            except Exception as e:
                RobotUUID = ''

            robot_found = None
            for r in self.robots:
                if r.UUID == RobotUUID:
                    robot_found = r
                    break

            if robot_found == None:
                return

            robot_found.Run(flag=True, parent=self)

            self.RobotView()

        elif _action == "actionRobotOneStop":
            try:
                RobotUUID = self.model._data[self.tableView_robot_current_index.row():self.tableView_robot_current_index.row() + 1]['RobotID'].values[0]
            except Exception as e:
                RobotUUID = ''

            robot_found = None
            for r in self.robots:
                if r.UUID == RobotUUID:
                    robot_found = r
                    break

            if robot_found == None:
                return

            reply = QMessageBox.question(self,"로봇 실행 중지", "로봇 실행을 중지할까요?\n%s" % robot_found.getstatus(),QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                pass
            elif reply == QMessageBox.No:
                pass
            elif reply == QMessageBox.Yes:
                robot_found.Run(flag=False, parent=None)

            self.RobotView()

        elif _action == "actionRobotRun":
            self.RobotRun()
            self.RobotView()

        elif _action == "actionRobotStop":
            reply = QMessageBox.question(self,"전체 로봇 실행 중지", "전체 로봇 실행을 중지할까요?",QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                pass
            elif reply == QMessageBox.No:
                pass
            elif reply == QMessageBox.Yes:
                for r in self.robots:
                    r.Run(flag=False, parent=None)

            self.RobotView()

        elif _action == "actionRobotRemove":
            try:
                RobotUUID = self.model._data[self.tableView_robot_current_index.row():self.tableView_robot_current_index.row() + 1]['RobotID'].values[0]

                robot_found = None
                for r in self.robots:
                    if r.UUID == RobotUUID:
                        robot_found = r
                        break

                if robot_found == None:
                    return

                reply = QMessageBox.question(self, "로봇 삭제", "로봇을 삭제할까요?\n%s" % robot_found.getstatus()[0:4], QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if reply == QMessageBox.Cancel:
                    pass
                elif reply == QMessageBox.No:
                    pass
                elif reply == QMessageBox.Yes:
                    self.robots.remove(robot_found)

                self.RobotView()
            except Exception as e:
                pass

        elif _action == "actionRobotClear":
            reply = QMessageBox.question(self, "로봇 전체 삭제", "로봇 전체를 삭제할까요?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                pass
            elif reply == QMessageBox.No:
                pass
            elif reply == QMessageBox.Yes:
                self.robots = []

            self.RobotView()

        elif _action == "actionRobotView":
            self.RobotView()
            for r in self.robots:
                logger.debug('%s %s %s %s' % (r.Name, r.UUID, len(r.portfolio), r.getstatus()))

        if _action in self.plugins.keys():
            robot = self.plugins[_action].instance()
            robot.set_database(database=DATABASE)
            robot.set_secret(계좌번호=self.계좌번호, 비밀번호=self.거래비밀번호)
            ret = robot.modal(parent=self)
            if ret == 1:
                self.robots.append(robot)
            self.RobotView()

        # 당월물 옵션전광판
        if _action == "actionCMOptionPrice":
            
            if self.dialog.get('당월물옵션전광판') is not None:

                try:
                    self.dialog['당월물옵션전광판'].show()
                except Exception as e:
                    self.dialog['당월물옵션전광판'] = 화면_당월물옵션전광판(parent=self)
                    self.dialog['당월물옵션전광판'].show()
            else:
                self.dialog['당월물옵션전광판'] = 화면_당월물옵션전광판(parent=self)
                self.dialog['당월물옵션전광판'].show()

    # ------------------------------------------------------------

if __name__ == "__main__":
    # Window 8, 10
    # Window 7은 한글을 못읽음
    # Speak("스카이봇이 시작됩니다.")

    #ToTelegram("SkyBot이 실행되었습니다.")

    # 1.로그 인스턴스를 만든다.
    logger = logging.getLogger('mymoneybot')
    # 2.formatter를 만든다.
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s]%(asctime)s>%(message)s')

    loggerLevel = logging.DEBUG
    filename = "LOG/mymoneybot.log"

    # 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
    filehandler = logging.FileHandler(filename)
    streamhandler = logging.StreamHandler()

    # 각 핸들러에 formatter를 지정한다.
    filehandler.setFormatter(formatter)
    streamhandler.setFormatter(formatter)

    # 로그 인스턴스에 스트림 핸들러와 파일 핸들러를 붙인다.
    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    logger.setLevel(loggerLevel)
    logger.debug("=============================================================================")
    logger.info("LOG START")

    app = QApplication(sys.argv)
    #app.setStyle(QStyleFactory.create('Cleanlooks'))
    app.setQuitOnLastWindowClosed(True)

    window = MainWindow()
    window.show()

    QTimer().singleShot(1, window.OnQApplicationStarted)

    sys.exit(app.exec_())