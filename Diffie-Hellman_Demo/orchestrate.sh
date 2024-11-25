#!/bin/sh

echo "Starting machine3 (MITM relay)..."
python /app/machine3/main.py &

sleep 2  # Allow machine3 to initialize

echo "Starting machine2..."
python /app/machine2/main.py &

sleep 2  # Allow machine2 to initialize

echo "Starting machine1..."
python /app/machine1/main.py
