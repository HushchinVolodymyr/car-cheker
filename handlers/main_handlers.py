from aiogram import types, Dispatcher
from app import bot, dp
from keyboards.inline import starter_inline_menu, create_car_mn, sepparate_car_fill_menu_1, sepparate_car_fill_menu_2
from text import greet_text



#@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    username = message.from_user.username
    await message.delete()
    await message.answer(f"Привет {username} {greet_text}", reply_markup = starter_inline_menu)#, print(f"Message from user: {text}")


#@dp.callback_query_handler(text = "create_car_menu")
async def create_car_menu(callback_query: types.CallbackQuery):
    username = callback_query.from_user.username
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(chat_id = chat_id,
                                message_id = message_id,
                                text = f"~Создание машины~",
                                reply_markup = create_car_mn)


#@dp.callback_query_handler(text = "find_by_number")
async def find_by_number(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите номер машины")


#@dp.callback_query_handler(text = "find_by_vin_number")
async def find_by_vin_number(message: types.Message):
    await bot.send_message(message.from_user.id, "Веведите Vin номер машины (VIN номер состоит из 17 символов)")




#@dp.callback_query_handler(text = "cancel")
async def cancel(callback_query: types.CallbackQuery):
    username = callback_query.from_user.username
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(chat_id = chat_id,
                                message_id = message_id,
                                text = f"Привет {username} {greet_text}",
                                reply_markup=starter_inline_menu)
                                




async def sep_fill_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(chat_id = chat_id,
                                message_id = message_id,
                                text = f"~Заполниьт по отдельности 1/2~",
                                reply_markup = sepparate_car_fill_menu_1)

async def sep_fill_2(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(chat_id = chat_id,
                                message_id = message_id,
                                text = f"~Заполниьт по отдельности 2/2~",
                                reply_markup = sepparate_car_fill_menu_2)





def register_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands = 'start')
    dp.register_callback_query_handler(create_car_menu, text = "create_car_menu")
    dp.register_callback_query_handler(find_by_number, text = "find_by_number")
    dp.register_callback_query_handler(find_by_vin_number, text = "find_by_vin_number")
    dp.register_callback_query_handler(cancel, text = "cancel")
    dp.register_callback_query_handler(sep_fill_1, text = "sepprate_fill")
    dp.register_callback_query_handler(sep_fill_2, text = "forward")
    # dp.register_message_handler(echo)