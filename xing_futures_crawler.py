import sys, os
from datetime import datetime
import pythoncom
import math
import time
import multiprocessing as mp
from multiprocessing import Queue
from configparser import ConfigParser
import psutil

from xing_config import *
from xing_api import *
from xing_utils import * 
from xing_futures_real_time import *

make_dir(TICKER_DATA_FOLDER_PATH)
TODAY = datetime.today().strftime("%Y-%m-%d")
TODAY_PATH = f"{TICKER_DATA_FOLDER_PATH}/{TODAY}"
make_dir(TODAY_PATH)

# Configuration Parser
parser = ConfigParser()
parser.read('.\skybot.ini', encoding='UTF-8')

REAL_SERVER = parser.getboolean('Server Type', 'Real Server')

KOSPI = '001'
KOSPI200 = '101'
KOSDAQ = '301'
FUTURES = '900'

SAMSUNG = '005930'
HYUNDAI = '005380'

#MP_FUT_SLEEP_SWITCH_MODE = parser.getboolean('User Switch', 'MP FUT Sleep Switching Mode')
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

# 여기에서 JIF, IJ, OVC, BM, PM등을 함께 요청
def futures_crawler(queue: Queue, main_proc_id, flag_high_speed=False, index_futures_quote=True, index_futures_tick=True):

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

        print('근월물 선물({0}) 예상체결 요청...\r'.format(listed_code_df['단축코드'][0]))
        real_time_yfc_tick.set_yfc_code(listed_code_df['단축코드'][0])

        print('차월물 선물({0}) 예상체결 요청...\r'.format(listed_code_df['단축코드'][1]))
        real_time_yfc_tick.set_yfc_code(listed_code_df['단축코드'][1])
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

            dt = datetime.now()

            ppid = os.getppid()

            if ppid != main_proc_id:
                print("my parent is gone...\r")
                p = psutil.Process(os.getpid())
                p.terminate()
                sys.exit(1)

            if dt.hour == 9 and 0 <= dt.minute <= FEVER_TIME_DURATION:
                pass
            else:
                if not flag_high_speed:
                    time.sleep(MP_SLEEP_SWITCHING_DELAY)
                else:
                    pass          
    else:
        pass
