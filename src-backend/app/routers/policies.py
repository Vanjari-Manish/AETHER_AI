from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.repositories.grid_repository import PolicyRepository, PolicyVersionRepository, PolicyExecutionRepository
from app.schemas.grid_schemas import (
    PolicyCreate, PolicyResponse, 
    PolicyVersionCreate, PolicyVersionResponse,
    PolicyExecutionCreate, PolicyExecutionResponse
)
from app.core.security import PermissionGuard, get_current_user
from app.core.response import send_success
from app.models.auth_models import User

router = APIRouter()

# --- Policies CRUD ---
@router.get("", response_model=dict)
def list_policies(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionGuard("policies:view"))
):
    repo = PolicyRepository(db)
    result = repo.get_page(
        page=page,
        page_size=limit,
        search_query=search,
        search_columns=["name", "description"]
    )
    records = [PolicyResponse.model_validate(r) for r in result["records"]]
    meta = {
        "page": result["page"],
        "limit": result["page_size"],
        "totalCount": result["total_records"],
        "totalPages": result["total_pages"]
    }
    return send_success([r.model_dump() for r in records], meta=meta)

@router.get("/{policy_id}", response_model=dict)
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionGuard("policies:view"))
):
    repo = PolicyRepository(db)
    policy = repo.get(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found.")
    return send_success(PolicyResponse.model_validate(policy).model_dump())

@router.post("", response_model=dict)
def create_policy(
    req: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionGuard("policies:compile"))
):
    repo = PolicyRepository(db)
    # Check if duplicate name
    if repo.get_by_name(req.name):
        raise HTTPException(status_code=400, detail="A policy with this name already exists.")
        
    data = req.model_dump()
    data["created_by"] = current_user.id
    data["status"] = "active"
    try:
        new_policy = repo.create(data)
        return send_success(PolicyResponse.model_validate(new_policy).model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{policy_id}", response_model=dict)
def delete_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionGuard("policies:compile"))
):
    repo = PolicyRepository(db)
    success = repo.delete(policy_id, soft=True)
    return send_success({"success": success})

# --- Policy Versions ---
@router.get("/{policy_id}/versions", response_model=dict)
def get_policy_versions(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionGuard("policies:view"))
):
    repo = PolicyVersionRepository(db)
    versions = repo.get_versions(policy_id)
    records = [PolicyVersionResponse.model_validate(v) for v in versions]
    return send_success([r.model_dump() for r in records])

@router.post("/versions", response_model=dict)
def create_policy_version(
    req: PolicyVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionGuard("policies:compile"))
):
    repo = PolicyVersionRepository(db)
    data = req.model_dump()
    data["created_by"] = current_user.id
    data["status"] = "active"
    try:
        new_version = repo.create(data)
        return send_success(PolicyVersionResponse.model_validate(new_version).model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Policy Executions (compiler runs) ---
@router.get("/versions/{version_id}/executions", response_model=dict)
def get_version_executions(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionGuard("policies:view"))
):
    repo = PolicyExecutionRepository(db)
    executions = repo.get_by_version(version_id)
    records = [PolicyExecutionResponse.model_validate(e) for e in executions]
    return send_success([r.model_dump() for r in records])

@router.post("/executions", response_model=dict)
def record_policy_execution(
    req: PolicyExecutionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionGuard("policies:deploy"))
):
    repo = PolicyExecutionRepository(db)
    data = req.model_dump()
    try:
        new_execution = repo.create(data)
        return send_success(PolicyExecutionResponse.model_validate(new_execution).model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
