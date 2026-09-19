from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings
from app.config.logging import setup_logging
from app.api.errors import MargDarshakException, margdarshak_exception_handler
from app.api.health import router as health_router
from app.api.profile import router as profile_router
from app.api.ontology import router as ontology_router
from app.api.job import router as job_router
from app.api.matching import router as matching_router
from app.api.gap import router as gap_router

settings = get_settings()
logger = setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(MargDarshakException, margdarshak_exception_handler)

# Routers
app.include_router(health_router, prefix="/api")
app.include_router(profile_router, prefix="/api/profile", tags=["profile"])
app.include_router(ontology_router, prefix="/api/ontology", tags=["ontology"])
app.include_router(job_router, prefix="/api/job", tags=["job"])
app.include_router(matching_router, prefix="/api/match", tags=["matching"])
app.include_router(gap_router, prefix="/api/gap", tags=["gap"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting MargDarshak API...")

@app.get("/")
async def root():
    return {"message": "Welcome to MargDarshak API"}





