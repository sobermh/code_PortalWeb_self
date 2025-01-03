import json
import os, time

from fastapi.responses import JSONResponse

from application.utils.logs import get_logger


async def log_requests(request, call_next):
    """日志中间件"""
    logger = get_logger(os.environ.get('APP_NAME'))
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"path={request.url.path} timer={formatted_process_time}ms status_code={response.status_code}")
    return response


async def response_request(request, call_next):
    """响应中间件"""
    response = await call_next(request)
    if isinstance(response, JSONResponse):
        response_content = response.content
        if response_content:
            response_content_dict = response_content.dict()
            response_content_dict['code'] = 200
            response.content = JSONResponse(content=response_content_dict)
    return response
