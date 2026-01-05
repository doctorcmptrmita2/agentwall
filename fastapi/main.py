"""
AgentWall FastAPI Proxy Engine
Main application entry point

Domain: agentwall.io
Motto: Guard the Agent, Save the Budget
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from config import settings
from api.v1 import chat, health
from middleware.auth import AuthMiddleware
from middleware.logging import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header to track overhead"""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000  # ms
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    
    # Log if overhead exceeds target
    if process_time > 10:
        logger.warning(
            f"High overhead detected: {process_time:.2f}ms for {request.url.path}"
        )
    
    return response

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(chat.router, prefix="/v1", tags=["openai-compatible"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all exceptions and return structured error"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Report to Laravel (async, non-blocking)
    # TODO: Implement error reporting
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "Internal server error",
                "type": "internal_error",
                "code": "internal_error"
            }
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"DLP mode: {settings.DLP_MODE}")
    logger.info(f"Max steps: {settings.MAX_STEPS}")
    
    # TODO: Initialize ClickHouse connection
    # TODO: Initialize Redis connection
    # TODO: Load ML models (sentence transformers)
    
    logger.info("Startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down...")
    
    # TODO: Flush pending logs to ClickHouse
    # TODO: Close Redis connections
    # TODO: Close ClickHouse connections
    
    logger.info("Shutdown complete")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "motto": "Guard the Agent, Save the Budget"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )
