import os
import time

from opentelemetry import metrics
from opentelemetry import trace
# from opentelemetry.exporter.otlp.metrics_exporter import OTLPMetricsExporter
from opentelemetry.exporter.opencensus.metrics_exporter import OpenCensusMetricsExporter
from opentelemetry.exporter.opencensus.trace_exporter import OpenCensusSpanExporter
from opentelemetry.sdk.metrics import Counter, MeterProvider, ValueRecorder, ValueObserver
from opentelemetry.sdk.metrics.export.controller import PushController


# get endpoint from env variable
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

endpoint = os.getenv('OTEL_ENDPOINT', 'localhost:55678')

# create the OLTP Metrics exporter
# metric_exporter = OTLPMetricsExporter(
#     endpoint=endpoint,
#     # optional:
#     # endpoint="myCollectorUrl:55678",
#     # service_name="test_service",
#     # host_name="machine/container name",
# )

metric_exporter = OpenCensusMetricsExporter(
    endpoint=endpoint,
    # endpoint="localhost:55680"
    # optional:
    # endpoint="myCollectorUrl:55678",
    # service_name="test_service",
    # host_name="machine/container name",
)

# Meter is responsible for creating and recording metrics
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
# meter = metrics.get_meter(__name__, True)
# controller collects metrics created from meter and exports it via the
# exporter every interval
controller = PushController(meter, metric_exporter, 5)


trace.set_tracer_provider(TracerProvider())
trace_exporter = OpenCensusSpanExporter(
    endpoint=endpoint,
    service_name='otel-app'
)
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(trace_exporter)
)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("foo"):
    with tracer.start_as_current_span("bar"):
        with tracer.start_as_current_span("baz"):
            print("Hello world from OpenTelemetry Python!")


print('Started otcollector-agent-opencensus metrics ...')

requests_counter = meter.create_metric(
    name="requests",
    description="number of requests",
    unit="1",
    value_type=int,
    metric_type=Counter
)

# Labels are used to identify key-values that are associated with a specific
# metric that you want to record. These are useful for pre-aggregation and can
# be used to store custom dimensions pertaining to a metric
labels = {"environment": "staging"}
requests_counter.add(25, labels)

print('Added counter')

# size_recorder = meter.create_metric(
#     name="size",
#     description="current size",
#     unit="1",
#     value_type=float,
#     metric_type=ValueRecorder
# )
#
# size_recorder.record(15.0, labels)


# def get_value_callback(observer):
#     observer.observe(15.0, {"cpu_number": '10'})
#
#
# meter.register_observer(
#     callback=get_value_callback,
#     name="get_value ",
#     description="test value",
#     unit="1",
#     value_type=float,
#     observer_type=ValueObserver,
# )

time.sleep(10000)  # give push_controller time to push metrics
