import time
from multiprocessing import Pool, cpu_count


def factorize_single(number: int):
    """
    Шукає всі числа, на які дане число ділиться без залишку.
    Наприклад: 6 -> [1, 2, 3, 6]
    """
    result = []
    for i in range(1, number + 1):
        if number % i == 0:
            result.append(i)
    return result


def factorize_sync(*numbers):
    """
    Синхронна (звичайна) версія:
    проходить усі числа по черзі, одне за одним.
    """
    results = []
    for num in numbers:
        results.append(factorize_single(num))
    return results


def factorize_parallel(*numbers):
    """
    Паралельна версія:
    використовує всі ядра процесора, щоб обчислювати кілька чисел одночасно.
    Це прискорює роботу на великих наборах даних.
    """
    with Pool(cpu_count()) as pool:
        results = pool.map(factorize_single, numbers)
    return results


if __name__ == "__main__":
    # Числа з прикладу з умови
    numbers = (128, 255, 99999, 10651060)

    print("🔹 Запуск синхронної версії...")
    start_time = time.time()
    a, b, c, d = factorize_sync(*numbers)
    sync_time = time.time() - start_time
    print(f"✅ Синхронна версія виконана за {round(sync_time, 4)} секунд")

    # Перевірка, що все працює правильно (тест із завдання)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439,
                 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140,
                 76079, 152158, 304316, 380395, 532553, 760790,
                 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print("\n🔹 Запуск паралельної версії...")
    start_time = time.time()
    a, b, c, d = factorize_parallel(*numbers)
    parallel_time = time.time() - start_time
    print(f"⚡ Паралельна версія виконана за {round(parallel_time, 4)} секунд")

    print(f"\n🧠 Використано ядер процесора: {cpu_count()}")
    print(f"⏱ Прискорення приблизно у {round(sync_time / parallel_time, 2)} раз(и)")