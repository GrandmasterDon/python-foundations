from click.testing import CliRunner
from hello_cli.__main__ import hello  # пакет hello_cli; модуль __main__; функция hello


def test_hello_three_languages():
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "Anna"])

    assert result.exit_code == 0
    assert "Hello, Anna!" in result.output
    assert "Hola, Anna!" in result.output
    assert "Привет, Anna!" in result.output


def test_hello_count():
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "Bob", "--count", "2"])

    assert result.exit_code == 0
    assert result.output.count("Hello, Bob!") == 2
