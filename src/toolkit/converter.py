from decimal import Decimal, getcontext, ROUND_HALF_UP
from .errors import ValidationError

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP

conversion_rates = {
    "g": Decimal("1"),
    "kg": Decimal("1000"),
    "mm": Decimal("1"),
    "cm": Decimal("10"),
    "m": Decimal("1000"),
    "km": Decimal("1000000"),
}

absolute_zero_values = {
    "k": Decimal("0"),
    "c": Decimal("-273.15"),
    "f": Decimal("-459.67")
}


def convert_units(input_value: str, source_unit: str, target_unit: str) -> Decimal:
    numeric_val = Decimal(input_value)
    src_mode = source_unit.lower()
    dst_mode = target_unit.lower()

    if src_mode in absolute_zero_values and numeric_val < absolute_zero_values[src_mode]:
        raise ValidationError(
            f"Физическая ошибка: {numeric_val}{src_mode.upper()} ниже абсолютного нуля."
        )

    if src_mode in conversion_rates:
        if dst_mode not in conversion_rates:
            raise ValidationError(f"Несовместимый тип конвертации: {src_mode} -> {dst_mode}")

        weight_group = {"g", "kg"}
        if (src_mode in weight_group) != (dst_mode in weight_group):
            raise ValidationError(f"Нельзя переводить массу в длину ({src_mode} -> {dst_mode})")

        base_scale = numeric_val * conversion_rates[src_mode]
        return (base_scale / conversion_rates[dst_mode]).normalize()

    if src_mode == "c":
        celsius_temp = numeric_val
    elif src_mode == "f":
        celsius_temp = (numeric_val - Decimal("32")) / Decimal("1.8")
    elif src_mode == "k":
        celsius_temp = numeric_val - Decimal("273.15")
    else:
        raise ValidationError(f"Неподдерживаемая единица: '{src_mode}'")

    if dst_mode == "c":
        final_score = celsius_temp
    elif dst_mode == "f":
        final_score = (celsius_temp * Decimal("1.8")) + Decimal("32")
    elif dst_mode == "k":
        final_score = celsius_temp + Decimal("273.15")
    else:
        raise ValidationError(f"Невозможно перевести в единицу: '{dst_mode}'")

    return final_score.normalize()
