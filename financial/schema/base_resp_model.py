from pydantic import BaseModel

'''
    Base model of all responses for financial_data and statistics 
'''

class Info(BaseModel):
    error: str = ''


class BaseResp(BaseModel):
    info: Info