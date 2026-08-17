# hello-cli

CLI-утилита: принимает имя и печатает приветствие на трёх языках (EN / ES / RU).

## Задача

Учебный проект из блока A (задача 1) roadmap justxor («Python и инструменты»):

- CLI на [Click](https://click.palletsprojects.com/)
- опции `--name` и `--count`
- вывод приветствия на 3 языках
- тесты на pytest

## Требования

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)

## Установка

```bash
cd 01-hello-cli
uv sync
uv pip install -e .
```

## Использование

```bash
uv run hello-cli --name Anna
uv run hello-cli --name Bob --count 2
```

Пример вывода:
```text
Hello, Anna!
Hola, Anna!
Привет, Anna!
```

## Тесты
```bash
uv run pytest -v # --verbose подробный режим вывода при запуске тестов
```

## Структура
01-hello-cli/
├── src/hello_cli/
│   ├── __init__.py
│   └── __main__.py      # CLI
├── tests/
│   └── test_hello.py
├── pyproject.toml
├── README.md
└── 01-Notes.md          # учебные заметки