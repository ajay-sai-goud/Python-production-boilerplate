from fastapi import APIRouter, HTTPException, status
from loguru import logger
from opentelemetry import trace

api_router = APIRouter()
tracer = trace.get_tracer(__name__)


@api_router.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    """
    Simple health check endpoint to confirm the API is running.
    """
    with tracer.start_as_current_span("health_check_span") as span:
        logger.info("Health check endpoint was called.")
        span.set_attribute("service.status", "ok")
        return {"status": "ok"}


@api_router.get("/error", tags=["Test"])
async def test_error_logging():
    """
    An endpoint to test error logging.
    """
    try:
        with tracer.start_as_current_span("error_test_span") as span:
            span.set_attribute("test.deliberate_error", True)
            result = 1 / 0
    except ZeroDivisionError as e:
        logger.exception("A deliberate error occurred for testing.")
        # Record the exception in the current span
        span = trace.get_current_span()
        span.record_exception(e)
        span.set_status(trace.Status(trace.StatusCode.ERROR, "Deliberate division by zero"))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred."
        )
    return {"status": "This should not be reached."} 