from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
import time
from fastapi.responses import JSONResponse
import logging
from fastapi.middleware.trustedhost import TrustedHostMiddleware
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
    
    # @app.middleware("http")
    # async def authorization (request: Request, call_next):
    #     if not "Authorization" in request.headers:
    #         return JSONResponse(
    #             status_code=401,
    #             content={"detail": "Authorization header missing",
    #                      "resolution":"Please provide a valid Authorization header."
    #                      }
    #             status_code=status.HTTP_401_UNAUTHORIZED
    #         )
    #     response = await call_next(request)
    #     return response

    # Register CORS middleware, add middleware to allow cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins, adjust as needed
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods, adjust as needed
        allow_headers=["*"],  # Allows all headers, adjust as needed
    )

    # Register TrustedHostMiddleware to restrict allowed hosts
    app.add_middleware(
        TrustedHostMiddleware,
        # allowed_hosts=["localhost", "127.0.0.1" ,"bookly-api-dc03.onrender.com","0.0.0.0"],
        allowed_hosts=["localhost", "127.0.0.1"],
    )