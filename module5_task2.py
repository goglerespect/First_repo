import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Генератор, що знаходить у тексті всі дійсні числа,
    які чітко відокремлені пробілами з обох боків.
    """
    for match in re.finditer(r" (\d+(?:\.\d+)?) ", text):
        yield float(match.group(1))


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Підсумовує всі числа, знайдені функцією-генератором.
    """
    return sum(func(text))


# Перевірка
text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")