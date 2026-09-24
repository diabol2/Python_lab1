import re
from decimal import Decimal, getcontext, InvalidOperation
from .errors import TokenizationError, ValidationError, CalculationError

getcontext().prec = 10

TOKEN_PATTERN = r"\s*(\d+(?:\.\d+)?|[+*/\-])"

def tokenize(expression):
    tokens = []
    position = 0
    length = len(expression)

    while position < length:
        match = re.match(TOKEN_PATTERN, expression[position:])

        if match is None:
            raise TokenizationError(f"Недопустимый символ на позиции {position}")

        matched_value = match.group(1)

        tokens.append(matched_value)

        position += match.end()

    return tokens



def is_number(token):
    try:
        Decimal(token)
        return True
    except InvalidOperation:
        return False


def normalize_unary(tokens):
    if not tokens:
        raise ValidationError("Ожидалось число")

    result = []
    expect_number = True
    i = 0

    while i < len(tokens):
        if expect_number:
            sign = 1
            while i < len(tokens) and tokens[i] in ("+", "-"):
                if tokens[i] == "-":
                    sign *= -1
                i += 1

            if i >= len(tokens):
                raise ValidationError("Ожидалось число")

            number = tokens[i]
            if not is_number(number):
                raise ValidationError(f"Ожидалось число, введите число вместо {number}")

            if sign == -1:
                result.append("-" + number)
            else:
                result.append(number)

            i += 1
            expect_number = False
        else:
            token = tokens[i]
            if token not in {"+", "-", "*", "/"}:
                raise ValidationError(f"Ожидался оператор, получен {token}")

            result.append(token)
            i += 1
            expect_number = True

    if expect_number:
        raise ValidationError("Ожидалось число")

    return result



