__all__ = ("router",)


from aiogram import Router

from core import DataBaseSession, db_helper
from .commands import router as commands_router
from .callbacks import router as callbacks_router

router = Router()
router.message.middleware(DataBaseSession(session=db_helper.session_factory))
router.include_routers(
    commands_router,
    callbacks_router,
)
