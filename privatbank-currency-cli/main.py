import asyncio
import sys
from services.currency_service import CurrencyService
from utils.date_utils import get_last_n_days


async def main():
    # Перевірка аргументів
    if len(sys.argv) != 2:
        print("❌ Використання: py main.py <кількість_днів>")
        return

    try:
        days = int(sys.argv[1])
    except ValueError:
        print("❌ Кількість днів повинна бути числом.")
        return

    if not (1 <= days <= 10):
        print("❌ Можна дізнатися курс максимум за останні 10 днів.")
        return

    dates = get_last_n_days(days)
    service = CurrencyService()

    results = []
    for date in dates:
        data = await service.get_rates_for_date(date)
        if data:
            results.append({date: data})

    print(results)


if __name__ == "__main__":
    asyncio.run(main())