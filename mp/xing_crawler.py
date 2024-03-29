from datetime import datetime
import pythoncom
import math
import time
import multiprocessing as mp
from multiprocessing import Queue
from configparser import ConfigParser

from mp.xing_config import *
from mp.xing_api import *
from mp.xing_utils import * 
from mp.xing_real_time import *

make_dir(TICKER_DATA_FOLDER_PATH)
TODAY = datetime.today().strftime("%Y-%m-%d")
TODAY_PATH = f"{TICKER_DATA_FOLDER_PATH}/{TODAY}"
make_dir(TODAY_PATH)

# Configuration Parser
parser = ConfigParser()
parser.read('.\skybot.ini')

REAL_SERVER = parser.getboolean('Server Type', 'Real Server')
SLEEP_SWITCH_MODE = parser.getboolean('User Switch', 'MP Sleep Switching Mode')
SLEEP_SWITCHING_DELAY = parser.getfloat('Initial Value', 'MP Sleep Switching Delay')
OPTION_SLEEP_SWITCH_MODE = parser.getboolean('User Switch', 'MP Option Sleep Switching Mode')
OPTION_SLEEP_SWITCHING_DELAY = parser.getfloat('Initial Value', 'MP Option Sleep Switching Delay')

SP500 = parser.get('Code of the Foreign Futures', 'S&P 500')
DOW = parser.get('Code of the Foreign Futures', 'DOW')
NASDAQ = parser.get('Code of the Foreign Futures', 'NASDAQ')
WTI = parser.get('Code of the Foreign Futures', 'WTI')
EUROFX = parser.get('Code of the Foreign Futures', 'EUROFX')
HANGSENG = parser.get('Code of the Foreign Futures', 'HANGSENG')
GOLD = parser.get('Code of the Foreign Futures', 'GOLD')

KOSPI = '001'
KOSPI200 = '101'
KOSDAQ = '301'
FUTURES = '900'

SAMSUNG = '005930'
HYUNDAI = '005380'

if REAL_SERVER:
    is_real_server = True
    config = {"id": "goldrune", "password": "sky1037045", "cert_password": "sky@1037045"}
else:
    is_real_server = False
    config = {"id": "goldrune", "password": "sky0000", "cert_password": "0"}

def stock_crawler(queue: Queue, kospi_quote=True, kospi_tick=True, kosdaq_quote=True, kosdaq_tick=True):

    result = XingAPI.login(config["id"], config["password"], config["cert_password"], is_real_server)
    result.append('주식')

    queue.put(result)

    if result[0] == 'login' and result[1] == '0000':

        # ################################# 코스피 ###################################################################
        listed_code_df = XingAPI.get_listed_code_list(market_type=1)
        listed_code_df.to_csv(f"{TODAY_PATH}/kospi_listed_code.csv", encoding='utf-8-sig')

        code_list = listed_code_df['단축코드'].tolist()

        # 호가
        if kospi_quote:
            real_time_kospi_quote = RealTimeKospiQuote(queue=queue)
            real_time_kospi_quote.set_code_list(code_list)

        # 체결
        if kospi_tick:
            real_time_kospi_tick = RealTimeKospiTick(queue=queue)
            real_time_kospi_tick.set_code_list(code_list)
        # ############################################################################################################

        # ################################# 코스닥 ###################################################################
        listed_code_df = XingAPI.get_listed_code_list(market_type=2)
        listed_code_df.to_csv(f"{TODAY_PATH}/kosdaq_listed_code.csv", encoding='utf-8-sig')

        code_list = listed_code_df['단축코드'].tolist()

        # 호가
        if kosdaq_quote:
            real_time_kosdaq_quote = RealTimeKosdaqQuote(queue=queue)
            real_time_kosdaq_quote.set_code_list(code_list)

        # 체결
        if kosdaq_tick:
            real_time_kosdaq_tick = RealTimeKosdaqTick(queue=queue)
            real_time_kosdaq_tick.set_code_list(code_list)
        # ############################################################################################################

        while True:
            pythoncom.PumpWaitingMessages()

            if SLEEP_SWITCH_MODE:
                time.sleep(SLEEP_SWITCHING_DELAY)
    else:
        pass

# 여기에서 JIF, IJ, OVC, BM, PM등을 함께 요청
def index_futures_crawler(queue: Queue, index_futures_quote=True, index_futures_tick=True):

    proc = mp.current_process()
    print(f'\r지수선물 Process Name = {proc.name}, Process ID = {proc.pid}')

    result = XingAPI.login(config["id"], config["password"], config["cert_password"], is_real_server)
    result.append('지수선물')

    queue.put(result)

    if result[0] == 'login' and result[1] == '0000':

        # ################################### JIF ####################################################################
        real_time_jif_tick = RealTimeJIFTick(queue=queue)
        real_time_jif_tick.set_jif_code('0')
        # ############################################################################################################

        # #################################### YJ ####################################################################
        real_time_yj_tick = RealTimeYJTick(queue=queue)
        real_time_yj_tick.set_yj_code(KOSPI200)
        real_time_yj_tick.set_yj_code(KOSPI)
        real_time_yj_tick.set_yj_code(FUTURES)
        # ############################################################################################################

        # #################################### IJ ####################################################################
        real_time_ij_tick = RealTimeIJTick(queue=queue)
        real_time_ij_tick.set_ij_code(KOSPI200)
        real_time_ij_tick.set_ij_code(KOSPI)
        real_time_ij_tick.set_ij_code(KOSDAQ)
        # ############################################################################################################

        # #################################### S3 ####################################################################
        real_time_s3_tick = RealTimeS3Tick(queue=queue)
        real_time_s3_tick.set_s3_code(SAMSUNG)
        real_time_s3_tick.set_s3_code(HYUNDAI)
        # ############################################################################################################

        # ################################### OVC ####################################################################        
        real_time_ovc_tick = RealTimeOVCTick(queue=queue)
        real_time_ovc_tick.set_ovc_code(SP500)    
        real_time_ovc_tick.set_ovc_code(DOW)
        real_time_ovc_tick.set_ovc_code(NASDAQ)
        real_time_ovc_tick.set_ovc_code(WTI)
        real_time_ovc_tick.set_ovc_code(EUROFX)
        real_time_ovc_tick.set_ovc_code(HANGSENG)
        real_time_ovc_tick.set_ovc_code(GOLD)        
        # ############################################################################################################

        # #################################### BM ####################################################################
        real_time_bm_tick = RealTimeBMTick(queue=queue)
        real_time_bm_tick.set_bm_code(FUTURES)
        real_time_bm_tick.set_bm_code(KOSPI)
        # ############################################################################################################

        # #################################### PM ####################################################################
        real_time_pm_tick = RealTimePMTick(queue=queue)
        real_time_pm_tick.set_pm_code('0')
        # ############################################################################################################

        # #################################### NWS ###################################################################
        real_time_nws_tick = RealTimeNWSTick(queue=queue)
        real_time_nws_tick.set_nws_code('NWS001')
        # ############################################################################################################
                
        # ################################# 지수선물 ##################################################################
        listed_code_df = XingAPI.get_index_futures_listed_code_list()

        fut_code_list = []
        fut_code_list.append('t8432')
        fut_code_list.append(listed_code_df)
        queue.put(fut_code_list)

        listed_code_df.to_csv(f"{TODAY_PATH}/index_futures_listed_code.csv", encoding='utf-8-sig')
        # ############################################################################################################
        
        # #################################### YFC ###################################################################
        real_time_yfc_tick = RealTimeYFCTick(queue=queue)
        real_time_yfc_tick.set_yfc_code(listed_code_df['단축코드'][0])
        # ############################################################################################################

        code_list = listed_code_df['단축코드'].tolist()

        # 호가
        if index_futures_quote:
            real_time_index_futures_quote = RealTimeIndexFuturesQuote(queue=queue)
            real_time_index_futures_quote.set_code_list(code_list, field="futcode")

        # 체결
        if index_futures_tick:
            real_time_index_futures_tick = RealTimeIndexFuturesTick(queue=queue)
            real_time_index_futures_tick.set_code_list(code_list, field="futcode")
        # ############################################################################################################

        while True:
            pythoncom.PumpWaitingMessages()

            if SLEEP_SWITCH_MODE:
                time.sleep(SLEEP_SWITCHING_DELAY)
    else:
        pass

def index_option_tick_crawler(queue: Queue, index_option_cm_tick=False, index_option_nm_tick=False):

    proc = mp.current_process()
    print(f'\r지수옵션 체결 Process Name = {proc.name}, Process ID = {proc.pid}')
                          
    result = XingAPI.login(config["id"], config["password"], config["cert_password"], is_real_server)
    result.append('지수옵션체결')

    queue.put(result)

    if result[0] == 'login' and result[1] == '0000':

        # ################################# 지수선물 근월물, 차월물 선물코드 ############################################
        gmshcode, cmshcode = XingAPI.get_index_futures_gm_cm_code()
        # ############################################################################################################
        
        # ################################# t2101 요청 ################################################################
        t2101_df = XingAPI.t2101(gmshcode)
        kp200 = float(t2101_df.at[0, 'KOSPI200지수'])

        temp = math.floor(round(kp200 / 2.5, 0) * 2.5)
        atm_txt = '{0:.0f}'.format(temp)        

        print('kp200 지수 =', kp200, atm_txt)
        # ############################################################################################################        

        # ################################# 지수옵션 ##################################################################
        listed_code_df, cm_call_code_list, cm_put_code_list, nm_call_code_list, nm_put_code_list = XingAPI.get_index_option_listed_code_list()
        listed_code_df.to_csv(f"{TODAY_PATH}/index_option_listed_code.csv", encoding='utf-8-sig')

        #option_code_list = listed_code_df['단축코드'].tolist()

        cm_code_list = cm_call_code_list + cm_put_code_list
        nm_code_list = nm_call_code_list + nm_put_code_list

        #print('cm_code_list =', cm_code_list)
        #print('nm_code_list =', nm_code_list)

        # 체결
        if index_option_cm_tick:
            print('본월물 실시간 체결요청...')
            real_time_index_option_tick = RealTimeIndexOptionTick(queue=queue)
            real_time_index_option_tick.set_code_list(cm_code_list, field="optcode")

        if index_option_nm_tick:
            print('차월물 실시간 체결요청...')
            real_time_index_option_tick = RealTimeIndexOptionTick(queue=queue)
            real_time_index_option_tick.set_code_list(nm_code_list, field="optcode")
        # ############################################################################################################

        while True:
            pythoncom.PumpWaitingMessages()

            if OPTION_SLEEP_SWITCH_MODE:
                time.sleep(OPTION_SLEEP_SWITCHING_DELAY)
    else:
        pass

def index_option_quote_crawler(queue: Queue, quote_request_number=5, index_option_cm_quote=False, index_option_nm_quote=False):

    proc = mp.current_process()
    print(f'\r지수옵션 호가 Process Name = {proc.name}, Process ID = {proc.pid}')
                          
    result = XingAPI.login(config["id"], config["password"], config["cert_password"], is_real_server)
    result.append('지수옵션호가')
    
    queue.put(result)
    
    if result[0] == 'login' and result[1] == '0000':
        
        # ################################# 지수선물 근월물, 차월물 선물코드 ############################################
        gmshcode, cmshcode = XingAPI.get_index_futures_gm_cm_code()
        # ############################################################################################################
        
        # ################################# t2101 요청 ################################################################
        t2101_df = XingAPI.t2101(gmshcode)
        kp200 = float(t2101_df.at[0, 'KOSPI200지수'])
    
        temp = math.floor(round(kp200 / 2.5, 0) * 2.5)
        atm_txt = '{0:.0f}'.format(temp)        
    
        print('kp200 지수 =', kp200, atm_txt)
        # ############################################################################################################        
    
        # ################################# 지수옵션 ##################################################################
        listed_code_df, cm_call_code_list, cm_put_code_list, nm_call_code_list, nm_put_code_list = XingAPI.get_index_option_listed_code_list()
        #listed_code_df.to_csv(f"{TODAY_PATH}/index_option_listed_code.csv", encoding='utf-8-sig')
    
        cm_call_atm_str = cm_call_code_list[0][0:5] + atm_txt
        cm_put_atm_str =  cm_put_code_list[0][0:5] + atm_txt
    
        nm_call_atm_str = nm_call_code_list[0][0:5] + atm_txt
        nm_put_atm_str =  nm_put_code_list[0][0:5] + atm_txt
    
        cm_call_atm_index = cm_call_code_list.index(cm_call_atm_str)
        cm_put_atm_index = cm_put_code_list.index(cm_put_atm_str)
        nm_call_atm_index = nm_call_code_list.index(nm_call_atm_str)
        nm_put_atm_index = nm_put_code_list.index(nm_put_atm_str)
        
        #print(f'{cm_call_atm_str}({cm_call_atm_index}), {cm_put_atm_str}({cm_put_atm_index})')
        #print(f'{nm_call_atm_str}({nm_call_atm_index}), {nm_put_atm_str}({nm_put_atm_index})')
        #print(cm_call_code_list[cm_call_atm_index])
    
        cm_call_atm_list = []
        nm_call_atm_list = []
    
        for i in range(quote_request_number+1):
            cm_call_atm_list.append(cm_call_code_list[cm_call_atm_index-i])
            nm_call_atm_list.append(nm_call_code_list[nm_call_atm_index-i])
    
        cm_call_atm_list.reverse()
        nm_call_atm_list.reverse()
    
        for i in range(quote_request_number):
            cm_call_atm_list.append(cm_call_code_list[cm_call_atm_index+i+1])
            nm_call_atm_list.append(nm_call_code_list[nm_call_atm_index+i+1])
    
        #print(cm_call_atm_list)
        #print(nm_call_atm_list)
    
        cm_put_atm_list = []
        nm_put_atm_list = []
    
        for i in range(quote_request_number+1):
            cm_put_atm_list.append(cm_put_code_list[cm_put_atm_index-i])
            nm_put_atm_list.append(nm_put_code_list[nm_put_atm_index-i])
    
        cm_put_atm_list.reverse()
        nm_put_atm_list.reverse()
    
        for i in range(quote_request_number):
            cm_put_atm_list.append(cm_put_code_list[cm_put_atm_index+i+1])
            nm_put_atm_list.append(nm_put_code_list[nm_put_atm_index+i+1])
    
        #print(cm_put_atm_list)
        #print(nm_put_atm_list)
    
        cm_opt_quote_list = cm_call_atm_list + cm_put_atm_list
        nm_opt_quote_list = nm_call_atm_list + nm_put_atm_list
    
        cm_opt_quote_cmd = []
        cm_opt_quote_cmd.append('quote')
        cm_opt_quote = cm_opt_quote_cmd + cm_opt_quote_list
    
        nm_opt_quote_cmd = []
        nm_opt_quote_cmd.append('quote')
        nm_opt_quote = nm_opt_quote_cmd + nm_opt_quote_list 
    
        # 호가
        if index_option_cm_quote:
            queue.put(cm_opt_quote)
            print('본월물 실시간 호가요청...')
            real_time_index_option_quote = RealTimeIndexOptionQuote(queue=queue)
            real_time_index_option_quote.set_code_list(cm_opt_quote_list, field="optcode")
    
        if index_option_nm_quote:
            queue.put(nm_opt_quote)
            print('차월물 실시간 호가요청...')
            real_time_index_option_quote = RealTimeIndexOptionQuote(queue=queue)
            real_time_index_option_quote.set_code_list(nm_opt_quote_list, field="optcode")
    
        # ############################################################################################################
    
        while True:
            pythoncom.PumpWaitingMessages()
    
            if OPTION_SLEEP_SWITCH_MODE:
                time.sleep(OPTION_SLEEP_SWITCHING_DELAY)
    else:
        pass