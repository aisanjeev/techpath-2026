"""CRUD operations module."""
from app.crud.base import CRUDBase
from app.crud.user import user_crud
from app.crud.service import service_crud
from app.crud.blog import blog_crud
from app.crud.contact import contact_crud, newsletter_crud

__all__ = [
    "CRUDBase",
    "user_crud",
    "service_crud",
    "blog_crud",
    "contact_crud",
    "newsletter_crud",
]

