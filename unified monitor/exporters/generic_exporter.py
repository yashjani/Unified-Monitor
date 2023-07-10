#!/usr/bin/env python3
"""
Simple exporter that fakes business metrics.

Exposes:
  • items_open_total
  • items_avg_value_usd
"""
import time, random
from prometheus_client import start_http_server, Gauge, Counter

OPEN   = Gauge("items_open_total",    "Open items")
AVGVAL = Gauge("items_avg_value_usd", "Average item value (USD)")
ERRORS = Counter("exporter_errors_total", "Errors")

def poll():
    while True:
        try:
            OPEN.set(random.randint(40, 150))
            AVGVAL.set(round(random.uniform(9_000, 25_000), 2))
        except Exception:
            ERRORS.inc()
        time.sleep(30)

if __name__ == "__main__":
    start_http_server(9102)
    poll()
