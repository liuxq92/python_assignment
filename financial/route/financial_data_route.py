from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query

from schema.base_resp_model import Info
from schema.financial_data_resp import FinancialDataResp, StatisticsResp
from service.financial_data_service import calc_statistics, get_financial_data as get_financial_data_service
from common.db import SessionLocal, get_db
from common.log import logger
from common.custom_route import CustomRoute



router = APIRouter(
    prefix="/api",
    route_class=CustomRoute,
    tags=["financial_data"]
)

@router.get("/financial_data",  response_model=FinancialDataResp)
def get_financial_data(
    start_date: str='', 
    end_date: str='', 
    symbol: str='', 
    limit: int=Query(default=5, ge=1), 
    page: int=Query(default=1, ge=1), 
    db: SessionLocal = Depends(get_db)
):
    # more request params check
    logger.info("Advanced date format check...")
    err = ''
    if start_date:
        err += validate_date_str(start_date, '%Y-%m-%d')
    if end_date:
        err += validate_date_str(end_date, '%Y-%m-%d')
    if err:
        raise HTTPException(status_code=400, detail=err)

    # get data from db
    logger.info("Call get_financial_data service")
    data = get_financial_data_service(db, start_date, end_date, symbol, limit, page)
    count = len(data)
    
    # pagination in response
    pagination = {
        "count": count,
        "page": page,
        "limit": limit,
        "pages": count//limit + 1
    }

    resp = FinancialDataResp(data=data, pagination=pagination, info={})
    return resp


@router.get("/statistics",  response_model=StatisticsResp)
def get_statistics(
    start_date: str=Query(default=..., regex='^\d{4}-\d{2}-\d{2}$', example='2022-03-13'), 
    end_date: str=Query(default=..., regex='^\d{4}-\d{2}-\d{2}$', example='2022-03-13'), 
    symbol: str=Query(default=..., example='IBM', description='Stock symbol for a company'),
    db: SessionLocal = Depends(get_db)
):
    # more request params check
    logger.info("Advanced date format check...")
    err = validate_date_str(start_date, '%Y-%m-%d')
    err += validate_date_str(end_date, '%Y-%m-%d')
    if err:
        raise HTTPException(status_code=400, detail=err)
    if start_date > end_date:
        raise HTTPException(status_code=400, detail='end_date is earlier than start_date')

    # call calculate statistics service
    logger.info(f"Call calc_statistics service(symbol={symbol}, start_date={start_date}, end_date={end_date})")
    data = calc_statistics(db, start_date, end_date, symbol)

    return StatisticsResp(info=Info(error=err),data=data)


def validate_date_str(date_str: str, format: str):
    err = ''
    try:
        datetime.strptime(date_str, format)
    except Exception as e:
        return str(e)
    
    return err