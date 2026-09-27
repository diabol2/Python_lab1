from .errors import ValidationError
from .tokenizator import is_number, to_normal_view


def to_rpn(tokens):
    """Формируем список токенов с помощью алгоритма ОПН для дальнейшего вычисления стеком."""
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output = []
    stack = []
    for token in tokens:
        if is_number(token):
            output.append(token)
        elif token in precedence:
            while stack and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        else:
            raise ValidationError(f"Неизвестный токен: {token}")

    while stack:
        output.append(stack.pop())

    return output