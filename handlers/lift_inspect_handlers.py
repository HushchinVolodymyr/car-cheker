from aiogram import types, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app import bot, dp
from database.database import session, engine, Car


class LiftInspect(StatesGroup):
    number = State()
    ag_ak_inspect = State()
    front_suspension = State()
    back_suspension = State()
    hoses_wiring = State()
    exhaust_system = State()


async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер машины")
    await LiftInspect.first()


async def set_lift_inspect(message: Message, state:FSMContext):
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Введите общее состояние АГ/АК покрытия")
        await LiftInspect.next()
    else:
        err_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(text = "Попробовать снова", callback_data = "lift_inspect")
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


async def set_ag_ak_inspect(message:Message, state:FSMContext):
    ag_ak_inspect = message.text
    await state.update_data(ag_ak_inspect = ag_ak_inspect)
    await message.answer("Введите состояние передней подвески")
    await LiftInspect.next()

async def set_front_suspension(message:Message, state:FSMContext):
    front_suspension = message.text
    await state.update_data(front_suspension = front_suspension)
    await message.answer("Введите состояние задней подвески")
    await LiftInspect.next()

async def set_back_suspension(message:Message, state:FSMContext):
    back_suspension = message.text
    await state.update_data(back_suspension = back_suspension)
    await message.answer("Введимте состояние шлангов и проводки")
    await LiftInspect.next()

async def set_hoses_wiring(message:Message, state:FSMContext):
    hoses_wiring = message.text
    await state.update_data(hoses_wiring = hoses_wiring)
    await message.answer("Введите состояние системы выхлопа")
    await LiftInspect.next()


async def set_exhaust_system(message:Message, state:FSMContext):
    exhaust_system = message.text

    data = await state.get_data()
    number = data.get("number")
    car = session.query(Car).filter_by(car_number = number).first()

    car.lift_inspect.ag_ak_inspect = data.get("ag_ak_inspect")
    car.lift_inspect.front_suspension = data.get("front_suspension")
    car.lift_inspect.back_suspension = data.get("back_suspension")
    car.lift_inspect.hoses_wiring = data.get("hoses_wiring")
    car.lift_inspect.exhaust_system = exhaust_system

    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(exhaust_system = exhaust_system)
    await message.answer("Все заполненно", reply_markup = end_murk)
    await state.reset_state()


def register_lift_inspection_handlers(dp:Dispatcher):
    dp.register_callback_query_handler(get_number, text = "lift_inspect")
    dp.register_message_handler(set_lift_inspect, state = LiftInspect.number)
    dp.register_message_handler(set_ag_ak_inspect, state=LiftInspect.ag_ak_inspect)
    dp.register_message_handler(set_front_suspension, state=LiftInspect.front_suspension)
    dp.register_message_handler(set_back_suspension, state=LiftInspect.back_suspension)
    dp.register_message_handler(set_hoses_wiring, state=LiftInspect.hoses_wiring)
    dp.register_message_handler(set_exhaust_system, state=LiftInspect.exhaust_system)
