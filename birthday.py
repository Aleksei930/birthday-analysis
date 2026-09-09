"""Анализ даты рождения и вывод даты в виде электронного табло."""

from calendar import isleap
from datetime import date


WEEKDAYS_RU = (
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
)

DIGITS = {
    "0": ("***", "* *", "* *", "* *", "***"),
    "1": ("  *", " **", "  *", "  *", "***"),
    "2": ("***", "  *", "***", "*  ", "***"),
    "3": ("***", "  *", "***", "  *", "***"),
    "4": ("* *", "* *", "***", "  *", "  *"),
    "5": ("***", "*  ", "***", "  *", "***"),
    "6": ("***", "*  ", "***", "* *", "***"),
    "7": ("***", "  *", "  *", "  *", "  *"),
    "8": ("***", "* *", "***", "* *", "***"),
    "9": ("***", "* *", "***", "  *", "***"),
    " ": ("     ", "     ", "     ", "     ", "     "),
}


def create_birth_date(
    day: int,
    month: int,
    year: int,
    today: date | None = None,
) -> date:
    """Создать дату рождения, отклонив невозможную или будущую дату."""
    try:
        result = date(year, month, day)
    except ValueError as exc:
        raise ValueError("Указанная дата не существует.") from exc

    if result > (today or date.today()):
        raise ValueError("Дата рождения не может быть в будущем.")
    return result


def weekday_ru(value: date) -> str:
    """Вернуть название дня недели по-русски."""
    return WEEKDAYS_RU[value.weekday()]


def is_leap_year(year: int) -> bool:
    """Определить високосность года по григорианскому календарю."""
    return isleap(year)


def calculate_age(born: date, today: date | None = None) -> int:
    """Вычислить количество полных лет."""
    current = today or date.today()
    birthday_is_ahead = (current.month, current.day) < (born.month, born.day)
    return current.year - born.year - birthday_is_ahead


def render_date(value: date) -> str:
    """Составить пять строк звёздочного табло для даты ``дд мм гггг``."""
    symbols = value.strftime("%d %m %Y")
    return "\n".join(" ".join(DIGITS[symbol][row] for symbol in symbols) for row in range(5))


def read_integer(prompt: str) -> int:
    """Запрашивать целое число, пока пользователь не введёт корректное значение."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число.")


def main() -> None:
    """Запустить интерактивный сценарий."""
    print("Анализ даты рождения")
    while True:
        day = read_integer("Введите день рождения: ")
        month = read_integer("Введите месяц рождения: ")
        year = read_integer("Введите год рождения: ")
        try:
            born = create_birth_date(day, month, year)
            break
        except ValueError as exc:
            print(f"Ошибка: {exc} Повторите ввод.\n")

    print(f"\nДата рождения: {born:%d %m %Y}")
    print(f"День недели: {weekday_ru(born)}")
    print(f"Год {'високосный' if is_leap_year(born.year) else 'не високосный'}.")
    print(f"Полных лет: {calculate_age(born)}")
    print("\nДата рождения на электронном табло:\n")
    print(render_date(born))


if __name__ == "__main__":
    main()
