from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import time

from app.config import settings
from app.routes import health, chat, leads, conversations, followups, dashboard, webhooks

app = FastAPI(
    title="PrimeHomes Realty Lead Bot API",
    description="Backend API for the PrimeHomes Realty Real Estate Lead Bot",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


# Routers
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(leads.router, prefix="/api/v1", tags=["Leads"])
app.include_router(conversations.router, prefix="/api/v1", tags=["Conversations"])
app.include_router(followups.router, prefix="/api/v1", tags=["Follow-ups"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(webhooks.router, prefix="/api/v1", tags=["Webhooks"])


@app.get("/")
async def root():
    return {
        "service": "primehomes-api",
        "status": "ok",
        "version": "0.1.0",
        "docs": "/docs",
    }
