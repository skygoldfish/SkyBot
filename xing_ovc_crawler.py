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
from xing_ovc_real_time import *

make_dir(TICKER_DATA_FOLDER_PATH)
TODAY = datetime.today().strftime("%Y-%m-%d")
TODAY_PATH = f"{TICKER_DATA_FOLDER_PATH}/{TODAY}"
make_dir(TODAY_PATH)

# Configuration Parser
parser = ConfigParser()
parser.read('.\skybot.ini')

REAL_SERVER = parser.getboolean('Server Type', 'Real Server')

SP500 = parser.get('Code of the Foreign Futures', 'S&P 500')
DOW = parser.get('Code of the Foreign Futures', 'DOW')
NASDAQ = parser.get('Code of the Foreign Futures', 'NASDAQ')
WTI = parser.get('Code of the Foreign Futures', 'WTI')
EUROFX = parser.get('Code of the Foreign Futures', 'EUROFX')
HANGSENG = parser.get('Code of the Foreign Futures', 'HANGSENG')
GOLD = parser.get('Code of the Foreign Futures', 'GOLD')

SLEEP_SWITCH_MODE = parser.getboolean('User Switch', 'MP Sleep Switching Mode')
SLEEP_SWITCHING_DELAY = parser.getfloat('Initial Value', 'MP Sleep Switching Delay')

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

def ovc_crawler(queue: Queue, index_ovc=True):

    proc = mp.current_process()
    print(f'\r지수선물 Process Name = {proc.name}, Process ID = {proc.pid}')

    result = XingAPI.login(config["id"], config["password"], config["cert_password"], is_real_server)
    result.append('지수선물')

    queue.put(result)

    if result[0] == 'login' and result[1] == '0000':

        # ################################### OVC ####################################################################        
        real_time_ovc_tick = RealTimeOVCTick(queue=queue)
            
        real_time_ovc_tick.set_ovc_code(DOW)

        if index_ovc:
            real_time_ovc_tick.set_ovc_code(SP500)
            real_time_ovc_tick.set_ovc_code(NASDAQ)
            real_time_ovc_tick.set_ovc_code(WTI)
            real_time_ovc_tick.set_ovc_code(EUROFX)
            real_time_ovc_tick.set_ovc_code(HANGSENG)
            real_time_ovc_tick.set_ovc_code(GOLD)
        else:
            pass 

        while True:
            pythoncom.PumpWaitingMessages()

            if SLEEP_SWITCH_MODE:
                time.sleep(SLEEP_SWITCHING_DELAY)
    else:
        pass
