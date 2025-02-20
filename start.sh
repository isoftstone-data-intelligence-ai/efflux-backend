#!/bin/bash
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8001 >> /app/app.log 2>&1 &