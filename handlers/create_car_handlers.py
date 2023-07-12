from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
import datetime

from app import bot, dp
from database.database import Car, session, engine
from keyboards.inline import starter_inline_menu, err_car_create_menu

class CreateCar(StatesGroup):
    Car_brand = State()
    Car_model = State()
    Car_year = State()
    Car_number = State()
    Car_vin_number = State()


#@dp.callback_query_handler(text = "create_car")
async def create_car(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите марку машины (BMW, Honda, Nissan)")
    await CreateCar.first()


#@dp.message_handler(state = CreateCar.Car_brand)
async def set_car_brand(message: types.Message, state:FSMContext):
    car_brand = message.text
    await state.update_data(car_brand = car_brand), #print(f"Car brand: {car_brand}")
    await message.answer("Введите модель машины (e200, x6, gtr)")
    await CreateCar.next()

#@dp.message_handler(state = CreateCar.Car_model)
async def set_car_model(message: types.Message, state:FSMContext):
    car_model = message.text
    await state.update_data(car_model = car_model), #print(f"Car model: {car_model}")
    await message.answer("Введите год выпуска машины")
    await CreateCar.next()


#@dp.message_handler(state = CreateCar.Car_year)
async def set_car_year(message: types.Message, state:FSMContext):
    car_year = message.text
    await state.update_data(car_year = car_year), #print(f"Car year: {car_year}")
    await message.answer("Введите номер машины (8 символов)")
    await CreateCar.next()


#@dp.message_handler(state = CreateCar.Car_number)
async def set_car_number(message: types.Message, state:FSMContext):
    car_number = message.text
    await state.update_data(car_number = car_number), #print(f"Car number: {car_number}")
    await message.answer("Введите VIN номер машины (17 символов)")
    await CreateCar.next()

@dp.message_handler(state = CreateCar.Car_vin_number)
async def set_car_vin_number(message: types.Message, state:FSMContext):
    car_vin_number = message.text
    
    data = await state.get_data()
    car_brand = data.get("car_brand")
    car_model = data.get("car_model")
    car_year = data.get("car_year")
    car_number = data.get("car_number")
    date = datetime.datetime.now()
    
  
    if len(car_number) == 4 and len(car_vin_number) == 17: 
        car = Car(
            car_brand = lower(car_brand), 
            car_model = lower(car_model),
            car_year = car_year,
            car_number = car_number,
            car_vin_number = car_vin_number,
            date = date
        )
        session.add(car)
        session.commit()
        # print(car_brand)
        # print(car_model)
        # print(car_year)
        # print(car_number)
        # print(car_vin_number)
        
        await state.update_data(car_vin_number = car_vin_number), #print(f"Car VIN number: {car_vin_number}")
        await message.answer("Все заполнено", reply_markup = starter_inline_menu)
        await state.reset_state()
    else:
        await message.answer("Вы ввели некорректные данные!", reply_markup = err_car_create_menu)
        await state.update_data(car_vin_number = car_vin_number)
        await state.reset_state()




def register_create_car_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(create_car, text = "create_car", state = None)
    dp.register_message_handler(set_car_brand, state = CreateCar.Car_brand)
    dp.register_message_handler(set_car_model, state = CreateCar.Car_model)
    dp.register_message_handler(set_car_year, state = CreateCar.Car_year)
    dp.register_message_handler(set_car_number, state = CreateCar.Car_number)