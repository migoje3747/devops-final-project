#!/usr/bin/env bash
set -euo pipefail
SONAR_HOST_URL="${SONAR_HOST_URL:-http://localhost:9090}"
SONAR_TOKEN="${SONAR_TOKEN:?SONAR_TOKEN must be set}"
PROJECT_KEY="${1:-devops-lab}"
TIMEOUT=${2:-120}   # seconds
INTERVAL=5
ELAPSED=0

# poll SonarQube for analysis status
while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  # fetch last analysis task status
  resp=$(curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/ce/component?component=${PROJECT_KEY}")
  taskId=$(echo "$resp" | jq -r '.queue[0].id // .current?.id // empty')
  if [ -z "$taskId" ]; then
    # maybe analysis finished; query project status
    status=$(curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${PROJECT_KEY}" | jq -r '.projectStatus.status')
    if [ "$status" = "OK" ]; then
      echo "SonarQube quality gate: OK"
      exit 0
    else
      echo "SonarQube quality gate: ${status}"
      exit 1
    fi
  fi

  # query task status
  task=$(curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/ce/task?id=${taskId}")
  taskStatus=$(echo "$task" | jq -r '.task.status')
  echo "Sonar analysis task ${taskId} status: ${taskStatus}"
  if [ "$taskStatus" = "SUCCESS" ]; then
    status=$(curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${PROJECT_KEY}" | jq -r '.projectStatus.status')
    echo "Quality gate: ${status}"
    if [ "$status" = "OK" ]; then
      exit 0
    else
      exit 1
    fi
  elif [ "$taskStatus" = "FAILED" ] || [ "$taskStatus" = "CANCELED" ]; then
    echo "Sonar analysis task failed."
    exit 1
  fi

  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

echo "Timed out waiting for SonarQube analysis."
exit 1