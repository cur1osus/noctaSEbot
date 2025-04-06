from __future__ import annotations

from enum import Enum

from aiogram.filters.callback_data import CallbackData

from bot.utils.callback_data_prefix_enums import CallbackDataPrefix


class PossibleLanguages(Enum):
    en = "en"  # English
    uk = "uk"  # Ukrainian


class LanguageWindowCB(CallbackData, prefix=CallbackDataPrefix.language_window):  # type: ignore[call-arg]
    pass


class SelectLanguageCB(CallbackData, prefix=CallbackDataPrefix.select_language):  # type: ignore[call-arg]
    language: PossibleLanguages



