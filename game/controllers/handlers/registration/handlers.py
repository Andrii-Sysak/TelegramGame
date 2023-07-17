import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from game.bl.player import create_player
from game.db.session import s
from game.db.models.soul import BackgroundCells
from game.controllers.handlers.registration.utils import bg_emoji_kb
from game.controllers.handlers.registration.states import Reg

reg_router = Router()

log = logging.getLogger(__name__)


@reg_router.message(Reg.unregistered)
async def start_command(message: Message, state: FSMContext) -> None:
    await message.answer('ПРИВІТ ЧОРТЯКО. Я БУДУ ТЕБЕ ВЧИТИ ЖИТИ :3')
    await message.answer('АЛЕ СПЕРШУ. . .  ЯК ТЕБЕ ЗВУТЬ?')
    await state.set_state(Reg.name)


@reg_router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext) -> None:
    await message.answer('ЧУДОВО, ТЕПЕР ДРУГУ ПОЛОВИНУ ІМЕНІ')
    await state.update_data(name=message.text)
    await state.set_state(Reg.name2)


@reg_router.message(Reg.name2)
async def reg_name2(message: Message, state: FSMContext) -> None:
    await state.update_data(name2=message.text)
    await state.set_state(Reg.background_emoji)
    await message.answer(
        'ВИБЕРИ ЕМОДЗІ ДЛЯ ЗАДНЬОГО ФОНУ:',
        reply_markup=bg_emoji_kb.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True
        ),
    )


@reg_router.message(Reg.background_emoji)
async def reg_bg_emoji(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        assert message.from_user
        assert message.text
        await create_player(
            message.from_user.id,
            data['name'] + data['name2'],
            BackgroundCells(message.text)
        )
        await s.session.flush()
    except Exception as e:
        log.exception(e)
        await message.answer('ВИБАЧ ЩОСЬ ПІШЛО НЕ ТАК, ДАВАЙ ЗНОВУ З ПОЧАТКУ')
        await state.set_state(Reg.name)
        return

    await state.clear()
    await message.answer('СУПЕР! ТИ В БАЗІ')
