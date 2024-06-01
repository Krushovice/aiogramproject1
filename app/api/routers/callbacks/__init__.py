__all__ = ("router",)


from aiogram import Router

from .questionary_cb_handler import router as register_router
from .main_callback_handlers import router as main_router
from .profile_callback_handlers import router as profile_router

router = Router()

router.include_routers(
    main_router,
    profile_router,
    register_router,
)
