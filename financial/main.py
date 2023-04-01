import os

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from schema.base_resp_model import BaseResp, Info
from common.log import logger

# environment variables
env = os.getenv('env', 'dev')
if env.lower() == 'dev':
    from config.dev import settings

# create a fastapi application
app = FastAPI()

# custom http exception handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc:StarletteHTTPException):
    '''
        Custom http exception handler to align with the response format
    '''
    logger.error(f'{str(exc.detail)}')
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(BaseResp(info=Info(error=str(exc.detail))))
    )

# custom request validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    '''
        Custom request validation exception handler to align with the response format
    '''
    logger.error(f'{str(exc.errors())}')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(BaseResp(info=Info(error=str(exc.errors()))))
    )

# health check
@app.get("/api/health_check")
def health_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content='OK'
    )

# assemble route to the fastapi app 
from route.financial_data_route import router as fd_router
app.include_router(fd_router)
