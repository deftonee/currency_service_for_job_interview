import aiohttp

from aiohttp import web

from enums import CurrencyEnum
from helpers import (
    save_rates, get_currencies, param_to_positive_int, get_last_rate,
    get_avg_volume)


async def fetch(request):
    async with aiohttp.ClientSession() as session:
        for c, url in CurrencyEnum.urls().items():
            async with session.get(url, ssl=True) as response:
                rows = await response.json()
                await save_rates(request.app['db_engine'], c, rows)
    return web.Response(body='Success')


async def currencies(request):
    objs = await get_currencies(request.app['db_engine'], **request.query)
    return web.json_response([[o.id, o.name] for o in objs])


async def rates(request):
    currency_id = param_to_positive_int(request.match_info, 'currency_id', 0)
    rate = await get_last_rate(request.app['db_engine'], currency_id)
    volume = await get_avg_volume(request.app['db_engine'], currency_id)

    return web.json_response([rate, volume])

