from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, cast

from aiogram import BaseMiddleware
from aiogram.types import Chat, Message, TelegramObject, Update, User

from bot.storages.func import _get_user_model

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


# 777000 is Telegram's user id of service messages
TG_SERVICE_USER_ID: Final[int] = 777000


class CheckUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        chat: Chat = data.get("event_chat")
        user: User = data.get("event_from_user")

        match event.event_type:
            case "message":
                if user.is_bot is False and user.id != TG_SERVICE_USER_ID:
                    data["user_model"] = await _get_user_model(
                        data["db_session"],
                        data["redis"],
                        user,
                        chat,
                    )

                msg: Message = cast(Message, event.event)

                if (
                    msg.reply_to_message
                    and msg.reply_to_message.from_user
                    and not msg.reply_to_message.from_user.is_bot
                    and msg.reply_to_message.from_user.id != TG_SERVICE_USER_ID
                ):
                    await _get_user_model(data["db_session"], data["redis"], msg.reply_to_message.from_user, chat)

            case "callback_query" | "my_chat_member" | "chat_member" | "inline_query":
                if user.is_bot is False and user.id != TG_SERVICE_USER_ID:
                    data["user_model"] = await _get_user_model(
                        data["db_session"],
                        data["redis"],
                        user,
                        chat,
                    )

            case _:
                pass

        return await handler(event, data)
