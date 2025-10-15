from services.api_client import PrivatBankApiClient


class CurrencyService:
    """Сервіс для обробки валютних курсів."""

    def __init__(self):
        self.api_client = PrivatBankApiClient()

    async def get_rates_for_date(self, date: str):
        """
        Повертає курси EUR та USD на конкретну дату.
        """
        response = await self.api_client.fetch_rates(date)
        if not response:
            return None

        result = {}
        for rate in response.get("exchangeRate", []):
            if rate.get("currency") in ["USD", "EUR"]:
                result[rate["currency"]] = {
                    "sale": rate.get("saleRate", rate.get("saleRateNB")),
                    "purchase": rate.get("purchaseRate", rate.get("purchaseRateNB")),
                }

        return result if result else None