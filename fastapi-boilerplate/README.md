# FastAPI Production Boilerplate

This is a production-ready boilerplate for creating robust and observable FastAPI applications. It is built with modern, high-performance tooling like `uv` and includes pre-configured, integrated logging and distributed tracing out-of-the-box.

## Core Features

- **High-Speed Tooling**: Uses `uv` for dependency management, virtual environments, and running the server.
- **Structured, Production-Ready Logging**: Configured with `loguru` for clear, colorized, and structured (JSON-optional) logging. It automatically intercepts logs from all standard libraries like Uvicorn.
- **Integrated Distributed Tracing**: Uses **OpenTelemetry** to automatically trace all incoming requests, providing deep insights into application performance.
- **Automatic Log & Trace Correlation**: Every log message is automatically enriched with the `trace_id` and `span_id` of the request that generated it. This allows you to instantly pivot from a specific log entry to the full request trace in an observability platform.
- **Centralized Configuration**: Uses `pydantic-settings` to manage all settings via environment variables, with a clear `.env.example` file.
- **Asynchronous by Default**: All API and service layers are `async`, leveraging the full power of FastAPI.
- **Clean, Scalable Structure**: Code is logically organized into `api`, `core`, `services`, `types`, and other packages to support future growth.

---

## Observability: Logging & Tracing Explained

This boilerplate is built on the principle that good observability is not an afterthought. The logging and tracing systems are designed to work together seamlessly.

### How It Works

1.  **Request Starts**: When a request hits the FastAPI app, the **OpenTelemetry Middleware** intercepts it and starts a new trace with a unique `trace_id`.
2.  **Logs Are Captured**: As your code executes (e.g., in an endpoint like `/api/health`), any call to `logger.info(...)` is processed.
3.  **Context is Injected**: Our custom `loguru` configuration automatically inspects the current OpenTelemetry context, finds the active `trace_id` and `span_id`, and injects them into the log record.
4.  **Unified Output**: The final log message, printed to your console or sent to a logging service, contains these IDs.

This creates a powerful link between your application's two most important observability signals.

**Example Log Output:**
When you call the `/api/health` endpoint, you will see a log message in your console like this:
```
2023-10-27 10:30:00.123 | INFO     | app.api.routes:health_check:16 | trace_id=0x... | span_id=0x... | Health check endpoint was called.
```
You can take that `trace_id`, search for it in a tracing tool like Jaeger, and see the entire request lifecycle.

---

## Getting Started

### Prerequisites

1.  **Install `uv`**:
    If you don't have `uv` installed, follow the official instructions:
    ```sh
    # macOS / Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Windows
    irm https://astral.sh/uv/install.ps1 | iex
    ```

### Setup and Running the App

1.  **Create a Virtual Environment**:
    Navigate to the `fastapi_boilerplate` directory and create a virtual environment with `uv`.
    ```sh
    uv venv
    ```

2.  **Activate the Environment**:
    ```sh
    # macOS / Linux
    source .venv/bin/activate

    # Windows
    .venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    Install the project dependencies using `uv`. The `-e .` installs the project in "editable" mode.
    ```sh
    uv pip install -e .
    ```

4.  **Configure Environment**:
    Copy the example environment file.
    ```sh
    cp .env.example .env
    ```

5.  **Run the Application**:
    You now have two scripts to run the server, defined in `pyproject.toml`.

    **For Development (with auto-reload):**
    ```sh
    uv run start_dev
    ```

    **For Production (multi-worker, no auto-reload):**
    ```sh
    uv run start_prod
    ```
    The API will be available at `http://127.0.0.1:8000`.

---

## Project Structure Explained

This boilerplate uses a clean, scalable architecture that separates concerns into different packages.

```
.
├── app/
│   ├── api/
│   │   └── routes.py           # Handles HTTP routing and I/O. Delegates logic to services.
│   ├── core/
│   │   ├── config.py           # Application configuration from environment variables.
│   │   ├── logging_config.py   # Loguru setup and trace correlation.
│   │   └── tracing_config.py   # OpenTelemetry setup.
│   ├── functions/
│   │   └── data_validation.py  # Example of a discrete, reusable business function.
│   ├── services/
│   │   └── health_service.py   # Encapsulates core business logic.
│   ├── types/
│   │   └── health.py           # Pydantic schemas for API request/response models.
│   ├── utils/
│   │   └── formatters.py       # Shared, stateless utility functions.
│   └── main.py                 # Main FastAPI app, middleware, and entrypoint.
├── .env.example
├── pyproject.toml
└── README.md
```

### Role of Each Directory:

*   **`app/api`**: The API Layer. Its only job is to define API routes (`@api_router.get(...)`), handle request validation (via types), and return HTTP responses. It calls the `services` layer to perform the actual work.
*   **`app/services`**: The Service Layer. This is where the core business logic of your application lives. Services can call functions from the `functions` package and use helpers from `utils`.
*   **`app/types`**: Pydantic Models. Defines the data shapes for your API. Used for request and response validation, and automatically generates OpenAPI schema.
*   **`app/functions`**: Business Functions. Contains small, single-purpose functions that encapsulate a specific piece of business logic (e.g., `is_valid_username`). These can be composed together in the service layer.
*   **`app/utils`**: Utility Helpers. Contains generic, reusable functions that are not tied to business logic (e.g., `format_timestamp_to_iso`).
*   **`app/core`**: Core Configuration. Manages the foundational aspects of the application, such as configuration, logging, and tracing.
*   **`app/main.py`**: The Application Entrypoint. Initializes the FastAPI app, sets up middleware, includes the API router, and defines the server runners.
