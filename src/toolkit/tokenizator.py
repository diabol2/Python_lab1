import re
from decimal import Decimal, InvalidOperation, getcontext

from .errors import TokenizationError, ValidationError

getcontext().prec = 10

token_pattern = r"\s*(\d+(?:\.\d+)?|[+*/\-])"

def tokenize(expression):
    """Разбиение полученного выражения на токены.

    Прохоидится по выражению и с помощью регулярных выражений ищет цепочки,
    подходящие под заданный паттерн, добавляет в список и идет до конца.
    """
    expression = expression.strip()
    tokens = []
    position = 0

    while position < len(expression):
        match = re.match(token_pattern, expression[position:])

        if match is None:
            raise TokenizationError(f"Недопустимый символ на позиции {position}")
        matched_group = match.group(1)

        tokens.append(matched_group)

        position += match.end()
    return tokens


def is_number(token):
    """Проверка токена на то, является ли он числом."""
    try:
        Decimal(token)
        return True
    except InvalidOperation:
        return False


def to_normal_view(tokens):
    """Преобразование списка токенов в понятный вид.

    Склеивает унарные плюсы и минусы перед числами в единый знак,
    формирут удобный список токенов для дальнейшего алгоритма ОПН,
    а также проверяет полученный список токенов на корректность.
    """
    if not tokens:
        raise ValidationError("Ожидалось число")

    result = []
    number_flag = True
    i = 0

    while i < len(tokens):
        if number_flag:
            sign = 1
            while i < len(tokens) and tokens[i] in ("+", "-"):
                if tokens[i] == "-":
                    sign *= -1
                i += 1

            if i >= len(tokens):
                raise ValidationError("Ожидалось число")

            number = tokens[i]
            if not is_number(number):
                raise ValidationError(f"Ожидалось число вместо {number}")
            if sign == -1:
                result.append("-" + number)
            else:
                result.append(number)

            i += 1
            number_flag = False

        else:
            token = tokens[i]
            if token not in ("+", "-", "*", "/"):
                raise ValidationError(f"Ожидался оператор вместо {token}")

            result.append(token)
            i += 1
            number_flag = True

    if number_flag:
        raise ValidationError("Ожидалось число")

    return result
