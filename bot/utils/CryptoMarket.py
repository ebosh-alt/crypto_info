import asyncio

import aiohttp
from bot.db.models import Quote, Coin


class CoinMarket:
    def __init__(self):
        self.api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '5a7a63d0-48b9-4b20-8ec9-d22fa6d2ff8d',
        }

    def __contains__(self, item) -> bool:
        data = asyncio.run(self.get_all_names())
        for coin in data:
            if coin.symbol == item or coin.name == item:
                return True
        return False

    async def get_info(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url, headers=self.headers) as resp:
                response = await resp.json()
                response: dict = response["data"]
                return response

    async def get_price_coin(self, name_coin) -> Coin:
        response = await self.get_info()
        for el in response:
            if el["name"] == name_coin or el["symbol"] == name_coin:
                quote = Quote(**el["quote"]["USD"])
                coin = Coin(name=el["name"], symbol=el["symbol"], quote=quote)
                return coin

    async def get_all_names(self) -> list[Coin]:
        response = await self.get_info()
        name_buttons = list()
        for el in response:
            name_buttons.append(Coin(name=el['name'], symbol=el["symbol"]))
        return name_buttons


if __name__ == '__main__':
    if "s" in CoinMarket():
        print("s")
