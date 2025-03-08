import pytest

from src.decorators import log


def test_log_to_console(capsys):
    @log()
    def add(a, b):
        return a + b

    add(1, 2)
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_file(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def div(a, b):
        return a / b

    div(4, 2)
    with open(log_file) as f:
        assert "div ok" in f.read()


def test_error_logging(capsys):
    @log()
    def fail_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        fail_func()
    captured = capsys.readouterr()
    assert "fail_func error: ValueError" in captured.out
    assert "Inputs: (), {}" in captured.out
