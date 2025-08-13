from datetime import datetime

def get_days_from_today(date: str) -> int:
    """
    Повертає кількість днів від заданої дати до поточної дати.
    Якщо дата в майбутньому — результат додатний.
    Якщо дата в минулому — результат від'ємний.
    
    :param date: Рядок у форматі 'YYYY-MM-DD'.
    :return: Ціле число (дні).
    :raises ValueError: якщо формат дати неправильний.
    """
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Невірний формат дати. Використовуйте 'YYYY-MM-DD'.")
    
    today = datetime.today().date()
    delta = target_date - today
    return delta.days
print(get_days_from_today("2021-10-09"))