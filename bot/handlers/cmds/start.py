from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart


if TYPE_CHECKING:
    from aiogram.types import Message
    from redis.asyncio import Redis


router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart(deep_link=True))
async def start_cmd_with_deep_link(msg: Message, command: CommandObject, redis: Redis) -> None:
    args = command.args.split() if command.args else []
    deep_link = args[0]

    logger.info("User %s started bot with deeplink: %s", msg.from_user.id, deep_link)


@router.message(CommandStart(deep_link=False))
async def start_cmd(msg: Message, redis: Redis) -> None:
    await msg.answer("Hello, world!")
