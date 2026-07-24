import argparse
import math
import turtle


def koch_curve(pen: turtle.Turtle, length: float, level: int) -> None:
    """Рекурсивно малює одну сторону кривої Коха."""
    if level == 0:
        pen.forward(length)
        return

    segment_length = length / 3
    angles = (60, -120, 60, 0)

    for angle in angles:
        koch_curve(pen, segment_length, level - 1)
        pen.left(angle)


def draw_koch_snowflake(level: int, size: float = 420) -> None:
    """Створює та відображає фрактал «сніжинка Коха»."""
    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха — рівень рекурсії {level}")
    screen.setup(width=900, height=800)
    screen.tracer(False)

    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    pen.penup()

    # Початкова позиція підібрана так, щоб сніжинка була ближче до центру.
    height = size * math.sqrt(3) / 2
    pen.goto(-size / 2, height / 3)
    pen.pendown()

    for _ in range(3):
        koch_curve(pen, size, level)
        pen.right(120)

    screen.update()
    screen.exitonclick()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Візуалізація фрактала «сніжинка Коха»."
    )
    parser.add_argument(
        "level",
        nargs="?",
        type=int,
        help="Невід'ємний рівень рекурсії.",
    )
    parser.add_argument(
        "--size",
        type=float,
        default=420,
        help="Довжина сторони сніжинки. За замовчуванням: 420.",
    )
    return parser.parse_args()


def read_level_from_user() -> int:
    """Просить користувача ввести коректний рівень рекурсії."""
    while True:
        try:
            level = int(input("Введіть рівень рекурсії (0 або більше): "))
            if level < 0:
                print("Рівень рекурсії не може бути від'ємним.")
                continue
            return level
        except ValueError:
            print("Введіть ціле число.")


def main() -> None:
    args = parse_arguments()
    level = args.level if args.level is not None else read_level_from_user()

    if level < 0:
        raise SystemExit("Помилка: рівень рекурсії не може бути від'ємним.")

    if args.size <= 0:
        raise SystemExit("Помилка: розмір має бути більшим за нуль.")

    if level > 6:
        print(
            "Попередження: високий рівень рекурсії може малюватися довго."
        )

    draw_koch_snowflake(level, args.size)


if __name__ == "__main__":
    main()
