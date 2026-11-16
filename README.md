# DEAL_ГНБ — Amazfit Balance 2

Фирменный циферблат в стиле ГНБ, Zepp OS, дисплей 480 × 480.

## Рабочая тестовая сборка (официальный компилятор Zeus)

- Файл: [DEAL_GNB_Balance2_Official_1.0.1.zpk](releases/DEAL_GNB_Balance2_Official_1.0.1.zpk)
- Прямой адрес: https://raw.githubusercontent.com/butorindenisnik-alt/Amazfit-watchface/main/releases/DEAL_GNB_Balance2_Official_1.0.1.zpk
- Результат GitHub Actions: https://github.com/butorindenisnik-alt/Amazfit-watchface/actions/runs/43923471040

**Сборка Zeus CLI прошла успешно, но работа на физических Amazfit Balance 2 пока не подтверждена.**
В версии 1.0.1 динамические показатели: время, дата, заряд, шаги и пульс.
Данные погоды пока отключены до подтверждения стабильности.

**НЕ устанавливайте `releases/DEAL_GNB_Balance2_TEST.zpk`.**
Это старый экспериментальный пакет, вызывавший чёрный экран. Он оставлен здесь только потому, что из него автоматически восстанавливаются исходные графические ресурсы в GitHub Actions.

Для установки через Zepp Developer Mode используется QR с адресом
`zpkd1://raw.githubusercontent.com/butorindenisnik-alt/Amazfit-watchface/main/releases/DEAL_GNB_Balance2_Official_1.0.1.zpk`.

Если после установки виден чёрный экран, верните стандартный циферблат через Zepp и сообщите об ошибке, не выполняйте сброс устройства.
