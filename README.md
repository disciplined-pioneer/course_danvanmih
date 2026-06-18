# Инструкции по настройке проекта

## Шаг 1: Получение токена бота

1. Перейдите в [BotFather](https://t.me/BotFather)
2. Скопируйте токен вашего Telegram-бота

---

## Шаг 2: Создание виртуального окружения (venv)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Проверка (по желанию):

```bash
python --version
```

---

## Шаг 3: Загрузка переменных окружения

1. Создайте файл `.env` в корне проекта и заполните:

```
BOT_TOKEN=

POSTGRES_USER=
POSTGRES_NAME=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_PASSWORD=
```

---

## Шаг 4: Установка зависимостей

После активации venv:

```bash
pip install -r requirements.txt
```

## Шаг 5: Запуск

```bash
python bot.py
```
