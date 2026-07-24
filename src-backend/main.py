import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Grid Policy Orchestrator (GPO) API Gateway",
    description="Enterprise Decision Intelligence Platform Backend Shell",
    version="1.3.0-ALPHA"
)

# CORS configuration to connect with Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "GPO API Gateway",
        "version": "1.3.0-ALPHA",
        "environment": "development"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
