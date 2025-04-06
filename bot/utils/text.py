import asyncio
from typing import Any, Self


class Text:
    def __init__(self, locale: str = "ru") -> None:
        self.locale = locale
        self.message_id: list[str] = []

    def __getattr__(self, attr: str) -> Self:
        self.message_id.append(attr)
        return self

    async def __call__(self, *args: list[Any], **kwds: dict[str, Any]) -> str:
        match len(self.message_id):
            case 1:
                return self.message_id[0]
            case 2:
                return "-".join(self.message_id)
            case _:
                return "-".join(self.message_id[:2]) + "_" + "_".join(self.message_id[2:])

