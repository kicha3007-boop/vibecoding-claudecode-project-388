"""Отправка сообщения в Telegram: python send.py "текст".

Только стандартная библиотека. Токен и chat id — из переменных окружения TELEGRAM_BOT_TOKEN и
TELEGRAM_CHAT_ID или из файла .env рядом со скриптом. Без токена — пробный режим: текст печатается
в консоль, в Telegram ничего не уходит.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_URL = "https://api.telegram.org/bot{token}/sendMessage"
TIMEOUT_SECONDS = 15


def load_env(path):
    """Дописывает в окружение переменные из .env, не перетирая уже заданные."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def send(token, chat_id, text):
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    request = urllib.request.Request(API_URL.format(token=token), data=data)
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        body = json.load(response)
    if not body.get("ok"):
        raise RuntimeError(body.get("description", "Telegram вернул ошибку"))


def main(argv):
    # Консоль Windows по умолчанию не UTF-8 — русский текст и эмодзи печатались бы кракозябрами
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    if len(argv) < 2 or not argv[1].strip():
        print('Использование: python send.py "текст"', file=sys.stderr)
        return 2
    text = argv[1]

    load_env(Path(__file__).resolve().parent / ".env")
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не заданы — пробный режим, сообщение:")
        print(text)
        return 0

    try:
        send(token, chat_id, text)
    except urllib.error.HTTPError as error:
        print(f"Не отправлено: Telegram ответил {error.code}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, RuntimeError, TimeoutError) as error:
        print(f"Не отправлено: {error}", file=sys.stderr)
        return 1

    print("Отправлено.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
