import argparse
import sys
from .rpn import to_rpn
from .calculator import calculate_rpn_decimal
from .tokenizator import tokenize, is_number, to_normal_view
from .converter import convert_units
from .errors import ToolkitError

def to_float(exp: float) -> str:
    """Форматирование вывода"""
    float_result = f"{exp:.12f}".rstrip('0').rstrip('.')
    return float_result


def main():
    """Точка входа в консольное приложение."""
    parser = argparse.ArgumentParser(prog="Математический калькулятор и конвертер величин",
                                     epilog="Доступные команды:\n"
                                            "calc - Вычислить математическое выражение\n"
                                            "convert - Конвертировать единицы измерени\n"
                                            "                                           \n" 
                                            "Важно знать:\n"
                                            "Калькулятор - поддерживает операторы +, -, *, /, "
                                            "умеет обрабатывать цепочки унарных знаков\n"
                                            "(например ----5 + 10)\n"
                                            "На вход подается выражeние заключенное в одинарные либо двойные кавычки\n"
                                            "                                                                         \n"
                                            "Конвертер - единицы измерения, поддерживаемые конвертером:\n"
                                                        "Масса: g, kg\n"
                                                        "Длина: mm, cm, dm, m, km\n"
                                                        "Температура: c, f, k\n"
                                            "                                                              \n"
                                            "Примеры вызова функций калькулятора и конвертера:\n"
                                            'python3 -m toolkit calc "---25 + 7 * -10"\n'
                                            "python3 -m toolkit convert 1.5 --from kg --to g\n",
                                     formatter_class = argparse.RawDescriptionHelpFormatter
                                     )

    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calc")
    calc_parser.add_argument("expression", type=str)

    conv_parser = subparsers.add_parser("convert")
    conv_parser.add_argument("value", type=str)
    conv_parser.add_argument("--from", dest="from_unit", type=str, required=True)
    conv_parser.add_argument("--to", dest="to_unit", type=str, required=True)

    args = parser.parse_args()

    try:
        if args.command == "calc":
            tokens = tokenize(args.expression)
            normalized_tokens = to_normal_view(tokens)
            rpn_tokens = to_rpn(normalized_tokens)
            result = calculate_rpn_decimal(rpn_tokens)
            float_result = float(result)

            print(to_float(float_result))
            sys.exit(0)

        elif args.command == "convert":
            conv_result = float(convert_units(args.value, args.from_unit, args.to_unit))
            float_conv_result = to_float(conv_result)
            print(float_conv_result)
            sys.exit(0)

    except ToolkitError as e:
        print(f"Ошибка вычисления: {e}", file=sys.stderr)
        sys.exit(2)

    except Exception as e:
        print(f"Ошибка вычисления: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()