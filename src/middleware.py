from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging

logger = logging.getLogger('uvicorn.access')
logger.disabled = True  # Disable Uvicorn's default access log

def register_middleware(app: FastAPI):
    # create login middleware

    @app.middleware("http")
    async def custom_loggin(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        process_time = time.time() - start_time
        message = f"Request: {request.method} {request.url.path} - complete after{process_time}s"
        print (message)
        return response