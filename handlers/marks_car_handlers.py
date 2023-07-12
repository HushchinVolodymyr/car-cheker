from aiogram import types, Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from app import dp, bot
#from FSM.create_car_FSM import Marks
from database.database import session, engine, Marks, Car
from text import greet_text
from keyboards.inline import starter_inline_menu, err_markup


class Marks(StatesGroup):
    number = State()
    outside_body = State()
    under_hood = State()
    trunk = State()
    main = State() 


#@dp.callback_query_handler(text = "marks")
async def get_number(message: Message):
    await bot.send_message(message.from_user.id, "Введите номер машины")
    await Marks.first()



async def set_marks(message: Message, state:FSMContext):
    number = message.text
    car = get_car_by_number(number)
    if car != None:
        await state.update_data(number = number)
        await bot.send_message(message.from_user.id, "Введите оценку внешенего состосяние машины")
        await Marks.next()
    else:
        await state.update_data(number = number)
        await state.reset_data()
        await state.reset_state()
        await message.answer("Машины с данным номером нет", reply_markup = err_markup)
    


#@dp.message_handler()
async def set_outside_body_mark(message: Message, state:FSMContext):
    outside_body_mark = message.text
    await state.update_data(outside_body_mark = outside_body_mark)
    await message.answer("Введите оценку подкапотного пространства машины")
    await Marks.next()


#@dp.message_handler()
async def set_under_hood_mark(message: Message, state:FSMContext):
    under_hood_mark = message.text
    await state.update_data(under_hood_mark = under_hood_mark)
    await message.answer("Введите оценку состоняие богажника")
    await Marks.next()


#@dp.message_handler()
async def set_trunk_mark(message: Message, state:FSMContext):
    trunk_mark = message.text
    await state.update_data(trunk_mark = trunk_mark)
    await message.answer("Введите оценку общего состоняие машины")
    await Marks.next()



#@dp.message_handler()
async def set_main_mark(message: Message, state:FSMContext):
    main = message.text
    await state.update_data(main = main)

    data = await state.get_data()
    car_number = data.get("number")
    outside_body_mark = data.get("outside_body_mark")
    under_hood_mark = data.get("under_hood_mark")
    trunk_mark = data.get("trunk_mark")
    main_mark = data.get("main")
    
    car = get_car_by_number(number = car_number)
    
    car.marks.main = main_mark
    car.marks.outside_body = outside_body_mark
    car.marks.under_hood = under_hood_mark
    car.marks.trunk = trunk_mark
    session.commit()

    end_murk = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "В главное меню", callback_data = "cancel")
            ]
        ]
    )

    await state.update_data(main = main)
    await message.answer("Все заполнено", reply_markup = end_murk)
    await state.reset_state()

    


def register_marks_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(get_number, text = "marks")
    dp.register_message_handler(set_marks, state = Marks.number)
    dp.register_message_handler(set_outside_body_mark, state = Marks.outside_body)
    dp.register_message_handler(set_under_hood_mark, state = Marks.under_hood)
    dp.register_message_handler(set_trunk_mark, state = Marks.trunk)
    dp.register_message_handler(set_main_mark, state = Marks.main)


def get_car_by_number(number):
    car = session.query(Car).filter_by(car_number = number).first()
    return car
