from aiogram import Router

from app.handlers.main_h import main_router
from app.handlers.shop_h import shop_router
from app.handlers.money_h import money_router
from app.handlers.strange_h import strange_router
from app.handlers.interactive_h import interactive_router


def setup_routers() -> Router:
    router = Router()
    router.include_routers(main_router)
    router.include_routers(shop_router)
    router.include_routers(money_router)
    router.include_routers(strange_router)
    router.include_routers(interactive_router)
    return router