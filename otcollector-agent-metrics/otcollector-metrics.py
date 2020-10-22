import os
import time

from opentelemetry import metrics
from opentelemetry.exporter.otlp.metrics_exporter import OTLPMetricsExporter
# from opentelemetry.exporter.opencensus.metrics_exporter import OpenCensusMetricsExporter
from opentelemetry.sdk.metrics import Counter, MeterProvider, ValueObserver
from opentelemetry.sdk.metrics.export.controller import PushController


# get endpoint from env variable
endpoint = os.getenv('OTEL_ENDPOINT', 'localhost:55680')

# create the OLTP Metrics exporter
metric_exporter = OTLPMetricsExporter(
    endpoint=endpoint,
    # optional:
    # endpoint="myCollectorUrl:55678",
    # service_name="test_service",
    # host_name="machine/container name",
)

# metric_exporter = OpenCensusMetricsExporter(
#     # endpoint="localhost:55680"
#     # optional:
#     # endpoint="myCollectorUrl:55678",
#     # service_name="test_service",
#     # host_name="machine/container name",
# )

# Meter is responsible for creating and recording metrics
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
# meter = metrics.get_meter(__name__, True)
# controller collects metrics created from meter and exports it via the
# exporter every interval
controller = PushController(meter, metric_exporter, 5)

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
