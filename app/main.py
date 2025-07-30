import uvicorn
from fastapi import FastAPI, Request
from loguru import logger
import time

from .core.config import settings
from .core.logging_config import configure_logging
from .core.tracing_config import configure_tracing
from .api.routes import api_router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Configure logging and tracing before creating the app instance
configure_logging()
configure_tracing()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None, # Disable redoc
)

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    FastAPI middleware to log incoming requests.
    """
    start_time = time.time()
    logger.info(f"--> {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}ms"
    
    logger.info(
        f"<-- {request.method} {request.url.path} - "
        f"Completed in {formatted_process_time} "
        f"Status: {response.status_code}"
    )
    
    return response

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
async def read_root():
    """A welcome message for the root endpoint."""
    logger.info("Root endpoint was hit.")
    return {"message": f"Welcome to {settings.APP_NAME}"}

def run_dev_server():
    """
    Run the Uvicorn server for development.
    This function is referenced in pyproject.toml's [project.scripts].
    It enables auto-reloading.
    """
    logger.info("Starting development server... (reload enabled)")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,  # We use our own Loguru config
    )

def run_prod_server():
    """
    Run the Uvicorn server for production.
    This function is referenced in pyproject.toml's [project.scripts].
    It disables auto-reloading and runs with multiple workers.
    """
    logger.info("Starting production server... (reload disabled, 4 workers)")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=4,
        log_config=None,  # We use our own Loguru config
    ) 