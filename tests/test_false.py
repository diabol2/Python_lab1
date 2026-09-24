import pytest
from src.toolkit.converter import convert_units
from src.toolkit.tokenizator import tokenize, normalize_unary
from src.toolkit.rpn import to_rpn
from src.toolkit.calculator import calculate_rpn_decimal
from src.toolkit.errors import TokenizationError, ValidationError, CalculationError


def test_invalid_characters():
    """Проверяем, что на буквы и запрещенные символы летит TokenizationError."""
    with pytest.raises(TokenizationError):
        tokenize("2 + abc")
    with pytest.raises(TokenizationError):
        tokenize("5 * @")


def test_empty_expression():
    """Проверяем, что пустая строка вызывает ValidationError."""
    tokens = tokenize("")
    with pytest.raises(ValidationError):
        normalize_unary(tokens)


def test_broken_structure():
    """Проверяем ошибку структуры выражения (например, забыли число после бинарного знака)."""
    tokens = tokenize("5 +")
    with pytest.raises(ValidationError):
        normalize_unary(tokens)


def test_division_by_zero():
    """Проверяем, что при делении на ноль выбрасывается CalculationError."""
    tokens = tokenize("10 / 0")
    rpn = to_rpn(normalize_unary(tokens))

    with pytest.raises(CalculationError):
        calculate_rpn_decimal(rpn)


def test_missing_operands():
    """Проверяем ошибку, когда операторы идут подряд без чисел."""
    tokens = tokenize("5 + * 3")
    with pytest.raises(ValidationError):
        normalize_unary(tokens)





def test_converter_absolute_zero_error():
    """Проверяем падение при температуре ниже абсолютного нуля."""
    with pytest.raises(ValidationError):
        convert_units("-1", "k", "c")
    with pytest.raises(ValidationError):
        convert_units("-300", "c", "k")

def test_converter_incompatible_units():
    """Проверяем запрет перевода массы в длину (килограммы в метры)."""
    with pytest.raises(ValidationError):
        convert_units("10", "kg", "m")

def test_converter_unknown_units():
    """Проверяем падение при вводе несуществующей единицы."""
    with pytest.raises(ValidationError):
        convert_units("5", "cm", "xyz")
    with pytest.raises(ValidationError):
        convert_units("20", "abc", "kg")