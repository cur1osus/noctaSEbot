from aiogram import Router

from . import cbs, cmds

router = Router()

router.include_routers(
    cbs.router,
    cmds.router
)
