from aiogram import Router

from game.controllers.handlers.map.handlers import movement_router
from game.controllers.handlers.registration.handlers import reg_router
from game.controllers.middlewares.session_middleware import SessionMiddleware

router = Router()
router.message.outer_middleware(SessionMiddleware())
router.include_router(reg_router)
router.include_router(movement_router)
