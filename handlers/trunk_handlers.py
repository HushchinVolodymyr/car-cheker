from aiogram import types, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app import bot, dp
from database.database import session, engine, Car

class Trunk(StatesGroup):
    number = State()
    floor_light_upholstery = State()
    additional_wheel = State()
    tools = State()


async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер машины")
    await Trunk.first()


async def set_trunk(message: Message, state:FSMContext):
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Введите состояние пола, обивки, освещения")
        await Trunk.next()
    else:
        err_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(text = "Попробовать снова", callback_data = "trunk")
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


async def set_floor_light_upholstery(message: Message, state:FSMContext):
    floor_light_upholstery = message.text
    await state.update_data(floor_light_upholstery = floor_light_upholstery)
    await message.answer("Введите состояние запасного колеса")
    await Trunk.next()


async def set_additional_wheel(message: Message, state:FSMContext):
    additional_wheel = message.text
    await state.update_data(additional_wheel = additional_wheel)
    await message.answer("Введите состояние инструментов и домкрата")
    await Trunk.next()


async def set_tools(message:Message, state:FSMContext):
    tools = message.text

    data = await state.get_data()
    number = data.get("number")
    car = session.query(Car).filter_by(car_number = number).first()

    car.trunk.floor_light_upholstery = data.get("floor_light_upholstery")
    car.trunk.additional_wheel = data.get("additional_wheel")
    car.trunk.tools = tools

    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(tools = tools)
    await message.answer("Все заполненно", reply_markup = end_murk)
    await state.reset_state()


def register_trunk_handlers(dp:Dispatcher):
    dp.register_callback_query_handler(get_number, text = "trunk")
    dp.register_message_handler(set_trunk, state = Trunk.number)
    dp.register_message_handler(set_floor_light_upholstery, state=Trunk.floor_light_upholstery)
    dp.register_message_handler(set_additional_wheel, state=Trunk.additional_wheel)
    dp.register_message_handler(set_tools, state=Trunk.tools)




