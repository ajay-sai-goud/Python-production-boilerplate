from loguru import logger
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def is_valid_username(username: str) -> bool:
    """
    A simple function to validate a username.

    This function represents a piece of discrete, reusable business logic.
    For example, it could check for profanity, length, or special characters.
    """
    with tracer.start_as_current_span("validate_username_function") as span:
        span.set_attribute("validation.username", username)
        
        if len(username) < 3:
            logger.warning(f"Validation failed: Username '{username}' is too short.")
            span.set_attribute("validation.result", "failure")
            return False
            
        logger.info(f"Username '{username}' passed validation.")
        span.set_attribute("validation.result", "success")
        return True
