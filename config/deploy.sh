#!/bin/bash
set -e
monaco deploy --environments="dynatrace-environments.yaml" -p nonprod --continue-on-error=true