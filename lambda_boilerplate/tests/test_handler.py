import json
import unittest.mock as mock
from src.app import handler
from src.types.hello import HelloResponse

def test_handler_success():
    """
    Tests the main Lambda handler for a successful invocation.
    """
    # Arrange: Create a mock event and context
    mock_event = {
        "queryStringParameters": {"username": "UnitTest"}
    }
    mock_context = mock.Mock()
    mock_context.function_name = "test-function"
    mock_context.aws_request_id = "12345-67890"

    # Act: Call the handler
    response = handler(mock_event, mock_context)

    # Assert: Check the response is what we expect
    assert response["statusCode"] == 200
    assert "Content-Type" in response["headers"]
    assert response["headers"]["Content-Type"] == "application/json"
    
    body = json.loads(response["body"])
    
    # Validate the response body against the Pydantic model
    validated_body = HelloResponse(**body)
    assert "Hello, UnitTest! Welcome to" in validated_body.message

def test_handler_no_username():
    """
    Tests the handler when no username is provided, expecting it to default to 'Guest'.
    """
    # Arrange
    mock_event = {}
    mock_context = mock.Mock()
    mock_context.function_name = "test-function"
    mock_context.aws_request_id = "09876-54321"

    # Act
    response = handler(mock_event, mock_context)

    # Assert
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    validated_body = HelloResponse(**body)
    assert "Hello, Guest! Welcome to" in validated_body.message
