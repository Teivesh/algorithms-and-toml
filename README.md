# Algorithms and TOML

Учебный Python-проект: массив (список Python), односвязный список, дек, AVL-дерево, пузырьковая и быстрая сортировки, а также конвертер TOML в JSON.

## Требования

- Python 3.11 или новее (для стандартного модуля `tomllib`).
- Тесты используют встроенный `unittest`, дополнительные зависимости не нужны.

## Запуск

```bash
python -m unittest discover -s tests -v
python -m algorithms_and_toml.toml_json input.toml output.json
```

Конвертер требует как минимум три поля верхнего уровня. Массивы в JSON отсортированы стабильно; для массивов смешанных JSON-типов используется детерминированный порядок по типу и значению.

## Структура

- `src/algorithms_and_toml/structures/` — динамический массив, связный список, двусторонняя очередь и AVL-дерево.
- `src/algorithms_and_toml/sorting.py` — bubble sort и quicksort, возвращающие новые списки.
- `src/algorithms_and_toml/toml_json.py` — проверка документа TOML и преобразование в JSON.
- `tests/` — модульные тесты.
- `.github/workflows/ci.yml` — запуск тестов на Python 3.11–3.13 при push и pull request.
