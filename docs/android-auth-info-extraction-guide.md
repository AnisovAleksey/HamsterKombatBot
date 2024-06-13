# Руководство по извлечению информации для авторизации на Android

## Шаги

### 1. Включение режима разработчика и USB отладки

1. Перейдите в **Настройки** вашего Android устройства.
2. Найдите раздел **О телефоне** или **О планшете**.
3. Несколько раз нажмите на **Номер сборки** (обычно 7 раз), пока не увидите сообщение "Вы стали разработчиком".
4. Вернитесь в **Настройки** и найдите новый раздел **Для разработчиков**.
5. Включите **Режим разработчика** и **USB отладку**.

### 2. Включение режима отладки в Telegram

1. Откройте Telegram на вашем устройстве.
2. Перейдите в **Настройки**.
3. Прокрутите вниз до самого конца и дважды долго жмите на **Версию Telegram**.
4. В появившемся меню выберите **Enable Web View Inspecting**.

### 3. Подключение устройства к ПК

1. Подключите ваше Android устройство к компьютеру с помощью USB кабеля.
2. На устройстве появится запрос на разрешение USB отладки - подтвердите его.

### 4. Открытие DevTools в Chrome

1. Откройте Google Chrome на вашем ПК.
2. В адресной строке введите `chrome://inspect/#devices` и нажмите Enter.

### 5. Дебаг Web View

1. На вашем устройстве откройте Telegram и перейдите в HamsterKombat бота.
2. В Chrome в списке устройств найдите ваше устройство и выберите любой из доступных процессов Hamster Kombat.![alt text](image.png)
3. Нажмите на кнопку **inspect**.

### 6. Использование DevTools

1. Откроется отдельное окно с DevTools. Перейдите на вкладку **Network**.![newtork-tab](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/b2cb512c-b10c-4286-84d5-60deb58454e6)

2. Перейдите во вкладку **earn**, чтобы сгенерировать HTTP запрос.![earn-tab](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/268dad87-6919-44fe-9eab-de1d98a40d9d)

3. В строке поиска введите `list-task` и выберете фильтр `Fetch/XHR`.![filters](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/d03fc2e2-70aa-47ba-97c8-6b5c8a2d8391)

4. Нажмите на запрос, чтобы открыть меню взаимодействия с HTTP запросом.![open-request](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/b69a8cf6-8f3a-4afa-84fd-d3a644bf80e5)

5. В открывшемся окне, в разделе **Headers**, перейдите в раздел **Request Headers**.![open-request-data](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/77265bea-0eb5-4a19-b41a-4af114d17dba)

6. Скопируйте токен в аттрибуте **Authorization:** и уберите `Bearer`, оставив лишь сам токен.
Например: `Bearer 9aFJ6C29b81cLmR04DKq7fXzQi52tHOG8e7R9vUj6iPcYwTxN0uMbA3SdV5Ks2WjMnLv8qZoJ3F1rY46tQm9` должен превратиться в `9aFJ6C29b81cLmR04DKq7fXzQi52tHOG8e7R9vUj6iPcYwTxN0uMbA3SdV5Ks2WjMnLv8qZoJ3F1rY46tQm9`.
Это и есть ваш токен.![fields](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/410a4a77-bfcd-46fb-8151-6dcb74965e41)

7. Все остальные поля, выделенные желтым цветом [`Accept-Encoding`,`Accept-Language`,`Sec-Ch-Ua`,`Sec-Ch-Ua-Mobile`,`Sec-Ch-Ua-Platform`] можно использовать для генерации кастомизациии **headers** в [headers.py](https://github.com/AnisovAleksey/HamsterKombatBot/blob/b66014360c5664c27936378c7b611feb5b6c46dd/bot/core/headers.py)
