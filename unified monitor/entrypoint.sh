#!/usr/bin/env bash
set -e

# patch Alertmanager with runtime Slack webhook
if [[ -n "$SLACK_WEBHOOK" ]]; then
  sed -i "s|\$SLACK_WEBHOOK|$SLACK_WEBHOOK|g" /etc/alertmanager/alertmanager.yml
fi

exec /init   # hand over to s6-overlay
