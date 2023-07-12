from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import bot, dp
from database.database import session, Car

class Doors(StatesGroup):
    number = State()
    left_front_door_min = State()
    left_front_door_max = State()
    left_back_door_min = State()
    left_back_door_max = State()
    right_front_door_min = State()
    right_front_door_max = State()
    right_back_door_min = State()
    right_back_door_max = State()


async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер")
    await Doors.first()


async def set_doors(message: Message, state:FSMContext):
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Введите минимальную толщину передней левой двери (МКР)")
        await Doors.next()
    else:
        err_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(text = "Попробовать снова", callback_data = "doors")
                ],
                [
                    InlineKeyboardButton(text = "Отмена", callback_data = "cancel")
                ]
            ]
        )
        await state.update_data(number = number)
        await state.reset_data()
        await state.reset_state()
        await message.answer("Машины с таким номером нет", reply_markup = err_markup)


async def set_left_front_door_min(message: Message, state:FSMContext):
    left_front_door_min = message.text
    await state.update_data(left_front_door_min = left_front_door_min)
    await message.answer("Введите максимальную толщину передней левой двери (МКР)")
    await Doors.next()


async def set_left_front_door_max(message: Message, state:FSMContext):
    left_front_door_max = message.text
    await state.update_data(left_front_door_max = left_front_door_max)
    await message.answer("Введите минимальную толщину задней левой двери (МКР)")
    await Doors.next()


async def set_left_back_door_min(message: Message, state:FSMContext):
    left_back_door_min = message.text
    await state.update_data(left_back_door_min = left_back_door_min)
    await message.answer("Введите максимальную толщину задней левой двери (МКР)")
    await Doors.next()


async def set_left_back_door_max(message: Message, state:FSMContext):
    left_back_door_max = message.text
    await state.update_data(left_back_door_max = left_back_door_max)
    await message.answer("Введите минимальную толщину передней правой двери (МКР)")
    await Doors.next()


async def set_right_front_door_min(message: Message, state:FSMContext):
    right_front_door_min = message.text
    await state.update_data(right_front_door_min = right_front_door_min)
    await message.answer("Введите максимальную толщину передней правой двери (МКР)")
    await Doors.next()


async def set_right_front_door_max(message: Message, state:FSMContext):
    right_front_door_max = message.text
    await state.update_data(right_front_door_max = right_front_door_max)
    await message.answer("Введите минимальную толщину задней правой двери (МКР)")
    await Doors.next()


async def set_right_back_door_min(message: Message, state:FSMContext):
    right_back_door_min = message.text
    await state.update_data(right_back_door_min = right_back_door_min)
    await message.answer("Введите минимальную толщину задней правой двери (МКР)")
    await Doors.next()


async def set_right_back_door_max(message: Message, state:FSMContext):
    right_back_door_max = message.text

    data = await state.get_data()

    number = data.get("number") 
    car = session.query(Car).filter_by(car_number = number).first()

    car.doors.left_front_door_min = data.get("left_front_door_min")
    car.doors.left_front_door_max = data.get("left_front_door_max")
    car.doors.left_back_door_min = data.get("left_back_door_min")
    car.doors.left_back_door_max = data.get("left_back_door_max")
    car.doors.right_front_door_min = data.get("right_front_door_min")
    car.doors.right_front_door_max = data.get("right_front_door_max")
    car.doors.right_back_door_min = data.get("right_back_door_min")
    car.doors.right_back_door_max = right_back_door_max

    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(right_back_door_max = right_back_door_max)
    await message.answer("Все заполнено", reply_markup = end_murk)
    await state.reset_state()


def register_doors_handler(dp : Dispatcher):
    dp.register_callback_query_handler(get_number, text = "doors")
    dp.register_message_handler(set_doors, state = Doors.number)
    dp.register_message_handler(set_left_front_door_min, state = Doors.left_front_door_min)
    dp.register_message_handler(set_left_front_door_max, state = Doors.left_front_door_max)
    dp.register_message_handler(set_left_back_door_min, state = Doors.left_back_door_min)
    dp.register_message_handler(set_left_back_door_max, state = Doors.left_back_door_max)
    dp.register_message_handler(set_right_front_door_min, state = Doors.right_front_door_min)
    dp.register_message_handler(set_right_front_door_max, state = Doors.right_front_door_max)
    dp.register_message_handler(set_right_back_door_min, state = Doors.right_back_door_min)
    dp.register_message_handler(set_right_back_door_max, state = Doors.right_back_door_max)    