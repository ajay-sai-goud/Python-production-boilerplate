from loguru import logger
from ..core.config import settings
from .. import schemas
from .. import functions
from .. import utils

class HelloService:
    """
    Service to handle the business logic for the hello endpoint.
    """
    def get_hello_message(self, event: dict) -> schemas.HelloResponse:
        """
        Processes the event and returns a formatted hello message.
        """
        logger.info("Executing hello service logic.")
        
        # 1. Use a function to parse and validate the input event
        username = functions.get_request_username(event)
        
        # 2. Use a utility to build the response message
        message = utils.build_success_message(username)
        
        logger.info(f"Successfully generated message for '{username}'.")
        
        return schemas.HelloResponse(message=message)
