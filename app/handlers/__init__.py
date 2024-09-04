from aiogram import Router

from app.handlers.main_handlers import main_router
from app.handlers.strange_handlers import strnage_router


def setup_routers() -> Router:
    router = Router()
    router.include_router(main_router)
    router.include_router(strnage_router)
    return router