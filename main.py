from functools import partial, wraps
import logging
from aiogram import Bot, Dispatcher, executor, types
from ytmusicapi import YTMusic
import asyncio

HOST = "https://58ee-2001-470-28-338-00-960.eu.ngrok.io/"
API_TOKEN = "SOMEBOTTOKEN"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


def duration_to_sec(dur: str):
    return int(dur.split(":")[0]) * 60 + int(dur.split(":")[1])


yt = YTMusic("headers.json")


@dp.inline_handler()
async def adf(query: types.InlineQuery):
    a = query.query
    if a == "":
        await query.answer(
            [
                types.InlineQueryResultArticle(
                    id="what",
                    title="Напиши что-нибудь :)",
                    description=f"Напиши что-нибудь.",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"Чтобы пользоваться ботом нужно в его инлайн режиме для начала написать хоть что-то.",
                        parse_mode="HTML",
                    ),
                )
            ]
        )
        return
    try:
        result = await wrap(yt.search)(a, limit=8, filter="songs")
        s, ids = [], []
        for i in result:
            if i["videoId"] in ids:
                continue
            ids.append(i["videoId"])
            s.append(
                types.InlineQueryResultAudio(
                    id=i["videoId"],
                    audio_duration=duration_to_sec(i["duration"]),
                    title=i["title"],
                    performer=i["artists"][0]["name"],
                    audio_url=f"{HOST}?video_id=" + i["videoId"] + "&a=dfs",
                )
            )
        await query.answer(s)
    except Exception as e:
        await query.answer(
            [
                types.InlineQueryResultArticle(
                    id="42069",
                    title="Что-то пошло не так!!",
                    input_message_content=types.InputTextMessageContent(
                        message_text="lol what"
                    ),
                )
            ]
        )
        pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
