---
name: tracker
description: Обходит зашитый список URL товаров, для каждого вызывает скилл extract-price и собирает таблицу прогона; сохраняет прогон в приватный репозиторий tracker-data (YYYY-MM-DD.json), сравнивает с прошлым прогоном по правилам KNOWLEDGE.md и отправляет сводку значимых изменений в Telegram через send.py. Применять по фразам «запусти трекер», «прогон цен», «что с ценами».
---

# tracker

## Список товаров

Ниша — книги (демо-магазин books.toscrape.com: стабильные ссылки, цена видна без логина). Чтобы следить за
своей нишей, замени список ниже — остальное менять не нужно.

| Товар | URL |
|---|---|
| A Light in the Attic | https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html |
| Tipping the Velvet | https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html |
| Soumission | https://books.toscrape.com/catalogue/soumission_998/index.html |
| Sharp Objects | https://books.toscrape.com/catalogue/sharp-objects_997/index.html |
| Sapiens | https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html |
| The Requiem Red | https://books.toscrape.com/catalogue/the-requiem-red_995/index.html |

## Сценарий прогона

### 1. Таблица прогона

Для **каждого** URL списка вызови скилл `extract-price` — логику извлечения здесь не повторяй. Собери
результаты в один JSON — таблицу прогона, одна строка на товар:

```json
{
  "date": "2026-10-26",
  "items": [
    { "title": "A Light in the Attic", "url": "https://…", "regular_price": 51.77, "sale_price": null, "has_credit": false }
  ]
}
```

Товар, по которому `extract-price` вернул `null`-цены, остаётся в таблице — правила KNOWLEDGE.md решают,
что с ним делать. Покажи таблицу пользователю (Markdown: товар · обычная · со скидкой · рассрочка).

### 2. Предыдущий прогон

Хранилище — отдельный **приватный** репозиторий `tracker-data` (владелец — из `TRACKER_DATA_REPO`,
формат `owner/tracker-data`). Через GitHub MCP:

1. получи список файлов в корне `tracker-data` (`get_file_contents` с путём `/`);
2. возьми файлы вида `YYYY-MM-DD.json`, кроме сегодняшнего, выбери последний по дате и прочитай его —
   это предыдущий прогон;
3. файлов нет — это первый запуск, сравнивать не с чем.

### 3. Diff и значимость

Сопоставь товары по `url`. Для каждого сравни `regular_price`, `sale_price`, `has_credit`. Отметь новые
товары (нет в прошлом прогоне) и пропавшие (нет в текущем). Затем примени правила из `KNOWLEDGE.md` и
оставь только значимые изменения. Первый прогон — сводка «📸 Первый прогон — снимок цен» со всеми
товарами.

### 4. Сохранение

Через GitHub MCP (`create_or_update_file`) закоммить таблицу прогона в корень `tracker-data` как
`YYYY-MM-DD.json` (дата прогона), сообщение коммита — `Прогон YYYY-MM-DD`. Файл уже есть (второй прогон
за день) — обнови его, передав `sha` текущей версии. Локальный `git clone` для этого не нужен.

### 5. Telegram

Сводка — одна строка на значимое изменение, формат и эмодзи — в `KNOWLEDGE.md` («Оформление сводки»).
Текст сводки делегируй сабагенту `tg-summary` (модель Haiku): передай ему список значимых изменений и
получи готовый текст. Отправь его командой:

```bash
python send.py "<текст сводки>"
```

(`python3`, если `python` нет.) Значимых изменений нет — отправь `Значимых изменений цен нет`.
Ожидаемый вывод скрипта — `Отправлено.`

## Без GitHub MCP и без Telegram

- `/mcp` не показывает `github` или отвечает 403 — те же шаги 2 и 4 делай обычным `git` с тем же токеном:
  `git clone https://x-access-token:$GITHUB_MCP_PAT@github.com/$TRACKER_DATA_REPO.git tracker-data`,
  затем чтение/запись файла, `git commit`, `git push`.
- Локальная репетиция без сети к GitHub: если задана `TRACKER_DATA_DIR`, читай и пиши прогоны в этой
  папке (её содержимое в репозиторий скиллов не коммитится — `tracker-data/` в `.gitignore`).
- `TELEGRAM_BOT_TOKEN` не задан — `send.py` печатает сводку в консоль и сообщает, что это пробный режим.

Секреты (токены, chat id) не выводи в ответах и не записывай в файлы репозитория.
