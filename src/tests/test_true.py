import pytest
from decimal import Decimal
from toolkit.converter import convert_units
from toolkit.tokenizator import tokenize, normalize_unary
from toolkit.rpn import to_rpn
from toolkit.calculator import calculate_rpn_decimal

def run_calculator(expression: str) -> Decimal:
    """Вспомогательная функция, которая пропускает строку через весь конвейер."""
    tokens = tokenize(expression)
    normalized = normalize_unary(tokens)
    rpn = to_rpn(normalized)
    return calculate_rpn_decimal(rpn)


def test_complex_unary_chains():
    """Проверка сложных цепочек унарных знаков перед числами."""
    # ---10 +++-5 / 2 -> -10 + (-5 / 2) -> -10 + -2.5 = -12.5
    assert run_calculator("---10 +++-5 / 2") == Decimal("-12.5")

def test_basic_arithmetic():
    """Проверка стандартных базовых операций и приоритетов (умножение/деление первее)."""
    assert run_calculator("2 * 3 + 4 / 2") == Decimal("8")
    assert run_calculator("10 - 2 * 4") == Decimal("2")

def test_single_number_with_unary():
    """Проверка выражений, состоящих только из одного числа с унарными знаками."""
    assert run_calculator("-5") == Decimal("-5")
    assert run_calculator("+++7") == Decimal("7")
    assert run_calculator("---3") == Decimal("-3")

def test_decimal_numbers():
    """Проверка работы с числами, содержащими плавающую точку (Decimal)."""
    assert run_calculator("2.5 + 1.25 * 2") == Decimal("5")
    assert run_calculator("10.0 / 4") == Decimal("2.5")

def test_zero_operations():
    """Проверка математических операций с нулём (кроме деления на ноль)."""
    assert run_calculator("0 * 5 + 0 - 0") == Decimal("0")
    assert run_calculator("-0") == Decimal("0")





def test_converter_mass_success():
    """Проверка перевода единиц массы."""
    assert convert_units("5", "kg", "g") == Decimal("5000")
    assert convert_units("1500", "g", "kg") == Decimal("1.5")

def test_converter_length_success():
    """Проверка перевода единиц длины."""
    assert convert_units("1000", "mm", "m") == Decimal("1")
    assert convert_units("2.5", "km", "m") == Decimal("2500")
    assert convert_units("100", "cm", "m") == Decimal("1")

def test_converter_temperature_success():
    """Проверка перевода температур в разных направлениях."""
    # 0 градусов Цельсия = 273.15 Кельвина
    assert convert_units("0", "c", "k") == Decimal("273.15")
    # 100 градусов Цельсия = 212 Фаренгейта
    assert convert_units("100", "c", "f") == Decimal("212")
    # Из Фаренгейта в Цельсий
    assert convert_units("32", "f", "c") == Decimal("0")