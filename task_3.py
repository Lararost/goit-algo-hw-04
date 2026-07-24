import argparse
import random
import timeit
from collections.abc import Callable


def insertion_sort(data: list[int]) -> list[int]:
    """Сортування вставками. Повертає новий відсортований список."""
    result = data.copy()

    for index in range(1, len(result)):
        current_value = result[index]
        position = index - 1

        while position >= 0 and result[position] > current_value:
            result[position + 1] = result[position]
            position -= 1

        result[position + 1] = current_value

    return result


def merge(left: list[int], right: list[int]) -> list[int]:
    """Зливає два відсортовані списки в один."""
    result = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def merge_sort(data: list[int]) -> list[int]:
    """Рекурсивне сортування злиттям."""
    if len(data) <= 1:
        return data.copy()

    middle = len(data) // 2
    left_part = merge_sort(data[:middle])
    right_part = merge_sort(data[middle:])

    return merge(left_part, right_part)


def timsort(data: list[int]) -> list[int]:
    """Вбудоване сортування Python, яке використовує Timsort."""
    return sorted(data)


def generate_datasets(size: int) -> dict[str, list[int]]:
    """Створює випадковий, відсортований і зворотно відсортований набори."""
    random_data = [
        random.randint(-size * 10, size * 10)
        for _ in range(size)
    ]

    return {
        "random": random_data,
        "sorted": sorted(random_data),
        "reversed": sorted(random_data, reverse=True),
    }


def measure_time(
    algorithm: Callable[[list[int]], list[int]],
    data: list[int],
    repeat: int,
) -> float:
    """Повертає найкращий час виконання алгоритму в секундах."""
    measurements = timeit.repeat(
        stmt=lambda: algorithm(data),
        repeat=repeat,
        number=1,
    )
    return min(measurements)


def verify_algorithms(
    algorithms: dict[str, Callable[[list[int]], list[int]]],
    data: list[int],
) -> None:
    """Перевіряє правильність результату кожного алгоритму."""
    expected = sorted(data)

    for name, algorithm in algorithms.items():
        result = algorithm(data)
        if result != expected:
            raise AssertionError(
                f"Алгоритм '{name}' повернув неправильний результат."
            )


def run_benchmark(sizes: list[int], repeat: int) -> None:
    algorithms = {
        "Merge sort": merge_sort,
        "Insertion sort": insertion_sort,
        "Timsort (sorted)": timsort,
    }

    print(
        f"{'Тип даних':<12}"
        f"{'Кількість':>12}"
        f"{'Merge sort':>16}"
        f"{'Insertion':>16}"
        f"{'Timsort':>16}"
    )
    print("-" * 72)

    for size in sizes:
        datasets = generate_datasets(size)

        for dataset_name, data in datasets.items():
            verify_algorithms(algorithms, data)

            results = {
                name: measure_time(algorithm, data, repeat)
                for name, algorithm in algorithms.items()
            }

            print(
                f"{dataset_name:<12}"
                f"{size:>12}"
                f"{results['Merge sort']:>16.6f}"
                f"{results['Insertion sort']:>16.6f}"
                f"{results['Timsort (sorted)']:>16.6f}"
            )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Порівняння сортування злиттям, вставками та Timsort "
            "за допомогою модуля timeit."
        )
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[100, 500, 1000, 2000],
        help="Розміри наборів даних.",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=3,
        help="Кількість повторних вимірювань для кожного тесту.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    if any(size <= 0 for size in args.sizes):
        raise SystemExit("Усі розміри наборів мають бути більшими за нуль.")

    if args.repeat <= 0:
        raise SystemExit("Кількість повторень має бути більшою за нуль.")

    random.seed(42)
    run_benchmark(args.sizes, args.repeat)


if __name__ == "__main__":
    main()
