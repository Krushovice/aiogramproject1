__all__ = ("router",)


from aiogram import Router

from .questionary_cb_handler import router as register_router

router = Router()

router.include_router(register_router)
