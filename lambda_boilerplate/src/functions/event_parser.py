from loguru import logger

def get_request_username(event: dict) -> str:
    """
    Parses the Lambda event to find a username.
    
    This function demonstrates extracting and validating a piece of data
    from the incoming request. It defaults to 'Guest' if no name is found.
    """
    logger.info("Parsing event for username.")
    
    # Example: Look for a username in the query string parameters
    username = event.get("queryStringParameters", {}).get("username", "Guest")
    
    if username == "Guest":
        logger.warning("No username found in query string, defaulting to 'Guest'.")
    else:
        logger.info(f"Found username: {username}")
        
    return username
