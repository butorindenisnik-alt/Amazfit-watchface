# DEAL_ГНБ — фирменный циферблат Amazfit Balance 2

## Актуальная тестовая версия v1.1.1 — интерактивные зоны

- [Установочный пакет ZPK v1.1.1](releases/DEAL_GNB_Balance2_Official_1.1.1.zpk)
- [Zeus CLI, успешная сборка](https://github.com/butorindenisnik-alt/Amazfit-watchface/actions/runs/44010752943)
- QR строка: `zpkd1://raw.githubusercontent.com/butorindenisnik-alt/Amazfit-watchface/main/releases/DEAL_GNB_Balance2_Official_1.1.1.zpk`

Невидимые сенсорные зоны на обычном экране:
- **Минуты** (x255–372, y202–295): открывает штатный **обратный отсчёт**.
- **Пульс** (x258–332, y338–413): открывает штатное приложение **Пульс**.
- **Погода** (x340–414, y338–413): открывает штатную **Погоду**.

Для AOD касания отключены. Графика, расположение секунд, дата, шаги, батарея и AOD унаследованы от v1.1.0 без изменений. Все три ссылки используют официальные системные идентификаторы Zepp OS и `@zos/router`.

**Статус:** компиляция Zeus CLI и целостность архива подтверждены, фактические переходы на Amazfit Balance 2 требуют проверки на часах.

[Вернуться на проверенную v1.1.0](releases/DEAL_GNB_Balance2_Official_1.1.0.zpk)
