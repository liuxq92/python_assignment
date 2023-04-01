from typing import Union, List, Dict
from pydantic import BaseModel

from schema.base_resp_model import BaseResp


class Pagination(BaseModel):
    '''
        Pydantic model of the pagination part of the financial_data response
    '''
    count: int
    page: int
    limit: int
    pages: int


class FinancialDataItem(BaseModel):
    '''
        Pydantic model for financial data
    '''
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str

    class Config:
        orm_mode = True


class FinancialDataResp(BaseResp):
    '''
        Pydantic model of financial_data response
    '''
    data: Union[List[FinancialDataItem], None] = None
    pagination: Union[Pagination, None] = None
    

class StatisticsData(BaseModel):
    '''
        Pydantic model of statistics data
    '''
    start_date: str
    end_date: str
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: int


class StatisticsResp(BaseResp):
    '''
        Pydantic model of statistics response
    '''
    data: Union[StatisticsData, Dict] = {}
