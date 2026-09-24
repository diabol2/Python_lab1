from decimal import Decimal, getcontext, ROUND_HALF_UP
from .tokenizator import is_number, normalize_unary
from .errors import CalculationError

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP

def calculate_rpn_decimal(rpn_tokens):
    stack = []

    for token in rpn_tokens:
        if is_number(token):
            stack.append(Decimal(token))
        else:
            if len(stack) < 2:
                raise CalculationError("Математическая ошибка: оператору не хватает чисел для вычисления.")

            right = stack.pop()
            left = stack.pop()

            if token == '+':
                result = left + right
            elif token == '-':
                result = left - right
            elif token == '*':
                result = left * right
            elif token == '/':
                if right == Decimal('0'):
                    raise CalculationError("Критическая ошибка: деление на ноль невозможно.")
                result = left / right
            else:
                raise CalculationError(f"Синтаксическая ошибка: неизвестный оператор '{token}'.")

            stack.append(result)

    if len(stack) != 1:
        raise CalculationError("Синтаксическая ошибка: выражение составлено неверно (пропущен оператор).")

    return stack[0].normalize()
