from datetime import datetime, timedelta
import json
import os

import requests
import pymysql

def get_stock_data(symbol, ak, start_date, end_date):
    '''
        Retrieve records via AlphaVantage API, filter and tranform data into the following format
            [{
                "symbol": "IBM",
                "date": "2023-02-14",
                "open_price": "153.08",
                "close_price": "154.52",
                "volume": "62199013",
            },...]
    '''
    print(f'Get stock date for {symbol}, start from {start_date_str} to {end_date_str}(inclusive)')

    data = []

    # retrieve records
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ak}'
    resp = requests.get(url)

    retry = 0
    while resp.status_code != 200 and retry < 3:
        resp = requests.get(url)
        retry += 1

    try:
        resp_json = json.loads(resp.text)

        # filter in the part we need 
        ts = resp_json.get('Time Series (Daily)', {})
        for k, v in ts.items():
            if k >= start_date and k <= end_date:
                data.append(
                    {
                        "symbol": symbol,
                        "date": k,
                        "open_price": v.get('1. open', ''),
                        "close_price": v.get('4. close', ''),
                        "volume": v.get('6. volume', ''),
                    }
                )
    except Exception as e:
        print(str(e))

    return data


def upsert_data_to_db(data):
    '''
        Upsert financial data to mysql db via executemany
    '''
    print('Upsert data into database ...')

    try:
        db = pymysql.connect(host=os.getenv('MYSQL_HOST'), port=int(os.getenv('MYSQL_PORT')), 
                             user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWD'), db="python_assignment")
        cursor = db.cursor()
    except Exception as e:
        print('Database connection error')
        print(str(e))
        return

    sql = "INSERT INTO financial_data(symbol, \
           date, open_price, close_price, volume) \
           VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE \
            open_price=values(open_price), close_price=values(close_price), volume=values(volume)"
    
    val = [(e.get('symbol', ''), e.get('date', ''), e.get('open_price', ''), e.get('close_price', ''), e.get('volume', '')) for e in data]
    
    try:
        cursor.executemany(sql, val)
        db.commit()
    except Exception as e:
        print('Upsert data fail')
        print(str(e))
        db.rollback()

    db.close()
    print('Upsert data success')


if __name__ == "__main__":
    ak = os.getenv('ALPHA_VANTAGE_AK')

    if not ak:
        print(f'Environment variable ALPHA_VANTAGE_AK not set.')
        exit(1)

    # The first/last day of last two weeks in string format "%Y-%m-%d"
    now = datetime.now()
    start_date = now - timedelta(days=now.weekday() + 14)
    end_date = now - timedelta(days=now.weekday() + 1)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    data = []

    # a dict where key is the company name, value is the symbol
    symbols = {'IBM': 'IBM', 'Apple Inc.': 'AAPL'}

    for _, symbol in symbols.items():
        data += get_stock_data(symbol, ak, start_date_str, end_date_str)
    
    if data:
        upsert_data_to_db(data)
