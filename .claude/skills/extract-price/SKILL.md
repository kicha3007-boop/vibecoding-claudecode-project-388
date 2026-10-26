---
name: extract-price
description: Извлекает цену товара с одной страницы по URL и возвращает строго объект { regular_price, sale_price, has_credit }. Применять, когда нужна цена одного товара — в том числе из скилла tracker для каждого URL списка.
---

# extract-price

## Контракт

- **Вход:** один URL страницы товара.
- **Выход:** ровно один JSON-объект, без пояснений вокруг:

```json
{ "regular_price": 1919, "sale_price": 1599, "has_credit": true }
```

| Поле | Тип | Значение |
|---|---|---|
| `regular_price` | число или `null` | обычная цена (без скидки) |
| `sale_price` | число или `null` | цена со скидкой; `null`, если скидки нет |
| `has_credit` | `true` / `false` | на странице предложена рассрочка или кредит |

Если страницу не удалось загрузить или цена не найдена, верни
`{ "regular_price": null, "sale_price": null, "has_credit": false }` — и одну строку с причиной **после**
объекта, если её просят. Текст в свободной форме вместо объекта — ошибка контракта.

## Как извлекать

1. Загрузи HTML страницы: `curl -sL -A "Mozilla/5.0" "<URL>"` (или WebFetch). Не выполняй действий на
   странице — цена должна быть видна без логина и корзины.
2. Ищи цену в порядке надёжности:
   1. JSON-LD (`<script type="application/ld+json">`): `offers.price`, `offers.highPrice`/`lowPrice`;
   2. микроразметка и мета-теги: `itemprop="price"`, `meta[property="product:price:amount"]`;
   3. видимые элементы цены: классы вроде `price`, `price_color`, `old-price`, `price--old`, `sale`.
3. Две цены на странице: большая (зачёркнутая, «старая») — `regular_price`, меньшая — `sale_price`.
   Одна цена — это `regular_price`, `sale_price = null`.
4. Нормализация числа: убери валюту (`₽`, `руб.`, `£`, `$`, `€`), пробелы (в том числе неразрывные
   ` `, ` `), разделители тысяч; десятичную запятую замени точкой; результат — число
   (`"1 919 ₽"` → `1919`, `"£51.77"` → `51.77`). Валюту в объект не добавляй.
5. `has_credit = true`, если на странице есть явное предложение: «рассрочка», «в кредит», «Сплит»,
   «Долями», «installment», «Buy now, pay later». Иначе `false`.

## Проверка

На демо-странице `https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html` ответ:

```json
{ "regular_price": 51.77, "sale_price": null, "has_credit": false }
```
