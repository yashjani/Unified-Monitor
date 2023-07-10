########################
# Builder – Python bits
FROM python:3.12-slim AS builder
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --user -r requirements.txt
COPY app/        /build/app
COPY exporters/  /build/exporters

########################
# Final image
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
# ---- system & s6-overlay ----
# RUN apt-get update && apt-get install -y curl ca-certificates && \
#     curl -L https://github.com/just-containers/s6-overlay/releases/download/v3.1.5.0/s6-overlay-amd64.tar.gz \
#       | tar xzf - -C /  

ARG S6_OVERLAY_VERSION=3.2.1.0

# Install necessary packages
RUN apt-get update && apt-get install -y curl xz-utils

# Download and extract s6-overlay
RUN curl -L -o /tmp/s6-overlay-noarch.tar.xz https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz && \
    curl -L -o /tmp/s6-overlay-x86_64.tar.xz https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz


# ---- install binaries ----
# Prometheus 2.53.4 (LTS) :contentReference[oaicite:0]{index=0}
RUN curl -L https://github.com/prometheus/prometheus/releases/download/v2.53.4/prometheus-2.53.4.linux-amd64.tar.gz \
      | tar xzf - -C /opt && mv /opt/prometheus-* /opt/prometheus
# Alertmanager 0.27.0
RUN curl -L https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz \
      | tar xzf - -C /opt && mv /opt/alertmanager-* /opt/alertmanager
# Grafana 12.0.0 :contentReference[oaicite:1]{index=1}
RUN curl -L https://dl.grafana.com/oss/release/grafana_12.0.0_amd64.deb -o /tmp/g.deb && \
    apt-get install -y /tmp/g.deb
# Loki 3.3.4 :contentReference[oaicite:2]{index=2}
RUN curl -L https://github.com/grafana/loki/releases/download/v3.3.4/loki-linux-amd64.zip -o /tmp/loki.zip && \
    apt-get install -y unzip && unzip /tmp/loki.zip -d /opt && mv /opt/loki-linux-amd64 /opt/loki
# Promtail 3.3.4
RUN curl -L https://github.com/grafana/loki/releases/download/v3.3.4/promtail-linux-amd64.zip -o /tmp/promtail.zip && \
    unzip /tmp/promtail.zip -d /opt && mv /opt/promtail-linux-amd64 /opt/promtail
# cAdvisor v0.52.1 :contentReference[oaicite:3]{index=3}
RUN curl -L https://github.com/google/cadvisor/releases/download/v0.52.1/cadvisor-v0.52.1-linux-amd64 -o /opt/cadvisor && \
    chmod +x /opt/cadvisor

# ---- copy python wheels & code ----
COPY --from=builder /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"
COPY --from=builder /build /srv

# ---- configs ----
COPY conf/prometheus.yml      /etc/prometheus/
COPY conf/alertmanager.yml    /etc/alertmanager/
COPY conf/loki.yml            /etc/loki/
COPY conf/promtail.yml        /etc/promtail/
COPY conf/grafana/            /etc/grafana/provisioning/
COPY entrypoint.sh            /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ---- s6 service definitions ----
COPY <<'EOF' /etc/services.d/api/run
#!/command/execlineb -P
with-contenv
cd /srv/app
gunicorn -b 0.0.0.0:8000 main:app
EOF
COPY <<'EOF' /etc/services.d/exporter/run
#!/command/execlineb -P
with-contenv
python /srv/exporters/generic_exporter.py
EOF
COPY <<'EOF' /etc/services.d/prometheus/run
#!/command/execlineb -P
with-contenv
/opt/prometheus/prometheus --config.file=/etc/prometheus/prometheus.yml
EOF
COPY <<'EOF' /etc/services.d/alertmanager/run
#!/command/execlineb -P
with-contenv
/opt/alertmanager/alertmanager --config.file=/etc/alertmanager/alertmanager.yml
EOF
COPY <<'EOF' /etc/services.d/loki/run
#!/command/execlineb -P
with-contenv
/opt/loki -config.file=/etc/loki/loki.yml
EOF
COPY <<'EOF' /etc/services.d/promtail/run
#!/command/execlineb -P
with-contenv
/opt/promtail -config.file=/etc/promtail/promtail.yml
EOF
COPY <<'EOF' /etc/services.d/cadvisor/run
#!/command/execlineb -P
with-contenv
/opt/cadvisor --docker_only --port=8080
EOF
COPY <<'EOF' /etc/services.d/grafana/run
#!/command/execlineb -P
with-contenv
grafana-server -homepath /usr/share/grafana
EOF

RUN chmod +x /etc/services.d/*/run

EXPOSE 3000 9090 9093 3100 9080 8080 8000 9102
ENTRYPOINT ["/entrypoint.sh"]
