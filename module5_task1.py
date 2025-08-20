def caching_fibonacci():
    # Кеш для збереження вже обчислених значень
    cache = {}

    def fibonacci(n):
        """Обчислює n-те число Фібоначчі з кешуванням."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif n in cache:  # якщо вже є у кеші
            return cache[n]

        # Рекурсивне обчислення з кешуванням
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci