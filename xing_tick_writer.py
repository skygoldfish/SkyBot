import csv
from typing import Tuple
import io
import win32file

from xing_config import *
from xing_utils import * 
from xing_constant import *

#from xing_crawler import *
from xing_ovc_crawler import *
from xing_futures_crawler import *
from xing_option_tick_crawler import *
from xing_option_quote_crawler import *

if not BUNDLE_BY_MARKET:
    win32file._setmaxstdio(1024 * 8)

CSV_HANDLER_STORE = dict()

def get_csv_writer(code: str, tick_type: DataType, bundle_by_market=True) -> Tuple[io.TextIOWrapper, csv.writer]:
    """
    bundle_by_market: True, 시장별 파일
                      False, 종목별 파일
    """
    if bundle_by_market:
        return bundle_writer(tick_type)
    else:
        return single_code_writer(code, tick_type)

def single_code_writer(code: str, tick_type: DataType) -> Tuple[io.TextIOWrapper, csv.writer]:

    global CSV_HANDLER_STORE

    handler_id = f"{code}|{tick_type.name}"
    csv_handler = CSV_HANDLER_STORE.get(handler_id, None)

    if csv_handler is None:
        tick_type_folder = f'{TODAY_PATH}/{tick_type.name}'
        make_dir(tick_type_folder)
        file_name = f'{tick_type_folder}/{code}.csv'
        is_exist = file_is_exist(file_name)

        f = open(file_name, 'a', newline='')
        writer = csv.writer(f)

        if not is_exist:
            write_header(tick_type, writer)

        csv_handler = (f, writer)
        CSV_HANDLER_STORE[handler_id] = csv_handler

    return csv_handler

def bundle_writer(tick_type: DataType) -> Tuple[io.TextIOWrapper, csv.writer]:

    handler_id = tick_type.name
    csv_handler = CSV_HANDLER_STORE.get(handler_id, None)

    if csv_handler is None:
        file_name = f'{TODAY_PATH}/{handler_id}.csv'
        is_exist = file_is_exist(file_name)

        f = open(file_name, 'a', newline='')
        writer = csv.writer(f)

        if not is_exist:
            write_header(tick_type, writer)

        csv_handler = (f, writer)
        CSV_HANDLER_STORE[handler_id] = csv_handler

    return csv_handler

def write_header(tick_type: DataType, writer: csv.writer) -> None:

    if tick_type == DataType.JIF_TICK:
        writer.writerow(JIF_COLUMNS_HEADER)
    elif tick_type == DataType.NWS_TICK:
        writer.writerow(NWS_COLUMNS_HEADER)
    elif tick_type == DataType.YJ_TICK:
        writer.writerow(YJ_COLUMNS_HEADER)
    elif tick_type == DataType.YFC_TICK:
        writer.writerow(YFC_COLUMNS_HEADER)
    elif tick_type == DataType.IJ_TICK:
        writer.writerow(IJ_COLUMNS_HEADER)
    elif tick_type == DataType.S3_TICK:
        writer.writerow(S3_COLUMNS_HEADER)
    elif tick_type == DataType.BM_TICK:
        writer.writerow(BM_COLUMNS_HEADER)
    elif tick_type == DataType.PM_TICK:
        writer.writerow(PM_COLUMNS_HEADER)
    elif tick_type == DataType.OVC_TICK:
        writer.writerow(OVC_COLUMNS_HEADER)
    elif tick_type in [DataType.KOSPI_QUOTE, DataType.KOSDAQ_QUOTE]:
        writer.writerow(QUOTE_COLUMNS_HEADER)
    elif tick_type in [DataType.KOSPI_TICK, DataType.KOSDAQ_TICK]:
        writer.writerow(TICK_COLUMNS_HEADER)    
    elif tick_type == DataType.INDEX_FUTURES_QUOTE:
        writer.writerow(INDEX_FUTURES_QUOTE_COLUMNS_HEADER)
    elif tick_type == DataType.INDEX_FUTURES_TICK:
        writer.writerow(INDEX_FUTURES_TICK_COLUMNS_HEADER)
    elif tick_type == DataType.INDEX_OPTION_QUOTE:
        writer.writerow(INDEX_OPTION_QUOTE_COLUMNS_HEADER)
    elif tick_type == DataType.INDEX_OPTION_TICK:
        writer.writerow(INDEX_OPTION_TICK_COLUMNS_HEADER)
    else:
        pass

def create_csv_writer(code_list: str, tick_type: DataType) -> None:

    for code in code_list:
        get_csv_writer(code, tick_type)

def handle_tick_data(tick_data: list, tick_type: DataType) -> None:
    """
    tick_data : [system_time, code, ...]
    """
    code = tick_data[1]
    f, writer = get_csv_writer(code, tick_type, BUNDLE_BY_MARKET)
    writer.writerow(tick_data)
    f.flush()

def close_all_writer() -> None:

    global CSV_HANDLER_STORE

    handler_id_list = list(CSV_HANDLER_STORE.keys())

    for handler_id in handler_id_list:
        handler = CSV_HANDLER_STORE.pop(handler_id)
        f, writer = handler
        f.close()
