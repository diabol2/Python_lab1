
import sys
import pytest
from toolkit.__main__ import main


def test_cli_convert_success(monkeypatch, capsys):
    """Проверяет успешный запуск команды convert с флагами --from и --to."""
    monkeypatch.setattr(
        sys, "argv", ["__main__.py", "convert", "1000", "--from", "MM", "--to", "M"]
    )

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 0

    captured = capsys.readouterr()
    assert captured.out.strip() == "1"


def test_cli_convert_error_handling(monkeypatch, capsys):
    """Проверяет, что ошибки конвертера (например, кг в метры) возвращают код 2."""
    monkeypatch.setattr(
        sys, "argv", ["__main__.py", "convert", "5", "--from", "kg", "--to", "m"]
    )

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 2

    captured = capsys.readouterr()
    assert "Ошибка вычисления:" in captured.err


def test_cli_shows_help_message(monkeypatch):
    """Проверяет, что при вызове --help программа успешно выводит справку и выходит с кодом 0."""
    monkeypatch.setattr(sys, "argv", ["__main__.py", "--help"])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 0


def test_cli_catches_toolkit_errors(monkeypatch, capsys):
    """Проверяет, что внутренние ошибки (например, деление на ноль) красиво перехватываются и возвращают код 2."""
    monkeypatch.setattr(sys, "argv", ["__main__.py", "calc", "5 / 0"])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 2

    captured = capsys.readouterr()
    assert "Критическая ошибка: деление на ноль невозможно." in captured.err


def test_cli_calculates_correct_response(monkeypatch, capsys):
    """Проверяет успешное вычисление стандартного выражения через команду calc."""
    monkeypatch.setattr(sys, 'argv', ['__main__.py', 'calc', '2 + 3 / 3 * 5 + 1'])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 0

    # Математика: 2 + (3 / 3 * 5) + 1 -> 2 + 5 + 1 = 8
    captured = capsys.readouterr()
    assert captured.out.strip() == '8'


def test_cli_formats_small_float_correctly(monkeypatch, capsys):
    """Проверяет, что дробные результаты выводятся в правильном формате без экспоненциальной записи."""
    monkeypatch.setattr(sys, 'argv', ['__main__.py', 'calc', '1 / 1000000'])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 0

    captured = capsys.readouterr()
    assert captured.out.strip() == '0.000001'
