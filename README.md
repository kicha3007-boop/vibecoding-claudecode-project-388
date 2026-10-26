# Трекер цен с Claude


[![hexlet-check](https://github.com/kicha3007-boop/vibecoding-claudecode-project-388/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kicha3007-boop/vibecoding-claudecode-project-388/actions)

Соберите на Claude-скиллах трекер цен: он сам следит за товарами и присылает в Telegram только значимые изменения.

Учебный проект Хекслета: https://ru.hexlet.io/programs/vibecoding-claudecode


## Стек

- Claude Code: скиллы, сабагент, MCP
- GitHub MCP — хранение прогонов в приватном репозитории `tracker-data`
- Python 3 (только стандартная библиотека) — отправка в Telegram

Полный цикл: список URL → `extract-price` на каждый → таблица прогона → сохранение `YYYY-MM-DD.json` в
`tracker-data` → сравнение с прошлым прогоном по правилам `KNOWLEDGE.md` → сводка значимых изменений в
Telegram.

```text
.claude/skills/extract-price/SKILL.md   # один URL → { regular_price, sale_price, has_credit }
.claude/skills/tracker/SKILL.md         # список URL, таблица, хранение, diff, Telegram
.claude/agents/tg-summary.md            # текст сводки на Haiku
KNOWLEDGE.md                            # правила значимости и оформление сводки
send.py                                 # python send.py "текст" → Telegram
.mcp.json                               # GitHub MCP, токен из ${GITHUB_MCP_PAT}
.env.example                            # какие переменные нужны (.env — в .gitignore)
```

Ниша — книги демо-магазина books.toscrape.com (стабильные страницы, цена без логина). Своя ниша —
заменить таблицу URL в `.claude/skills/tracker/SKILL.md`.

## Установка

```bash
git clone https://github.com/kicha3007-boop/vibecoding-claudecode-project-388.git
cd vibecoding-claudecode-project-388
cp .env.example .env    # заполнить значения
```

Что подготовить один раз:

1. **Telegram.** В `@BotFather` — `/newbot`, токен в `TELEGRAM_BOT_TOKEN`; свой chat id (`@userinfobot`)
   в `TELEGRAM_CHAT_ID`. Обязательно написать своему боту любое сообщение — иначе он не сможет написать
   первым. Проверка: `python send.py "тест"` → `Отправлено.` и сообщение в Telegram.
2. **Хранилище прогонов.** На GitHub — новый **приватный** репозиторий `tracker-data` (с README).
   `TRACKER_DATA_REPO=<логин>/tracker-data`.
3. **GitHub MCP.** Fine-grained токен только на `tracker-data`: `Contents: Read and write`,
   `Metadata: Read-only`. Перед запуском Claude Code: `export GITHUB_MCP_PAT=<токен>` — `.mcp.json`
   подставит его сам. В Claude Code `/mcp` должен показать `github` — `connected`. Если 403 и с верным
   токеном — доступ к GitHub MCP аккаунту не выдан; трекер тогда пишет в `tracker-data` обычным `git`
   с тем же токеном (описано в скилле).

## Использование

В Claude Code в корне репозитория (локально `claude` или на `claude.ai/code`):

```text
> запусти трекер
```

Трекер обойдёт список, покажет таблицу, сохранит прогон, сравнит с прошлым и пришлёт сводку. Чтобы
увидеть diff в первый же день — поправить пару цен в последнем файле `tracker-data` и запустить снова.
Отдельно проверить одну страницу:

```text
> extract-price https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
{ "regular_price": 51.77, "sale_price": null, "has_credit": false }
```

### Без внешних сервисов

- Без Telegram: не задавать `TELEGRAM_BOT_TOKEN` — `send.py` напечатает сводку в консоль (пробный режим).
- Без GitHub: `TRACKER_DATA_DIR=tracker-data` — прогоны пишутся в локальную папку (она в `.gitignore`).

Так весь цикл прогоняется на своём компьютере, а внешние сервисы подключаются, когда будут готовы.

### Секреты

Токен бота, chat id и токен GitHub — только в `.env` или переменных окружения; в скиллах, README и
истории коммитов их нет. Засветился токен бота — `/revoke` в `@BotFather`; токен GitHub — отозвать на
`github.com/settings/personal-access-tokens`.

> Статус: файлы инструмента готовы, ссылки и `send.py` проверены (пробный режим и ответ Telegram на
> неверный токен). Живой прогон с ботом и `tracker-data` ещё не делался — нужны свои токены по шагам выше.

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
