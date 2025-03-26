import asyncio
import json
import keyboard
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
with open("config.json", "r+", encoding = "utf-8") as config_open:
    CONFIG_JSON = json.load(config_open)
with open("messages.json", "r+", encoding = "utf-8") as messages_open:
    MESSAGES_JSON = json.load(messages_open)


bot = Bot(token=CONFIG_JSON["TG_TOKEN"])
dp = Dispatcher()


@dp.message(lambda message: message.chat.id == -4707616830)
async def i_hate(message):
    pass



@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(MESSAGES_JSON["start"].format(name = message.from_user.full_name), reply_markup = keyboard.basic())

@dp.message(F.text.lower() == "стереометрия")
async def echo_handler(message: types.Message) -> None:
    await message.answer(MESSAGES_JSON["input_requests"])

@dp.message(F.text.lower() == "планиметрия")
async def echo_handler(message: types.Message) -> None:
    await message.answer(MESSAGES_JSON["input_requests"])

@dp.message(F.text.lower() == "информация")
async def echo_handler(message: types.Message) -> None:
    await message.answer(MESSAGES_JSON["information"])

@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())