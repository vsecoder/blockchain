import asyncio
import logging
import uvicorn

import coloredlogs

from app.config import Config, parse_config

from app.dispatcher import dispatcher

from datetime import datetime


async def on_startup(disp, config: Config, **kwargs):
    logging.info(f"Started at: {kwargs['start_time']}")

    web_config = config.web.get_config()

    logging.error("Started!")

    uvicorn.run(disp, host=web_config["host"], port=web_config["port"])


async def on_shutdown():
    logging.warning("Stopping...")


async def main():
    coloredlogs.install(level=logging.INFO)
    logging.warning("Starting...")

    config = parse_config("config.toml")

    start_time = datetime.now()
    context_kwargs = {"start_time": start_time}

    disp = dispatcher(context_kwargs)

    await on_startup(disp, config, **context_kwargs)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        asyncio.run(on_shutdown())
        logging.error("Stopped!")
