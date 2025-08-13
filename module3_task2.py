import random

def get_numbers_ticket(min_num: int, max_num: int, quantity: int) -> list:
    """
    Генерує відсортований список унікальних випадкових чисел для лотереї.

    :param min_num: Мінімальне можливе число (>= 1)
    :param max_num: Максимальне можливе число (<= 1000)
    :param quantity: Кількість чисел для вибору
    :return: Відсортований список унікальних випадкових чисел або пустий список, якщо параметри некоректні.
    """
    # Перевірка вхідних параметрів
    if (
        not isinstance(min_num, int)
        or not isinstance(max_num, int)
        or not isinstance(quantity, int)
        or min_num < 1
        or max_num > 1000
        or min_num > max_num
        or quantity < 1
        or quantity > (max_num - min_num + 1)
    ):
        return []

    # Генерація унікальних чисел
    numbers = random.sample(range(min_num, max_num + 1), quantity)

    # Повертаємо відсортований список
    return sorted(numbers)
#Приклад використання
lottery_numbers = get_numbers_ticket(1, 49, 6)
print("Ваші лотерейні числа:", lottery_numbers)
