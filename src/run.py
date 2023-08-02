import asyncio

from loguru import logger

from src.infrastructure.telegram import COMMANDS_LIST, bot

logger.add("fbb.log", rotation="50 MB")


async def set_commands():
    logger.info("Commands installed 🔧")
    try:
        await bot.set_my_commands(COMMANDS_LIST)
    except Exception as err:
        logger.error(f"Error while setting commands: {err}")


async def start_bot_loop():
    await set_commands()
    logger.info("Bot started 🚀")
    while True:
        try:
            await bot.polling(none_stop=True)
        except Exception as err:
            logger.error(err)
            logger.error("🔴 Bot is down.\nRestarting...")
            await asyncio.sleep(15)


asyncio.run(start_bot_loop())
