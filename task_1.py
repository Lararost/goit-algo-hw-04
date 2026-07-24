import argparse
import shutil
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """Зчитує шляхи до вихідної та цільової директорій."""
    parser = argparse.ArgumentParser(
        description=(
            "Рекурсивно копіює файли з вихідної директорії та "
            "сортує їх у піддиректорії за розширеннями."
        )
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Шлях до вихідної директорії.",
    )
    parser.add_argument(
        "destination",
        nargs="?",
        type=Path,
        default=Path("dist"),
        help="Шлях до цільової директорії. За замовчуванням: dist.",
    )
    return parser.parse_args()


def get_file_category(file_path: Path) -> str:
    """Повертає розширення файлу без крапки або окрему категорію."""
    extension = file_path.suffix.lower().lstrip(".")
    return extension if extension else "no_extension"


def get_unique_path(destination_file: Path) -> Path:
    """
    Повертає вільний шлях для файлу.

    Це запобігає перезаписуванню, якщо в різних вихідних папках є
    файли з однаковими назвами.
    """
    if not destination_file.exists():
        return destination_file

    counter = 1
    while True:
        candidate = destination_file.with_name(
            f"{destination_file.stem}_{counter}{destination_file.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def copy_file(file_path: Path, destination: Path) -> Path:
    """Копіює файл у піддиректорію, названу за його розширенням."""
    category = get_file_category(file_path)
    category_directory = destination / category
    category_directory.mkdir(parents=True, exist_ok=True)

    destination_file = get_unique_path(category_directory / file_path.name)
    shutil.copy2(file_path, destination_file)
    return destination_file


def process_directory(
    source: Path,
    destination: Path,
    destination_resolved: Path,
) -> tuple[int, int]:
    """
    Рекурсивно обходить директорію та копіює знайдені файли.

    Повертає кількість успішно скопійованих файлів і кількість помилок.
    """
    copied_count = 0
    error_count = 0

    try:
        items = list(source.iterdir())
    except (PermissionError, OSError) as error:
        print(f"Не вдалося прочитати директорію '{source}': {error}")
        return 0, 1

    for item in items:
        try:
            # Якщо папка dist розташована всередині source, не обходимо її,
            # інакше програма могла б копіювати вже скопійовані файли повторно.
            if item.is_dir() and item.resolve() == destination_resolved:
                continue

            if item.is_dir():
                copied, errors = process_directory(
                    item,
                    destination,
                    destination_resolved,
                )
                copied_count += copied
                error_count += errors

            elif item.is_file():
                new_path = copy_file(item, destination)
                copied_count += 1
                print(f"Скопійовано: {item} -> {new_path}")

        except (PermissionError, FileNotFoundError, OSError) as error:
            error_count += 1
            print(f"Помилка під час обробки '{item}': {error}")

    return copied_count, error_count


def main() -> None:
    args = parse_arguments()

    source = args.source.expanduser().resolve()
    destination = args.destination.expanduser().resolve()

    if not source.exists():
        raise SystemExit(f"Помилка: директорія '{source}' не існує.")

    if not source.is_dir():
        raise SystemExit(f"Помилка: '{source}' не є директорією.")

    if source == destination:
        raise SystemExit(
            "Помилка: вихідна та цільова директорії не можуть бути однаковими."
        )

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as error:
        raise SystemExit(
            f"Не вдалося створити цільову директорію '{destination}': {error}"
        ) from error

    copied_count, error_count = process_directory(
        source,
        destination,
        destination.resolve(),
    )

    print("\nОбробку завершено.")
    print(f"Успішно скопійовано файлів: {copied_count}")
    print(f"Кількість помилок: {error_count}")
    print(f"Результат збережено у: {destination}")


if __name__ == "__main__":
    main()
