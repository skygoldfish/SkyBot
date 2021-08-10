from datetime import datetime
import pythoncom
import math
import time
import multiprocessing as mp
from multiprocessing import Queue
from configparser import ConfigParser

from xing_config import *
from xing_api import *
from xing_utils import * 
from xing_option_quote_real_time import *

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

계좌정보 = pd.read_csv("secret/passwords.csv", converters={'계좌번호': str, '거래비밀번호': str})

if REAL_SERVER:
    주식계좌정보 = 계좌정보.query("구분 == '거래'")
    print('MP 실서버에 접속합니다.')

    ID = 주식계좌정보['사용자ID'].values[0].strip()            
    PWD = 주식계좌정보['비밀번호'].values[0].strip()
    CERT = 주식계좌정보['공인인증비밀번호'].values[0].strip()

    is_real_server = True
    config = {"id": ID, "password": PWD, "cert_password": CERT}
else:
    주식계좌정보 = 계좌정보.query("구분 == '모의'")
    print('MP 모의서버에 접속합니다.')

    ID = 주식계좌정보['사용자ID'].values[0].strip()            
    PWD = 주식계좌정보['비밀번호'].values[0].strip()
    CERT = 주식계좌정보['공인인증비밀번호'].values[0].strip()

    is_real_server = False
    config = {"id": ID, "password": PWD, "cert_password": "0"}

def option_quote_crawler(queue: Queue, quote_request_number=5, index_option_cm_quote=False, index_option_nm_quote=False):

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