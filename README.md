# FastAPI Production Boilerplate

This is a production-ready boilerplate for creating robust and observable FastAPI applications. It is built with modern, high-performance tooling like `uv` and includes pre-configured, integrated logging and distributed tracing out-of-the-box.

## Core Features

- **High-Speed Tooling**: Uses `uv` for dependency management, virtual environments, and running the server.
- **Structured, Production-Ready Logging**: Configured with `loguru` for clear, colorized, and structured (JSON-optional) logging. It automatically intercepts logs from all standard libraries like Uvicorn.
- **Integrated Distributed Tracing**: Uses **OpenTelemetry** to automatically trace all incoming requests, providing deep insights into application performance.
- **Automatic Log & Trace Correlation**: This is the key feature. Every log message is automatically enriched with the `trace_id` and `span_id` of the request that generated it. This allows you to instantly pivot from a specific log entry to the full request trace in an observability platform.
- **Centralized Configuration**: Uses `pydantic-settings` to manage all settings via environment variables, with a clear `.env.example` file.
- **Asynchronous by Default**: All API and service layers are `async`, leveraging the full power of FastAPI.
- **Clean, Scalable Structure**: Code is logically organized into `api` and `core` directories to support future growth.

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
2023-10-27 10:30:00.123 | INFO     | app.api.routes:health_check:21 | trace_id=0x... | span_id=0x... | Health check endpoint was called.
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
    Navigate to the `fastapi_base_code_setup` directory and create a virtual environment with `uv`.
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

### Visualizing Traces with Jaeger (Optional)

To see the distributed traces in a UI, you can run Jaeger, a popular open-source tracing tool.

1.  **Run Jaeger with Docker**:
    This command will download and run the "all-in-one" Jaeger container.
    ```sh
    docker run -d --name jaeger -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one:latest
    ```
2.  **Configure the Exporter Endpoint**:
    In your `.env` file, set the endpoint URL:
    ```
    OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
    ```
3.  **Restart the App**:
    Stop and restart the FastAPI server. It will now send traces to Jaeger.
4.  **View Traces**:
    Open the Jaeger UI in your browser at `http://localhost:16686`. You should see your service (`fastapi-boilerplate`) in the "Service" dropdown.

---

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Application configuration
│   │   ├── logging_config.py   # Loguru setup and log/trace correlation
│   │   └── tracing_config.py   # OpenTelemetry setup
│   └── main.py                 # Main FastAPI app & server entrypoint
├── .env.example
├── pyproject.toml
└── README.md
```