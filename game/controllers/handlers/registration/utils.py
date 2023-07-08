from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from game.db.models.soul import BackgroundCells

bg_emoji_kb = ReplyKeyboardBuilder([[
    KeyboardButton(text=emoji) for emoji in BackgroundCells
]])
