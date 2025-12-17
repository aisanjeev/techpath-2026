"""Main API v1 router."""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, services, blog, contact, ai, case_studies

router = APIRouter()

# Include all endpoint routers
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(services.router, prefix="/services", tags=["Services"])
router.include_router(blog.router, prefix="/blog", tags=["Blog"])
router.include_router(case_studies.router, prefix="/case-studies", tags=["Case Studies"])
router.include_router(contact.router, prefix="/contact", tags=["Contact"])
router.include_router(ai.router, prefix="/ai", tags=["AI"])

