# Incident Response OpenEnv

A simple OpenEnv-compatible environment for AI-driven incident diagnosis and recovery.

## Overview
This project simulates a production incident where an agent observes alerts, logs, CPU, memory, and service status, then takes actions to resolve the issue.

## Endpoints
- `POST /reset`
- `POST /step`
- `GET /state`

## Task
- `easy`: service down incident

## Example Action
```json
{
  "action": "restart_service"
}