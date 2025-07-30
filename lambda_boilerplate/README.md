# AWS Lambda Production Boilerplate

This is a production-ready boilerplate for creating robust and observable AWS Lambda functions in Python. It is designed for clarity, maintainability, and easy deployment using AWS SAM.

## Core Features

- **Structured, Production-Ready Logging**: Pre-configured with `loguru`.
- **Automatic Log Correlation**: Every log message is automatically enriched with the `aws_request_id`.
- **Centralized Configuration**: Uses `pydantic-settings` to manage settings.
- **Modern Packaging**: Uses `pyproject.toml` for dependency management.
- **Unit Tested**: Comes with a `tests` directory and `pytest` integration.
- **Containerized**: Includes an optimized `Dockerfile` for local testing and container-based Lambda deployments.
- **Clean, Scalable Structure**: Code is organized into a `src/` directory with `services`, `types`, `functions`, and `utils` packages.

---

## Getting Started

### Prerequisites

1.  **Install Docker**: [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2.  **Install AWS SAM CLI**: [Installing the AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
3.  **Install `uv`** (Recommended): [Installing uv](https://astral.sh/uv/install.sh).

---

## Local Development & Testing

### 1. Running Unit Tests

This project uses `pytest` for unit testing.

1.  **Navigate to the Directory**:
    ```sh
    cd lambda_boilerplate
    ```

2.  **Install Dependencies (including test dependencies)**:
    ```sh
    uv pip install -e .[test]
    ```

3.  **Run Tests**:
    ```sh
    pytest
    ```

### 2. Testing Locally with Docker

You can also test your Lambda function's container image locally.

1.  **Build the Docker Image**:
    ```sh
    docker build -t lambda-boilerplate-test .
    ```

2.  **Run the Container with a Test Event**:
    This command runs the container and sends the content of `test_event.json` as the event payload to your handler.
    ```sh
    # Windows (PowerShell)
    docker run --rm -v "${PWD}/test_event.json:/event.json:ro" lambda-boilerplate-test "src.app.handler" (Get-Content -Raw /event.json)

    # macOS / Linux
    docker run --rm -v "$(pwd)/test_event.json:/event.json:ro" lambda-boilerplate-test 'src.app.handler' "$(cat /event.json)"
    ```

---

## Deployment to AWS

Use the AWS SAM CLI to build and deploy the application.

```sh
sam build
sam deploy --guided
```

---

## Project Structure Explained

```
.
├── src/
│   ├── app.py                  # Main Lambda handler (entry point)
│   ├── core/                   # Core configuration (settings, logging)
│   # ... etc.
├── tests/
│   └── test_handler.py         # Unit tests for the Lambda handler
├── .dockerignore               # Excludes unnecessary files from the Docker image
├── Dockerfile                  # For containerizing the Lambda function
├── pyproject.toml
├── template.yaml               # AWS SAM template
├── test_event.json             # Sample event for local testing
└── README.md
```
