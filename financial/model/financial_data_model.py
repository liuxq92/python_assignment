from sqlalchemy import Column, String

from common.db import Base


class FinancialData(Base):
    '''
        ORM model for the table `financial_data`
    '''
    __tablename__ = 'financial_data'

    symbol = Column(String, primary_key=True)
    date = Column(String, primary_key=True)
    open_price = Column(String)
    close_price = Column(String)
    volume = Column(String)


    def __repr__(self) -> str:
        return f"FinancialData(symbol={self.symbol!r}, date={self.date!r}, open_price={self.open_price!r}, close_price={self.close_price!r}, volume={self.volume!r})"
    
    def to_dict(self):
        '''
            convert all values to a dict
        '''
        return {c.name: getattr(self, c.name, '') for c in self.__table__.columns}