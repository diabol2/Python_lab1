from decimal import Decimal, getcontext, ROUND_HALF_UP
from .tokenizator import is_number, to_normal_view
from .errors import CalculationError

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP


def calculate_rpn_decimal(rpn_tokens):
    """Вычисляет математическое выражение, переданное в виде списка токенов ОПН.

       Для выполнения операций используется стек. Чтобы избежать потери точности
       при работе с плавающей точкой, все вычисления производятся с помощью Decimal.
    """
    stack = []

    for token in rpn_tokens:
        if is_number(token):
            stack.append(Decimal(token))
        else:
            if len(stack) < 2:
                raise CalculationError("Оператору не хватает чисел для вычисления")

            right = stack.pop()
            left = stack.pop()

            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            elif token == "/":
                if right == Decimal('0'):
                    raise CalculationError("Деление на ноль невозможно")
                result = left / right
            else:
                raise CalculationError(f"Неизвестный оператор: '{token}'")

            stack.append(result)

    if len(stack) != 1:
        raise CalculationError("Выражение составлено неверно - пропущен оператор")

    return stack[0].normalize()