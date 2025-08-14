def total_salary(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        total = 0
        count = 0

        for line in lines:
            # Прибираємо пробіли і перенос рядка
            line = line.strip()
            if not line:
                continue  # пропускаємо пусті рядки

            try:
                name, salary = line.split(",")
                total += int(salary)
                count += 1
            except ValueError:
                # Якщо рядок у неправильному форматі, пропускаємо
                print(f"Помилка обробки рядка: {line}")
                continue

        if count == 0:
            return 0, 0

        average = total / count
        return total, average

    except FileNotFoundError:
        print(f"Файл '{path}' не знайдено.")
        return 0, 0
    except Exception as e:
        print(f"Виникла помилка: {e}")
        return 0, 0


