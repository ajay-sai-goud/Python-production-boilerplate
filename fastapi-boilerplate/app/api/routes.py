from fastapi import APIRouter, HTTPException, status, Depends
from loguru import logger
from opentelemetry import trace

from app import schemas
from app import services

api_router = APIRouter()
tracer = trace.get_tracer(__name__)


# ===============================================
# Health Check Endpoint
# ===============================================
@api_router.get(
    "/health", 
    response_model=schemas.HealthStatus, 
    status_code=status.HTTP_200_OK, 
    tags=["Health"]
)
async def health_check(health_service: services.HealthService = Depends()) -> schemas.HealthStatus:
    """
    Endpoint to check the health of the application.
    It delegates the actual health check logic to the HealthService.
    """
    logger.info("Health check endpoint was called.")
    return await health_service.get_health_status()


# ===============================================
# User Endpoints
# ===============================================
@api_router.post(
    "/users",
    response_model=schemas.UserDisplay,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
async def create_user(
    user: schemas.UserCreate, 
    user_service: services.UserService = Depends()
) -> schemas.UserDisplay:
    """
    Endpoint to create a new user.
    """
    logger.info(f"Received request to create user: {user.username}")
    return await user_service.create_user(user)


# ===============================================
# Test Endpoint
# ===============================================
@api_router.get("/error", tags=["Test"])
async def test_error_logging():
    """
    An endpoint to test error logging and tracing.
    """
    try:
        with tracer.start_as_current_span("error_test_span") as span:
            span.set_attribute("test.deliberate_error", True)
            result = 1 / 0
    except ZeroDivisionError as e:
        logger.exception("A deliberate error occurred for testing.")
        
        span = trace.get_current_span()
        span.record_exception(e)
        span.set_status(trace.Status(trace.StatusCode.ERROR, "Deliberate division by zero"))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred."
        )
    return {"status": "This should not be reached."}
