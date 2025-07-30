import sys
import logging
from loguru import logger
from .config import settings
from opentelemetry import trace


class InterceptHandler(logging.Handler):
    """
    Intercepts standard logging messages and redirects them to Loguru.
    This handler is part of the setup to make Loguru the primary logger.
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 0
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def trace_context_processor(record):
    """
    Loguru processor to add OpenTelemetry trace and span IDs to the log record.
    """
    span = trace.get_current_span()
    if span.get_span_context().is_valid:
        ctx = span.get_span_context()
        record["extra"]["trace_id"] = f"0x{ctx.trace_id:032x}"
        record["extra"]["span_id"] = f"0x{ctx.span_id:016x}"
    else:
        # Use setdefault to avoid KeyError in format string if keys don't exist
        record["extra"].setdefault("trace_id", "N/A")
        record["extra"].setdefault("span_id", "N/A")


def configure_logging():
    """
    Configures the Loguru logger to be the primary logger for the application,
    intercepting standard library logging calls, and enriching logs with
    OpenTelemetry trace context.
    """
    # Remove any default handlers and reconfigure
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL.upper(),
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<yellow>trace_id={extra[trace_id]}</yellow> | <yellow>span_id={extra[span_id]}</yellow> | "
            "<level>{message}</level>"
        ),
        colorize=True,
        serialize=settings.LOGURU_JSON_LOGS,
    )

    # Add processor for OpenTelemetry context. This is more efficient and thread-safe.
    logger.configure(patcher=trace_context_processor)

    # Intercept standard logging messages toward your configured loguru sinks
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.info("Logging configured successfully.")