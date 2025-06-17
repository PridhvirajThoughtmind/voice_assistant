# Start the server
PORT=${BACKEND_PORT:-8000}
exec uvicorn app.main:app --reload --host 0.0.0.0 --port $PORT --reload-dir /app