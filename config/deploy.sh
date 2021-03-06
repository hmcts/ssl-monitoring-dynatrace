#!/bin/bash
set +e
MAC_VERSION="v1.5.0"
MONACO_DOWNLOAD_URL="https://github.com/dynatrace-oss/dynatrace-monitoring-as-code/releases/download/$MAC_VERSION/monaco-linux-amd64"
sudo curl -SL $MONACO_DOWNLOAD_URL -o /usr/bin/monaco
sudo chmod +x /usr/bin/monaco

function deploy(){
  /usr/bin/monaco deploy --environments "/home/vsts/work/1/s/config/dynatrace-environments.yaml" --project nonprod --continue-on-error="true"
  return 0
}

deploy