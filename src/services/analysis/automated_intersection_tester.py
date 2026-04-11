import math
import sys

# === КОНСТАНТИ ВАРІАНТУ ===
XC = 3
YC = 28
R = 78
MIN_VAL = -128
MAX_VAL = 128
EPSILON = 1e-8


def validate_line_data(a, b, c):
    """
    Функція валідації (Defensive Programming).
    Повертає (bool_status, message).
    """
    try:
        a, b, c = int(a), int(b), int(c)
    except (ValueError, TypeError):
        return (
            False,
            "Помилка: Введено нечислові дані. Будь ласка, вводьте лише цілі числа.",
        )

    for val, name in zip((a, b, c), ("a", "b", "c")):
        if not (MIN_VAL <= val <= MAX_VAL):
            return (
                False,
                f"Помилка: Значення {name}={val} поза діапазоном [{MIN_VAL}; {MAX_VAL}].",
            )

    if a == 0 and b == 0:
        return (
            False,
            "Помилка логіки: Коефіцієнти a та b не можуть одночасно дорівнювати 0 (це не пряма).",
        )

    return True, (a, b, c)


def analyze_intersection(a1, b1, c1, a2, b2, c2):
    """Чиста математична логіка."""
    delta = a1 * b2 - a2 * b1

    if delta == 0:
        if a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1:
            return "Прямі співпадають"
        else:
            return "Прямі паралельні"

    x0 = (b1 * c2 - b2 * c1) / delta
    y0 = (a2 * c1 - a1 * c2) / delta

    distance_to_center = math.sqrt((x0 - XC) ** 2 + (y0 - YC) ** 2)

    if abs(distance_to_center - R) <= EPSILON:
        return f"Прямі перетинаються в точці ({x0:.2f}, {y0:.2f}), що лежить на околі"
    elif distance_to_center < R:
        return f"Прямі перетинаються в точці ({x0:.2f}, {y0:.2f}) усередині кола"
    else:
        return f"Прямі перетинаються в точці ({x0:.2f}, {y0:.2f}) поза колом"


def manual_mode():
    """Режим ручного вводу користувачем"""
    print("\n" + "-" * 50)
    print(" РУЧНИЙ РЕЖИМ ВВОДУ")
    print("-" * 50)

    lines_data = []
    for i in range(1, 3):
        print(f"\nВведіть параметри Прямої {i} (Ax + By + c = 0):")
        while True:
            a = input("a: ")
            b = input("b: ")
            c = input("c: ")

            is_valid, result = validate_line_data(a, b, c)
            if is_valid:
                lines_data.extend(result)
                break
            else:
                print(f"❌ {result}")

    output = analyze_intersection(*lines_data)
    print("\n" + "=" * 50)
    print(" РЕЗУЛЬТАТ РОЗРАХУНКУ:")
    print(f" >>> {output}")
    print("=" * 50 + "\n")


def run_automated_tests():
    """Автоматизоване тестування з красивим виводом таблиці"""
    print("\nГенерація Таблиці 1 (Результати тестування)...\n")

    test_cases = [
        ("Обидві прямі — ліва границя класу", -128, -128, -128, -128, -128, -128),
        ("Обидві прямі — права границя класу", 128, 128, 128, 128, 128, 128),
        ("Обидві прямі — типове значення (середина)", 1, -1, 25, 1, 1, -31),
        ("1-а: найбл. до лівої, 2-а: найбл. до правої", -127, 10, 10, 127, 10, 10),
        ("1-а: найбл. до лівої, 2-а: типове значення", -127, -127, -127, 1, 1, 1),
        ("1-а: типове значення, 2-а: найбл. до правої", 1, -1, 0, 127, 127, 127),
        ("Вихід за ліву границю (недопустиме число)", -129, 10, 10, 10, 10, 10),
        ("Вихід за праву границю (недопустиме число)", 129, 10, 10, 10, 10, 10),
        ("Порушення логіки: a=0 та b=0", 0, 0, 15, 10, 10, 10),
        ("Введення нечислових даних (літери)", "a", "b", "c", 10, 10, 10),
    ]

    # Підготовка даних
    table_data = []
    headers = [
        "№",
        "Опис тестового випадку",
        "Вхідні дані (a1, b1, c1; a2, b2, c2)",
        "Дійсний результат (реакція програми)",
    ]

    for i, test in enumerate(test_cases, 1):
        desc = test[0]
        inputs = test[1:]

        is_valid_1, res1 = validate_line_data(inputs[0], inputs[1], inputs[2])
        if not is_valid_1:
            reaction = res1
        else:
            is_valid_2, res2 = validate_line_data(inputs[3], inputs[4], inputs[5])
            if not is_valid_2:
                reaction = res2
            else:
                reaction = analyze_intersection(*inputs)

        inputs_str = f"({inputs[0]}, {inputs[1]}, {inputs[2]}); ({inputs[3]}, {inputs[4]}, {inputs[5]})"
        table_data.append([str(i), desc, inputs_str, reaction])

    col_widths = [len(h) for h in headers]
    for row in table_data:
        for i in range(len(row)):
            if len(row[i]) > col_widths[i]:
                col_widths[i] = len(row[i])

    def print_separator():
        segments = ["-" * (w + 2) for w in col_widths]
        print("+" + "+".join(segments) + "+")

    def print_row(row_data):
        segments = [
            f" {row_data[i].ljust(col_widths[i])} " for i in range(len(row_data))
        ]
        print("|" + "|".join(segments) + "|")

    print_separator()
    print_row(headers)
    print_separator()
    for row in table_data:
        print_row(row)
    print_separator()


def main():
    print("=" * 60)
    print(" ПРАКТИЧНА РОБОТА №1. ТЕСТУВАННЯ ТА ВІДЛАГОДЖЕННЯ")
    print(" Виконав: студент Литвиненко Дмитро")
    print("-" * 60)
    print(" === ПАРАМЕТРИ ВАРІАНТУ ===")
    print(f" Діапазон вхідних значень (a, b, c): [{MIN_VAL}; {MAX_VAL}]")
    print(f" Центр кола (Xc, Yc):                ({XC}; {YC})")
    print(f" Радіус кола (R):                    {R}")
    print("=" * 60)

    print("\nОБЕРІТЬ РЕЖИМ РОБОТИ:")
    print("1 - Ручний режим (введення значень з клавіатури)")
    print("2 - Автоматичне тестування (генерація звіту для Таблиці 1)")

    choice = input("\nВаш вибір (1 або 2): ")

    if choice == "1":
        manual_mode()
    elif choice == "2":
        run_automated_tests()
    else:
        print("Невідомий вибір. Завершення програми.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограму примусово завершено користувачем. До побачення!")
        sys.exit(0)
