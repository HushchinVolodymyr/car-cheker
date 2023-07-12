from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import dp, bot
from database.database import session, engine, Car
from keyboards.inline import err_markup, starter_inline_menu

class GlassMirrors(StatesGroup):
    number = State()
    left_light = State()
    left_PTF = State()
    left_mirror = State()
    right_light = State()
    right_PTF = State()
    right_mirror = State() 


async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер")
    await GlassMirrors.first()


async def set_glass_mirrors(message: Message, state:FSMContext):    
    number = message.text
    car = session.query(Car).filter_by(car_number = number).first()
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Введите  информацию про левую фару")
        await GlassMirrors.next()
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


async def set_left_light(message: Message, state:FSMContext):
    left_light = message.text
    await state.update_data(left_light = left_light)
    await message.answer("Введите иннфрмацию про левую ПТФ")
    await GlassMirrors.next()


async def set_left_ptf(message: Message, state:FSMContext):
    left_PTF = message.text
    await state.update_data(left_PTF = left_PTF)
    await message.answer("Введите иннфрмацию про левое зеркало")
    await GlassMirrors.next()


async def set_left_mirror(message: Message, state:FSMContext):
    left_mirror = message.text
    await state.update_data(left_mirror = left_mirror)
    await message.answer("Введите иннфрмацию про правую фару")
    await GlassMirrors.next()


async def set_right_light(message: Message, state:FSMContext):
    right_light = message.text
    await state.update_data(right_light = right_light)
    await message.answer("Введите информацию про правую ПТФ")
    await GlassMirrors.next()


async def set_right_PTF(message: Message, state:FSMContext):
    right_PTF = message.text
    await state.update_data(right_PTF = right_PTF)
    await message.answer("Введите информацию про правое зеркало")
    await GlassMirrors.next()


async def set_right_mirror(message: Message, state:FSMContext):
    right_mirror = message.text

    data = await state.get_data()

    car = session.query(Car).filter_by(car_number = data.get("number")).first()
    
    car.glass_mirrors.left_light = data.get("left_light")
    car.glass_mirrors.left_PTF = data.get("left_PTF")
    car.glass_mirrors.left_mirror = data.get("left_mirror")
    car.glass_mirrors.right_light = data.get("right_light")
    car.glass_mirrors.right_PTF = data.get("right_PTF")
    car.glass_mirrors.right_mirror = right_mirror

    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="В главное меню", callback_data="cancel")
            ]
        ]
    )

    await state.update_data(right_mirror = right_mirror)
    await message.answer("Все заполненно", reply_markup = end_murk)
    await state.reset_state()



def register_glass_mirrors_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(get_number, text = "glass_mirros")
    dp.register_message_handler(set_glass_mirrors, state = GlassMirrors.number)
    dp.register_message_handler(set_left_light, state = GlassMirrors.left_light)
    dp.register_message_handler(set_left_ptf, state = GlassMirrors.left_PTF)
    dp.register_message_handler(set_left_mirror, state = GlassMirrors.left_mirror)
    dp.register_message_handler(set_right_light, state = GlassMirrors.right_light)
    dp.register_message_handler(set_right_PTF, state = GlassMirrors.right_PTF)
    dp.register_message_handler(set_right_mirror, state = GlassMirrors.right_mirror)
