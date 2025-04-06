from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters.callback_data import CallbackData

from bot.utils.callback_data_prefix_enums import CallbackDataPrefix

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery
    from redis.asyncio import Redis

router = Router()


class UniversalWindowCloseCB(CallbackData, prefix=CallbackDataPrefix.universal_close):  # type: ignore[call-arg]
    pass


@router.callback_query(UniversalWindowCloseCB.filter())
async def universal_close_cb(cb: CallbackQuery, redis: Redis) -> None:
    pass
