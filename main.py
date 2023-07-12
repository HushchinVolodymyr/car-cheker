import aiogram
import logging
import asyncio

from aiogram import executor

from handlers.main_handlers import register_handlers
from handlers.create_car_handlers import register_create_car_handlers
from handlers.marks_car_handlers import register_marks_handlers
from handlers.upper_body_handlers import register_upper_body_handlers
from handlers.side_body_handlers import register_side_body_handlers
from handlers.doors_handlers import register_doors_handler
from handlers.glass_mirorrs_handlers import register_glass_mirrors_handlers
from handlers.wheels_handlers import register_wheels_handlers
from handlers.under_hood_handlers import register_under_hood_handlers
from handlers.trunk_handlers import register_trunk_handlers
from handlers.lift_inspect_handlers import register_lift_inspection_handlers
from handlers.repair_handlers import register_repair_handlers

from app import bot, dp

logging.basicConfig(level = logging.INFO)


register_handlers(dp)
register_create_car_handlers(dp)
register_marks_handlers(dp)
register_upper_body_handlers(dp)
register_side_body_handlers(dp)
register_doors_handler(dp)
register_glass_mirrors_handlers(dp)
register_wheels_handlers(dp)
register_under_hood_handlers(dp)
register_trunk_handlers(dp)
register_lift_inspection_handlers(dp)
register_repair_handlers(dp)



if __name__ == "__main__":
    executor.start_polling(dispatcher = dp, skip_updates = True)