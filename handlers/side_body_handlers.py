from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import dp, bot
from database.database import session, engine, Car
from keyboards.inline import err_markup, starter_inline_menu


class SideBody(StatesGroup):
    number = State()
    left_front_fender_min = State()
    left_front_fender_max = State()
    left_back_fender_min = State()
    left_back_fender_max = State()
    right_front_fender_min = State()
    right_front_fender_max = State()
    right_back_fender_min = State()
    right_back_fender_max = State()


async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер")
    await SideBody.first()


async def set_side_body(message: Message, state:FSMContext):
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Введите минимальную толщину левого переднего крыла (МКР)")
        await SideBody.next()
    else:
        err_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(text = "Попробовать снова", callback_data = "side_body")
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


async def set_left_front_fender_min(message: Message, state:FSMContext):
    left_front_fender_min = message.text
    await state.update_data(left_front_fender_min = left_front_fender_min)
    await message.answer("Введите максимальную толщину левого переднего крыла (МКР)")
    await SideBody.next()


async def set_left_front_fender_max(message: Message, state:FSMContext):
    left_front_fender_max = message.text
    await state.update_data(left_front_fender_max = left_front_fender_max)
    await message.answer("Введите минимальную толщину левого заднего крыла (МКР)")
    await SideBody.next()


async def set_left_back_fender_min(message: Message, state:FSMContext):
    left_back_fender_min = message.text
    await state.update_data(left_back_fender_min = left_back_fender_min)
    await message.answer("Введите максимальную толщину левого заднего крыла (МКР)")
    await SideBody.next()


async def set_left_back_fender_max(message: Message, state:FSMContext):
    left_back_fender_max = message.text
    await state.update_data(left_back_fender_max = left_back_fender_max)
    await message.answer("Введите минимальную толщину правого переднего крыла (МКР)")
    await SideBody.next()


async def set_right_front_fender_min(message: Message, state:FSMContext):
    right_front_fender_min = message.text
    await state.update_data(right_front_fender_min = right_front_fender_min)
    await message.answer("Введите максимальную толщину правого переднего крыла (МКР)")
    await SideBody.next()


async def set_right_front_fender_max(message: Message, state:FSMContext):
    right_front_fender_max = message.text
    await state.update_data(right_front_fender_max = right_front_fender_max)
    await message.answer("Введите минимального толщину правого заднего крыла (МКР)")
    await SideBody.next()


async def set_right_back_fender_min(message: Message, state:FSMContext):
    right_back_fender_min = message.text
    await state.update_data(right_back_fender_min = right_back_fender_min)
    await message.answer("Введите максимальную толщину правого заднего крыла (МКР)")
    await SideBody.next()


async def set_right_back_fender_max(message: Message, state:FSMContext):
    right_back_fender_max = message.text

    data = await state.get_data()

    number = data.get("number")
    left_front_fender_min = data.get("left_front_fender_min")
    left_front_fender_max = data.get("left_front_fender_max")
    left_back_fender_min = data.get("left_back_fender_min")
    left_back_fender_max = data.get("left_back_fender_max")
    right_front_fender_min = data.get("right_front_fender_min")
    right_front_fender_max = data.get("right_front_fender_max")
    right_back_fender_min = data.get("right_back_fender_min")
    
    car = session.query(Car).filter_by(car_number = number).first()

    car.side_body.left_front_fender_min = left_front_fender_min    
    car.side_body.left_front_fender_max = left_front_fender_max
    car.side_body.left_back_fender_min = left_back_fender_min
    car.side_body.left_back_fender_max = left_back_fender_max
    car.side_body.right_front_fender_min = right_front_fender_min
    car.side_body.right_front_fender_max = right_front_fender_max
    car.side_body.right_back_fender_min = right_back_fender_min
    car.side_body.right_back_fender_max = right_back_fender_max

    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(right_back_fender_max = right_back_fender_max)
    await message.answer("Все заполненно", reply_markup = end_murk)
    await state.reset_state()


def register_side_body_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(get_number, text = "side_body")
    dp.register_message_handler(set_side_body, state = SideBody.number)
    dp.register_message_handler(set_left_front_fender_min, state = SideBody.left_front_fender_min)
    dp.register_message_handler(set_left_front_fender_max, state = SideBody.left_front_fender_max)
    dp.register_message_handler(set_left_back_fender_min, state = SideBody.left_back_fender_min)
    dp.register_message_handler(set_left_back_fender_max, state = SideBody.left_back_fender_max)
    dp.register_message_handler(set_right_front_fender_min, state = SideBody.right_front_fender_min)
    dp.register_message_handler(set_right_front_fender_max, state = SideBody.right_front_fender_max)
    dp.register_message_handler(set_right_back_fender_min, state = SideBody.right_back_fender_min)
    dp.register_message_handler(set_right_back_fender_max, state = SideBody.right_back_fender_max)