from aiogram.utils.keyboard import ReplyKeyboardBuilder

from game.db.models.player import BackgroundCells

bg_emoji_kb = ReplyKeyboardBuilder()
for cell in BackgroundCells:
    bg_emoji_kb.button(text=cell)
