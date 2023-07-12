from aiogram import types, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app import bot, dp
from database.database import session, Car


class Repair(StatesGroup):
    number = State()
    add_wheel_complect = State()
    anti_theft_heating_system = State()
    electricity = State()
    body_glasses = State()
    engine_transmission = State()
    brakes_suspension = State()
    cabin = State()
    others = State()
    cost = State()


async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер машины")
    await Repair.first()


async def set_repair(message: Message, state:FSMContext):
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Второй компелкт резины/колес")
        await Repair.next()
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


async def set_add_wheel_complect(message:Message, state:FSMContext):
    add_wheel_complect = message.text
    await state.update_data(add_wheel_complect = add_wheel_complect)
    await message.answer("Противоугонная система")
    await Repair.next()


async def set_anti_theft_heating_system(message:Message, state:FSMContext):
    anti_theft_heating_system = message.text
    await state.update_data(anti_theft_heating_system = anti_theft_heating_system)
    await message.answer("Электрика")
    await Repair.next()


async def set_electricity(message:Message, state:FSMContext):
    electricity = message.text
    await state.update_data(electricity = electricity)
    await message.answer("Кузов, стекла")
    await Repair.next()


async def set_body_glasses(message:Message, state:FSMContext):
    body_glasses = message.text
    await state.update_data(body_glasses = body_glasses)
    await message.answer("Двигатель трансмиссия")
    await Repair.next()


async def set_engine_transmission(message:Message, state:FSMContext):
    engine_transmission = message.text
    await state.update_data(engine_transmission = engine_transmission)
    await message.answer("Подвеска, тормоза")
    await Repair.next()


async def set_brakes_suspension(message:Message, state:FSMContext):
    brakes_suspension = message.text
    await state.update_data(brakes_suspension = brakes_suspension)
    await message.answer("Салон")
    await Repair.next()


async def set_cabin(message:Message, state:FSMContext):
    cabin = message.text
    await state.update_data(cabin = cabin)
    await message.answer("Прочее")
    await Repair.next()


async def set_others(message:Message, state:FSMContext):
    others = message.text
    await state.update_data(others = others)
    await message.answer("Общая цена ремонта")
    await Repair.next()


async def set_cost(message:Message, state:FSMContext):
    cost = message.text

    data = await state.get_data()
    number = data.get("number")
    car = session.query(Car).filter_by(car_number = number).first()


    car.repair.add_wheel_complect = data.get("add_wheel_complect")
    car.repair.anti_theft_heating_system = data.get("anti_theft_heating_system")
    car.repair.electricity = data.get("electricity")
    car.repair.body_glasses = data.get("body_glasses")
    car.repair.engine_transmission = data.get("engine_transmission")
    car.repair.brakes_suspension = data.get("brakes_suspension")
    car.repair.cabin = data.get("cabin")
    car.repair.others = data.get("others")
    car.repair.cost = cost


    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(cost = cost)
    await message.answer("Все заполненно", reply_markup = end_murk)
    await state.reset_state()


def register_repair_handlers(dp:Dispatcher):
    dp.register_callback_query_handler(get_number, text = "repair")
    dp.register_message_handler(set_repair, state=Repair.number)    
    dp.register_message_handler(set_add_wheel_complect, state=Repair.add_wheel_complect)
    dp.register_message_handler(set_anti_theft_heating_system, state=Repair.anti_theft_heating_system)
    dp.register_message_handler(set_electricity, state=Repair.electricity)
    dp.register_message_handler(set_body_glasses, state=Repair.body_glasses)
    dp.register_message_handler(set_engine_transmission, state=Repair.engine_transmission)
    dp.register_message_handler(set_brakes_suspension, state=Repair.brakes_suspension)
    dp.register_message_handler(set_cabin, state=Repair.cabin)
    dp.register_message_handler(set_others, state=Repair.others)
    dp.register_message_handler(set_cost, state=Repair.cost)







