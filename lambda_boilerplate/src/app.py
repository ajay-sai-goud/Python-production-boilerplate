import json
from loguru import logger
from opentelemetry import trace

# This block allows the script to be run directly for local testing,
# by adding the project root to the Python path.
if __name__ == "__main__":
    import sys
    import os
    # Add the project root directory to the Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)
    # Now we can use absolute imports from 'src'
    from src.core.logging_config import configure_logging
    from src.core.tracing_config import configure_tracing
    from src import services
else:
    # Use relative imports when running as part of a package (e.g., in Lambda)
    from .core.logging_config import configure_logging
    from .core.tracing_config import configure_tracing
    from . import services

# Configure logging and tracing at the module level
configure_logging()
configure_tracing()

# Instantiate your service(s)
hello_service = services.HelloService()
tracer = trace.get_tracer(__name__)

def handler(event, context):
    """
    Main Lambda handler.
    """
    with tracer.start_as_current_span("lambda_handler") as span:
        with logger.contextualize(lambda_context=context):
            try:
                if hasattr(context, 'aws_request_id'):
                    span.set_attribute("aws.request_id", context.aws_request_id)
                
                logger.info(f"Received event: {json.dumps(event)}")
                
                response_data = hello_service.get_hello_message(event)

                logger.info("Lambda execution finished successfully.")
                
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": response_data.model_dump_json(),
                }
            except Exception as e:
                logger.exception("An error occurred during Lambda execution.")
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                
                return {
                    "statusCode": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "An internal server error occurred."}),
                }

# This block allows you to run the handler locally for simple testing
if __name__ == "__main__":
    from types import SimpleNamespace
    
    # Create a mock event and context object
    mock_event = {
        "queryStringParameters": {"username": "LocalTest"}
    }
    # A SimpleNamespace is a simple way to create an object with attributes
    mock_context = SimpleNamespace(aws_request_id="local-test-12345")
    
    print("--- Running Handler Locally ---")
    response = handler(mock_event, mock_context)
    print("\n--- Handler Response ---")
    print(json.dumps(response, indent=2))
    print("--------------------------")
