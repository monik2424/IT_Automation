#!/bin/bash

# Load environment variables from .env
export $(grep -v '^#' .env | xargs)

echo "Starting Auto-Ops System..."

# Start FastAPI in background
echo "[1/4] Starting API server..."
uvicorn api.main:app --reload &
API_PID=$!
sleep 2  # Give the API time to start before others connect

# Start alert generator in background
echo "[2/4] Starting alert generator..."
python api/alert_generator.py &
ALERT_PID=$!

# Start remediation agent in background
echo "[3/4] Starting remediation agent..."
python remediation/agent.py &
AGENT_PID=$!

# Start dashboard in background
echo "[4/4] Starting dashboard..."
streamlit run dashboard/app.py &
DASH_PID=$!

echo ""
echo "All systems running:"
echo "  API:        http://localhost:8000"
echo "  API Docs:   http://localhost:8000/docs"
echo "  Dashboard:  http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop everything."

# When you press Ctrl+C, kill all 4 processes cleanly
trap "echo 'Shutting down...'; kill $API_PID $ALERT_PID $AGENT_PID $DASH_PID; exit" SIGINT

# Keep script alive so Ctrl+C works
wait