from fastapi import HTTPException

from dal.financial_data_dal import query_financial_data
from common.db import SessionLocal
from common.log import logger


def get_financial_data(db: SessionLocal, start_date: str, end_date: str, symbol: str, limit: int, page: int):
    '''
        To query data from db via dal, then filter in the records needed by limit and page
    '''
    try:
        logger.info(f"Query financial data(symbol={symbol}, start_date={start_date}, end_date={end_date})")
        records = query_financial_data(db, symbol, start_date, end_date)
        logger.info(f"Records(symbol={symbol}, start_date={start_date}, end_date={end_date}): {records}")

        data = []
        count = len(records)
        start = (page-1)*limit
        end = min(count, start+limit)
        for r in records[start: end]:
            data.append(r.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'get financial data encountered an error: {str(e)}')
    
    logger.info(f"Filtered records(symbol={symbol}, start_date={start_date}, end_date={end_date}, limit={limit}, page={page}):{data}")

    return data


def calc_statistics(db: SessionLocal, start_date: str, end_date: str, symbol: str):
    '''
        Query data from db via dal, then calculate statistics(average of open_price, average of close_price, average of volume)
    '''
    logger.info(f"Query financial data(symbol={symbol}, start_date={start_date}, end_date={end_date})")
    records = query_financial_data(db, symbol, start_date, end_date)
    logger.info(f"Records(symbol={symbol}, start_date={start_date}, end_date={end_date}): {records}")

    count = len(records)

    # data structure of the data part of statistics response
    data = {
        'start_date': start_date,
        'end_date': end_date,
        'symbol': symbol,
        'average_daily_open_price': 0,
        'average_daily_closing_price': 0,
        'average_daily_volume': 0
    }
    
    # do statistics calculation here
    try:
        for r in records:
            data['average_daily_open_price'] += float(r.open_price)
            data['average_daily_closing_price'] += float(r.close_price)
            data['average_daily_volume'] += int(r.volume)

        data['average_daily_open_price'] /= count
        data['average_daily_open_price'] = round(data['average_daily_open_price'], 2)
        data['average_daily_closing_price'] /= count
        data['average_daily_closing_price'] = round(data['average_daily_closing_price'], 2)
        data['average_daily_volume'] //= count 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'statistics calculation encountered an error: {str(e)}')

    logger.info(f"Statistics(symbol={symbol}, start_date={start_date}, end_date={end_date}):{data}")

    return data