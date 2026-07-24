import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
import models
import auth
from database import engine, get_db
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Initialize database schema tables dynamically on startup
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[GPO-DB] Warning: Table creation deferred. Ensure MySQL server is online: {e}")

app = FastAPI(
    title="Grid Policy Orchestrator (GPO) API Gateway",
    description="Enterprise Decision Intelligence Platform Backend Shell",
    version="1.3.0-ALPHA"
)

# CORS configuration to connect with Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    organization: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/auth/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # Check if user email is already registered
    existing_user = db.query(models.User).filter(models.User.email == req.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already registered."
        )
    
    # Create new user row with password hashing
    hashed_pwd = auth.get_password_hash(req.password)
    new_user = models.User(
        email=req.email,
        password_hash=hashed_pwd,
        full_name=req.full_name,
        organization=req.organization,
        role="Viewer" # Default role
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as db_err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database insertion failed: {str(db_err)}"
        )
    
    # Return user details
    return {
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "organization": new_user.organization,
        "role": new_user.role,
    }

@app.post("/api/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not auth.verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
    
    # Create access token
    token_data = {"sub": user.email, "id": user.id, "role": user.role}
    access_token = auth.create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "organization": user.organization,
            "role": user.role
        }
    }

security = HTTPBearer()

@app.get("/api/auth/me")
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session has expired. Please sign in again."
        )
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token."
        )
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found."
        )
        
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "organization": user.organization,
        "role": user.role
    }

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
