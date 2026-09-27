from decimal import Decimal, getcontext, ROUND_HALF_UP
from .errors import ConversionError

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP

conversion_rates = {
    "g": Decimal("1"),
    "kg": Decimal("1000"),
    "mm": Decimal("1"),
    "cm": Decimal("10"),
    "dm": Decimal("100"),
    "m": Decimal("1000"),
    "km": Decimal("1000000"),
}

absolute_zero_values = {
    "k": Decimal("0"),
    "c": Decimal("-273.15"),
    "f": Decimal("-459.67")
}


def convert_units(input_value: str, source_unit: str, target_unit: str) -> Decimal:
    """Конвертирует значение из одной единицы измерения в другую.

       Функция поддерживает перевод мер длины (mm, cm, dm, m, km), массы (g, kg) и
       температуры (C, F, K). Вычисления производятся с использованием модуля Decimal
       для сохранения точности. При переводе температур проверяется достижение
       абсолютного нуля. При переводе мер длины и массы проверяется их совместимость.
    """
    numeric_val = Decimal(input_value)
    source_mode = source_unit.lower()
    target_mode = target_unit.lower()

    if source_mode in absolute_zero_values and numeric_val < absolute_zero_values[source_mode]:
        raise ConversionError(
            f"Ошибка: {numeric_val}{source_mode.upper()} ниже абсолютного нуля"
        )

    if source_mode in conversion_rates:
        if target_mode not in conversion_rates:
            raise ConversionError(f"Несовместимый тип конвертации: ({source_mode} -> {target_mode})")

        weight_group = {"g", "kg"}
        if (source_mode in weight_group) != (target_mode in weight_group):
            raise ConversionError(f"Нельзя переводить массу в длину ({source_mode} -> {target_mode})")

        base_scale = numeric_val * conversion_rates[source_mode]
        return (base_scale / conversion_rates[target_mode]).normalize()

    if source_mode == "c":
        celsius_temp = numeric_val
    elif source_mode == "f":
        celsius_temp = (numeric_val - Decimal("32")) / Decimal("1.8")
    elif source_mode == "k":
        celsius_temp = numeric_val - Decimal("273.15")
    else:
        raise ConversionError(f"Неподдерживаемая единица: '{source_mode}'")

    if target_mode == "c":
        final_score = celsius_temp
    elif target_mode == "f":
        final_score = (celsius_temp * Decimal("1.8")) + Decimal("32")
    elif target_mode == "k":
        final_score = celsius_temp + Decimal("273.15")
    else:
        raise ConversionError(f"Невозможно перевести в: '{target_mode}'")

    return final_score.normalize()
