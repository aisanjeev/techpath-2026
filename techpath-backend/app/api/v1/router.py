"""Main API v1 router."""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    ai,
    auth,
    blog,
    case_studies,
    classroom,
    classroom_ws,
    contact,
    content,
    courses,
    media,
    page,
    pilot_signup,
    secrets,
    services,
    settings,
    student_portal,
    trainer,
    trainer_reports,
    training,
    training_roster,
    uploads,
)


router = APIRouter()

# Include all endpoint routers
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(services.router, prefix="/services", tags=["Services"])
router.include_router(blog.router, prefix="/blog", tags=["Blog"])
router.include_router(page.router, prefix="/pages", tags=["Pages"])
router.include_router(case_studies.router, prefix="/case-studies", tags=["Case Studies"])
router.include_router(courses.router, prefix="/courses", tags=["Courses"])
router.include_router(training.router, prefix="/training", tags=["Training Content"])
router.include_router(training_roster.router, prefix="/training", tags=["Training Roster"])
router.include_router(trainer_reports.router, prefix="/trainer", tags=["Trainer"])
router.include_router(trainer.router, prefix="/trainer", tags=["Trainer"])
router.include_router(classroom.router, prefix="/classroom", tags=["Live Classroom"])
router.include_router(classroom_ws.router, prefix="/ws", tags=["Live Classroom"])
router.include_router(student_portal.router, prefix="/student", tags=["Student Portal"])
router.include_router(content.router, prefix="/content", tags=["Content"])
router.include_router(contact.router, prefix="/contact", tags=["Contact"])
router.include_router(pilot_signup.router, prefix="/pilot-signup", tags=["Pilot Signup"])
router.include_router(ai.router, prefix="/ai", tags=["AI"])
router.include_router(uploads.router, prefix="/uploads", tags=["Uploads"])
router.include_router(media.router, prefix="/media", tags=["Media Library"])
router.include_router(secrets.router, prefix="/secrets", tags=["Secrets Management"])
router.include_router(settings.router, prefix="/settings", tags=["App Settings"])

