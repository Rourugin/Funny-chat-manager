from aiogram import Router

from app.handlers.main_h import main_router
from app.handlers.light_h import light_router
from app.handlers.strange_h import strange_router


def setup_routers() -> Router:
    router = Router()
    router.include_routers(main_router)
    router.include_routers(light_router)
    router.include_routers(strange_router)
    return router