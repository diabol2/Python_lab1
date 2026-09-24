import argparse
import sys
from .rpn import to_rpn
from .calculator import calculate_rpn_decimal
from .tokenizator import tokenize, is_number, normalize_unary
from .converter import convert_units
from .errors import ToolkitError


def format_float(a: float) -> str:
    """Форматирование вывода типа float"""
    return f"{a:.10f}".rstrip('0').rstrip('.')


def main():
    parser = argparse.ArgumentParser(
        prog="python -m toolkit",
        description="Математический калькулятор и конвертер величин"
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")

    calc_parser = subparsers.add_parser("calc", help="Вычислить математическое выражение")
    calc_parser.add_argument("expression", type=str, help="Выражение в кавычках (например, '2 + 3 * 4')")

    conv_parser = subparsers.add_parser("convert", help="Конвертировать единицы измерения")
    conv_parser.add_argument("value", type=str, help="Значение для конвертации")

    conv_parser.add_argument("--from", dest="from_unit", type=str, required=True,
                             help="Исходная единица (например, kg, m, c)")
    conv_parser.add_argument("--to", dest="to_unit", type=str, required=True,
                             help="Целевая единица (например, g, cm, f)")

    args = parser.parse_args()

    try:
        if args.command == "calc":
            tokens = tokenize(args.expression)
            normalized_tokens = normalize_unary(tokens)
            rpn_tokens = to_rpn(normalized_tokens)
            result = calculate_rpn_decimal(rpn_tokens)
            float_result = float(result)

            print(format_float(float_result))
            sys.exit(0)

        elif args.command == "convert":
            result = convert_units(args.value, args.from_unit, args.to_unit)
            print(result)
            sys.exit(0)

    except ToolkitError as e:
        print(f"Ошибка вычисления: {e}", file=sys.stderr)
        sys.exit(2)

    except Exception as e:
        print(f"Ошибка вычисления: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
