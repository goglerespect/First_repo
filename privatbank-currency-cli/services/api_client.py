import aiohttp


class PrivatBankApiClient:
    """Клас для запитів до публічного API ПриватБанку."""

    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    async def fetch_rates(self, date: str):
        """
        Отримати курси валют на конкретну дату.
        :param date: у форматі dd.mm.yyyy
        """
        params = {"json": "", "date": date}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params, timeout=10) as resp:
                    if resp.status != 200:
                        print(f"⚠ Помилка: код відповіді {resp.status} для {date}")
                        return None
                    return await resp.json()
        except aiohttp.ClientError as e:
            print(f"⚠ Помилка з'єднання: {e}")
            return None
        except asyncio.TimeoutError:
            print(f"⚠ Перевищено час очікування для дати {date}")
            return None