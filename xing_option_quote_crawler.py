import sys, os
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
parser.read('.\skybot.ini', encoding='UTF-8')

REAL_SERVER = parser.getboolean('Server Type', 'Real Server')
#MP_OPTION_SLEEP_SWITCH_MODE = parser.getboolean('User Switch', 'MP Option Sleep Switching Mode')
MP_SLEEP_SWITCHING_DELAY = parser.getfloat('Initial Value', 'MP Sleep Switching Delay')
FEVER_TIME_DURATION = parser.getint('Initial Value', 'Fever Time Duration')

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

def option_quote_crawler(queue: Queue, main_proc_id, flag_high_speed=False, call_itm_number=5, call_otm_number=5, put_itm_number=5, put_otm_number=5, index_option_cm_quote=False, index_option_nm_quote=False):

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
        # ############################################################################################################        
    
        # ################################# 지수옵션 ##################################################################
        listed_code_df, cm_call_code_list, cm_put_code_list, nm_call_code_list, nm_put_code_list = XingAPI.get_index_option_listed_code_list()

        cm_call_code_list.reverse()
        cm_put_code_list.reverse()
        nm_call_code_list.reverse()
        nm_put_code_list.reverse()

        cm_code_list = cm_call_code_list + cm_put_code_list
        nm_code_list = nm_call_code_list + nm_put_code_list
        
        cm_call_atm_str = cm_call_code_list[0][0:5] + atm_txt
        cm_put_atm_str =  cm_put_code_list[0][0:5] + atm_txt

        nm_call_atm_str = nm_call_code_list[0][0:5] + atm_txt
        nm_put_atm_str =  nm_put_code_list[0][0:5] + atm_txt        

        cm_call_atm_index = cm_call_code_list.index(cm_call_atm_str)
        cm_put_atm_index = cm_put_code_list.index(cm_put_atm_str)

        nm_call_atm_index = nm_call_code_list.index(nm_call_atm_str)
        nm_put_atm_index = nm_put_code_list.index(nm_put_atm_str)

        cm_call_atm_list = []

        for i in range(cm_call_atm_index - call_otm_number, cm_call_atm_index + call_itm_number + 1):
            cm_call_atm_list.append(cm_call_code_list[i])

        cm_put_atm_list = []

        for i in range(cm_put_atm_index - put_itm_number, cm_put_atm_index + put_otm_number + 1):
            cm_put_atm_list.append(cm_put_code_list[i])

        cm_opt_quote_list = cm_call_atm_list + cm_put_atm_list

        nm_call_atm_list = []

        for i in range(nm_call_atm_index - call_otm_number, nm_call_atm_index + call_itm_number + 1):
            nm_call_atm_list.append(nm_call_code_list[i])

        nm_put_atm_list = []

        for i in range(nm_put_atm_index - put_itm_number, nm_put_atm_index + put_otm_number + 1):
            nm_put_atm_list.append(nm_put_code_list[i])

        nm_opt_quote_list = nm_call_atm_list + nm_put_atm_list
    
        cm_opt_quote_cmd = []
        cm_opt_quote_cmd.append('quote')

        if DayTime:
            cm_opt_quote = cm_opt_quote_cmd + cm_opt_quote_list
        else:
            #cm_opt_quote = cm_opt_quote_cmd + cm_code_list
            cm_opt_quote = cm_opt_quote_cmd + cm_opt_quote_list
    
        nm_opt_quote_cmd = []
        nm_opt_quote_cmd.append('quote')

        if DayTime:
            nm_opt_quote = nm_opt_quote_cmd + nm_opt_quote_list
        else:
            #nm_opt_quote = nm_opt_quote_cmd + nm_code_list
            nm_opt_quote = nm_opt_quote_cmd + nm_opt_quote_list
    
        # 호가
        if index_option_cm_quote:
            queue.put(cm_opt_quote)
            print('근월물 옵션 실시간 호가요청...')
            real_time_index_option_quote = RealTimeIndexOptionQuote(queue=queue)

            real_time_index_option_quote.set_code_list(cm_opt_quote_list, field="optcode")
    
        if index_option_nm_quote:
            queue.put(nm_opt_quote)
            print('차월물 옵션 실시간 호가요청...')
            real_time_index_option_quote = RealTimeIndexOptionQuote(queue=queue)

            real_time_index_option_quote.set_code_list(nm_opt_quote_list, field="optcode")                
    
        # ############################################################################################################
    
        while True:
            pythoncom.PumpWaitingMessages()

            if index_option_cm_quote:
    
                dt = datetime.now()

                ppid = os.getppid()

                if ppid != main_proc_id:
                    print("my parent is gone...\r")
                    sys.exit(1)

                if dt.hour == 9 and 0 <= dt.minute <= FEVER_TIME_DURATION:
                    pass
                else:
                    if not flag_high_speed:
                        time.sleep(MP_SLEEP_SWITCHING_DELAY)
                    else:
                        pass

            if index_option_nm_quote:

                if not flag_high_speed:
                    time.sleep(MP_SLEEP_SWITCHING_DELAY)
                else:
                    pass
    else:
        pass