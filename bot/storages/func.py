from __future__ import annotations

from typing import TYPE_CHECKING, cast

from aiogram.enums import ChatType
from sqlalchemy import insert, select, update
from sqlalchemy.sql.operators import eq, ne

from bot.storages.redis.user_model import RDUserModel
from bot.storages.sqlite.user_model import DBUserModel

if TYPE_CHECKING:
    from aiogram.types import Chat, User
    from redis.asyncio.client import Redis
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def _get_or_create_user(user: User, chat: Chat, session: AsyncSession) -> DBUserModel:
    if user.username:
        stmt = select(DBUserModel).where(eq(DBUserModel.username, user.username), ne(DBUserModel.id_user, user.id))
        another_user: DBUserModel = await session.scalar(stmt)

        if another_user:
            stmt = update(DBUserModel).where(eq(DBUserModel.id_user, another_user.id)).values(username=None)
            await session.execute(stmt)

    stmt = select(DBUserModel).where(eq(DBUserModel.id_user, user.id))
    user_model: DBUserModel | None = await session.scalar(stmt)

    if not user_model:
        stmt = (
            insert(DBUserModel)
            .values(
                id_user=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                pm_active=chat.type == ChatType.PRIVATE,
            )
            .returning(DBUserModel)
        )
        user_model = await session.scalar(stmt)

    else:
        user_model.username = user.username
        user_model.first_name = user.first_name
        user_model.last_name = user.last_name

    return cast(DBUserModel, user_model)


async def _get_user_model(
    db_session: async_sessionmaker[AsyncSession],
    redis: Redis,
    user: User,
    chat: Chat,
) -> RDUserModel:
    user_model: RDUserModel | None = await RDUserModel.get(redis, user.id)

    if user_model:
        return user_model

    async with db_session() as session:
        async with session.begin():
            user_model: DBUserModel = await _get_or_create_user(user, chat, session)

            await session.commit()

        user_model: RDUserModel = RDUserModel.from_orm(user_model)

        await cast(RDUserModel, user_model).save(redis)

    return cast(RDUserModel, user_model)
