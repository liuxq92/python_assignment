import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from common.log import logger

class CustomRoute(APIRoute):
    '''
        Custom route to highlight more info 
    '''
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            '''
                New route handler to put request into log, calculate response time etc.
            '''
            logger.info(f"New request url: {request.url} {request.body}")
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            logger.info(f"route duration: {duration}")
            logger.info(f"route response: {response.body}")
            logger.info(f"route response headers: {response.headers}")
            return response

        return custom_route_handler
