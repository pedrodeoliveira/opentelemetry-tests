import uvicorn
from fastapi import FastAPI
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export.controller import PushController
from starlette_exporter import PrometheusMiddleware, handle_metrics

app = FastAPI()
app_name = 'api'
app.add_middleware(PrometheusMiddleware, app_name=app_name)
app.add_route("/metrics", handle_metrics)

metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
exporter = PrometheusMetricsExporter(app_name)
controller = PushController(meter, exporter, 5)

staging_labels = {"environment": "staging"}

requests_counter = meter.create_metric(
    name="requests",
    description="number of requests",
    unit="1",
    value_type=int,
    metric_type=Counter,
    label_keys=("environment",),
)


@app.get("/")
async def predictions():
    requests_counter.add(5, staging_labels)
    return "hello"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
