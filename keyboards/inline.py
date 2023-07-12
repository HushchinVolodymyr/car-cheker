from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


starter_inline_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "Создать машину", callback_data = "create_car_menu")
        ],
        [
            InlineKeyboardButton(text = "Найти по номеру", callback_data = "find_by_number"),
            InlineKeyboardButton(text = "Найти по VIN номеру", callback_data = "find_by_vin_number")
        ]
    ]
)


err_car_create_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "Поробовать снова", callback_data = "create_car")
        ],
        [
            InlineKeyboardButton(text = "Отмена",  callback_data = "cancel")
        ]
    ]
)

create_car_mn = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "Заполнить все сразу", callback_data = "create_car")
        ],
        [
            InlineKeyboardButton(text = "Создать машину, заполнить позже", callback_data = "create_sep")
        ],
        [
            InlineKeyboardButton(text = "Заполниить по отдельности", callback_data = "sepprate_fill")
        ],
        [
            InlineKeyboardButton(text = "Отмена",  callback_data = "cancel")
        ]
    ]
)

sepparate_car_fill_menu_1 = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "Оценки", callback_data = "marks")
        ],
        [
            InlineKeyboardButton(text = "Верхняя часть кузова", callback_data = "upper_body")
        ],
        [
            InlineKeyboardButton(text = "Боковоая часть кузова", callback_data = "side_body")
        ],
        [
            InlineKeyboardButton(text = "Двери", callback_data = "doors")
        ],
        [
            InlineKeyboardButton(text = "Стекла, зеркала", callback_data = "glass_mirros")
        ],
        [
            InlineKeyboardButton(text = "Отмена", callback_data = "cancel"),
            InlineKeyboardButton(text = "Вперед", callback_data = "forward")
        ]
    ]
)

sepparate_car_fill_menu_2 = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "Колеса", callback_data = "wheels")
        ],
        [
            InlineKeyboardButton(text = "Подкапотное протсранство", callback_data = "under_hood")
        ],
        [
            InlineKeyboardButton(text = "Богажник", callback_data = "trunk")
        ],
        [
            InlineKeyboardButton(text = "Осмотр на подьемнике", callback_data = "lift_inspect")
        ],
        [
            InlineKeyboardButton(text = "Цена ремонта", callback_data = "repair")
        ],
        [
            InlineKeyboardButton(text = "Назад", callback_data = "sepprate_fill"),
            InlineKeyboardButton(text = "Отмена", callback_data = "cancel")
        ]
    ]
)

err_markup = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(text = "Попробовать снова", callback_data = "marks")
                ],
                [
                    InlineKeyboardButton(text = "Отмена", callback_data = "cancel")
                ]
            ]
)