"""
This package contains discrete, single-purpose business functions 
that may be composed together within the service layer.
"""
from .data_validation import is_valid_username

__all__ = ["is_valid_username"]
