from aiogram import types, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app import bot, dp
from database.database import session, engine, Car


class UpperBody(StatesGroup):
    number = State()
    hood_MKR_min = State()
    hood_MKR_max = State()
    roof_MKR_min = State()
    roof_MKR_max = State()
    trunk_MKR_min = State()
    trunk_MKR_max = State()
    bumper_front_verdict = State()
    bumper_back_verdict = State()


#@dp.callback_query_handler(text = "upper_body")
async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер машины")
    await UpperBody.first()


async def set_upper_body(message: Message, state:FSMContext):
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Введите минимальную толщину капота (МКР)")
        await UpperBody.next()
    else:
        err_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(text = "Попробовать снова", callback_data = "upper_body")
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


async def set_hood_mkr_min(message: Message, state:FSMContext):
    hood_mkr_min = message.text
    await state.update_data(hood_mkr_min = hood_mkr_min)
    await message.answer("Введите максимальную толщину капота (МКР)")
    await UpperBody.next()


async def set_hood_mkr_max(message: Message, state:FSMContext):
    hood_mkr_max = message.text
    await state.update_data(hood_mkr_max = hood_mkr_max)
    await message.answer("Введите минимальную толщину крыши (МКР)")
    await UpperBody.next()


async def set_roof_mkr_min(message: Message, state:FSMContext):
    roof_mkr_min = message.text
    await state.update_data(roof_mkr_min = roof_mkr_min)
    await message.answer("Введите максимальную толщину крыши (МКР)")
    await UpperBody.next()


async def set_roof_mkr_max(message: Message, state:FSMContext):
    roof_mkr_max = message.text
    await state.update_data(roof_mkr_max = roof_mkr_max)
    await message.answer("Введите минимальную толщину богажника (МКР)")
    await UpperBody.next()


async def set_trunk_mkr_min(message: Message, state:FSMContext):
    trunk_mkr_min = message.text
    await state.update_data(trunk_mkr_min = trunk_mkr_min)
    await message.answer("Введите максимальную толщину богажника (МКР)")
    await UpperBody.next()


async def set_trunk_mkr_max(message: Message, state:FSMContext):
    trunk_mkr_max = message.text
    await state.update_data(trunk_mkr_max = trunk_mkr_max)
    await message.answer("Введите вердикт по переднему бамперу")
    await UpperBody.next()


async def set_bumper_front_verdict(message: Message, state:FSMContext):
    bumper_front_verdict = message.text
    await state.update_data(bumper_front_verdict = bumper_front_verdict)
    await message.answer("Введите вердикт по заднему бамперу")
    await UpperBody.next()


async def set_bumper_back_verdict(message: Message, state:FSMContext):
    bumper_back_verdict = message.text

    data = await state.get_data()

    number = data.get("number")
    hood_MKR_min = data.get("hood_mkr_min")
    hood_MKR_max = data.get("hood_mkr_max")
    roof_MKR_max = data.get("roof_mkr_max")
    roof_MKR_min = data.get("roof_mkr_min")
    trunk_MKR_min = data.get("trunk_mkr_min")
    trunk_MKR_max = data.get("trunk_mkr_max")
    bumper_front_verdict = data.get("bumper_front_verdict")
    

    car = session.query(Car).filter_by(car_number = number).first()
    
    car.upper_body.hood_MKR_min = hood_MKR_min
    car.upper_body.hood_MKR_max = hood_MKR_max
    car.upper_body.roof_MKR_min = roof_MKR_min
    car.upper_body.roof_MKR_max = roof_MKR_max
    car.upper_body.trunk_MKR_min = trunk_MKR_min
    car.upper_body.trunk_MKR_max = trunk_MKR_max
    car.upper_body.bumper_front_verdict = bumper_front_verdict
    car.upper_body.bumper_back_verdict = bumper_back_verdict

    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(bumper_back_verdict = bumper_back_verdict)
    await message.answer("Все заполненно", reply_markup = end_murk)
    await state.reset_state()


def register_upper_body_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(get_number, text = "upper_body")
    dp.register_message_handler(set_upper_body, state = UpperBody.number)
    dp.register_message_handler(set_hood_mkr_min, state = UpperBody.hood_MKR_min)
    dp.register_message_handler(set_hood_mkr_max, state = UpperBody.hood_MKR_max)
    dp.register_message_handler(set_roof_mkr_min, state = UpperBody.roof_MKR_min)
    dp.register_message_handler(set_roof_mkr_max, state = UpperBody.roof_MKR_max)
    dp.register_message_handler(set_trunk_mkr_min, state = UpperBody.trunk_MKR_min)
    dp.register_message_handler(set_trunk_mkr_max, state = UpperBody.trunk_MKR_max)
    dp.register_message_handler(set_bumper_front_verdict, state = UpperBody.bumper_front_verdict)
    dp.register_message_handler(set_bumper_back_verdict, state = UpperBody.bumper_back_verdict)

