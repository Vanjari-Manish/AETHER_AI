import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Initialize logging before anything else
import app.core.logging  # noqa: F401 — triggers log handlers setup

from app.config.settings import settings
from app.database.init_db import init_db
from app.database.connection import dispose_engine
from app.core.exceptions import GPOException, RecordNotFoundError, DuplicateKeyError, ConstraintViolationError
from app.core.response import send_error

# Import routers
from app.routers import auth, users, grid_assets, policies, incidents
from app.routers import notifications, reports, audit_logs, system_settings, health, digital_twin
from app.routers import substations, buses, transmission_lines, transformers, generators, loads, switches

logger = logging.getLogger("gpo.api")
perf_logger = logging.getLogger("gpo.performance")

# ──────────────────────────────────────────────────────────
# Lifespan Handler (startup + shutdown)
# ──────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info("GPO API Gateway starting up...")
    try:
        init_db()
        logger.info("Database initialized and seeded successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    yield
    # --- Shutdown ---
    logger.info("GPO API Gateway shutting down...")
    dispose_engine()
    logger.info("Database connections disposed.")


# ──────────────────────────────────────────────────────────
# FastAPI Application Factory
# ──────────────────────────────────────────────────────────
app = FastAPI(
    title="Grid Policy Orchestrator (GPO) API Gateway",
    description="Enterprise Decision Intelligence Platform Backend",
    version="1.3.0-ALPHA",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# ──────────────────────────────────────────────────────────
# CORS Middleware
# ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────────────────
# Performance Logging Middleware
# ──────────────────────────────────────────────────────────
@app.middleware("http")
async def log_request_performance(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    perf_logger.info(
        f"{request.method} {request.url.path} → {response.status_code} [{duration_ms}ms]"
    )
    response.headers["X-Response-Time"] = f"{duration_ms}ms"
    return response


# ──────────────────────────────────────────────────────────
# Global Exception Handlers
# ──────────────────────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    details = [
        {"field": ".".join(str(l) for l in e.get("loc", [])), "message": e.get("msg", "")}
        for e in errors
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=send_error("ERR.VAL-SCHEMA", "Request validation failed.", details),
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    code_map = {
        400: "ERR.VAL-LIMIT",
        401: "ERR.AUTH-EXPIRED",
        403: "ERR.AUTHZ-PERM",
        404: "ERR.RES-NOT-FOUND",
        409: "ERR.RES-CONFLICT",
        422: "ERR.VAL-SCHEMA",
        500: "ERR.SYS-INTERNAL",
    }
    error_code = code_map.get(exc.status_code, "ERR.SYS-UNKNOWN")
    return JSONResponse(
        status_code=exc.status_code,
        content=send_error(error_code, exc.detail),
    )

@app.exception_handler(RecordNotFoundError)
async def record_not_found_handler(request: Request, exc: RecordNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=send_error("ERR.RES-NOT-FOUND", exc.message, exc.details),
    )

@app.exception_handler(DuplicateKeyError)
async def duplicate_key_handler(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=send_error("ERR.RES-CONFLICT", exc.message, exc.details),
    )

@app.exception_handler(ConstraintViolationError)
async def constraint_violation_handler(request: Request, exc: ConstraintViolationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=send_error("ERR.VAL-CONSTRAINT", exc.message, exc.details),
    )

@app.exception_handler(GPOException)
async def gpo_exception_handler(request: Request, exc: GPOException):
    logging.getLogger("gpo.error").error(f"GPOException: {exc.message} | {exc.details}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=send_error("ERR.SYS-DATABASE-DOWN", exc.message, exc.details),
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logging.getLogger("gpo.error").exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=send_error("ERR.SYS-INTERNAL", "An unexpected internal error occurred."),
    )


# ──────────────────────────────────────────────────────────
# Router Registration — Versioned API (v1)
# ──────────────────────────────────────────────────────────
app.include_router(auth.router,            prefix="/api/v1/auth",            tags=["Authentication"])
app.include_router(users.router,           prefix="/api/v1/users",           tags=["Users"])
app.include_router(grid_assets.router,     prefix="/api/v1/grid-assets",     tags=["Grid Assets"])
app.include_router(policies.router,        prefix="/api/v1/policies",        tags=["Policies"])
app.include_router(incidents.router,       prefix="/api/v1/incidents",       tags=["Incidents"])
app.include_router(notifications.router,   prefix="/api/v1/notifications",   tags=["Notifications"])
app.include_router(reports.router,         prefix="/api/v1/reports",         tags=["Reports"])
app.include_router(audit_logs.router,      prefix="/api/v1/audit-logs",      tags=["Audit Logs"])
app.include_router(system_settings.router, prefix="/api/v1/settings",        tags=["System Settings"])
app.include_router(health.router,          prefix="/api/v1/health",          tags=["Health"])
app.include_router(digital_twin.router,    prefix="/api/v1/digital-twin",    tags=["Digital Twin"])

# Phase 3.2 — Digital Twin Asset CRUD APIs
app.include_router(substations.router,        prefix="/api/v1/substations",        tags=["Substations"])
app.include_router(buses.router,              prefix="/api/v1/buses",              tags=["Buses"])
app.include_router(transmission_lines.router, prefix="/api/v1/transmission-lines", tags=["Transmission Lines"])
app.include_router(transformers.router,       prefix="/api/v1/transformers",       tags=["Transformers"])
app.include_router(generators.router,         prefix="/api/v1/generators",         tags=["Generators"])
app.include_router(loads.router,              prefix="/api/v1/loads",              tags=["Loads"])
app.include_router(switches.router,           prefix="/api/v1/switches",           tags=["Switches"])

# ──────────────────────────────────────────────────────────
# Backward-Compatible Routes (Frontend currently uses /api/auth/*)
# ──────────────────────────────────────────────────────────
app.include_router(auth.router,   prefix="/api/auth",   tags=["Authentication (Legacy)"])
app.include_router(health.router, prefix="/api/health", tags=["Health (Legacy)"])
