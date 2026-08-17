# 01-hello-cli

- CLI-утилита при помощи click: принимает имя и печатает приветствие на трёх языках (EN/ES/RU).

## Дата: 2026-08-17

## Задача

Сделать CLI через Click:
- аргумент/опция `--name`
- опция `--count` (сколько раз повторить)
- вывод на 3 языках
- тесты на pytest

Часть блока A («Python и инструменты») из roadmap justxor.

## Подход

1. Click вместо argparse (короче и удобнее)
2. `src/hello_cli/` layout + `pyproject.toml`
3. Тесты через `click.testing.CliRunner`

## Что сделал:

- CLI-утилита на Click: `--name`, `--count`
- Приветствие на 3 языках (EN / ES / RU)
- Тесты на pytest через `click.testing.CliRunner` (2 passed)
- Структура `src/hello_cli/` + `tests/`
- Editable install: `uv pip install -e .`
- Репозиторий `python-foundations`, коммиты, push на GitHub

## Что узнал / на чём споткнулся:

### **Git**
- Вложенный `.git` внутри `01-hello-cli` (от `uv init`) ломает `git add` в корне → удалить
- `.gitignore` — в корне `python-foundations`, с игнором `.venv/`

### **Окружение**
- `uv init` / `uv add` / `uv sync` делать **внутри** папки задачи (`01-hello-cli`), не в корне `python-foundations`
  python-foundations/         <--- не здесь
    ├── 01-hello-cli/         <--- вот здесь uv init + uv add 
- Запуск только через `uv run ...`, иначе подхватывается системный Python → `ModuleNotFoundError`
- После перехода на `src/`-layout нужен `uv pip install -e .`, иначе pytest не видит пакет `hello_cli`

### **Имена и структура**
- Модули Python — только `snake_case` (`hello_cli.py`), не дефис
- Папка задачи может быть `01-hello-cli` (дефис ок)
- Нормальная раскладка: `src/hello_cli/__main__.py` + `tests/test_hello.py`,т.е. вот так
  01-hello-cli/
  ├── src/
  │   └── hello_cli/
  │       ├── __init__.py # можно оставлять пустым
  │       └── __main__.py # или cli.py. Здесь основной код задачи.
  ├── tests/
  │   └── test_hello.py   # пишется код самого теста
  ├── pyproject.toml      # модифицированный по объёму в два раза от стока, созданным uv
  ├── .python-version     # указывается версия python в виртуальном окружении (не мной, автоматически)
  ├── uv.lock
  ├── README.md
  ├── 01-Notes.md
  └── .venv/              # не в git

### **Click и тесты**
- `if __name__ == "__main__":` нужен, чтобы CLI не запускался при `import` в тестах
- `CliRunner` — способ тестировать Click без реального терминала
- `from hello_cli.__main__ import hello` — обычный импорт функции из пакета
-  Узнал, что очень часто в pytest используют assert. Сама конструкция такая:
`assert условие`

```Python
# Если условие False — тест падает.
# Если True — идём дальше.
```

### Что бы улучшил:
- Сразу начинать с `src/` + `tests/`, не с плоского файла в корне

Как было:
```text
01-hello-cli/
  hello_cli.py      ← один .py прямо в корне папки задачи
  test_hello.py
```

Как стало:
```text
01-hello-cli/
  src/hello_cli/__main__.py
  tests/test_hello.py
```

- В `pyproject.toml` сразу прописывать `[project.scripts]` и `pythonpath` для pytest

- Notes и .README нужно разделять