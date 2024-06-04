#!/bin/sh


echo "Starting FastAPI server"
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
echo "FastAPI server started"