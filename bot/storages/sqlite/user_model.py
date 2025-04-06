from datetime import datetime

from sqlalchemy import BigInteger, Index
from sqlalchemy.dialects.sqlite import TIMESTAMP, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from bot.storages.sqlite.base import Base


class DBUserModel(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(32), nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True, server_default=expression.null())
    registration_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=expression.text("(datetime('now', 'utc'))"),
    )
    pm_active: Mapped[bool] = mapped_column(nullable=False, server_default=expression.false())

    __table_args__ = (Index(None, "username", unique=True),)
