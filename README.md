# Инструмент для обновления кодов ОКТМО в базе данных

Этот Python-скрипт предназначен для обновления кодов ОКТМО и названий населенных пунктов в базе данных PostgreSQL, в таблицах схемы `автоформа`. Скрипт подключается к базе данных и предоставляет два основных функционала:
1. Обновление кода ОКТМО для населенного пункта.
2. Изменение названия населенного пункта.

## Требования

- Python 3.x
- Библиотека `psycopg2` для работы с PostgreSQL

Установка `psycopg2`:
```bash
pip install psycopg2
```

## Использование

1. Клонируйте репозиторий или загрузите файлы скрипта.

2. Запустите скрипт:

   ```bash
   python <название_файла>.py

## Введите данные для подключения к базе данных:

- **IP-адрес сервера базы данных**
- **Название базы данных**
- **Имя пользователя**
- **Пароль**

## Выберите нужное действие:

- **1:** Обновить код ОКТМО населенного пункта
- **2:** Изменить название населенного пункта

## Пример работы

### Вариант 1: Обновление кода ОКТМО

Скрипт запросит:

- **Старый ОКТМО** — текущий код ОКТМО в базе данных.
- **Новый ОКТМО** — новый код ОКТМО, который нужно установить.

**Процесс:**

1. Скрипт найдет населенный пункт по указанному старому коду ОКТМО.
2. Если населенный пункт найден, скрипт:
   - Установит `дата_искл` (дату окончания) для текущей записи.
   - Найдет `id_поселение` по префиксу нового ОКТМО (первые 8 цифр).
   - Вставит новую запись с новым ОКТМО, `id_поселение` и текущей датой.
   - Добавит запись в таблицу `перекодировочная`, связывая старый и новый коды ОКТМО.

### Вариант 2: Обновление названия населенного пункта

Скрипт запросит:

- **ОКТМО** — код ОКТМО населенного пункта.
- **Новое название** — новое название населенного пункта.

**Процесс:**

1. Скрипт найдет `id_нп` (ID) населенного пункта по ОКТМО.
2. Если населенный пункт найден, скрипт:
   - Установит `дата_искл` для текущей записи с названием.
   - Вставит новую запись с `id_нп`, текущим кодом ОКТМО и новым названием.

## Обработка ошибок

Скрипт обрабатывает ошибки подключения к базе данных и запросов, выводя сообщения об ошибках.  
В случае ошибки в процессе обновления транзакция откатывается, чтобы предотвратить частичное обновление данных.

## Структура кода

- **connect_db**: Подключается к базе данных PostgreSQL.
- **update_oktmo**: Обновляет коды ОКТМО для населенного пункта и управляет историческими данными.
- **update_np_name**: Обновляет название населенного пункта и управляет историческими данными.
