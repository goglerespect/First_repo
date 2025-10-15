from datetime import datetime, timedelta


def get_last_n_days(n: int):
    """
    Повертає список дат у форматі dd.mm.yyyy за останні n днів.
    """
    today = datetime.now()
    return [
        (today - timedelta(days=i)).strftime("%d.%m.%Y")
        for i in range(n)
    ]