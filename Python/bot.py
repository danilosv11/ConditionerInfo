import asyncio
from aiohttp import web
import table_manager

from loguru import logger
import config


from aiogram import Bot, types, Dispatcher, filters, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


logger.add(
    config.settings["LOG_FILE"],
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip",
)


class ConditionerInfoTelegrambot(Bot):
    def __init__(
            self,
            token: str,
    ) -> None:
        super().__init__(token)


bot: ConditionerInfoTelegrambot = ConditionerInfoTelegrambot(
    token=config.settings["TOKEN"],
)
dp = Dispatcher(bot)

button_last_data = KeyboardButton(text='Последние данные', callback_data='last_data')
button_day_average_data = KeyboardButton(text='Средние по дням', callback_data='day_average_data')
button_month_average_data = KeyboardButton(text='Средние по месяцам', callback_data='month_average_data')
button_year_average_data = KeyboardButton(text='Средние по годам', callback_data='year_average_data')

keyboard=[[button_last_data,button_day_average_data],[button_month_average_data,button_year_average_data]]
kb = ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True)

@dp.message_handler(commands=['start'])
async def process_start_command(message_from: types.Message):
    await bot_commands_handler(message_from)


@dp.message_handler(filters.Regexp(regexp=r"(((Б|б)от))"))
async def bot_commands_handler(message_from: types.Message) -> None:
    # Обработчик команды Бот
    user_id: str = str(message_from.from_id)
    message = (
        f"СИСТЕМА СБОРА ДАННЫХ ДЛЯ ДИАГНОСТИКИ СОСТОЯНИЯ КОНДИЦИОНЕРА\n\n"
        f"Создал:\n"
        f"Студент группы МММ-201-О\n"
        f"Михайлов Данил Александрович\n\n"
        f"Для навигации по боту воспользуйтесь кнопками на экране\n"
    )
    try:
        await message_from.answer(message, reply_markup=kb)
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        return


@dp.message_handler(filters.Regexp(regexp=r"(((П|п)оследние данные))"))
async def last_data_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    try:
        await message_from.answer("Подождите немного, сверяем данные")
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
    values = table_manager.get_last_data()
    if values == -1:
        message = 'Нет данных'
    else:
        data = values.split(";")
        message = (
            f"{data[0]} {data[1]}\n"
            f"Температура IN: {data[2]} С\n"
            f"Влажность IN: {data[3]} %\n"
            f"Температура OUT: {data[4]} С\n"
            f"Влажность OUT: {data[5]} %\n"
            f"Скорость потока: {data[6].strip()} м/с"
        )
        try:
            await message_from.answer(message, reply_markup=kb)
        except Exception as send_error:
            logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        return
    try:
        await message_from.reply(message, reply_markup=kb)
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        await message_from.reply("Какая-то ошибка")
    return

@dp.message_handler(filters.Regexp(regexp=r"(((С|с)редние по дням))"))
async def day_average_handler(message_from: types.Message) -> None:
    # Обработчик команды Средние по дням
    user_id: str = str(message_from.from_id)
    try:
        await message_from.answer("Подождите немного, сверяем данные")
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
    values = table_manager.get_day_average_data()
    if values == -1:
        message = 'Нет данных'
    else:
        message = values
        try:
            await message_from.answer(message, reply_markup=kb)
        except Exception as send_error:
            logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        return
    try:
        await message_from.reply(message, reply_markup=kb)
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        await message_from.reply("Какая-то ошибка")
    return


@dp.message_handler(filters.Regexp(regexp=r"(((С|с)редние по месяцам))"))
async def month_average_handler(message_from: types.Message) -> None:
    # Обработчик команды Средние по месяцам
    user_id: str = str(message_from.from_id)
    try:
        await message_from.answer("Подождите немного, сверяем данные")
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
    values = table_manager.get_month_average_data()
    if values == -1:
        message = 'Нет данных'
    else:
        message = values
        try:
            await message_from.answer(message, reply_markup=kb)
        except Exception as send_error:
            logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        return
    try:
        await message_from.reply(message, reply_markup=kb)
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        await message_from.reply("Какая-то ошибка")
    return

@dp.message_handler(filters.Regexp(regexp=r"(((С|с)редние по годам))"))
async def day_average_handler(message_from: types.Message) -> None:
    # Обработчик команды Средние по годам
    user_id: str = str(message_from.from_id)
    try:
        await message_from.answer("Подождите немного, сверяем данные")
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
    values = table_manager.get_year_average_data()
    if values == -1:
        message = 'Нет данных'
    else:
        message = values
        try:
            await message_from.answer(message, reply_markup=kb)
        except Exception as send_error:
            logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        return
    try:
        await message_from.reply(message, reply_markup=kb)
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        await message_from.reply("Какая-то ошибка")
    return

@dp.message_handler(filters.Regexp(regexp=r"(.+)"))
async def bad_command_handler(message_from: types.file.File) -> None:
    #Обработчик команды Неверная команда.
    user_id: str = str(message_from.from_id)
    try:
        await message_from.reply("Неопознаная команда. Пожалуйста воспользуйтесь <u>кнопками</u> для навигации по боту",
                                 parse_mode=types.ParseMode.HTML, reply_markup=kb)
    except Exception as send_error:
        logger.debug(f"{send_error.args}: Trouble id: {user_id}")
        await message_from.reply("Какая-то ошибка")
    return


async def handle_post(request):
    body = await request.text()
    print(f"Received message:\n{body}")
    table_manager.upload_data(body)
    return web.Response(text="Message received")


def start_server(host='0.0.0.0', port=8080):
    app = web.Application()
    app.router.add_post('/', handle_post)
    runner = web.AppRunner(app)
    loop = asyncio.get_event_loop()

    async def run_server():
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        print(f"Server started on {host}:{port}")

    loop.run_until_complete(run_server())
    executor.start_polling(dp, skip_updates=True)
    loop.run_forever()


if __name__ == "__main__":
    start_server()
