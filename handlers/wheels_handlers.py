from aiogram import types, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app import bot, dp
from database.database import session, Car

class Wheels(StatesGroup):
    number = State()

    left_front_wheel = State()
    left_front_disk = State()
    left_front_block = State()
    left_back_wheel = State()
    left_back_disk = State()
    left_back_block = State()
    right_front_wheel = State()
    right_front_disk = State()
    right_front_block = State()
    right_back_wheel = State()
    right_back_disk = State()
    right_back_block = State()


async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер машины")
    await Wheels.first() 


async def set_wheels(message: Message, state:FSMContext):
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Левое переедне колесо")
        await Wheels.next()
    else:
        err_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(text = "Попробовать снова", callback_data = "wheels")
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

async def set_left_front_wheel(message: Message, state:FSMContext):
    left_front_wheel = message.text
    await state.update_data(left_front_wheel = left_front_wheel)
    await bot.send_message(message.from_user.id, "Левый передний диск")
    await Wheels.next()



async def set_left_front_disk(message: Message, state:FSMContext):
    left_front_disk = message.text
    await state.update_data(left_front_disk = left_front_disk)
    await bot.send_message(message.from_user.id, "Левая передняя колодка")
    await Wheels.next()


async def set_left_front_block(message: Message, state:FSMContext):
    left_front_block = message.text
    await state.update_data(left_front_block = left_front_block)
    await bot.send_message(message.from_user.id, "Левое заднее колесо")
    await Wheels.next()


async def set_left_back_wheel(message: Message, state:FSMContext):
    left_back_wheel = message.text
    await state.update_data(left_back_wheel = left_back_wheel)
    await bot.send_message(message.from_user.id, "Левый задний диск")
    await Wheels.next()


async def set_left_back_disk(message: Message, state:FSMContext):
    left_back_disk = message.text
    await state.update_data(left_back_disk = left_back_disk)
    await bot.send_message(message.from_user.id, "Левая задняя колодка")
    await Wheels.next()


async def set_left_back_block(message: Message, state:FSMContext):
    left_back_block = message.text 
    await state.update_data(left_back_block = left_back_block)
    await bot.send_message(message.from_user.id, "Правое переднее колесо")
    await Wheels.next()

async def set_right_front_wheel(message: Message, state:FSMContext):
    right_front_wheel = message.text
    await state.update_data(right_front_wheel = right_front_wheel)
    await bot.send_message(message.from_user.id, "Правый передний диск")
    await Wheels.next()


async def set_right_front_disk(message: Message, state:FSMContext):
    right_front_disk = message.text
    await state.update_data(right_front_disk = right_front_disk)
    await bot.send_message(message.from_user.id, "Правая передняя колодка")
    await Wheels.next()


async def set_right_front_block(message: Message, state:FSMContext):
    right_front_block = message.text
    await state.update_data(right_front_block = right_front_block)
    await bot.send_message(message.from_user.id, "Правое заднее колесо")
    await Wheels.next()

async def set_right_back_wheel(message: Message, state:FSMContext):
    right_back_wheel = message.text
    await state.update_data(right_back_wheel = right_back_wheel)
    await bot.send_message(message.from_user.id, "Правый задний диск")
    await Wheels.next()


async def set_right_back_disk(message: Message, state:FSMContext):
    right_back_disk = message.text
    await state.update_data(right_back_disk = right_back_disk)
    await bot.send_message(message.from_user.id, "Правая задняя колодка")
    await Wheels.next()


async def set_right_back_block(message: Message, state:FSMContext):
    right_back_block = message.text

    data = await state.get_data()
    number = data.get("number")
    car = session.query(Car).filter_by(car_number = number).first()

    car.wheels.left_front_wheel = data.get("left_front_wheel")
    car.wheels.left_front_disk = data.get("left_front_disk")
    car.wheels.left_front_block = data.get("left_front_block")
    car.wheels.left_back_wheel = data.get("left_back_wheel")
    car.wheels.left_back_disk = data.get("left_back_disk")
    car.wheels.left_back_block = data.get("left_back_block")
    car.wheels.right_front_wheel = data.get("right_front_wheel")
    car.wheels.right_front_disk = data.get("right_front_disk")
    car.wheels.right_front_block = data.get("right_front_block")
    car.wheels.right_back_wheel = data.get("right_back_wheel")
    car.wheels.right_back_disk = data.get("right_back_disk")
    car.wheels.right_back_block = right_back_block

    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(right_back_block = right_back_block)
    await message.answer("Все заполненно", reply_markup = end_murk)
    await state.reset_state()


def register_wheels_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(get_number, text = "wheels")
    dp.register_message_handler(set_wheels, state = Wheels.number)
    dp.register_message_handler(set_left_front_wheel, state = Wheels.left_front_wheel)
    dp.register_message_handler(set_left_front_disk, state = Wheels.left_front_disk)
    dp.register_message_handler(set_left_front_block, state = Wheels.left_front_block)
    dp.register_message_handler(set_left_back_wheel, state = Wheels.left_back_wheel)
    dp.register_message_handler(set_left_back_disk, state = Wheels.left_back_disk)
    dp.register_message_handler(set_left_back_block, state = Wheels.left_back_block)
    dp.register_message_handler(set_right_front_wheel, state = Wheels.right_front_wheel)
    dp.register_message_handler(set_right_front_disk, state = Wheels.right_front_disk)
    dp.register_message_handler(set_right_front_block, state = Wheels.right_front_block)
    dp.register_message_handler(set_right_back_wheel, state = Wheels.right_back_wheel)
    dp.register_message_handler(set_right_back_disk, state = Wheels.right_back_disk)
    dp.register_message_handler(set_right_back_block, state = Wheels.right_back_block)

