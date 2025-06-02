from fastapi import FastAPI
from fastapi.requests import Request
import time
from fastapi.responses import JSONResponse

logger = logging.getLogger('uvicorn.access')
logger.disabled = True  # Disable Uvicorn's default access log

def register_middleware(app: FastAPI):
    # create login middleware

    @app.middleware("http")
    async def custom_loggin(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        process_time = time.time() - start_time
        message = f"Request: {request.client.host} {request.client.port} - {request.method} - {request.url.path} - complete after{process_time}s"
        print (message)
        return response
    
    @app.middleware("http")
    async def authorization (request: Request, call_next):
        if "Authorization" not in request.headers:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing",
                         "resolution":"Please provide a valid Authorization header."
                         }
            )