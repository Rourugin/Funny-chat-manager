from aiogram import Router

from app.handlers.main_h import main_router
from app.handlers.main_h import light_router
from app.handlers.strange_h import strnage_router


def setup_routers() -> Router:
    router = Router()
    router.include_router(main_router)
    router.include_router(light_router)
    router.include_router(strnage_router)

    return router