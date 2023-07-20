# Unified-Monitor
Unified monitor for Microservice

[![Docker Pulls](https://img.shields.io/docker/pulls/yjani204/unified-monitoring)](https://hub.docker.com/r/yjani204/unified-monitoring)

## Run

Pull the image from Docker Hub:

```bash
docker pull yjani204/unified-monitoring

```

```
docker run -d --name auto-mon \
  -p 3000:3000 \    # Grafana UI
  -p 9090:9090 \    # Prometheus
  -p 9093:9093 \    # Alertmanager
  -p 3100:3100 \    # Loki
  -p 4318:4318 \    # OTLP (traces)
  -p 3200:3200 \    # Tempo
  -p 9100:9100 \    # Node Exporter
  -p 8080:8080 \    # cAdvisor
  -v /var/run/docker.sock:/var/run/docker.sock \
  yjani204/unified-monitoring:latest
```
