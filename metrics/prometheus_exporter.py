import sys
import time

from prometheus_client import start_http_server

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics import Counter, MeterProvider, ValueRecorder
from opentelemetry.sdk.metrics.export.controller import PushController

# Start Prometheus client
start_http_server(port=8000, addr="localhost")

metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
# meter = metrics.get_meter(__name__, True)
exporter = PrometheusMetricsExporter("MyAppPrefix")
controller = PushController(meter, exporter, 5)

staging_labels = {"environment": "staging"}

requests_counter = meter.create_metric(
    name="requests",
    description="number of requests",
    unit="1",
    value_type=int,
    metric_type=Counter,
)

size_recorder = meter.create_metric(
    name="size",
    description="current size",
    unit="1",
    value_type=int,
    metric_type=ValueRecorder,
)

size_recorder.record(3, staging_labels)

requests_counter.add(25, staging_labels)
time.sleep(5)


# This line is added to keep the HTTP server up long enough to scrape.
input("Press any key to exit...")
