import uvicorn
from app.main import app

# Grid Policy Orchestrator (GPO) — Entry Point
# Path: src-backend/main.py
# Delegates to app/main.py for full application configuration.

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
