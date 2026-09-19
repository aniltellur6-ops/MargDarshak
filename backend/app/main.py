from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import Error Handlers
from app.api.errors import global_exception_handler

# Import Routers
from app.api.profile import router as profile_router
from app.api.job import router as job_router
from app.api.match import router as match_router
from app.api.gap import router as gap_router
from app.api.priority import router as priority_router
from app.api.opportunity import router as opportunity_router
from app.api.course import router as course_router
from app.api.project import router as project_router
from app.api.assessment import router as assessment_router
from app.api.progress import router as progress_router
from app.api.news import router as news_router
from app.api.orchestrator import router as orchestrator_router

load_dotenv()

app = FastAPI(
    title="MargDarshak API",
    description="Core Intelligence API for the MargDarshak Career & Skill-Gap Platform.",
    version="1.0.0",
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Register Global Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)

# Health Check Route
@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "healthy", "version": app.version}

# Include all Feature Routers
app.include_router(profile_router, prefix="/api/profile", tags=["profile"])
app.include_router(job_router, prefix="/api/job", tags=["job"])
app.include_router(match_router, prefix="/api/match", tags=["match"])
app.include_router(gap_router, prefix="/api/gap", tags=["gap"])
app.include_router(priority_router, prefix="/api/priority", tags=["priority"])
app.include_router(opportunity_router, prefix="/api/opportunity", tags=["opportunity"])
app.include_router(course_router, prefix="/api/course", tags=["course"])
app.include_router(project_router, prefix="/api/project", tags=["project"])
app.include_router(assessment_router, prefix="/api/assessment", tags=["assessment"])
app.include_router(progress_router, prefix="/api/progress", tags=["progress"])
app.include_router(news_router, prefix="/api/news", tags=["news"])
app.include_router(orchestrator_router, prefix="/api/orchestrator", tags=["orchestrator"])
