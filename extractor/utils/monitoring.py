from prometheus_client import start_http_server, Counter, Gauge

EXTRACTION_SUCCESS = Counter(
    'extraction_success_total',
    'Successful data extractions'
)

EXTRACTION_FAILURE = Counter(
    'extraction_failure_total',
    'Failed data extractions',
    ['source']
)

def start_monitoring(port=8000):
    start_http_server(port)