import argparse
import re
import sys

from .calculator import calculate_rpn_decimal
from .converter import convert_units
from .errors import ToolkitError
from .rpn import to_rpn
from .tokenizator import to_normal_view, tokenize


def to_float(exp: float) -> str:
    """Форматирование вывода.

    Обрабатывает полученное число (например из 5.0 делает просто 5).
    Decimal делает вычисление точным, если число настолько крошечное, что
    появляются E то функция это предотвращает и делает число полноценным.
    """
    float_result = f"{exp:.12f}".rstrip("0").rstrip(".")
    if float_result in ("0", "-0") or "e" in float_result.lower():
        from decimal import Decimal

        res_dec = Decimal(str(exp))
        if res_dec == 0:
            res_dec = res_dec + Decimal(0)
        float_result = f"{res_dec:f}".rstrip("0").rstrip(".")

    if float_result == "-0":
        float_result = "0"

    return float_result


def main():
    """Главная функция для запуска программы из терминала.

    Она настраивает интерфейс командной строки, чтобы программа понимала
    три команды: "calc" (для калькулятора) и "convert" (для конвертера)
    и --help (для справки).
    Также функция ловит ошибки в процессе вычислений и выводит их на экран.
    """
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
    calc_parser._negative_number_matcher = re.compile(r'^-.+')
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

    except (ToolkitError, Exception) as e: # noqa: BLE001
        print(f"Ошибка вычисления: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
