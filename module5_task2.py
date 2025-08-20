import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Генератор, що знаходить у тексті всі дійсні числа
    і повертає їх як float.
    """
    # Регулярний вираз для пошуку чисел з плаваючою крапкою або цілих
    for match in re.finditer(r"\d+(?:\.\d+)?", text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Підсумовує всі числа, знайдені функцією-генератором.
    """
    return sum(func(text))