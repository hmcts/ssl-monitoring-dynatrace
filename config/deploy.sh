#!/bin/bash
MAC_VERSION="v1.5.0"
MONACO_DOWNLOAD_URL="https://github.com/dynatrace-oss/dynatrace-monitoring-as-code/releases/download/$MAC_VERSION/monaco-linux-amd64"
curl -SL $MONACO_DOWNLOAD_URL -o /usr/bin/monaco
chmod +x /usr/bin/monaco

monaco deploy --environments="dynatrace-environments.yaml" -p nonprod --continue-on-error=true