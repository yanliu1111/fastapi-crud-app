from fastapi import FastAPI
from fastapi.requests import Request
import time

def register_middleware(app: FastAPI):
    # create login middleware

    @app.middleware("http")
    async def custom_loggin(request: Request, call_next):
        start_time = time.time()
        print('before', start_time)
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"Request: {request.method} {request.url} completed in {process_time:.4f} seconds")
        return response