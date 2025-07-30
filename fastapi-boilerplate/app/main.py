import uvicorn
from fastapi import FastAPI, Request
from loguru import logger
import time
from fastapi.middleware.cors import CORSMiddleware

from . import core
from . import api
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Configure logging and tracing before creating the app instance
core.configure_logging()
core.configure_tracing()

app = FastAPI(
    title=core.settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None, # Disable redoc
)

# ===============================================
# Middleware
# ===============================================
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=core.settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# ===============================================
# API Routes
# ===============================================
app.include_router(api.api_router, prefix="/api")

@app.get("/", tags=["Root"])
async def read_root():
    """A welcome message for the root endpoint."""
    logger.info("Root endpoint was hit.")
    return {"message": f"Welcome to {core.settings.APP_NAME}"}

# ===============================================
# Server Runners
# ===============================================
def run_dev_server():
    """
    Run the Uvicorn server for development.
    """
    logger.info("Starting development server... (reload enabled)")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
    )

def run_prod_server():
    """
    Run the Uvicorn server for production.
    """
    logger.info("Starting production server... (reload disabled, 4 workers)")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=4,
        log_config=None,
    )
