from pydantic import BaseModel, Field

class HelloResponse(BaseModel):
    """
    Pydantic model for the Lambda's response payload.
    """
    message: str = Field(..., description="A welcome message.", json_schema_extra={"example": "Hello from MyLambdaApp!"})
