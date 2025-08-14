def get_cats_info(path):
    cats_list = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # пропускаємо порожні рядки
                try:
                    cat_id, name, age = line.split(",")
                    cats_list.append({
                        "id": cat_id,
                        "name": name,
                        "age": age
                    })
                except ValueError:
                    print(f"Помилка обробки рядка: {line}")
                    continue
        return cats_list

    except FileNotFoundError:
        print(f"Файл '{path}' не знайдено.")
        return []
    except Exception as e:
        print(f"Виникла помилка: {e}")
        return []



