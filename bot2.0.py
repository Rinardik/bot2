from aiogram import Bot, Dispatcher
from app.const import TOKEN
from app.handlers import router
import asyncio
from app.const import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))