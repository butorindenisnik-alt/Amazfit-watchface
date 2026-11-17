# DEAL_ГНБ — фирменный циферблат Amazfit Balance 2

## Актуальная тестовая версия v1.1.2 — календарь по нажатию на дату

- [Установочный пакет ZPK v1.1.2](releases/DEAL_GNB_Balance2_Official_1.1.2.zpk)
- [Zeus CLI: успешная сборка v1.1.2](https://github.com/butorindenisnik-alt/Amazfit-watchface/actions/runs/44011219907)
- QR строка: `zpkd1://raw.githubusercontent.com/butorindenisnik-alt/Amazfit-watchface/main/releases/DEAL_GNB_Balance2_Official_1.1.2.zpk`

Невидимые области на основном экране (480×480):
- Минуты (x255–372, y202–286): обратный отсчёт
- Дата (x85–395, y287–330): штатный календарь `SYSTEM_APP_CALENDAR`
- Пульс (x258–332, y338–413): штатное приложение пульса
- Погода (x340–414, y338–413): штатное приложение погоды

Зона минут укорочена на 9 px, чтобы не перекрывать нажатие на дату. Четыре зоны создаются без видимых элементов только в обычном режиме. Внешний вид, секундомер и AOD не изменены.

**Статус:** Zeus CLI прошёл, ZPK проверен; именно нажатие на дату на физических Amazfit Balance 2 ещё нужно проверить.

[Проверенная пользователем версия v1.1.1 с тремя рабочими областями](releases/DEAL_GNB_Balance2_Official_1.1.1.zpk)
