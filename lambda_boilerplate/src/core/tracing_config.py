from typing import Sequence
from loguru import logger
from opentelemetry import trace
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
    SpanExportResult,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from .config import settings

class NullSpanExporter(SpanExporter):
    """A SpanExporter that does nothing, effectively silencing trace output."""
    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True

def configure_tracing():
    """
    Configures OpenTelemetry for distributed tracing in the Lambda environment.
    """
    resource = Resource(attributes={"service.name": settings.OTEL_SERVICE_NAME})
    provider = TracerProvider(resource=resource)

    exporter: SpanExporter
    if settings.OTEL_EXPORTER_OTLP_ENDPOINT:
        exporter = OTLPSpanExporter(
            endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True
        )
        log_message = f"OpenTelemetry configured with OTLP exporter to {settings.OTEL_EXPORTER_OTLP_ENDPOINT}"
    elif settings.OTEL_DEBUG_LOG_SPANS:
        exporter = ConsoleSpanExporter()
        log_message = "OpenTelemetry configured with ConsoleSpanExporter. Traces will be printed to the console."
    else:
        exporter = NullSpanExporter()
        log_message = "OpenTelemetry tracing is active. Spans are not being exported."

    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    logger.info(log_message)
