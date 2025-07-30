"""
This package contains discrete, single-purpose business functions 
that may be composed together within the service layer.
"""
from .event_parser import get_request_username

__all__ = ["get_request_username"]
