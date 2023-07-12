from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from app import bot, dp
from database.database import session, Car


class UnderHood(StatesGroup):
    number = State()
    lkp_status = State()
    plastic_details = State()
    engine_tools = State()


async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер машины")
    await UnderHood.first()


async def set_under_hood(message: Message, state:FSMContext):
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Введите состояние ЛКП подкопотного пространстваr")
        await UnderHood.next()
    else:
        err_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(text = "Попробовать снова", callback_data = "under_hood")
                ],
                [
                    InlineKeyboardButton(text = "Отмена", callback_data = "cancel")
                ]
            ]
        )
        await state.update_data(number = number)
        await state.reset_data()
        await state.reset_state()
        await message.answer("Машины с данным номером нет", reply_markup = err_markup)


async def set_lkp_status(message:Message, state:FSMContext):
    lkp_status = message.text
    await state.update_data(lkp_status = lkp_status)
    await message.answer("Введите состояние пластиковый деталей")
    await UnderHood.next()


async def set_plastic_details(message: Message, state:FSMContext):
    plastic_details = message.text
    await state.update_data(plastic_details = plastic_details)
    await message.answer("Введите состояние двигателя, навесного оборудования")
    await UnderHood.next()


async def set_engine_tools(message: Message, state:FSMContext):
    engine_tools = message.text

    data = await state.get_data()

    number = data.get("number")
    car = session.query(Car).filter_by(car_number = number).first()

    car.under_hood.lkp_status = data.get("lkp_status")
    car.under_hood.plastic_details = data.get("plastic_details")
    car.under_hood.engine_tools = engine_tools

    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(engine_tools = engine_tools)
    await message.answer("Все заполненно", reply_markup = end_murk)
    await state.reset_state()


def register_under_hood_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(get_number, text = "under_hood")
    dp.register_message_handler(set_under_hood, state = UnderHood.number)
    dp.register_message_handler(set_lkp_status, state = UnderHood.lkp_status)
    dp.register_message_handler(set_plastic_details, state = UnderHood.plastic_details)
    dp.register_message_handler(set_engine_tools, state = UnderHood.engine_tools)
