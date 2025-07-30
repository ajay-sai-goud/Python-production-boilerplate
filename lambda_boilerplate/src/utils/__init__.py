"""
This package contains shared utility functions that can be used across the Lambda function.
"""
from .response_builder import build_success_message

__all__ = ["build_success_message"]
