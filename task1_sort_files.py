import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def copy_file(file_path: Path, dest_dir: Path):
    """
    Копіює один файл у потрібну папку за його розширенням.
    Наприклад: myphoto.jpg -> dist/jpg/myphoto.jpg
    """
    if not file_path.is_file():
        return

    # Отримуємо розширення файлу (jpg, png тощо)
    ext = file_path.suffix.lower().lstrip('.') or 'no_ext'

    # Створюємо папку для цього типу файлів, якщо її ще немає
    target_dir = dest_dir / ext
    target_dir.mkdir(parents=True, exist_ok=True)

    # Копіюємо файл у нову папку
    shutil.copy2(file_path, target_dir / file_path.name)


def process_directory(src_dir: Path, dest_dir: Path, executor: ThreadPoolExecutor):
    """
    Проходить по всіх файлах і підпапках у заданій папці.
    Для кожного файлу — запускає копіювання в окремому потоці.
    Для кожної підпапки — теж запускає її обробку в окремому потоці.
    """
    futures = []

    for item in src_dir.iterdir():
        if item.is_dir():
            # Якщо це папка — обробляємо її окремо (рекурсивно)
            futures.append(executor.submit(process_directory, item, dest_dir, executor))
        elif item.is_file():
            # Якщо це файл — копіюємо його в іншому потоці
            futures.append(executor.submit(copy_file, item, dest_dir))

    return futures


def main():
    """
    Головна функція — читає аргументи з командного рядка та запускає процес.
    """
    if len(sys.argv) < 2:
        print("Використання: python sort_files_multithreaded.py <шлях_до_папки> [шлях_куди_копіювати]")
        sys.exit(1)

    # Звідки беремо файли
    src_dir = Path(sys.argv[1])

    # Куди копіюємо (за замовчуванням у папку 'dist')
    dest_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")

    # Перевіряємо, що вихідна папка існує
    if not src_dir.exists() or not src_dir.is_dir():
        print(f"Помилка: '{src_dir}' не існує або не є папкою.")
        sys.exit(1)

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Створюємо пул потоків (кількість залежить від кількості ядер процесора)
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        futures = process_directory(src_dir, dest_dir, executor)

        # Чекаємо, поки всі потоки завершать роботу
        for _ in as_completed(futures):
            pass

    print(f"\n✅ Готово! Файли скопійовано до '{dest_dir}'.")


if __name__ == "__main__":
    main()