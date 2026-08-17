# </> hello-cli

Минималистичная CLI-утилита на Python: принимает имя и печатает приветствие на трёх языках (EN / ES / RU).

Учебный проект из **блока A (задача 1)** roadmap [justxor](https://github.com/justxor/MachineLearningRoadmap#-%D0%B1%D0%BB%D0%BE%D0%BA-a-python-%D0%B8-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8-110) — «Python и инструменты».

## 🛠 Технологический стек

- **Python 3.13+**
- **[uv](https://github.com/astral-sh/uv)** — менеджер проектов и зависимостей
- **[Click](https://click.palletsprojects.com/)** — CLI-фреймворк
- **pytest** — тесты
- **CliRunner** — тестирование Click без реального терминала

## 🙌 Возможности

- опция `--name` — имя для приветствия
- опция `--count` — сколько раз повторить вывод (по умолчанию 1)
- приветствие сразу на **английском, испанском и русском**
- покрытие тестами (`2 passed`)

## 🚀 Установка

```bash
cd 01-hello-cli
uv sync
uv pip install -e .
```

## 🎮 Использование

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

## 🧪 Тесты
```bash
uv run pytest -v # --verbose подробный режим вывода при запуске тестов
```

## 📁 Структура проекта
```text
01-hello-cli/
├── src/
│   └── hello_cli/
│       ├── __init__.py
│       └── __main__.py      # CLI-логика
├── tests/
│   └── test_hello.py        # pytest + CliRunner
├── pyproject.toml           # зависимости и scripts
├── README.md
└── 01-Notes.md              # учебные заметки
```