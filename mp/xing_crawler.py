from datetime import datetime
import pythoncom
import multiprocessing as mp
from multiprocessing import Queue

from mp.xing_config import *
from mp.xing_api import *
from mp.xing_utils import * 
from mp.xing_real_time import *

make_dir(TICKER_DATA_FOLDER_PATH)
TODAY = datetime.today().strftime("%Y-%m-%d")
TODAY_PATH = f"{TICKER_DATA_FOLDER_PATH}/{TODAY}"
make_dir(TODAY_PATH)

if REAL_SERVER:
    is_real_server = True
else:
    is_real_server = False

def stock_crawler(queue: Queue, kospi_quote=True, kospi_tick=True, kosdaq_quote=True, kosdaq_tick=True):

    result = XingAPI.login(config["id"], config["password"], config["cert_password"], is_real_server)
    result.append('주식')

    queue.put(result)

    if result[0] == '0000':

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
    else:
        pass

# 여기에서 JIF, IJ, OVC, BM, PM등을 함께 요청
def index_futures_crawler(queue: Queue, index_futures_quote=True, index_futures_tick=True):

    proc = mp.current_process()
    print(f'\r지수선물 Process Name = {proc.name}, Process ID = {proc.pid}')

    result = XingAPI.login(config["id"], config["password"], config["cert_password"], is_real_server)
    result.append('지수선물')

    queue.put(result)

    if result[0] == '0000':

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
        listed_code_df.to_csv(f"{TODAY_PATH}/index_futures_listed_code.csv", encoding='utf-8-sig')
        
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
    else:
        pass

def index_option_crawler(queue: Queue, index_option_quote=True, index_option_tick=True):

    proc = mp.current_process()
    print(f'\r지수옵션 Process Name = {proc.name}, Process ID = {proc.pid}')
                          
    result = XingAPI.login(config["id"], config["password"], config["cert_password"], is_real_server)
    result.append('지수옵션')

    queue.put(result)

    if result[0] == '0000':        

        # ################################# 지수옵션 ##################################################################
        listed_code_df = XingAPI.get_index_option_listed_code_list()
        listed_code_df.to_csv(f"{TODAY_PATH}/index_option_listed_code.csv", encoding='utf-8-sig')

        code_list = listed_code_df['단축코드'].tolist()

        # 호가
        if index_option_quote:
            real_time_index_option_quote = RealTimeIndexOptionQuote(queue=queue)
            real_time_index_option_quote.set_code_list(code_list, field="optcode")

        # 체결
        if index_option_tick:
            real_time_index_option_tick = RealTimeIndexOptionTick(queue=queue)
            real_time_index_option_tick.set_code_list(code_list, field="optcode")
        # ############################################################################################################

        while True:
            pythoncom.PumpWaitingMessages()
    else:
        pass