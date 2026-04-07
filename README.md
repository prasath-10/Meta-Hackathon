---
title: incident-response-openenv
emoji: 🚑
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
---

# Incident Response OpenEnv

A simple OpenEnv-compatible environment for AI-driven incident diagnosis and recovery.

## Endpoints
- POST /reset
- POST /step
- GET /state

## Task
- easy: service_down incident

## Run locally
uvicorn server.main:app --reload

## Run with Docker
docker build -t incident-response-openv .
docker run -p 7860:7860 incident-response-openv