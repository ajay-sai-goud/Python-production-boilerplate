from ..core.config import settings

def build_success_message(name: str) -> str:
    """
    A simple utility to build a standardized success message.
    """
    return f"Hello, {name}! Welcome to {settings.APP_NAME}."
