#!/bin/sh


echo "Starting FastAPI server"
exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
echo "FastAPI server started"