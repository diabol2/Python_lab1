from .errors import ValidationError
from .tokenizator import is_number, normalize_unary

def to_rpn(tokens):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
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