"""
api.py
Root api file.
"""

# Import dependencies
from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from config.settings import MiddlewareConfig, load_tags, JWTSettings

# Security imports
from fastapi_jwt_auth import AuthJWT
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException

# Router imports
from routers.auth_routes import auth_router
from routers.user_routes import user_router


# Define utilities
tags = load_tags()
app = FastAPI(openapi_tags=tags)
middleware_config = MiddlewareConfig()


# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins = middleware_config.origins,
    allow_credentials = True,
    allow_headers = middleware_config.allow_headers,
    allow_methods = middleware_config.allow_methods
)

# JWT setup
@AuthJWT.load_config
def load_jwt_config():
    return JWTSettings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
