# Monorepo for Production-Ready Python Boilerplates

This repository contains two distinct, production-grade boilerplates for common Python application patterns: a FastAPI web service and an AWS Lambda function.

Both projects are built with modern tooling and share a common philosophy of robust logging, configuration, and scalability.

---

## 1. FastAPI Production Boilerplate (`fastapi-boilerplate/`)

This is a comprehensive, production-ready boilerplate for creating robust and observable FastAPI applications. It is built with modern, high-performance tooling like `uv` and includes pre-configured, integrated logging and distributed tracing out-of-the-box.

### Core Features:

- **High-Speed Tooling**: Uses `uv` for dependency management and task running.
- **Structured Logging**: Configured with `loguru` for clear, structured (JSON-optional) logging.
- **Integrated Distributed Tracing**: Uses **OpenTelemetry** to automatically trace all incoming requests.
- **Log & Trace Correlation**: Every log message is automatically enriched with the `trace_id` and `span_id` of the request that generated it.
- **Clean, Scalable Structure**: Code is logically organized into a scalable structure:
    - `app/api`: API endpoints (routing layer).
    - `app/services`: Core business logic.
    - `app/types`: Pydantic schemas for data validation.
    - `app/functions`: Discrete, single-purpose business functions.
    - `app/utils`: Shared utility functions.
    - `app/core`: Cross-cutting concerns like config and logging.

### Getting Started

For detailed setup and usage instructions, please refer to the README inside the directory:
[**`fastapi-boilerplate/README.md`**](./fastapi-boilerplate/README.md)

---

## 2. AWS Lambda Production Boilerplate (`lambda_boilerplate/`)

This is a production-ready boilerplate for creating robust and observable AWS Lambda functions in Python. It is designed for clarity, maintainability, and easy deployment using the AWS SAM CLI.

### Core Features:

- **Structured Logging**: Pre-configured with `loguru`.
- **Automatic Log Correlation**: Every log message is automatically enriched with the `aws_request_id` for easy debugging in CloudWatch.
- **Centralized Configuration**: Uses `pydantic-settings` to manage settings via environment variables.
- **Infrastructure as Code**: Comes with a `template.yaml` for easy and repeatable deployments with AWS SAM.

### Getting Started

For detailed setup and deployment instructions, please refer to the README inside the directory:
[**`lambda_boilerplate/README.md`**](./lambda_boilerplate/README.md)

---

This monorepo structure allows for shared development practices and tooling while keeping the individual projects decoupled.
