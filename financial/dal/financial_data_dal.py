from sqlalchemy import select

from model.financial_data_model import FinancialData
from common.db import SessionLocal


def query_financial_data(db:SessionLocal, symbol: str, start_date: str, end_date: str):
    '''
        Data access layer query function to fetch data from db.
    '''
    stmt = select(FinancialData)
    if symbol:
        stmt = stmt.where(FinancialData.symbol == symbol)
    if start_date:
        stmt = stmt.where(FinancialData.date >= start_date)
    if end_date:
        stmt = stmt.where(FinancialData.date <= end_date)

    results = db.scalars(stmt).all()
    
    return results